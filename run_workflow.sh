#!/bin/bash

# This script executes the 8 phases of the development workflow in sequence.
# It stops if any phase fails.

set -e

# Check for issue ID argument
if [ -z "$1" ]; then
  echo "Usage: ./run_workflow.sh <issue_id>"
  exit 1
fi

ISSUE_ID=$1
echo "Starting workflow for issue: $ISSUE_ID"

# --- Execute Workflow ---
# The first phase outputs the project path, which is captured here.
PROJECT_PATH=$(python3 workflows/phase_1_discovery.py "$ISSUE_ID" | tail -n 1)
echo "Phase 1 finished. Project path: $PROJECT_PATH"

python3 workflows/phase_2_context_analysis.py "$PROJECT_PATH"
echo "Phase 2 finished."

python3 workflows/phase_3_requirements_analysis.py "$PROJECT_PATH"
echo "Phase 3 finished."

python3 workflows/phase_4_strategic_planning.py "$PROJECT_PATH"
echo "Phase 4 finished."

python3 workflows/phase_5_report_generation.py "$PROJECT_PATH"
echo "Phase 5 finished."

python3 workflows/phase_6_ai_review.py "$PROJECT_PATH"
echo "Phase 6 finished."

python3 workflows/phase_7_implementation.py "$PROJECT_PATH"
echo "Phase 7 finished."

python3 workflows/phase_8_documentation.py "$PROJECT_PATH"
echo "Phase 8 finished."

echo "Workflow completed successfully."
