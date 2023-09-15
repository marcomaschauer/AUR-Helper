#!/usr/bin/env python3

import os
import sys
import subprocess
import shutil

AUR_DIR = os.path.expanduser("~/.aur-helper")
DEBUG = False

def run_cmd_with_output(cmd, cwd=None):
    try:
        result = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, universal_newlines=True)
        if DEBUG:
            print(result.stdout)
            print(result.stderr, file=sys.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(e.output, file=sys.stderr)
        return False

def rollback_installation(pkg_name):
    pkg_path = os.path.join(AUR_DIR, pkg_name)
    if os.path.exists(pkg_path):
        shutil.rmtree(pkg_path)
        print(f"==> Rolled back changes for {pkg_name}.")


def install_package(repositories):
    for repo in repositories:
        repo_name = repo.split('/')[-1].replace('.git', '')
        if not os.path.exists(os.path.join(AUR_DIR, repo_name)):
            if run_cmd_with_output(['git', 'clone', repo], AUR_DIR):
                if run_cmd_with_output(['makepkg', '-si', '--noconfirm'], os.path.join(AUR_DIR, repo_name)):
                    print(f"==> Successfully installed {repo_name}")
                else:
                    rollback_installation(repo_name)
                    print(f"==> ERROR: Could not install {repo_name}")
                    sys.exit(1)
            else:
                rollback_installation(repo_name)
                print(f"==> ERROR: Could not clone repository for {repo_name}")
                sys.exit(1)
        else:
            print(f"{repo_name} is already installed. Use 'update' to update it.")

def remove_package(packages):
    for pkg in packages:
        pkg_dir = os.path.join(AUR_DIR, pkg)
        if os.path.exists(pkg_dir):
            if run_cmd_with_output(['sudo', 'pacman', '-Rns', '--noconfirm', pkg]):
                shutil.rmtree(pkg_dir)
                print(f"==> Successfully removed {pkg}")
            else:
                print(f"==> ERROR: Could not remove {pkg}. Please check if it's correctly installed or if it's a valid package name.")
        else:
            print(f"{pkg} is not managed by aur-helper or doesn't exist.")


def update_packages():
    updates_available = False
    for dir_name in os.listdir(AUR_DIR):
        dir_path = os.path.join(AUR_DIR, dir_name)
        if os.path.isdir(dir_path):
            print(f"==> Checking updates for {dir_name}")
            git_result = subprocess.run(["git", "pull"], cwd=dir_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            if DEBUG:
                print(git_result.stdout)
            if not git_result.returncode == 0 or "Already up to date." not in git_result.stdout:
                updates_available = True
                if run_cmd_with_output(['makepkg', '-si', '--noconfirm'], dir_path):
                    print(f"==> Successfully updated {dir_name}")
                else:
                    print(f"==> ERROR: Could not update {dir_name}")
                    sys.exit(1)
    if not updates_available:
        print("Nothing to do.")

def list_packages():
    if not os.path.exists(AUR_DIR):
        print("No AUR packages installed by aur-helper.")
        return

    packages = [d for d in os.listdir(AUR_DIR) if os.path.isdir(os.path.join(AUR_DIR, d))]
    if not packages:
        print("No AUR packages installed by aur-helper.")
    else:
        print("Installed AUR packages:")
        for pkg in packages:
            print(f"- {pkg}")

if __name__ == "__main__":
    if "--debug" in sys.argv:
        DEBUG = True
        sys.argv.remove("--debug")

    if len(sys.argv) < 2:
        print("Usage: aur-helper [install|remove|update|list] <args>")
        sys.exit(1)

    action = sys.argv[1]

    if action == "install" and len(sys.argv) > 2:
        install_package(sys.argv[2:])
    elif action == "remove" and len(sys.argv) > 2:
        remove_package(sys.argv[2:])
    elif action == "update":
        update_packages()
    elif action == "list":
        list_packages()
    else:
        print("Invalid command or missing arguments")
        sys.exit(1)
