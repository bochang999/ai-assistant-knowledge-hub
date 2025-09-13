#!/bin/bash

# Knowledge Loader Script for AI Assistant Knowledge Hub
# Usage: bash run.sh [project-name] "[user-instruction]"

set -e

# Check arguments
if [ $# -lt 2 ]; then
    echo "Usage: $0 <project-name> <user-instruction>"
    echo "Example: $0 project-A \"ビルドエラーが発生したので、build_error_correctionワークフローを開始して\""
    exit 1
fi

PROJECT_NAME="$1"
USER_INSTRUCTION="$2"

# Get script directory to handle relative paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Initialize prompt string
PROMPT=""

# 1. Always load commons/constitution.md
CONSTITUTION_FILE="$SCRIPT_DIR/commons/constitution.md"
if [ -f "$CONSTITUTION_FILE" ]; then
    echo "Loading constitution..."
    PROMPT+="# Constitutional Principles"$'\n\n'
    PROMPT+="$(cat "$CONSTITUTION_FILE")"$'\n\n'
else
    echo "Warning: constitution.md not found at $CONSTITUTION_FILE"
fi

# 2. Load project context
PROJECT_CONTEXT_FILE="$SCRIPT_DIR/projects/$PROJECT_NAME/context.md"
if [ -f "$PROJECT_CONTEXT_FILE" ]; then
    echo "Loading project context for $PROJECT_NAME..."
    PROMPT+="# Project Context: $PROJECT_NAME"$'\n\n'
    PROMPT+="$(cat "$PROJECT_CONTEXT_FILE")"$'\n\n'

    # 3. Parse context.md for workflow and template references
    echo "Parsing context.md for workflow and template references..."

    # Extract workflow references (look for workflows/filename.md patterns)
    WORKFLOW_REFS=$(grep -o 'workflows/[^)]*\.md' "$PROJECT_CONTEXT_FILE" 2>/dev/null || true)
    if [ -n "$WORKFLOW_REFS" ]; then
        echo "Found workflow references: $WORKFLOW_REFS"
        while IFS= read -r workflow_ref; do
            WORKFLOW_FILE="$SCRIPT_DIR/$workflow_ref"
            if [ -f "$WORKFLOW_FILE" ]; then
                echo "Loading workflow: $workflow_ref"
                PROMPT+="# Workflow: $(basename "$workflow_ref" .md)"$'\n\n'
                PROMPT+="$(cat "$WORKFLOW_FILE")"$'\n\n'
            else
                echo "Warning: Referenced workflow not found: $WORKFLOW_FILE"
            fi
        done <<< "$WORKFLOW_REFS"
    fi

    # Extract template references (look for templates/filename.md patterns)
    TEMPLATE_REFS=$(grep -o 'templates/[^)]*\.md' "$PROJECT_CONTEXT_FILE" 2>/dev/null || true)
    if [ -n "$TEMPLATE_REFS" ]; then
        echo "Found template references: $TEMPLATE_REFS"
        while IFS= read -r template_ref; do
            TEMPLATE_FILE="$SCRIPT_DIR/$template_ref"
            if [ -f "$TEMPLATE_FILE" ]; then
                echo "Loading template: $template_ref"
                PROMPT+="# Template: $(basename "$template_ref" .md)"$'\n\n'
                PROMPT+="$(cat "$TEMPLATE_FILE")"$'\n\n'
            else
                echo "Warning: Referenced template not found: $TEMPLATE_FILE"
            fi
        done <<< "$TEMPLATE_REFS"
    fi

else
    echo "Warning: Project context not found at $PROJECT_CONTEXT_FILE"
    echo "Available projects:"
    ls -1 "$SCRIPT_DIR/projects/" 2>/dev/null | grep -v '.gitkeep' || echo "No projects found"
fi

# 4. Add user instruction
PROMPT+="# User Instruction"$'\n\n'
PROMPT+="$USER_INSTRUCTION"$'\n'

# 5. Execute claude-cli with the assembled prompt
echo "Executing claude-cli with assembled knowledge..."
echo "=========================================="

# Pass the prompt to claude-cli via stdin
echo "$PROMPT" | claude-cli

echo "=========================================="
echo "Knowledge loader execution completed."