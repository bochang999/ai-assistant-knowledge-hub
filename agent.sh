#!/bin/bash

# Self-Contained Agent Script for AI Assistant Knowledge Hub
# Usage: bash agent.sh do [ISSUE_ID]
# Purpose: Complete task automation from clean environment to task execution

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[AGENT]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check command line arguments
if [[ $# -ne 2 ]] || [[ "$1" != "do" ]]; then
    error "Usage: $0 do [ISSUE_ID]"
    error "Example: $0 do BOC-65"
    exit 1
fi

ISSUE_ID="$2"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

log "Starting self-contained agent for issue: $ISSUE_ID"

# ========================================
# STEP A: Environment Self-Diagnosis and Setup
# ========================================

log "Step A: Environment self-diagnosis and setup"

# A1: Check if we're in the correct repository
if [[ ! -f "$SCRIPT_DIR/run.sh" ]] || [[ ! -d "$SCRIPT_DIR/.git" ]]; then
    error "This script must be run from the ai-assistant-knowledge-hub repository root"
    exit 1
fi

# A2: Check Linear API key
LINEAR_API_KEY_FILE="$HOME/.linear-api-key"
if [[ ! -f "$LINEAR_API_KEY_FILE" ]]; then
    error "Linear API key not found at $LINEAR_API_KEY_FILE"
    error "Please set up your Linear API key before running this script"
    error "You can get your API key from: https://linear.app/settings/api"
    exit 1
fi

# A3: Check required tools
REQUIRED_TOOLS=("curl" "jq" "git")
for tool in "${REQUIRED_TOOLS[@]}"; do
    if ! command -v "$tool" &> /dev/null; then
        error "Required tool '$tool' not found"
        warn "Please install missing tools:"
        warn "  Termux: pkg install curl jq git"
        warn "  Ubuntu/Debian: apt install curl jq git"
        warn "  MacOS: brew install curl jq git"
        exit 1
    fi
done

# A4: Check git configuration
if ! git config --get user.email &> /dev/null; then
    warn "Git user email not configured. Setting up minimal git config..."
    git config --global user.email "agent@ai-assistant.local"
    git config --global user.name "AI Agent"
fi

# A5: Set up Linear API key
LINEAR_API_KEY=$(cat "$LINEAR_API_KEY_FILE")

success "Environment diagnosis completed - all requirements satisfied"

# ========================================
# Linear API Functions
# ========================================

# Function to get issue details from Linear API
get_linear_issue() {
    local issue_id="$1"
    local query='{
        "query": "query($id: String!) { issue(id: $id) { id title description state { name } } }",
        "variables": { "id": "'"$issue_id"'" }
    }'

    curl -s -X POST "https://api.linear.app/graphql" \
        -H "Authorization: $LINEAR_API_KEY" \
        -H "Content-Type: application/json" \
        -d "$query"
}

# Function to post comment to Linear issue
post_linear_comment() {
    local issue_id="$1"
    local comment_text="$2"
    local mutation='{
        "query": "mutation($id: String!, $body: String!) { commentCreate(input: { issueId: $id, body: $body }) { success comment { id } } }",
        "variables": { "id": "'"$issue_id"'", "body": "'"$comment_text"'" }
    }'

    curl -s -X POST "https://api.linear.app/graphql" \
        -H "Authorization: $LINEAR_API_KEY" \
        -H "Content-Type: application/json" \
        -d "$mutation"
}

# ========================================
# STEP B: Task Details Retrieval
# ========================================

log "Step B: Retrieving task details from Linear for $ISSUE_ID"

# B1: Get issue details using direct API calls
# Create local temp directory if it doesn't exist
mkdir -p "${SCRIPT_DIR}/temp"
ISSUE_DATA_FILE="${SCRIPT_DIR}/temp/agent_issue_${ISSUE_ID}.json"
if ! get_linear_issue "$ISSUE_ID" > "$ISSUE_DATA_FILE" 2>/dev/null; then
    error "Failed to retrieve issue $ISSUE_ID from Linear"
    error "Please check that the issue ID is correct and accessible"
    exit 1
fi

# B2: Parse issue details using jq
if ! command -v jq &> /dev/null; then
    error "jq is required for JSON parsing but not found"
    exit 1
fi

ISSUE_TITLE=$(jq -r '.data.issue.title // "Unknown"' "$ISSUE_DATA_FILE")
ISSUE_DESCRIPTION=$(jq -r '.data.issue.description // "No description"' "$ISSUE_DATA_FILE")
ISSUE_STATE=$(jq -r '.data.issue.state.name // "Unknown"' "$ISSUE_DATA_FILE")

if [[ "$ISSUE_TITLE" == "null" ]] || [[ "$ISSUE_TITLE" == "Unknown" ]]; then
    error "Could not parse issue title from Linear response"
    error "Raw response saved to: $ISSUE_DATA_FILE"
    exit 1
fi

log "Issue Title: $ISSUE_TITLE"
log "Issue State: $ISSUE_STATE"

# B3: Extract project context from issue description
# Look for project patterns in the description
PROJECT_NAME=""

# Check if description contains project references
if echo "$ISSUE_DESCRIPTION" | grep -q "knowledge.*hub"; then
    PROJECT_NAME="knowledge_hub_mng"
elif echo "$ISSUE_DESCRIPTION" | grep -qi "laminator\|dashboard"; then
    PROJECT_NAME="laminator_dashboard"
elif echo "$ISSUE_DESCRIPTION" | grep -qi "recipe\|app"; then
    PROJECT_NAME="recipe_app"
else
    # Default to knowledge hub management if no specific project detected
    PROJECT_NAME="knowledge_hub_mng"
fi

log "Detected project: $PROJECT_NAME"

# B4: Extract AI command preference (default to claude-cli if not specified)
AI_COMMAND="claude-cli"
if echo "$ISSUE_DESCRIPTION" | grep -qi "gemini"; then
    AI_COMMAND="gemini-cli"
elif echo "$ISSUE_DESCRIPTION" | grep -qi "gpt\|chatgpt"; then
    AI_COMMAND="gpt-cli"
fi

log "AI Command: $AI_COMMAND"

# B5: Prepare user instruction from issue description
USER_INSTRUCTION="$ISSUE_TITLE"$'\n\n'"$ISSUE_DESCRIPTION"

success "Task details retrieved and parsed successfully"

# ========================================
# STEP C: Knowledge Loader Execution
# ========================================

log "Step C: Executing Knowledge Loader with assembled information"

# C1: Check if the detected project exists
PROJECT_CONTEXT_FILE="$SCRIPT_DIR/projects/$PROJECT_NAME/context.md"
if [[ ! -f "$PROJECT_CONTEXT_FILE" ]]; then
    warn "Project context not found at: $PROJECT_CONTEXT_FILE"
    warn "Available projects:"
    ls -1 "$SCRIPT_DIR/projects/" 2>/dev/null | grep -v '.gitkeep' || warn "No projects found"

    # Try to use a fallback project or create a minimal one
    FALLBACK_PROJECT="knowledge_hub_mng"
    FALLBACK_CONTEXT="$SCRIPT_DIR/projects/$FALLBACK_PROJECT/context.md"
    if [[ -f "$FALLBACK_CONTEXT" ]]; then
        warn "Using fallback project: $FALLBACK_PROJECT"
        PROJECT_NAME="$FALLBACK_PROJECT"
    else
        error "No suitable project context found. Cannot proceed."
        exit 1
    fi
fi

# C2: Check if AI command exists
if ! command -v "$AI_COMMAND" &> /dev/null; then
    warn "AI command '$AI_COMMAND' not found, trying claude-cli as fallback"
    AI_COMMAND="claude-cli"
    if ! command -v "$AI_COMMAND" &> /dev/null; then
        error "No suitable AI command found (tried: claude-cli, $AI_COMMAND)"
        error "Please install at least one AI CLI tool"
        exit 1
    fi
fi

# C3: Update Linear issue status to "In Progress"
log "Updating issue status to 'In Progress'"
IN_PROGRESS_ID="1cebb56e-524e-4de0-b676-0f574df9012a"
curl -s -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $(cat ~/.linear-api-key)" \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"mutation{issueUpdate(id:\\\"$(jq -r '.data.issue.id' "$ISSUE_DATA_FILE")\\\",input:{stateId:\\\"$IN_PROGRESS_ID\\\"})}\"}}" > /dev/null

# C4: Execute run.sh with assembled parameters
log "Executing run.sh with parameters:"
log "  Project: $PROJECT_NAME"
log "  AI Command: $AI_COMMAND"
log "  User Instruction: [Assembled from issue]"

echo "=========================================="
success "Agent initialization complete - starting task execution"
echo "=========================================="

# Execute the knowledge loader
cd "$SCRIPT_DIR"
exec bash run.sh "$PROJECT_NAME" "$AI_COMMAND" "$USER_INSTRUCTION"

# Note: exec replaces the current process, so cleanup code here won't run
# Cleanup would need to be handled by the called script if needed