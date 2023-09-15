## AUR Helper

A simple tool to manage AUR packages on Arch Linux.

### Features

- **Installation**: Easily install packages directly from git repositories.
- **Update**: Update all installed AUR packages.
- **Removal**: Remove installed AUR packages and their associated data.

### Usage

1. **Installing AUR Packages**:

   Use the `install` command followed by the link to the git repository.
   
   ```bash
   aur-helper install [link-to-git-repository]
   ```
   
   In case of errors during the installation, the tool will automatically rollback any changes made during the installation process and provide feedback.

2. **Updating AUR Packages**:

   Simply use the `update` command to update all the installed AUR packages.
   
   ```bash
   aur-helper update
   ```

3. **Removing AUR Packages**:

   Use the `remove` command followed by the package name you wish to remove.
   
   ```bash
   aur-helper remove [packagename]
   ```

   This will also remove the associated package data from `~/.aur-helper`.

### Debugging

For detailed output, use the `--debug` argument. This provides verbose information which can be useful for troubleshooting.

```bash
aur-helper --debug [command] [arguments]
```

---

### Disclaimer

The use of this script is at your own risk. I am is not responsible for any damage or loss that may arise from using this script. This is a private project and is provided "as is" without any guarantees or warranty.

---