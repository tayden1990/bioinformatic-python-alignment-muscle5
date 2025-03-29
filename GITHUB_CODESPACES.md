# Running MUSCLE5 Alignment Tool in GitHub Codespaces

GitHub Codespaces provides an easy way to run the MUSCLE5 Alignment Tool without any local installation. This guide will help you get started.

## Quick Start

1. Click the green "Code" button at the top of this repository
2. Select the "Codespaces" tab
3. Click "Create codespace on main"
4. Once the environment loads (this might take a minute), run:
   ```bash
   python codespaces_start.py
   ```
5. Click the "Open in Browser" notification when it appears, or click the "PORTS" tab at the bottom of VS Code, then click the "Open in Browser" icon next to port 7860

The application will then open in a new browser tab, fully configured and ready to use.

## What Happens Automatically

When you start a Codespace:

1. Python and all dependencies are installed automatically
2. MUSCLE5 is downloaded and configured for your session
3. The web interface will be available on port 7860

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

## Saving Your Work

To save your work before the session times out:
- Use the "Export Results" button to download alignment results
- Save any important sequence data to your local machine
