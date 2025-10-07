# workflows/phase_1_discovery.py
import sys


def phase_1_discovery(issue_id):
    """
    Phase 1: Issue Intelligence & Project Discovery
    - Fetches issue details from a source (e.g., Linear).
    - Identifies the project context.
    """
    print(f"--- Phase 1: Discovering issue {issue_id} ---")
    # Placeholder for actual logic:
    # - API call to Linear/Jira
    # - Look up project path from a mapping file
    print("Fetching issue details...")
    print("Identifying project context...")
    project_path = "."  # Placeholder
    print(f"Project path identified: {project_path}")
    print("--- Phase 1 Complete ---")
    return project_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python workflows/phase_1_discovery.py <issue_id>")
        sys.exit(1)

    issue_id = sys.argv[1]
    project_path = phase_1_discovery(issue_id)
    # Print the project path so it can be piped to the next script
    print(project_path)
