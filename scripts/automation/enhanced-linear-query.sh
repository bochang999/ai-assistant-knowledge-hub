#!/bin/bash

# Enhanced Linear Issue Query System
# Prevents project identification errors by extracting complete issue context

SCRIPT_DIR="$(dirname "$0")"
PROJECT_MAPPING_FILE="$HOME/ai-assistant-knowledge-hub/scripts/automation/project-mapping.json"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to get complete issue information
get_complete_issue_info() {
    local issue_number=$1

    echo -e "${BLUE}🔍 Fetching complete issue information for #${issue_number}...${NC}"

    local query='query($number: Float!) {
        issues(filter: { number: { eq: $number } }) {
            nodes {
                id
                title
                description
                state { id name }
                project { id name }
                team { id name key }
                labels { nodes { name } }
                assignee { name }
                createdAt
                updatedAt
            }
        }
    }'

    local variables="{\"number\": $issue_number}"

    curl -s -X POST "https://api.linear.app/graphql" \
        -H "Authorization: $(cat ~/.linear-api-key)" \
        -H "Content-Type: application/json" \
        -d "{\"query\": \"$query\", \"variables\": $variables}"
}

# Function to extract and validate project information
extract_project_info() {
    local issue_data=$1

    # Extract project information
    local project_name=$(echo "$issue_data" | jq -r '.data.issues.nodes[0].project.name // empty')

    # Extract team information (fallback method)
    local team_key=$(echo "$issue_data" | jq -r '.data.issues.nodes[0].team.key // empty')
    local team_name=$(echo "$issue_data" | jq -r '.data.issues.nodes[0].team.name // empty')

    # Extract labels (additional context)
    local labels=$(echo "$issue_data" | jq -r '.data.issues.nodes[0].labels.nodes[].name' 2>/dev/null | tr '\n' ',' | sed 's/,$//')

    echo -e "${YELLOW}📊 Project Information:${NC}"
    echo "  Project Name: ${project_name:-'NOT_FOUND'}"
    echo "  Team Key: ${team_key:-'NOT_FOUND'}"
    echo "  Team Name: ${team_name:-'NOT_FOUND'}"
    echo "  Labels: ${labels:-'NONE'}"

    # Determine primary project identifier
    local primary_identifier=""

    # Map project names to our project keys
    case "${project_name,,}" in
        "ai assistant knowledge hub"|"ai-assistant-knowledge-hub")
            primary_identifier="ai-assistant-knowledge-hub"
            ;;
        "petit recipe")
            primary_identifier="petit-recipe"
            ;;
        "laminator dashboard"|"laminator-dashboard")
            primary_identifier="laminator-dashboard"
            ;;
        "recipebox web"|"recipebox-web")
            primary_identifier="recipebox-web"
            ;;
        "tarot")
            primary_identifier="tarot"
            ;;
        *)
            # Try team key as fallback
            if [ -n "$team_key" ]; then
                primary_identifier=$(echo "${team_key,,}" | sed 's/[^a-z0-9-]/-/g')
            else
                echo -e "${RED}❌ ERROR: Cannot determine project identifier${NC}"
                return 1
            fi
            ;;
    esac

    echo -e "${GREEN}✅ Primary Project Identifier: $primary_identifier${NC}"
    echo "$primary_identifier"
}

# Function to get project mapping
get_project_mapping() {
    local project_id=$1

    if [ ! -f "$PROJECT_MAPPING_FILE" ]; then
        echo -e "${RED}❌ Project mapping file not found: $PROJECT_MAPPING_FILE${NC}"
        return 1
    fi

    local mapping=$(jq -r ".[\"$project_id\"] // empty" "$PROJECT_MAPPING_FILE")

    if [ -z "$mapping" ] || [ "$mapping" = "null" ]; then
        echo -e "${RED}❌ No mapping found for project: $project_id${NC}"
        return 1
    fi

    echo "$mapping"
}

# Function to validate project environment
validate_project_environment() {
    local project_mapping=$1

    local base_path=$(echo "$project_mapping" | jq -r '.basePath')
    local procedures=$(echo "$project_mapping" | jq -r '.procedures[]')

    echo -e "${BLUE}🔍 Validating project environment...${NC}"
    echo "  Base Path: $base_path"

    # Expand tilde in path
    base_path="${base_path/#\~/$HOME}"

    if [ ! -d "$base_path" ]; then
        echo -e "${RED}❌ Project directory not found: $base_path${NC}"
        return 1
    fi

    # Check for procedure files
    local missing_procedures=0
    while IFS= read -r procedure; do
        local procedure_path="$base_path/$procedure"
        if [ ! -f "$procedure_path" ]; then
            echo -e "${RED}❌ Missing procedure file: $procedure_path${NC}"
            ((missing_procedures++))
        else
            echo -e "${GREEN}✅ Found procedure file: $procedure${NC}"
        fi
    done <<< "$procedures"

    if [ $missing_procedures -gt 0 ]; then
        echo -e "${YELLOW}⚠️  Warning: $missing_procedures procedure file(s) missing${NC}"
    fi

    echo -e "${GREEN}✅ Project environment validated${NC}"
    echo "$base_path"
}

# Function to display issue summary
display_issue_summary() {
    local issue_data=$1
    local project_info=$2

    local title=$(echo "$issue_data" | jq -r '.data.issues.nodes[0].title')
    local description=$(echo "$issue_data" | jq -r '.data.issues.nodes[0].description // "No description"')
    local state=$(echo "$issue_data" | jq -r '.data.issues.nodes[0].state.name')
    local assignee=$(echo "$issue_data" | jq -r '.data.issues.nodes[0].assignee.name // "Unassigned"')

    echo -e "${BLUE}📋 Issue Summary:${NC}"
    echo "  Title: $title"
    echo "  State: $state"
    echo "  Assignee: $assignee"
    echo "  Project: $project_info"
    echo ""
    echo "  Description:"
    echo "  $(echo "$description" | head -3 | sed 's/^/    /')"
    if [ $(echo "$description" | wc -l) -gt 3 ]; then
        echo "    ..."
    fi
}

# Main function
main() {
    local issue_number=$1

    if [ -z "$issue_number" ]; then
        echo -e "${RED}Usage: $0 <issue_number>${NC}"
        exit 1
    fi

    echo -e "${GREEN}🚀 Enhanced Linear Issue Analysis for #${issue_number}${NC}"
    echo "=================================================="

    # Step 1: Get complete issue information
    local issue_data=$(get_complete_issue_info "$issue_number")

    if [ -z "$issue_data" ] || [ "$(echo "$issue_data" | jq -r '.data.issues.nodes | length')" = "0" ]; then
        echo -e "${RED}❌ Issue #${issue_number} not found${NC}"
        exit 1
    fi

    # Step 2: Extract and validate project information
    local project_id=$(extract_project_info "$issue_data")
    if [ $? -ne 0 ]; then
        exit 1
    fi

    # Step 3: Get project mapping
    local project_mapping=$(get_project_mapping "$project_id")
    if [ $? -ne 0 ]; then
        exit 1
    fi

    # Step 4: Validate project environment
    local base_path=$(validate_project_environment "$project_mapping")
    if [ $? -ne 0 ]; then
        exit 1
    fi

    # Step 5: Display comprehensive summary
    echo ""
    echo "=================================================="
    display_issue_summary "$issue_data" "$project_id"

    echo -e "${GREEN}✅ Safe to proceed with project: $project_id${NC}"
    echo -e "${GREEN}✅ Working directory: $base_path${NC}"

    # Export environment variables for use by other scripts
    echo "export ISSUE_PROJECT_ID='$project_id'"
    echo "export ISSUE_BASE_PATH='$base_path'"
    echo "export ISSUE_MAPPING='$project_mapping'"
}

main "$@"
