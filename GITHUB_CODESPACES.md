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
5. When the application starts, you have two options to access it:
   - Click the notification that appears asking to "Open in Browser"
   - OR go to the "PORTS" tab at the bottom of VS Code, right-click on port 7860, and select "Open in Browser"

The application will then open in a new browser tab, fully configured and ready to use.

## Important: If You See "GitHub Codespaces Environment" Message Only

If your browser only shows a message about running in GitHub Codespaces (instead of the actual application), try these steps:

1. Go back to VS Code
2. Find the "PORTS" tab at the bottom panel
3. Look for port 7860, right-click and select "Open in Browser"
4. If that doesn't work, try "Open in Preview" instead
5. If you still see only the environment message, try running:
   ```bash
   python run_simple.py
   ```

## What Happens Automatically

When you start a Codespace:

1. Python and all dependencies are installed automatically
2. MUSCLE5 is downloaded and configured for your session
3. The web interface will be available on port 7860

## Troubleshooting

If you encounter any issues:

- **Empty page or loading forever**: Try a different browser, or use a private/incognito window

- **Application errors**: Try restarting with a fresh setup:
  ```bash
  python setup_muscle.py --force
  python codespaces_start.py
  ```

- **Port already in use**: If you get a "port already in use" error, another instance might be running. Stop it with:
  ```bash
  pkill -f "python app.py"
  ```

- **Only see the welcome message**: Click the "Open in Browser" button in the PORTS tab, not just the preview pane

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

# Running in GitHub Codespaces

This guide provides instructions for using the MUSCLE5 Sequence Alignment Tool in GitHub Codespaces.

## Automatic Startup

When you open this repository in GitHub Codespaces, the application should start automatically. If it doesn't, you can start it manually:

```bash
python codespaces_start.py
```

## Access the Application

When the application starts, you'll see a public URL in the terminal output that looks like:
```
Running on public URL: https://xxxxxxxxxxxxx.gradio.live
```

Click on this URL to access the full application interface.

## Troubleshooting

If you see only a placeholder message instead of the full application:

1. Check the terminal output for any error messages
2. Ensure the application has fully started before accessing the URL
3. Try restarting the application with: `python codespaces_start.py`
4. If problems persist, try refreshing the browser or using a different browser

## Important Notes

- The public sharing URL is temporary and will expire after 72 hours
- For large datasets, consider downloading the application and running it locally
- GitHub Codespaces sessions will timeout after 30 minutes of inactivity
- The MUSCLE5 executable is included in the Codespaces environment by default

## Performance Considerations

GitHub Codespaces provides limited resources. For large sequence alignments:
- Use the Super5 algorithm option for better memory efficiency
- Consider running locally for very large datasets (>10MB)
- Export your results frequently to avoid losing work

## Getting Help

If you encounter issues running the application in GitHub Codespaces, please [open an issue](https://github.com/tayden1990/bioinformatic-python-alignment-muscle5/issues) with details about the problem.
