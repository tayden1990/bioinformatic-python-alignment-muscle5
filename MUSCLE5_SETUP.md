# MUSCLE5 Setup Guide

This guide will help you download, install, and configure the MUSCLE executable for use with the Sequence Alignment Tool.

## Step 1: Download MUSCLE

Download the appropriate MUSCLE executable for your operating system:

- **Windows**: [muscle_win64.tar.gz](https://drive5.com/muscle/muscle_win64.tar.gz)
- **macOS Intel**: [muscle_macos_intel64.tar.gz](https://drive5.com/muscle/muscle_macos_intel64.tar.gz)
- **macOS ARM/M1/M2**: [muscle_macos_arm64.tar.gz](https://drive5.com/muscle/muscle_macos_arm64.tar.gz)
- **Linux Intel**: [muscle_linux_intel64.tar.gz](https://drive5.com/muscle/muscle_linux_intel64.tar.gz)
- **Linux ARM**: [muscle_linux_arm64.tar.gz](https://drive5.com/muscle/muscle_linux_arm64.tar.gz)

You can also visit the [official MUSCLE website](https://drive5.com/muscle/) for the latest versions.

<details>
<summary>Screenshot: MUSCLE Download Page</summary>

![MUSCLE Download Page](screenshots/muscle_download_page.png)
</details>

## Step 2: Extract and Make the executable accessible

### Windows
1. Extract the downloaded `.tar.gz` file using 7-Zip, WinRAR, or similar tools
2. Save the extracted `muscle.exe` file to a location you can remember, such as `C:\Program Files\muscle\muscle.exe`
3. No additional setup required, as `.exe` files are already executable

<details>
<summary>Screenshot: Windows Setup</summary>

![Windows MUSCLE Setup](screenshots/windows_setup.png)
</details>

### macOS
1. Extract the downloaded `.tar.gz` file by double-clicking it or using the terminal:
   ```bash
   tar -xvzf muscle_macos_*.tar.gz
   ```
2. Save the extracted `muscle` file to a location like `/usr/local/bin/muscle` or `~/Applications/muscle`
3. Open Terminal and navigate to the folder where you saved the file
4. Make the file executable with: `chmod +x muscle`

<details>
<summary>Screenshot: macOS Setup</summary>

![macOS MUSCLE Setup](screenshots/mac_setup.png)
</details>

### Linux
1. Extract the downloaded `.tar.gz` file using the terminal:
   ```bash
   tar -xvzf muscle_linux_*.tar.gz
   ```
2. Save the extracted `muscle` file to a location like `/usr/local/bin/muscle` or `~/bin/muscle`
3. Open Terminal and navigate to the folder where you saved the file
4. Make the file executable with: `chmod +x muscle`

<details>
<summary>Screenshot: Linux Setup</summary>

![Linux MUSCLE Setup](screenshots/linux_setup.png)
</details>

## Step 3: Configure the path in the application

1. Launch the MUSCLE5 Sequence Alignment Tool
2. In the "MUSCLE5 Executable Selection" section, click the "Browse..." button
3. Navigate to and select the MUSCLE executable you downloaded
4. Click "Update MUSCLE5 Path"
5. Verify the status shows a success message with a green checkmark

<details>
<summary>Screenshot: Application Configuration</summary>

![MUSCLE Path Configuration](screenshots/muscle_config_app.png)
</details>

## Troubleshooting

If you encounter issues with MUSCLE:

- **"File is not executable"**: Ensure you've made the file executable with `chmod +x` (macOS/Linux)
- **"Not a valid MUSCLE executable"**: Confirm you downloaded the correct file for your operating system
- **"Failed to run command"**: Try running the executable directly from your terminal/command prompt to check for any system-specific errors

### Alternative Installation Methods

If you're still having trouble, try these alternative installation methods:

#### Using Conda/Bioconda
```bash
conda install -c bioconda muscle
```

#### Using Homebrew (macOS)
```bash
brew install muscle
```

#### Using Package Managers (Linux)
```bash
# Ubuntu/Debian
sudo apt-get install muscle

# CentOS/RHEL
sudo yum install muscle
```

## Environment Variable (Advanced)

You can permanently set the MUSCLE path by setting an environment variable:

- **Windows**: Set `MUSCLE5_PATH=C:\path\to\muscle.exe` in your environment variables
- **macOS/Linux**: Add `export MUSCLE5_PATH=/path/to/muscle` to your `~/.bashrc` or `~/.zshrc` file

This will save you from having to select the executable each time you use the application.
