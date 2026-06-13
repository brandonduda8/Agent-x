import subprocess
import os

def initialize_git_repo(project_dir: str) -> str:
    """Initializes a git repo and commits the generated code."""
    print(f"🚀 [DEPLOY] Initializing Git in {project_dir}...")
    try:
        # Configure git locally to prevent prompts
        subprocess.run(["git", "config", "--global", "user.email", "agent-x@local"], capture_output=True)
        subprocess.run(["git", "config", "--global", "user.name", "Agent-X"], capture_output=True)
        
        os.chdir(project_dir)
        subprocess.run(["git", "init"], capture_output=True)
        subprocess.run(["git", "add", "."], capture_output=True)
        result = subprocess.run(["git", "commit", "-m", "chore: initial AI-generated build"], capture_output=True, text=True)
        
        if result.returncode == 0:
            return f"✅ Git repo initialized and committed successfully in {project_dir}"
        else:
            return f"⚠️ Git commit warning: {result.stderr}"
    except Exception as e:
        return f"❌ Git deployment failed: {str(e)}"
