# MUSCLE5 Setup Guide

This guide will help you download, install, and configure the MUSCLE5 executable for use with the Sequence Alignment Tool.

## Step 1: Download MUSCLE5

Download the appropriate MUSCLE5 executable for your operating system:

- **Windows**: [muscle5.1.win64.exe](https://drive5.com/muscle5/muscle5.1.win64.exe)
- **macOS**: [muscle5.1.macos](https://drive5.com/muscle5/muscle5.1.macos)
- **Linux**: [muscle5.1.linux_intel64](https://drive5.com/muscle5/muscle5.1.linux_intel64)

You can also visit the [official MUSCLE website](https://drive5.com/muscle/) for the latest versions.

<details>
<summary>Screenshot: MUSCLE5 Download Page</summary>

![MUSCLE5 Download Page](screenshots/muscle_download_page.png)
</details>

## Step 2: Make the executable accessible

### Windows
1. Save the downloaded `.exe` file to a location you can remember, such as `C:\Program Files\muscle\muscle.exe`
2. No additional setup required, as `.exe` files are already executable

<details>
<summary>Screenshot: Windows Setup</summary>

![Windows MUSCLE5 Setup](screenshots/windows_setup.png)
</details>

### macOS
1. Save the downloaded file to a location like `/usr/local/bin/muscle` or `~/Applications/muscle`
2. Open Terminal and navigate to the folder where you saved the file
3. Make the file executable with: `chmod +x muscle5.1.macos`
4. Optionally rename it to just `muscle` for simplicity: `mv muscle5.1.macos muscle`

<details>
<summary>Screenshot: macOS Setup</summary>

![macOS MUSCLE5 Setup](screenshots/mac_setup.png)
</details>

### Linux
1. Save the downloaded file to a location like `/usr/local/bin/muscle` or `~/bin/muscle`
2. Open Terminal and navigate to the folder where you saved the file
3. Make the file executable with: `chmod +x muscle5.1.linux_intel64`
4. Optionally rename it to just `muscle` for simplicity: `mv muscle5.1.linux_intel64 muscle`

<details>
<summary>Screenshot: Linux Setup</summary>

![Linux MUSCLE5 Setup](screenshots/linux_setup.png)
</details>

## Step 3: Configure the path in the application

1. Launch the MUSCLE5 Sequence Alignment Tool
2. In the "MUSCLE5 Executable Selection" section, click the "Browse..." button
3. Navigate to and select the MUSCLE5 executable you downloaded
4. Click "Update MUSCLE5 Path"
5. Verify the status shows a success message with a green checkmark

<details>
<summary>Screenshot: Application Configuration</summary>

![MUSCLE5 Path Configuration](screenshots/muscle_config_app.png)
</details>

## Troubleshooting

If you encounter issues with MUSCLE5:

- **"File is not executable"**: Ensure you've made the file executable with `chmod +x` (macOS/Linux)
- **"Not a valid MUSCLE executable"**: Confirm you downloaded the correct file for your operating system
- **"Failed to run command"**: Try running the executable directly from your terminal/command prompt to check for any system-specific errors

## Environment Variable (Advanced)

You can permanently set the MUSCLE5 path by setting an environment variable:

- **Windows**: Set `MUSCLE5_PATH=C:\path\to\muscle.exe` in your environment variables
- **macOS/Linux**: Add `export MUSCLE5_PATH=/path/to/muscle` to your `~/.bashrc` or `~/.zshrc` file

This will save you from having to select the executable each time you use the application.
