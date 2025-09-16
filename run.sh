#!/bin/bash

# Knowledge Loader Script for AI Assistant Knowledge Hub
# Usage: bash run.sh [project-name] "[ai-command]" "[user-instruction]" [--debug]

echo "[PROOF] 'run.sh' started for project $1 at $(date)" >> ~/execution.log

set -e

# Initialize variables
DEBUG=false

# Parse arguments and options
ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        --debug)
            DEBUG=true
            shift
            ;;
        *)
            ARGS+=("$1")
            shift
            ;;
    esac
done

# Check required arguments
if [ ${#ARGS[@]} -lt 3 ]; then
    echo "Usage: $0 <project-name> <ai-command> <user-instruction> [--debug]"
    echo "Example: $0 knowledge_hub_mng \"claude-cli\" \"タスクを洗い出して\" --debug"
    echo "Example: $0 project-A \"gemini-cli\" \"ビルドエラーが発生したので、build_error_correctionワークフローを開始して\""
    exit 1
fi

PROJECT_NAME="${ARGS[0]}"
AI_COMMAND="${ARGS[1]}"
USER_INSTRUCTION="${ARGS[2]}"

# Get script directory to handle relative paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if AI command exists in system PATH
if ! command -v "$AI_COMMAND" &> /dev/null; then
    echo "Error: AI command '$AI_COMMAND' not found in system PATH."
    echo "Please ensure the specified AI command is installed and accessible."
    exit 1
fi

# Initialize prompt string
PROMPT=""

# 1. Always load commons/constitution.md (required file)
CONSTITUTION_FILE="$SCRIPT_DIR/commons/constitution.md"
if [ -f "$CONSTITUTION_FILE" ]; then
    echo "Loading constitution..."
    PROMPT+="# Constitutional Principles"$'

'
    PROMPT+="$(cat "$CONSTITUTION_FILE")"$'

'
else
    echo "Error: Required file 'constitution.md' not found at $CONSTITUTION_FILE"
    echo "Please ensure the constitutional principles file exists in the commons/ directory."
    exit 1
fi

# 2. Load project context (required file)
PROJECT_CONTEXT_FILE="$SCRIPT_DIR/projects/$PROJECT_NAME/context.md"
if [ -f "$PROJECT_CONTEXT_FILE" ]; then
    echo "Loading project context for $PROJECT_NAME..."
    PROMPT+="# Project Context: $PROJECT_NAME"$'

'
    PROMPT+="$(cat "$PROJECT_CONTEXT_FILE")"$'

'

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
                PROMPT+="# Workflow: $(basename "$WORKFLOW_FILE" .md)"$'

'
                PROMPT+="$(cat "$WORKFLOW_FILE")"$'

'
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
                PROMPT+="# Template: $(basename "$TEMPLATE_FILE" .md)"$'

'
                PROMPT+="$(cat "$TEMPLATE_FILE")"$'

'
            else
                echo "Warning: Referenced template not found: $TEMPLATE_FILE"
            fi
        done <<< "$TEMPLATE_REFS"
    fi

else
    echo "Error: Project context file not found at $PROJECT_CONTEXT_FILE"
    echo "Available projects:"
    ls -1 "$SCRIPT_DIR/projects/" 2>/dev/null | grep -v '.gitkeep' || echo "No projects found"
    echo "Please ensure the project '$PROJECT_NAME' exists with a context.md file."
    exit 1
fi

# 4. Add executor.py instructions
PROMPT+='''# Executor.py Usage Instructions

To perform file system operations or Git actions, you MUST use the `executor.py` script. Do NOT use direct shell commands like `echo > file`, `git add`, `git commit`, `git push`, `mkdir`, `rm`, etc.

Here are the available functions in `executor.py` and how to use them:

## 1. write_file(path, content)
Writes the given content to the specified file path.

**Usage:**
`"$SCRIPT_DIR/executor.py" write_file "path/to/file.txt" "Content to write"`

**Example:**
`"$SCRIPT_DIR/executor.py" write_file "report.md" "## Daily Report\n- Task A completed\n- Task B in progress"

## 2. run_command(command_string)
Executes a shell command. Use this for any command that is not a file write or Git operation.

**Usage:**
`"$SCRIPT_DIR/executor.py" run_command "ls -la"`

**Example:**
`"$SCRIPT_DIR/executor.py" run_command "npm install"

## 3. git_push(commit_message)
Performs `git add .`, `git commit -m "commit_message"`, and `git push`.

**Usage:**
`"$SCRIPT_DIR/executor.py" git_push "Your commit message"`

**Example:**
`"$SCRIPT_DIR/executor.py" git_push "feat: Add new report generation logic"

**IMPORTANT:**
- Always enclose path and content arguments in double quotes.
- Always use `"$SCRIPT_DIR/executor.py"` when calling the executor script.
- The executor.py script will print "SUCCESS" or "ERROR" to stdout. You should capture and report these results.

'''

PROMPT+="# User Instruction"$'

'
PROMPT+="$USER_INSTRUCTION"$'
'

# 5. Debug output (if enabled)
if [ "$DEBUG" = true ]; then
    echo "=========================================="
    echo "DEBUG: Final assembled prompt:"
    echo "=========================================="
    echo "$PROMPT"
    echo "=========================================="
    echo "DEBUG: Executing AI command: $AI_COMMAND"
    echo "=========================================="
fi

# 6. Execute AI command with the assembled prompt
echo "Executing $AI_COMMAND with assembled knowledge..."
echo "=========================================="

# Pass the prompt to the AI command via stdin
echo "$PROMPT" | "$AI_COMMAND"

echo "=========================================="
echo "Knowledge loader execution completed."
