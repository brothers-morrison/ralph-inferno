#!/usr/bin/env python3
"""
VM Setup Script for Ralph-Inferno Project

Converts the original bash setup script to Python for better maintainability
and cross-platform compatibility.
Not sure how much I like it now that I see it.  TBD: rework.

TODO:
- Upgrade to use Terraform instead of manual/scripted setup
- Explore CI/CD options (GitHub Actions, etc.)
- Automate GitHub CLI authentication
- Fix SSH key addition via gh CLI

.EXAMPLE
    # Set environment variables (never hardcode sensitive data!)
    export GIT_EMAIL='your-email@users.noreply.github.com'
    export OPENROUTER_API_KEY='your-actual-api-key'
    export GITHUB_REPO='https://github.com/sandstream/ralph-inferno.git'  # optional

    # Run the script
    chmod +x vm_setup.py
    python3 vm_setup.py

    ## NOTE: files got put under here after install local
    C:\Users\<username>\.ralph\
    C:\Users\<username>\.ralph\.claude\commands
"""

import subprocess
import sys
import os
from typing import Optional, Union, List
from pathlib import Path


class CommandLineInterface:
    """Utility class for running shell commands."""
    
    @staticmethod
    def run(
        command: Union[str, List[str]],
        shell: bool = False,
        capture: bool = True,
        check: bool = True,
        cwd: Optional[str] = None,
        env: Optional[dict] = None,
        timeout: Optional[int] = None
    ) -> subprocess.CompletedProcess:
        """
        Execute a shell command and return the result.
        
        Args:
            command: Command to execute (string if shell=True, list otherwise)
            shell: Whether to run command through shell
            capture: Whether to capture stdout/stderr
            check: Whether to raise exception on non-zero exit
            cwd: Working directory for command
            env: Environment variables
            timeout: Timeout in seconds
        
        Returns:
            CompletedProcess object with stdout, stderr, returncode
        """
        try:
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=capture,
                text=True,
                check=check,
                cwd=cwd,
                env=env,
                timeout=timeout
            )
            return result
        except subprocess.CalledProcessError as e:
            print(f"Command failed with exit code {e.returncode}", file=sys.stderr)
            print(f"stdout: {e.stdout}", file=sys.stderr)
            print(f"stderr: {e.stderr}", file=sys.stderr)
            raise
        except subprocess.TimeoutExpired as e:
            print(f"Command timed out after {timeout} seconds", file=sys.stderr)
            raise
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            raise
            

    @staticmethod
    def print_box(message: str, boxchar: str = '-'):
            """Print a formatted block:"""
            print(f"\n{boxchar*100}")
            print(f"{boxchar}  {message}  {boxchar}")
            print(f"{boxchar*100}\n")

    @staticmethod
    def print_h2_header(message: str, divider_char: str = '-'):
            """Print a formatted section header."""
            print(f"{divider_char*10}  {message}  {divider_char*10}")

    @staticmethod
    def print_title_header(message: str, divider_char: str = '🔥'):
            """Print a formatted section header."""
            CommandLineInterface.print_box(message, divider_char)


def h2(message: str, divider_char: str = '-'):
    """Print a formatted section header."""
    CommandLineInterface.print_h2_header(message, divider_char)


def title(message: str, divider_char: str = '🔥'):
    """Print a formatted section header."""
    CommandLineInterface.print_title_header(message, divider_char)


class VMSetup:
    """Main setup class for configuring VM for Ralph-Inferno."""
    
    def __init__(self, github_repo: str, email: str, api_key: str, project_repo: str = ""):
        self.github_repo = github_repo
        self.project_repo = project_repo
        self.email = email
        self.api_key = api_key
        self.cli = CommandLineInterface()

    def run(self, *args, **kwargs):
        """Shorthand for self.cli.run()"""
        return self.cli.run(*args, **kwargs)

    def cmd(self, command: str):
        """
        .SYNOPSIS
            shorthand / alias for the more verbose, and more precise self.cli.run
            self.cli.run(['git', 'clone', self.github_repo])
            
        .EXAMPLE
            # trying to more accurately reflect what the exact command line script would be, 
            # which could be copy+pasted directly in and wrapped with this function.
            cmd(f'git clone {self.github_repo}')
        
            # however, the longer form, split apart args version self.cli.run([]) is recommended for better accuracy.
        """
        args = command.split(' ')
        self.cli.run(args)
        return
    
    
    def clone_and_configure_git(self):
        """Clone repository and configure Git settings."""
        title(VMSetup.clone_and_configure_git.__doc__)

        print("NOTE: GitHub Personal Access Tokens (PAT) can only be used with HTTPS, not SSH")
        print("See: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens")

        # Clone repository
        h2(f"\nCloning repository: {self.github_repo}")
        self.run(['git', 'clone', self.github_repo])

        # Configure Git globally
        h2("\nConfiguring Git user settings...")
        self.run(['git', 'config', '--global', 'user.email', self.email])
        self.run(['git', 'config', '--global', 'user.name', 'Ralph Wiggum'])

        h2("✓ Git configuration complete")
    
    def setup_nodejs(self):
        """Install Node.js and npm."""
        title(VMSetup.setup_nodejs.__doc__)

        # Make setup.sh executable (if it exists)
        if Path('setup.sh').exists():
            self.run(['sudo', 'chmod', '+x', 'setup.sh'])

        # Install Node.js
        h2("Installing Node.js 20.x...")
        self.run(
            'curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -',
            shell=True
        )
        self.run(['sudo', 'apt-get', 'install', '-y', 'nodejs'])

        # Verify installation
        result = self.run(['node', '--version'])
        print(f"✓ Node.js installed: {result.stdout.strip()}")

        result = self.run(['npm', '--version'])
        print(f"✓ npm installed: {result.stdout.strip()}")

    def setup_api_key(self):
        """Configure OpenRouter API key."""
        title(VMSetup.setup_api_key.__doc__)

        h2("Setting OPENROUTER_API_KEY environment variable...")
        os.environ['OPENROUTER_API_KEY'] = self.api_key

        # Add to .bashrc for persistence
        bashrc_path = Path.home() / '.bashrc'
        export_line = f'export OPENROUTER_API_KEY="{self.api_key}"\n'

        with open(bashrc_path, 'a') as f:
            f.write(f'\n# Added by VM setup script\n{export_line}')

        print("✓ API key configured and added to .bashrc")

    def setup_playwright(self):
        """Install Playwright and its dependencies."""
        title(VMSetup.setup_playwright.__doc__)

        h2("Installing Playwright dependencies...")
        self.run(['npx', 'playwright', 'install-deps'])

        h2("Installing Playwright browsers...")
        self.run(['npx', 'playwright', 'install'])

        print("✓ Playwright installation complete")

    def setup_github_cli(self):
        """Install and configure GitHub CLI."""
        title(VMSetup.setup_github_cli.__doc__)

        h2("Installing GitHub CLI...")
        self.run(['sudo', 'apt-get', 'install', '-y', 'gh'])

        title("MANUAL STEP REQUIRED: GitHub CLI Authentication")

        print("\nPlease run the following command manually and follow the prompts:")
        print("  gh auth login")
        print("\nThis will authenticate you with GitHub interactively.")
        print("TODO: Explore automation options for this step\n")

    def setup_ssh_keys(self):
        """Generate SSH keys for GitHub."""
        title(VMSetup.setup_ssh_keys.__doc__)

        ssh_key_path = Path.home() / '.ssh' / 'id_ed25519'

        if ssh_key_path.exists():
            print(f"SSH key already exists at {ssh_key_path}")
            response = input("Do you want to overwrite it? (y/N): ")
            if response.lower() != 'y':
                print("Skipping SSH key generation")
                return

        print(f"Generating SSH key with email: {self.email}")
        title("MANUAL STEP: You will be prompted for a passphrase")

        try:
            self.run(
                ['ssh-keygen', '-t', 'ed25519', '-C', self.email],
                capture=False  # Let user see prompts
            )
        except subprocess.CalledProcessError:
            print("SSH key generation was cancelled or failed")
            return

        pub_key_path = Path.home() / '.ssh' / 'id_ed25519.pub'

        if pub_key_path.exists():
            with open(pub_key_path, 'r') as f:
                pub_key = f.read().strip()

            title("SSH Public Key Generated")
            print(f"\nYour public key:\n{pub_key}\n")
            print("Please add this key to your GitHub account:")
            print("  https://github.com/settings/keys")
            print("\nNote: The 'gh ssh-key add' command currently fails with:")
            print("  'HTTP 403: Resource not accessible by personal access token'")
            print("TODO: Fix automated SSH key addition via gh CLI\n")
        else:
            print("SSH key file not found after generation")

    def sync_repository(self, repo_name: str):
        """Fetch, pull, and push repository changes."""
        title(VMSetup.sync_repository.__doc__)
        
        repo_path = Path(repo_name)
        if not repo_path.exists():
            print(f"Repository directory '{repo_name}' not found")
            return
        
        print(f"Working in repository: {repo_path}")
        
        # Fetch updates
        print("Fetching from remote...")
        self.run(['git', 'fetch'], cwd=str(repo_path))

        # Pull changes
        print("Pulling changes...")
        try:
            self.run(['git', 'pull'], cwd=str(repo_path))
        except subprocess.CalledProcessError as e:
            print(f"Warning: git pull failed: {e}")

        # Push changes
        print("Pushing to remote...")
        try:
            self.run(
                ['git', 'push', '--set-upstream', 'origin', 'main'],
                cwd=str(repo_path)
            )
        except subprocess.CalledProcessError as e:
            print(f"Warning: git push failed: {e}")
            print("You may need to authenticate or set up the remote properly")
    
    def run_full_setup(self):
        """Execute the complete setup process."""
        title(VMSetup.run_full_setup.__doc__)

        print("\n" + "="*70)
        print("  Ralph-Inferno VM Setup Script")
        print("="*70)
        
        try:
            self.clone_and_configure_git()
            self.setup_nodejs()
            self.setup_api_key()
            self.setup_playwright()
            self.setup_github_cli()
            self.setup_ssh_keys()
            
            # Extract repo name from URL
            repo_name = self.github_repo.split('/')[-1].replace('.git', '')
            self.sync_repository(repo_name)
            
            CommandLineInterface.print_title_header("Setup Complete!")
            print("Your VM is now configured for Ralph-Inferno development.")
            print("\nNext steps:")
            print("  1. Complete GitHub CLI authentication: gh auth login")
            print("  2. Add your SSH key to GitHub (see above)")
            print("  3. Navigate to your repository and start developing!")
            
        except Exception as e:
            print(f"\n❌ Setup failed with error: {e}", file=sys.stderr)
            sys.exit(1)

    @staticmethod
    def get_secrets_from_env():
        title(VMSetup.get_secrets_from_env.__doc__)

        # Configuration - IMPORTANT: Do not hardcode sensitive values!
        # These should be passed as environment variables or command-line arguments
        GITHUB_REPO = os.getenv('GITHUB_REPO', 'https://github.com/sandstream/ralph-inferno.git')
        EMAIL = os.getenv('GIT_EMAIL', '{{your-masked-github-email-here@users.noreply.github.com}}')
        API_KEY = os.getenv('OPENROUTER_API_KEY', '{{inject-your-key-here-do-not-hardcode}}')
        PROJECT_REPO = os.getenv('PROJECT_REPO', '')
        
        # Validate configuration
        if '{{' in EMAIL or '{{' in API_KEY:
            print("\n❌ ERROR: Please configure environment variables before running!", file=sys.stderr)
            print("\nRequired environment variables:")
            print("  export GIT_EMAIL='your-email@users.noreply.github.com'")
            print("  export OPENROUTER_API_KEY='your-api-key-here'")
            print("  export GITHUB_REPO='https://github.com/your-username/your-repo.git'  # optional")
            sys.exit(1)
        
        # Run setup
        return VMSetup(
            github_repo=GITHUB_REPO,
            email=EMAIL,
            api_key=API_KEY,
            project_repo=PROJECT_REPO
        )


def main():
    """Main entry point for the setup script."""
    title(main.__doc__)

    vm_setup = VMSetup.get_secrets_from_env()
    vm_setup.run_full_setup()


if __name__ == '__main__':
    main()