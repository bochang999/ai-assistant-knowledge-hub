#!/bin/bash

# Enhanced doit command with automatic project validation
# Prevents workflow confusion by ensuring correct project identification

SCRIPT_DIR="$(dirname "$0")"
QUERY_SCRIPT="$SCRIPT_DIR/enhanced-linear-query.sh"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Function to update Linear issue status
update_issue_status() {
    local issue_id=$1
    local state_id=$2
    local status_name=$3

    echo -e "${BLUE}🔄 Updating issue status to: $status_name${NC}"

    local query='mutation($issueId: String!, $stateId: String!) {
        issueUpdate(id: $issueId, input: { stateId: $stateId }) {
            success
            issue { id title state { name } }
        }
    }'

    local variables="{\"issueId\": \"$issue_id\", \"stateId\": \"$state_id\"}"

    local result=$(curl -s -X POST "https://api.linear.app/graphql" \
        -H "Authorization: $(cat ~/.linear-api-key)" \
        -H "Content-Type: application/json" \
        -d "{\"query\": \"$query\", \"variables\": $variables}")

    local success=$(echo "$result" | jq -r '.data.issueUpdate.success')

    if [ "$success" = "true" ]; then
        echo -e "${GREEN}✅ Issue status updated successfully${NC}"
    else
        echo -e "${RED}❌ Failed to update issue status${NC}"
        echo "$result" | jq '.errors' 2>/dev/null
    fi
}

# Function to get issue ID from issue number
get_issue_id() {
    local issue_number=$1

    local query='query($number: Float!) {
        issues(filter: { number: { eq: $number } }) {
            nodes { id }
        }
    }'

    local variables="{\"number\": $issue_number}"

    local result=$(curl -s -X POST "https://api.linear.app/graphql" \
        -H "Authorization: $(cat ~/.linear-api-key)" \
        -H "Content-Type: application/json" \
        -d "{\"query\": \"$query\", \"variables\": $variables}")

    echo "$result" | jq -r '.data.issues.nodes[0].id // empty'
}

# Function to display help
show_help() {
    echo "Enhanced doit - Safe Linear Issue Workflow"
    echo ""
    echo "Usage:"
    echo "  $0 <issue_number> [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --interactive, -i    Start interactive Claude session"
    echo "  --help, -h          Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 89                # Analyze and prepare issue BOC-89"
    echo "  $0 89 --interactive  # Analyze and start interactive session"
    echo ""
    echo "This command will:"
    echo "  1. Fetch complete issue information from Linear"
    echo "  2. Identify the correct project automatically"
    echo "  3. Validate the project environment"
    echo "  4. Update issue status to 'In Progress'"
    echo "  5. Navigate to the correct project directory"
    echo "  6. Optionally start interactive Claude session"
}

# Main function
main() {
    local issue_number=$1
    local interactive_mode=false

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -i|--interactive)
                interactive_mode=true
                shift
                ;;
            *)
                if [ -z "$issue_number" ]; then
                    issue_number=$1
                fi
                shift
                ;;
        esac
    done

    if [ -z "$issue_number" ]; then
        echo -e "${RED}❌ Error: Issue number is required${NC}"
        echo "Use --help for usage information"
        exit 1
    fi

    echo -e "${GREEN}🚀 Enhanced doit - Starting safe workflow for Issue #${issue_number}${NC}"
    echo "================================================================="

    # Step 1: Validate issue and project environment
    echo -e "${BLUE}Step 1: Issue Analysis and Project Validation${NC}"

    if [ ! -x "$QUERY_SCRIPT" ]; then
        echo -e "${RED}❌ Enhanced query script not found or not executable: $QUERY_SCRIPT${NC}"
        exit 1
    fi

    local validation_output
    validation_output=$("$QUERY_SCRIPT" "$issue_number" 2>&1)
    local validation_exit_code=$?

    if [ $validation_exit_code -ne 0 ]; then
        echo -e "${RED}❌ Issue validation failed${NC}"
        echo "$validation_output"
        echo ""
        echo -e "${RED}Cannot proceed safely. Please check:${NC}"
        echo "  - Issue number is correct"
        echo "  - Issue has proper project/team assignment"
        echo "  - Project mapping is configured"
        exit 1
    fi

    # Extract environment variables from validation output
    local env_vars
    env_vars=$(echo "$validation_output" | grep "^export " | tail -3)

    if [ -z "$env_vars" ]; then
        echo -e "${RED}❌ Failed to extract environment variables from validation${NC}"
        exit 1
    fi

    # Set environment variables
    eval "$env_vars"

    echo -e "${GREEN}✅ Project validated: $ISSUE_PROJECT_ID${NC}"
    echo -e "${GREEN}✅ Working directory: $ISSUE_BASE_PATH${NC}"

    # Step 2: Update issue status to "In Progress"
    echo ""
    echo -e "${BLUE}Step 2: Updating Issue Status${NC}"

    local issue_id
    issue_id=$(get_issue_id "$issue_number")

    if [ -z "$issue_id" ]; then
        echo -e "${RED}❌ Failed to get issue ID${NC}"
        exit 1
    fi

    # Linear state IDs from CLAUDE.md
    local IN_PROGRESS_STATE_ID="1cebb56e-524e-4de0-b676-0f574df9012a"
    update_issue_status "$issue_id" "$IN_PROGRESS_STATE_ID" "In Progress"

    # Step 3: Navigate to project directory
    echo ""
    echo -e "${BLUE}Step 3: Environment Setup${NC}"

    if [ ! -d "$ISSUE_BASE_PATH" ]; then
        echo -e "${RED}❌ Project directory not found: $ISSUE_BASE_PATH${NC}"
        exit 1
    fi

    cd "$ISSUE_BASE_PATH" || {
        echo -e "${RED}❌ Failed to change to project directory${NC}"
        exit 1
    }

    echo -e "${GREEN}✅ Changed to project directory: $(pwd)${NC}"

    # Display project context
    echo ""
    echo -e "${BLUE}📋 Project Context:${NC}"
    if [ -f "README.md" ]; then
        echo "  📄 README.md found - contains project overview"
    fi

    # Parse and display project mapping info
    local mapping
    mapping=$(echo "$ISSUE_MAPPING" | jq -r 2>/dev/null)
    if [ $? -eq 0 ] && [ -n "$mapping" ]; then
        local description
        description=$(echo "$mapping" | jq -r '.description // "No description"')
        local technologies
        technologies=$(echo "$mapping" | jq -r '.technologies[]? // empty' | tr '\n' ', ' | sed 's/,$//')
        local build_command
        build_command=$(echo "$mapping" | jq -r '.buildCommand // "No build command"')

        echo "  📝 Description: $description"
        echo "  🔧 Technologies: $technologies"
        echo "  🏗️  Build Command: $build_command"
    fi

    # Step 4: Interactive mode
    if [ "$interactive_mode" = true ]; then
        echo ""
        echo -e "${BLUE}Step 4: Starting Interactive Session${NC}"
        echo -e "${YELLOW}💡 You are now ready to work on Issue #${issue_number}${NC}"
        echo -e "${YELLOW}💡 Project: $ISSUE_PROJECT_ID${NC}"
        echo -e "${YELLOW}💡 Directory: $(pwd)${NC}"
        echo ""

        # Start interactive shell with project context
        echo -e "${GREEN}🎯 Starting interactive session...${NC}"
        echo "Type 'exit' to end the session"

        # Export variables for the interactive session
        export CURRENT_ISSUE_NUMBER="$issue_number"
        export CURRENT_PROJECT_ID="$ISSUE_PROJECT_ID"
        export CURRENT_BASE_PATH="$ISSUE_BASE_PATH"

        # Start a new shell with enhanced prompt
        PS1="[Issue #$issue_number | $ISSUE_PROJECT_ID] \$ " bash --norc

    else
        echo ""
        echo -e "${GREEN}✅ Issue #${issue_number} is ready for work${NC}"
        echo -e "${GREEN}✅ Project: $ISSUE_PROJECT_ID${NC}"
        echo -e "${GREEN}✅ Directory: $(pwd)${NC}"
        echo ""
        echo -e "${YELLOW}💡 To start interactive mode: $0 $issue_number --interactive${NC}"
    fi

    echo ""
    echo -e "${GREEN}🎉 Enhanced doit completed successfully${NC}"
}

# Handle signals
trap 'echo -e "\n${YELLOW}⚠️  Enhanced doit interrupted${NC}"; exit 1' INT TERM

# Run main function
main "$@"
