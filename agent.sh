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

# Parse command line arguments
COMMAND=""
ISSUE_ID=""
SPECIFIED_AI_COMMAND=""
INTERACTIVE_MODE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        do)
            COMMAND="$1"
            shift
            ;;
        --ai-command)
            SPECIFIED_AI_COMMAND="$2"
            shift 2
            ;;
        --interactive)
            INTERACTIVE_MODE=true
            shift
            ;;
        *)
            if [[ -z "$ISSUE_ID" ]] && [[ -n "$COMMAND" ]]; then
                ISSUE_ID="$1"
            else
                error "Unknown argument: $1"
                exit 1
            fi
            shift
            ;;
    esac
done

# Validate arguments
if [[ "$COMMAND" != "do" ]] || [[ -z "$ISSUE_ID" ]]; then
    error "Usage: $0 do [ISSUE_ID] [--ai-command <command>] [--interactive]"
    error "Example: $0 do BOC-65"
    error "Example: $0 do BOC-65 --ai-command gpt-cli"
    error "Example: $0 do BOC-65 --interactive"
    exit 1
fi

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
# AI Command Detection and Selection
# ========================================

# A6: Auto-detect available AI commands
log "Step A6: Detecting available AI commands"

# List of known AI commands in priority order (highest to lowest)
KNOWN_AI_COMMANDS=("claude-cli" "gemini-cli" "gpt-cli" "openai-cli" "anthropic-cli")
AVAILABLE_AI_COMMANDS=()

# Detect available commands
for cmd in "${KNOWN_AI_COMMANDS[@]}"; do
    if command -v "$cmd" &> /dev/null; then
        AVAILABLE_AI_COMMANDS+=("$cmd")
        log "Found: $cmd"
    fi
done

# Check if any AI commands are available
if [[ ${#AVAILABLE_AI_COMMANDS[@]} -eq 0 ]]; then
    error "No AI commands found in system PATH"
    error "Please install at least one of the following AI CLI tools:"
    for cmd in "${KNOWN_AI_COMMANDS[@]}"; do
        error "  - $cmd"
    done
    exit 1
fi

# Select AI command based on user specification or priority
SELECTED_AI_COMMAND=""
if [[ -n "$SPECIFIED_AI_COMMAND" ]]; then
    # User specified a command - validate it exists
    COMMAND_FOUND=false
    for available_cmd in "${AVAILABLE_AI_COMMANDS[@]}"; do
        if [[ "$available_cmd" == "$SPECIFIED_AI_COMMAND" ]]; then
            SELECTED_AI_COMMAND="$SPECIFIED_AI_COMMAND"
            COMMAND_FOUND=true
            log "Using user-specified AI command: $SELECTED_AI_COMMAND"
            break
        fi
    done

    if [[ "$COMMAND_FOUND" == false ]]; then
        error "Specified AI command '$SPECIFIED_AI_COMMAND' is not available"
        error "Available commands: ${AVAILABLE_AI_COMMANDS[*]}"
        exit 1
    fi
else
    # Auto-select highest priority available command
    SELECTED_AI_COMMAND="${AVAILABLE_AI_COMMANDS[0]}"
    log "Auto-selected AI command: $SELECTED_AI_COMMAND (highest priority available)"
fi

log "Available AI commands: ${AVAILABLE_AI_COMMANDS[*]}"
success "AI command selection completed: $SELECTED_AI_COMMAND"

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

# B4: Use the dynamically selected AI command
AI_COMMAND="$SELECTED_AI_COMMAND"
log "AI Command: $AI_COMMAND (from dynamic selection)"

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

# C2: Read working directory from context.md and navigate there
PROJECT_CONTEXT_FILE="$SCRIPT_DIR/projects/$PROJECT_NAME/context.md"
WORKING_DIR=""

if [[ -f "$PROJECT_CONTEXT_FILE" ]]; then
    log "Reading context.md to determine working directory..."

    # Extract working directory from context.md
    WORKING_DIR_LINE=$(grep "作業ディレクトリ" "$PROJECT_CONTEXT_FILE" | head -1)
    if [[ -n "$WORKING_DIR_LINE" ]]; then
        # Extract everything after the colon and clean it up
        AFTER_COLON=$(echo "$WORKING_DIR_LINE" | cut -d':' -f2)
        WORKING_DIR=$(echo "$AFTER_COLON" | sed 's/`//g' | sed 's/^ *//' | sed 's/ *$//')
    fi

    if [[ -n "$WORKING_DIR" ]] && [[ "$WORKING_DIR" != "作業ディレクトリ:" ]]; then
        # Expand tilde to home directory if needed
        WORKING_DIR_EXPANDED="${WORKING_DIR/#\~/$HOME}"

        log "Found working directory in context.md: $WORKING_DIR"
        log "Expanded path: $WORKING_DIR_EXPANDED"

        if [[ -d "$WORKING_DIR_EXPANDED" ]]; then
            log "Navigating to working directory: $WORKING_DIR_EXPANDED"
            cd "$WORKING_DIR_EXPANDED"
            success "Successfully changed to working directory: $(pwd)"
        else
            warn "Working directory $WORKING_DIR_EXPANDED does not exist"
            warn "Staying in current directory: $(pwd)"
        fi
    else
        log "No working directory specified in context.md"
        log "Staying in agent script directory: $(pwd)"
    fi
else
    log "No context.md found, staying in agent script directory"
fi

# C2b: AI command validation already completed in dynamic selection step
log "Using validated AI command: $AI_COMMAND"

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

# Execute either interactive mode or normal mode
if [[ "$INTERACTIVE_MODE" == true ]]; then
    # ========================================
    # INTERACTIVE MODE EXECUTION
    # ========================================
    log "INTERACTIVE MODE: Starting phase-by-phase execution"
    log "Working directory: $(pwd)"

    # Detect workflow type from issue description
    WORKFLOW_TYPE=""
    if echo "$ISSUE_DESCRIPTION" | grep -qi "build.*error\|error.*build\|ビルド.*エラー\|エラー.*ビルド"; then
        WORKFLOW_TYPE="build_error_correction"
    else
        error "Could not detect workflow type from issue description"
        error "Currently supported workflows: build_error_correction"
        exit 1
    fi

    log "Detected workflow type: $WORKFLOW_TYPE"

    # Find workflow directory
    WORKFLOW_DIR=""
    if [[ -d "$SCRIPT_DIR/workflows/$WORKFLOW_TYPE" ]]; then
        WORKFLOW_DIR="$SCRIPT_DIR/workflows/$WORKFLOW_TYPE"
    elif [[ -d "workflows/$WORKFLOW_TYPE" ]]; then
        WORKFLOW_DIR="workflows/$WORKFLOW_TYPE"
    else
        error "Workflow directory not found: $WORKFLOW_TYPE"
        error "Expected: $SCRIPT_DIR/workflows/$WORKFLOW_TYPE or workflows/$WORKFLOW_TYPE"
        exit 1
    fi

    log "Using workflow directory: $WORKFLOW_DIR"

    # Get list of phase files
    PHASE_FILES=($(ls "$WORKFLOW_DIR"/phase*.md | sort))
    if [[ ${#PHASE_FILES[@]} -eq 0 ]]; then
        error "No phase files found in $WORKFLOW_DIR"
        exit 1
    fi

    log "Found ${#PHASE_FILES[@]} phase files:"
    for phase_file in "${PHASE_FILES[@]}"; do
        log "  - $(basename "$phase_file")"
    done

    # Interactive phase-by-phase execution
    CURRENT_PHASE=0
    TOTAL_PHASES=${#PHASE_FILES[@]}

    while [[ $CURRENT_PHASE -lt $TOTAL_PHASES ]]; do
        PHASE_FILE="${PHASE_FILES[$CURRENT_PHASE]}"
        PHASE_NAME=$(basename "$PHASE_FILE" .md)
        NEXT_PHASE=$((CURRENT_PHASE + 1))

        echo ""
        echo "=========================================="
        success "PHASE $((CURRENT_PHASE + 1))/$TOTAL_PHASES: $PHASE_NAME"
        echo "=========================================="

        # Create phase-specific instruction
        PHASE_INSTRUCTION="Execute ${ISSUE_ID} ${PHASE_NAME} only.

Read and follow the instructions from: ${PHASE_FILE}

Original Issue:
${USER_INSTRUCTION}

IMPORTANT: Execute ONLY this phase. Do not proceed to other phases."

        log "Executing phase: $PHASE_NAME"
        log "Phase file: $PHASE_FILE"

        # Execute this phase
        bash "$SCRIPT_DIR/run.sh" "$PROJECT_NAME" "$AI_COMMAND" "$PHASE_INSTRUCTION"

        # Wait for user approval before continuing
        if [[ $NEXT_PHASE -lt $TOTAL_PHASES ]]; then
            echo ""
            echo "=========================================="
            log "Phase $((CURRENT_PHASE + 1)) completed"
            read -p "$(echo -e "${YELLOW}[AGENT]${NC} Proceed to Phase $((NEXT_PHASE + 1)) ($(basename "${PHASE_FILES[$NEXT_PHASE]}" .md))? (y/N): ")" USER_RESPONSE
            echo "=========================================="

            if [[ "$USER_RESPONSE" =~ ^[Yy]$ ]]; then
                CURRENT_PHASE=$NEXT_PHASE
                log "Proceeding to next phase..."
            else
                warn "Interactive execution stopped by user"
                log "Completed phases: $((CURRENT_PHASE + 1))/$TOTAL_PHASES"
                exit 0
            fi
        else
            CURRENT_PHASE=$NEXT_PHASE
        fi
    done

    echo ""
    echo "=========================================="
    success "ALL PHASES COMPLETED!"
    success "Interactive workflow execution finished for $ISSUE_ID"
    echo "=========================================="

else
    # ========================================
    # NORMAL MODE EXECUTION (Original behavior)
    # ========================================
    log "NORMAL MODE: Executing full workflow"

    # Execute the knowledge loader from the script directory
    # (Note: We may have changed to a working directory above, so we need to reference run.sh with full path)
    AI_RESPONSE=$(bash "$SCRIPT_DIR/run.sh" "$PROJECT_NAME" "$AI_COMMAND" "$USER_INSTRUCTION")

    log "=========================================="

    # Note: exec replaces the current process, so cleanup code here won't run
    # Cleanup would need to be handled by the called script if needed
fi
