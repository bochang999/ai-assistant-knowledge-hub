# workflows/phase_8_documentation.py
import sys


def phase_8_documentation(project_path):
    """
    Phase 8: Documentation & Continuity
    - Automatically commits work to GitHub.
    - Saves context for the next session.
    """
    print(f"--- Phase 8: Documenting changes for project at {project_path} ---")
    # Placeholder for actual logic:
    # - Stage changes with 'git add'
    # - Generate a commit message and run 'git commit'
    # - Save key details to a session file
    print("Committing work to version control...")
    print("Saving context for next session...")
    print("--- Phase 8 Complete ---")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python workflows/phase_8_documentation.py <project_path>")
        sys.exit(1)

    project_path = sys.argv[1]
    phase_8_documentation(project_path)
