#!/bin/bash

# Working Enhanced Doit - Final Solution for Project Confusion Prevention

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Function to validate and process issue
validate_issue() {
    local issue_number=$1

    echo -e "${BLUE}🔍 Analyzing Issue #${issue_number}...${NC}"

    # Get issue data from Linear
    local api_response=$(curl -s -X POST "https://api.linear.app/graphql" \
        -H "Authorization: $(cat ~/.linear-api-key)" \
        -H "Content-Type: application/json" \
        -d "{\"query\": \"query { issues(filter: { number: { eq: $issue_number } }) { nodes { id title description project { name } team { key name } labels { nodes { name } } state { name } assignee { name } } } }\"}")

    # Check if we got data
    local issue_count=$(echo "$api_response" | jq -r '.data.issues.nodes | length' 2>/dev/null || echo "0")
    if [ "$issue_count" = "0" ]; then
        echo -e "${RED}❌ Issue #${issue_number} not found${NC}"
        return 1
    fi

    # Extract issue information
    local title=$(echo "$api_response" | jq -r '.data.issues.nodes[0].title' 2>/dev/null || echo "No title")
    local project_name=$(echo "$api_response" | jq -r '.data.issues.nodes[0].project.name // empty' 2>/dev/null)
    local team_name=$(echo "$api_response" | jq -r '.data.issues.nodes[0].team.name // empty' 2>/dev/null)
    local issue_id=$(echo "$api_response" | jq -r '.data.issues.nodes[0].id' 2>/dev/null)

    echo -e "${YELLOW}📊 Issue Information:${NC}"
    echo "  Title: $title"
    echo "  Project: ${project_name:-'Not specified'}"
    echo "  Team: ${team_name:-'Not specified'}"

    # Determine target project directory
    local target_project=""
    local target_dir=""

    case "${project_name,,}" in
        *"petit recipe"*)
            target_project="petit-recipe"
            target_dir="$HOME/petit-recipe"
            ;;
        *"ai assistant knowledge hub"*)
            target_project="ai-assistant-knowledge-hub"
            target_dir="$HOME/ai-assistant-knowledge-hub"
            ;;
        *"laminator"*|*"dashboard"*)
            target_project="laminator-dashboard"
            target_dir="$HOME/laminator-dashboard"
            ;;
        *"recipebox"*)
            target_project="recipebox-web"
            target_dir="$HOME/recipebox-web"
            ;;
        *"tarot"*)
            target_project="tarot"
            target_dir="$HOME/tarot"
            ;;
        *)
            # Default based on team or current setup
            target_project="ai-assistant-knowledge-hub"
            target_dir="$HOME/ai-assistant-knowledge-hub"
            echo -e "${YELLOW}⚠️  Using default project mapping${NC}"
            ;;
    esac

    # Verify directory exists
    if [ ! -d "$target_dir" ]; then
        echo -e "${RED}❌ Target directory not found: $target_dir${NC}"
        return 1
    fi

    echo -e "${GREEN}✅ Target Project: $target_project${NC}"
    echo -e "${GREEN}✅ Target Directory: $target_dir${NC}"

    # Export results
    export ISSUE_PROJECT="$target_project"
    export ISSUE_DIR="$target_dir"
    export ISSUE_ID="$issue_id"
    export ISSUE_TITLE="$title"

    return 0
}

# Function to update Linear status
update_status() {
    local status=$1  # "in_progress" or "completed"

    if [ -z "$ISSUE_ID" ]; then
        echo -e "${RED}❌ No issue ID available${NC}"
        return 1
    fi

    local state_id=""
    case "$status" in
        "in_progress")
            state_id="1cebb56e-524e-4de0-b676-0f574df9012a"
            ;;
        "completed")
            state_id="33feb1c9-3276-4e13-863a-0b93db032a0f"
            ;;
        *)
            echo -e "${RED}❌ Invalid status: $status${NC}"
            return 1
            ;;
    esac

    echo -e "${BLUE}🔄 Updating status to: $status${NC}"

    local result=$(curl -s -X POST "https://api.linear.app/graphql" \
        -H "Authorization: $(cat ~/.linear-api-key)" \
        -H "Content-Type: application/json" \
        -d "{\"query\": \"mutation { issueUpdate(id: \\\"$ISSUE_ID\\\", input: { stateId: \\\"$state_id\\\" }) { success } }\"}")

    local success=$(echo "$result" | jq -r '.data.issueUpdate.success' 2>/dev/null || echo "false")

    if [ "$success" = "true" ]; then
        echo -e "${GREEN}✅ Status updated successfully${NC}"
    else
        echo -e "${YELLOW}⚠️  Status update may have failed${NC}"
    fi
}

# Main function
main() {
    local issue_number=$1
    local interactive=false

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -i|--interactive)
                interactive=true
                shift
                ;;
            -h|--help)
                echo "Working Enhanced Doit"
                echo "Usage: $0 <issue_number> [--interactive]"
                echo "Example: $0 89 --interactive"
                exit 0
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
        echo -e "${RED}❌ Issue number required${NC}"
        echo "Usage: $0 <issue_number> [--interactive]"
        exit 1
    fi

    echo -e "${GREEN}🚀 Working Enhanced Doit - Issue #${issue_number}${NC}"
    echo "================================================"

    # Step 1: Validate issue and determine project
    if ! validate_issue "$issue_number"; then
        exit 1
    fi

    # Step 2: Update status to In Progress
    echo ""
    echo -e "${BLUE}📌 Step 2: Updating Issue Status${NC}"
    update_status "in_progress"

    # Step 3: Navigate to project directory
    echo ""
    echo -e "${BLUE}📂 Step 3: Project Environment${NC}"
    cd "$ISSUE_DIR" || {
        echo -e "${RED}❌ Failed to navigate to $ISSUE_DIR${NC}"
        exit 1
    }

    echo -e "${GREEN}✅ Current Directory: $(pwd)${NC}"
    echo -e "${GREEN}✅ Project: $ISSUE_PROJECT${NC}"
    echo -e "${GREEN}✅ Issue: $ISSUE_TITLE${NC}"

    # Step 4: Interactive mode if requested
    if [ "$interactive" = true ]; then
        echo ""
        echo -e "${BLUE}🎯 Step 4: Interactive Session${NC}"
        echo -e "${YELLOW}💡 You are now in the correct project directory${NC}"
        echo -e "${YELLOW}💡 Issue #${issue_number}: $ISSUE_TITLE${NC}"
        echo ""
        echo "Type 'exit' to end session"

        PS1="[Issue #$issue_number | $ISSUE_PROJECT] \$ " bash --norc
    else
        echo ""
        echo -e "${GREEN}✅ Ready to work on Issue #${issue_number}${NC}"
        echo -e "${YELLOW}💡 Add --interactive to start interactive session${NC}"
    fi

    echo ""
    echo -e "${GREEN}🎉 Enhanced Doit completed successfully${NC}"
}

# Run main function
main "$@"
