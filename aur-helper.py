#!/usr/bin/env python3

import sys
import os
import subprocess

AUR_DIR = os.path.expanduser("~/.aur-helper")

def run_cmd(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return process.returncode, stdout.decode(), stderr.decode()

def install_package(git_url):
    os.makedirs(AUR_DIR, exist_ok=True)
    
    repo_name = os.path.basename(git_url).replace('.git', '')
    clone_path = os.path.join(AUR_DIR, repo_name)

    # Clone the repo
    returncode, stdout, stderr = run_cmd(["git", "clone", git_url, clone_path])
    if returncode != 0:
        print(stderr)
        return

    # Build and install the package
    os.chdir(clone_path)
    returncode, stdout, stderr = run_cmd(["makepkg", "-si", "--noconfirm"])
    if returncode != 0:
        print(stderr)

def update_packages():
    for item in os.listdir(AUR_DIR):
        path = os.path.join(AUR_DIR, item)
        if os.path.isdir(path):
            os.chdir(path)
            run_cmd(["git", "pull"])
            returncode, stdout, stderr = run_cmd(["makepkg", "-si", "--noconfirm"])
            if returncode != 0:
                print(stderr)

def remove_package(package_name):
    returncode, stdout, stderr = run_cmd(["sudo", "pacman", "-Rns", package_name, "--noconfirm"])
    if returncode != 0:
        print(stderr)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: aur-helper (install|update|remove) [arg]")
        sys.exit(1)

    action = sys.argv[1]
    
    if action == "install" and len(sys.argv) == 3:
        install_package(sys.argv[2])
    elif action == "update":
        update_packages()
    elif action == "remove" and len(sys.argv) == 3:
        remove_package(sys.argv[2])
    else:
        print("Invalid arguments!")
