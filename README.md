# AUR Helper

AUR Helper is a simple Python script designed to simplify the process of installing, updating, removing, and listing AUR packages on an Arch Linux system.

## Features

- **Install AUR packages** directly using Git repository URLs.
- **Update all installed AUR packages** with a single command.
- **Remove specific AUR packages** that were installed using this script.
- **List all installed AUR packages** managed by this script.

## Disclaimer

Usage of this script is at your own risk. The author is not responsible for any damage or issues caused by this script, as it is a private project.

## Usage

1. **Install Packages**
    ```
    aur-helper install [link-to-git-repository1] [link-to-git-repository2] ...
    ```

2. **Remove Packages**
    ```
    aur-helper remove [packagename1] [packagename2] ...
    ```

3. **Update Installed Packages**
    ```
    aur-helper update
    ```

4. **List Installed Packages**
    ```
    aur-helper list
    ```

5. **Debug Mode**  
   Add the `--debug` flag to see detailed output of the commands:
   ```
   aur-helper --debug install [link-to-git-repository]
   ```
