# Running MUSCLE5 Alignment Tool in GitHub Codespaces

This guide explains how to run the MUSCLE5 Alignment Tool in GitHub Codespaces, a cloud-based development environment by GitHub.

## Quick Start

1. Click the "Code" button on the GitHub repository
2. Select the "Codespaces" tab
3. Click "Create codespace on main"
4. Wait for the environment to set up (this may take a few minutes)
5. Once ready, open a terminal and run:
   ```bash
   python app.py
   ```
6. Click the "Open in Browser" button that appears when the application starts
7. The Gradio interface will open in a new browser tab

## Automatic Setup

The following steps happen automatically when you create a Codespace:

1. Python 3.9 is installed
2. Required dependencies are installed from requirements.txt
3. MUSCLE5 executable is downloaded and configured
4. Port 7860 is forwarded for web access

## Manual Setup (if needed)

If the automatic setup didn't work, you can run these commands manually:

```bash
# Update dependencies
pip install -r requirements.txt

# Download and configure MUSCLE5
python setup_muscle.py --force

# Start the application
python app.py
```

## Troubleshooting

- If you see "Address already in use" error, another process is using port 7860.
  Run `pkill -f "python app.py"` to stop any running instances.
  
- If MUSCLE5 fails to download, you can check the logs with:
  ```bash
  cat ~/.muscle_setup.log
  ```
  
- For other issues, please open an issue on the GitHub repository.

## Limitations

When running in GitHub Codespaces:

- Available CPU and memory resources may be limited compared to local execution
- Large alignments might take longer to process
- File uploads are limited to 200MB
- The session will terminate after 30 minutes of inactivity

For processing very large datasets, consider running the application locally instead.
