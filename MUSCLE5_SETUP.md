# MUSCLE5 Setup Guide

This guide will help you download, install, and configure the MUSCLE executable for use with the Sequence Alignment Tool.

## Step 1: Download MUSCLE

Download the appropriate MUSCLE executable for your operating system:

- **Windows**: [muscle5.1.win64.exe](https://drive5.com/muscle5/muscle5.1.win64.exe)
- **macOS Intel**: [muscle5.1.macos_intel64](https://drive5.com/muscle5/muscle5.1.macos_intel64)
- **macOS ARM/M1/M2**: [muscle5.1.macos_arm64](https://drive5.com/muscle5/muscle5.1.macos_arm64)
- **Linux Intel**: [muscle5.1.linux_intel64](https://drive5.com/muscle5/muscle5.1.linux_intel64)
- **Linux ARM**: [muscle5.1.linux_arm64](https://drive5.com/muscle5/muscle5.1.linux_arm64)

You can also visit the [official MUSCLE5 website](https://drive5.com/muscle5/) for the latest versions.

<details>
<summary>Screenshot: MUSCLE Download Page</summary>

![MUSCLE Download Page](screenshots/muscle_download_page.png)
</details>

## Step 2: Extract and Make the executable accessible

### Windows
1. The downloaded file is already an executable (.exe) file
2. Save the file to a location you can remember, such as `C:\Program Files\muscle5\muscle5.exe`
3. No additional setup required, as `.exe` files are already executable

<details>
<summary>Screenshot: Windows Setup</summary>

![Windows MUSCLE Setup](screenshots/windows_setup.png)
</details>

### macOS
1. The downloaded file is already an executable file (no need to extract)
2. Save the file to a location like `/usr/local/bin/muscle5` or `~/Applications/muscle5`
3. Open Terminal and navigate to the folder where you saved the file
4. Make the file executable with: `chmod +x muscle5`

<details>
<summary>Screenshot: macOS Setup</summary>

![macOS MUSCLE Setup](screenshots/mac_setup.png)
</details>

### Linux
1. The downloaded file is already an executable file (no need to extract)
2. Save the file to a location like `/usr/local/bin/muscle5` or `~/bin/muscle5`
3. Open Terminal and navigate to the folder where you saved the file
4. Make the file executable with: `chmod +x muscle5`

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

- **Windows**: Set `MUSCLE5_PATH=C:\path\to\muscle5.exe` in your environment variables
- **macOS/Linux**: Add `export MUSCLE5_PATH=/path/to/muscle5` to your `~/.bashrc` or `~/.zshrc` file

This will save you from having to select the executable each time you use the application.
