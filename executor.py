import subprocess
import sys

def write_file(path, content):
    try:
        with open(path, 'w') as f:
            f.write(content)
        print("SUCCESS: File written successfully.")
        return True
    except Exception as e:
        print(f"ERROR: Failed to write file: {e}")
        return False

def run_command(command_string):
    try:
        result = subprocess.run(command_string, shell=True, check=True, capture_output=True, text=True)
        print(f"SUCCESS: Command executed successfully.\nStdout: {result.stdout}\nStderr: {result.stderr}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Command failed with exit code {e.returncode}.\nStdout: {e.stdout}\nStderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"ERROR: Failed to run command: {e}")
        return False

def git_push(commit_message):
    try:
        # Add all changes
        run_command("git add .")
        # Commit changes
        run_command(f'git commit -m "{commit_message}"')
        # Push to remote
        run_command("git push")
        print("SUCCESS: Git push completed successfully.")
        return True
    except Exception as e:
        print(f"ERROR: Git push failed: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ERROR: No function specified.")
        sys.exit(1)

    function_name = sys.argv[1]
    args = sys.argv[2:]

    if function_name == "write_file":
        if len(args) != 2:
            print("ERROR: write_file requires path and content arguments.")
            sys.exit(1)
        write_file(args[0], args[1])
    elif function_name == "run_command":
        if len(args) != 1:
            print("ERROR: run_command requires a command string argument.")
            sys.exit(1)
        run_command(args[0])
    elif function_name == "git_push":
        if len(args) != 1:
            print("ERROR: git_push requires a commit message argument.")
            sys.exit(1)
        git_push(args[0])
    else:
        print(f"ERROR: Unknown function: {function_name}")
        sys.exit(1)
