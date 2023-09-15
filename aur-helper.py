#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess

AUR_DIR = os.path.expanduser("~/.aur-helper")

DEBUG = "--debug" in sys.argv

def run_cmd(cmd):
    if DEBUG:
        print(f"Executing: {' '.join(cmd)}\n")
        process = subprocess.Popen(cmd)
    else:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, stderr = process.communicate()

    if process.returncode != 0:
        return stderr.decode() if stderr else 'Unknown error.'
    return None

def run_cmd_with_output(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return process.returncode, stdout.decode(), stderr.decode()

def install_package(git_url):
    package_name = git_url.split("/")[-1].replace(".git", "")
    print(f"Installing package: {package_name}")

    os.makedirs(AUR_DIR, exist_ok=True)
    os.chdir(AUR_DIR)

    error = run_cmd(["git", "clone", git_url])
    if error:
        print(f"==> ERROR: Could not clone {package_name}. Message: {error}")
        print("Rolling back installation steps...")
        rollback_installation(package_name)
        sys.exit(1)

    os.chdir(package_name)
    error = run_cmd(["makepkg", "-si", "--noconfirm"])
    if error:
        print(f"==> ERROR: Could not install {package_name}. Message: {error}")
        print("Rolling back installation steps...")
        rollback_installation(package_name)
        sys.exit(1)

    print(f"Package {package_name} was successfully installed!")

def rollback_installation(package_name):
    package_path = os.path.join(AUR_DIR, package_name)
    if os.path.exists(package_path):
        print(f"Removing cloned directory: {package_path}")
        shutil.rmtree(package_path)
    else:
        print("No cloned directory found. Nothing to rollback.")

def remove_package(package_name):
    print(f"Attempting to remove package: {package_name}")

    error = run_cmd(["sudo", "pacman", "-Rns", package_name, "--noconfirm"])
    if error:
        print(f"==> ERROR: Could not remove {package_name}. Message: {error}")
        sys.exit(1)

    # Remove the directory from ~/.aur-helper
    package_dir = os.path.join(AUR_DIR, package_name)
    if os.path.exists(package_dir):
        print(f"Removing directory: {package_dir}")
        shutil.rmtree(package_dir)

    print(f"Package {package_name} was successfully removed!")

def update_packages():
    no_updates = True  # Initially assume no packages need updates

    for item in os.listdir(AUR_DIR):
        path = os.path.join(AUR_DIR, item)
        if os.path.isdir(path):
            print(f"Checking updates for: {item}")
            os.chdir(path)

            _, stdout, _ = run_cmd_with_output(["git", "pull"])

            if not "Already up to date." in stdout:
                no_updates = False  # An update was found for at least one package
                error = run_cmd(["makepkg", "-si", "--noconfirm"])
                if error:
                    print(f"==> ERROR: Could not update {item}. Message: {error}")
                    sys.exit(1)

    if no_updates:
        print("Nothing to do.")

if __name__ == "__main__":
    if DEBUG:  # If --debug is present, remove it from sys.argv for further processing
        sys.argv.remove("--debug")

    if len(sys.argv) < 2:
        print("Usage: aur-helper [install|remove|update] <args>")
        sys.exit(1)

    action = sys.argv[1]

    if action == "install" and len(sys.argv) > 2:
        install_package(sys.argv[2])
    elif action == "remove" and len(sys.argv) > 2:
        remove_package(sys.argv[2])
    elif action == "update":
        update_packages()
    else:
        print("Invalid command or missing arguments")
        sys.exit(1)

