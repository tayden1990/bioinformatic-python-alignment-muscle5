# Quick Start: MUSCLE5 in GitHub Codespaces

## One-click Launch

To use the MUSCLE5 Sequence Alignment Tool in GitHub Codespaces:

1. Run this one command:

```bash
python launch.py
```

2. When the application starts, click on the link in the terminal OR:
   - Look for the "PORTS" tab at the bottom of VS Code
   - Find port 7860, right-click and select "Open in Browser"

That's it! The application will open in your browser, ready to use.

## If Something Goes Wrong

If you encounter any issues:

1. Try the automatic repair:

```bash
python setup_muscle.py --force && python launch.py
```

2. If you only see a welcome message instead of the full application, refresh your browser.

3. Make sure to open the application in a browser tab, not just in the preview pane.

## MUSCLE Setup Issues

If you encounter errors with MUSCLE installation:

1. Manual installation in Codespaces:

```bash
# Download MUSCLE directly
wget https://drive5.com/muscle/muscle_linux_intel64.tar.gz
tar -xvzf muscle_linux_intel64.tar.gz
chmod +x muscle

# Set up the configuration
echo "$(pwd)/muscle" > muscle_config.txt

# Launch the application
python launch.py
```

2. Alternatively, you can install MUSCLE using the Ubuntu package manager:

```bash
sudo apt-get update && sudo apt-get install -y muscle
echo "$(which muscle)" > muscle_config.txt
python launch.py
```

Remember that in Codespaces, any files you create will be retained between sessions as long as the Codespace remains active.

## Using the Application

1. Upload a FASTA file with DNA sequences
2. Choose an alignment method
3. Run the alignment
4. View and export your results

For detailed usage instructions, see the [main README](README.md).
