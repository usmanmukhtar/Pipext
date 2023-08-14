import sys
import subprocess

def get_installed_version(package_name):
    """Get the version of an installed package."""
    installed_packages = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']).decode('utf-8').splitlines()
    for package in installed_packages:
        if package.startswith(package_name + '=='):
            return package
    return None

def comment_out_package_in_requirements(package_name):
    """Comment out a package in requirements.txt."""
    with open('requirements.txt', 'r') as f:
        lines = f.readlines()
    
    with open('requirements.txt', 'w') as f:
        for line in lines:
            if line.startswith(package_name):
                f.write(f"# {line}")
            else:
                f.write(line)

def uncomment_or_append_in_requirements(installed_version):
    """Uncomment a package in requirements.txt or append it if not found."""
    with open('requirements.txt', 'r') as f:
        lines = f.readlines()

    # Check if the package (commented or not) exists in the requirements
    found = False
    with open('requirements.txt', 'w') as f:
        for line in lines:
            if line.startswith(f"# {installed_version}") or line.startswith(installed_version):
                f.write(installed_version + "\n")
                found = True
            else:
                f.write(line)
    
    # If not found, append it
    if not found:
        with open('requirements.txt', 'a') as f:
            f.write(installed_version + "\n")

def install_and_update_requirements(package_name):
    # Use pip to install the package
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name])

    # Get the installed version
    installed_version = get_installed_version(package_name)

    # Uncomment or append to requirements.txt
    if installed_version:
        uncomment_or_append_in_requirements(installed_version)
        print(f"Updated requirements.txt with {installed_version}")
    else:
        print(f"Could not retrieve the version for {package_name}. Please check manually.")

def uninstall_and_comment_out_requirements(package_name):
    # Use pip to uninstall the package
    subprocess.check_call([sys.executable, '-m', 'pip', 'uninstall', '-y', package_name])

    # Comment out the package in requirements.txt
    comment_out_package_in_requirements(package_name)
    print(f"Commented out {package_name} in requirements.txt")

def main():
    if len(sys.argv) > 2:
        action = sys.argv[1]
        package_name = sys.argv[2]
        
        if action == "install":
            install_and_update_requirements(package_name)
        elif action == "uninstall":
            uninstall_and_comment_out_requirements(package_name)
        else:
            print("Invalid action. Use either 'install' or 'uninstall'.")
    else:
        print("Please provide an action (install/uninstall) and a package name.")
