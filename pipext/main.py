import sys
import subprocess
import os
from rich.console import Console
from rich.panel import Panel

console = Console()

DEFAULT_REQUIREMENTS_FILE = 'requirements.txt'
REQUIREMENTS_DIR = 'requirements'


def get_requirements_file(args):
    """Get the path to the requirements file."""
            
    # If the '-e' flag is provided, extract the environment name
    if '-e' in args:
        env_index = args.index('-e')
        if env_index + 1 < len(args):
            env_name = args[env_index + 1]
            # Remove the -e flag and its argument from args list
            args.pop(env_index)
            args.pop(env_index)
            file_name = f"{env_name}.txt"
            file_path = os.path.join(REQUIREMENTS_DIR, file_name)

            # If requirements directory doesn't exist, create it
            if not os.path.exists(REQUIREMENTS_DIR):
                os.mkdir(REQUIREMENTS_DIR)
            
            # Create the environment-specific requirements file if it doesn't exist
            if not os.path.exists(file_path):
                open(file_path, "w").close()

            return file_path
    else:
        # Ensure the requirements file is created if it does not exist
        if not os.path.exists(DEFAULT_REQUIREMENTS_FILE):
            open(DEFAULT_REQUIREMENTS_FILE, "w").close()

    return DEFAULT_REQUIREMENTS_FILE

def get_installed_version(package_name):
    """Get the version of an installed package."""
    installed_packages = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']).decode('utf-8').splitlines()
    for package in installed_packages:
        if package.startswith(package_name + '=='):
            return package
    return None

def comment_out_package_in_requirements(package_name, req_file):
    """Comment out a package in the specified requirements file."""
    with open(req_file, 'r') as f:
        lines = f.readlines()
    
    with open(req_file, 'w') as f:
        for line in lines:
            if line.startswith(package_name):
                f.write(f"# {line}")
            else:
                f.write(line)

def extract_base_package_name(package_name):
    """Extract the base package name without any optional dependencies."""
    return package_name.split("[")[0].replace("'", "")

def uncomment_or_append_in_requirements(installed_version, req_file):
    """Uncomment a package in the specified requirements file."""
    with open(req_file, 'r') as f:
        lines = f.readlines()

    # Check if the package (commented or not) exists in the requirements
    found = False
    with open(req_file, 'w') as f:
        for line in lines:
            if line.startswith(f"# {installed_version}") or line.startswith(installed_version):
                f.write(installed_version + "\n")
                found = True
            else:
                f.write(line)
    
    # If not found, append it
    if not found:
        with open(req_file, 'a') as f:
            f.write(installed_version + "\n")

def install_and_update_requirements(args):
    # Use pip to install the package
    req_file = get_requirements_file(args)
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', args[-1]])

        # Extract the base package name
        base_package_name = extract_base_package_name(args[-1])

        # Get the installed version
        installed_version = get_installed_version(base_package_name)

        # Uncomment or append to requirements.txt
        if installed_version:
            uncomment_or_append_in_requirements(installed_version, req_file)
            message = f"Updated requirements.txt with [green]{installed_version}[/green]"
            console.print(Panel(message, title="Package Update", expand=False))
        else:
            message = f"Could not retrieve the version for [red]{base_package_name}.[/red] Please check manually."
            console.print(Panel(message, title="Error", expand=False))
    except Exception as e:
        pass
        

def uninstall_and_comment_out_requirements(args):
    req_file = get_requirements_file(args)
    # Use pip to uninstall the package
    subprocess.check_call([sys.executable, '-m', 'pip', 'uninstall', '-y', args[-1]])
    
    # Extract the base package name
    base_package_name = extract_base_package_name(args[-1])

    # Comment out the package in requirements.txt
    comment_out_package_in_requirements(base_package_name, req_file)

    message = f"Commented out [yellow]{base_package_name}[/yellow] in requirements.txt"
    console.print(Panel(message, title="Package Update", expand=False))

def main():
    if len(sys.argv) > 2:
        action = sys.argv[1]
        args = sys.argv[2:]
        
        if action == "install":
            install_and_update_requirements(args)
        elif action == "uninstall":
            uninstall_and_comment_out_requirements(args)
        else:
            message = f"[red]Invalid action. Use either 'install' or 'uninstall'.[/red]"
            console.print(Panel(message, title="Error", expand=False))
    else:
        message = f"[red]Please provide an action (install/uninstall) and a package name.[/red]"
        console.print(Panel(message, title="Error", expand=False))
