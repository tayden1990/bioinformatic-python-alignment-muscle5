# Running MUSCLE5 Alignment Tool in GitHub Codespaces

This guide explains how to run the MUSCLE5 Alignment Tool in GitHub Codespaces without installing anything on your computer.

## Quick Start (One-Command Method)

1. Click the "Code" button on the GitHub repository
2. Select the "Codespaces" tab
3. Click "Create codespace on main"
4. Once the environment loads, run this single command:

   ```bash
   python codespaces_start.py
   ```

5. A browser tab will automatically open with the application

That's it! The script handles everything else for you.

## What Happens Behind the Scenes

The `codespaces_start.py` script:

1. Checks if MUSCLE5 is installed and downloads it if needed
2. Configures the environment variables correctly for Codespaces
3. Starts the application server with proper settings
4. Opens a browser tab with the Gradio interface

## Troubleshooting

If you encounter any issues:

- **No browser tab opens**: Click the "PORTS" tab at the bottom of VS Code, then click the "Open in Browser" icon next to port 7860

- **Application errors**: Try restarting with a fresh setup:
  ```bash
  python setup_muscle.py --force
  python codespaces_start.py
  ```

- **Port already in use**: If you get a "port already in use" error, another instance might be running. Stop it with:
  ```bash
  pkill -f "python app.py"
  ```

## Limitations

When running in GitHub Codespaces:

- Available CPU and memory resources may be limited compared to local execution
- Large alignments (>100 sequences) might take longer to process
- File uploads are limited to 200MB
- The session will terminate after 30 minutes of inactivity
