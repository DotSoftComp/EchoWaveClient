import os
import subprocess
import sys

# Step 1: Check if Python is installed
def check_python_installed():
    try:
        # Try to get the Python version
        subprocess.run(["python", "--version"], check=True)
        print("Python is already installed.")
        return True
    except subprocess.CalledProcessError:
        print("Python is not installed.")
        return False

# Step 2: Download and install Python if not installed
def install_python():
    # This step will vary depending on your OS and setup
    print("Downloading and installing Python...")
    
    # Example for Windows:
    os.system('curl -o python-installer.exe https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe')
    os.system('start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1')
    
    # You can customize this section for other operating systems or Python versions


# List of requirements as strings
list_of_requirements = [
    "google-auth-oauthlib",
    "google-auth",
    "requests",
    "PyPDF2"
]

def install_packages():
    for package in list_of_requirements:
        command = f"{sys.executable} -m pip install {package}"
        print(f"Executing command: {command}")
        try:
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
            print(result.stdout)
            print(f"{package} a été installé avec succès.")
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de l'installation de {package}:\n{e.stderr}")
            sys.exit(1)

    print("Tous les paquets ont été installés avec succès.")
    input("Press a key to continue...")

if __name__ == "__main__":
    print("starting the installation of the libraries...")
    install_packages()



def main():
    input("install python")
    if not check_python_installed():
        install_python()

    install_packages()

if __name__ == "__main__":
    main()
