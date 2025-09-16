#!/bin/bash

# Simple Issue Validator - Working solution for BOC-89 problem

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Function to get issue information
get_issue_info() {
    local issue_number=$1

    echo -e "${BLUE}🔍 Fetching issue #${issue_number}...${NC}"

    local result=$(curl -s -X POST "https://api.linear.app/graphql" \
        -H "Authorization: $(cat ~/.linear-api-key)" \
        -H "Content-Type: application/json" \
        -d "{\"query\": \"query { issues(filter: { number: { eq: $issue_number } }) { nodes { id title description project { name } team { key name } labels { nodes { name } } state { name } assignee { name } } } }\"}")

    echo "$result"
}

# Function to determine project mapping
determine_project() {
    local issue_data=$1

    local project_name=$(echo "$issue_data" | jq -r '.data.issues.nodes[0].project.name // empty')
    local team_key=$(echo "$issue_data" | jq -r '.data.issues.nodes[0].team.key // empty')

    echo -e "${YELLOW}📊 Issue Information:${NC}"
    echo "  Project: ${project_name}"
    echo "  Team: ${team_key}"

    # Map to our directory structure
    local target_project=""
    case "${project_name,,}" in
        "petit recipe")
            target_project="petit-recipe"
            ;;
        "ai assistant knowledge hub")
            target_project="ai-assistant-knowledge-hub"
            ;;
        "laminator dashboard")
            target_project="laminator-dashboard"
            ;;
        "recipebox web")
            target_project="recipebox-web"
            ;;
        "tarot")
            target_project="tarot"
            ;;
        *)
            # Default to team-based mapping
            target_project="bochang-labo"
            ;;
    esac

    echo -e "${GREEN}✅ Target Project: $target_project${NC}"
    echo "$target_project"
}

# Function to get project directory
get_project_directory() {
    local project_name=$1

    case "$project_name" in
        "ai-assistant-knowledge-hub")
            echo "$HOME/ai-assistant-knowledge-hub"
            ;;
        "petit-recipe")
            echo "$HOME/petit-recipe"
            ;;
        "laminator-dashboard")
            echo "$HOME/laminator-dashboard"
            ;;
        "recipebox-web")
            echo "$HOME/recipebox-web"
            ;;
        "tarot")
            echo "$HOME/tarot"
            ;;
        *)
            echo "$HOME"
            ;;
    esac
}

# Main function
main() {
    local issue_number=$1

    if [ -z "$issue_number" ]; then
        echo -e "${RED}Usage: $0 <issue_number>${NC}"
        exit 1
    fi

    echo -e "${GREEN}🚀 Issue Validation for #${issue_number}${NC}"
    echo "============================================"

    # Get issue information
    local issue_data=$(get_issue_info "$issue_number")

    if [ -z "$issue_data" ] || [ "$(echo "$issue_data" | jq -r '.data.issues.nodes | length')" = "0" ]; then
        echo -e "${RED}❌ Issue #${issue_number} not found${NC}"
        exit 1
    fi

    # Determine project
    local project_id=$(determine_project "$issue_data")
    local project_dir=$(get_project_directory "$project_id")

    # Validate directory exists
    if [ ! -d "$project_dir" ]; then
        echo -e "${RED}❌ Project directory not found: $project_dir${NC}"
        exit 1
    fi

    # Display summary
    local title=$(echo "$issue_data" | jq -r '.data.issues.nodes[0].title')
    local description=$(echo "$issue_data" | jq -r '.data.issues.nodes[0].description // "No description"')

    echo ""
    echo -e "${BLUE}📋 Issue Summary:${NC}"
    echo "  Title: $title"
    echo "  Project: $project_id"
    echo "  Directory: $project_dir"
    echo "  Description: $(echo "$description" | head -1)"

    echo ""
    echo -e "${GREEN}✅ Validation successful!${NC}"
    echo -e "${GREEN}✅ Project: $project_id${NC}"
    echo -e "${GREEN}✅ Directory: $project_dir${NC}"

    # Export for other scripts
    export VALIDATED_ISSUE_PROJECT="$project_id"
    export VALIDATED_ISSUE_DIR="$project_dir"
    export VALIDATED_ISSUE_ID="$(echo "$issue_data" | jq -r '.data.issues.nodes[0].id')"

    return 0
}

main "$@"
