import os
import sys
import subprocess
import tempfile
import multiprocessing
import psutil
import gradio as gr
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from Bio import SeqIO, AlignIO
from Bio.Align import MultipleSeqAlignment
from datetime import datetime
import re
import platform

# Import our compatibility utilities if available
try:
    from utils.compatibility import is_codespaces, has_pyobjc, is_compatible_python_version
except ImportError:
    # Define fallback if the module isn't available
    def is_codespaces():
        return "CODESPACES" in os.environ or "CODESPACE_NAME" in os.environ
    
    def has_pyobjc():
        try:
            # Use importlib to check for the module without directly importing it
            import importlib.util
            spec = importlib.util.find_spec("pyobjc_framework_Cocoa")
            return spec is not None
        except ImportError:
            return False
    
    def is_compatible_python_version():
        major = sys.version_info.major
        minor = sys.version_info.minor
        if sys.platform == "darwin" and (major, minor) < (3, 9):
            return False
        return True

# Check Python compatibility and warn if needed
if not is_compatible_python_version():
    print("\n" + "!" * 80)
    print(f"WARNING: Running on Python {sys.version_info.major}.{sys.version_info.minor} on macOS.")
    print("Some functionality requiring PyObjC (which needs Python 3.9+) will be limited.")
    print("For best experience, consider upgrading to Python 3.9 or higher.")
    print("!" * 80 + "\n")

# Better path handling for MUSCLE5
def get_default_muscle_path():
    """Returns the default muscle path based on operating system"""
    if platform.system() == "Windows":
        # Check common Windows locations
        paths = [
            os.path.join(os.environ.get("PROGRAMFILES", "C:\\Program Files"), "muscle", "muscle.exe"),
            os.path.join(os.environ.get("PROGRAMFILES(X86)", "C:\\Program Files (x86)"), "muscle", "muscle.exe"),
            "muscle.exe",  # If in PATH or current directory
            "muscle-win64.v5.3.exe"  # Common downloaded name
        ]
    elif platform.system() == "Darwin":  # macOS
        paths = [
            "/usr/local/bin/muscle",
            "/opt/homebrew/bin/muscle",
            "muscle"  # If in PATH or current directory
        ]
    else:  # Linux and others
        paths = [
            "/usr/bin/muscle",
            "/usr/local/bin/muscle",
            "muscle"  # If in PATH or current directory
        ]
    
    # Check if any path exists
    for path in paths:
        if os.path.exists(path):
            return path
    
    # Return a default that will be checked later
    return "muscle"

# Read from configuration file first
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "muscle_config.txt")
if os.path.exists(config_path):
    try:
        with open(config_path, "r") as f:
            muscle_path = f.read().strip()
            if os.path.exists(muscle_path):
                MUSCLE5_PATH = muscle_path
            else:
                MUSCLE5_PATH = os.environ.get("MUSCLE5_PATH", get_default_muscle_path())
    except:
        MUSCLE5_PATH = os.environ.get("MUSCLE5_PATH", get_default_muscle_path())
else:
    MUSCLE5_PATH = os.environ.get("MUSCLE5_PATH", get_default_muscle_path())

# Create a global variable to store the path that can be updated from the UI
current_muscle_path = MUSCLE5_PATH

# Check if we need to setup MUSCLE5
def check_and_setup_muscle():
    """Check if MUSCLE5 needs to be setup and run setup script if needed"""
    global MUSCLE5_PATH, current_muscle_path
    
    is_valid, _ = validate_muscle_executable(current_muscle_path)
    if not is_valid:
        print("MUSCLE5 executable not found or invalid. Attempting auto-setup...")
        try:
            setup_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "setup_muscle.py")
            if os.path.exists(setup_script):
                subprocess.run([sys.executable, setup_script], check=True)
                
                # Reload path from config after setup
                if os.path.exists(config_path):
                    with open(config_path, "r") as f:
                        muscle_path = f.read().strip()
                        if os.path.exists(muscle_path):
                            MUSCLE5_PATH = muscle_path
                            current_muscle_path = muscle_path
                            return True
            return False
        except Exception as e:
            print(f"Auto-setup failed: {str(e)}")
            return False
    return True

def validate_muscle_executable(executable_path):
    """
    Validates that the provided path is a valid MUSCLE5 executable
    
    Args:
        executable_path: Path to the potential MUSCLE5 executable
    
    Returns:
        Tuple of (is_valid, message)
    """
    if not os.path.exists(executable_path):
        return False, f"File does not exist: {executable_path}"
    
    if not os.access(executable_path, os.X_OK) and not executable_path.endswith('.exe'):
        return False, f"File is not executable: {executable_path}"
    
    try:
        # Try running with -version to see if it's actually MUSCLE
        process = subprocess.run(
            [executable_path, "-version"], 
            capture_output=True, 
            text=True,
            check=False,
            timeout=3  # Add a timeout to avoid hanging
        )
        
        # Check for common MUSCLE version strings in output
        if "MUSCLE" in process.stdout or "muscle" in process.stdout or "MUSCLE" in process.stderr or "muscle" in process.stderr:
            return True, f"Valid MUSCLE executable detected: {os.path.basename(executable_path)}"
        else:
            return False, f"File does not appear to be a MUSCLE executable: {executable_path}"
    
    except Exception as e:
        return False, f"Error validating executable: {str(e)}"

# Function to update the muscle path when selected from UI
def update_muscle_path(file):
    global current_muscle_path, MUSCLE5_PATH
    
    if file is None:
        return "No file selected. Using current path."
    
    if not os.path.exists(file.name):
        return f"Error: File does not exist: {file.name}"
    
    # Normalize the path for better cross-platform compatibility
    normalized_path = os.path.normpath(file.name)
    
    # Validate that this is actually a MUSCLE executable
    is_valid, message = validate_muscle_executable(normalized_path)
    
    if is_valid:
        current_muscle_path = normalized_path
        MUSCLE5_PATH = normalized_path
        # Save the path to a configuration file for future use
        try:
            with open(os.path.join(os.path.dirname(__file__), "muscle_config.txt"), "w") as f:
                f.write(normalized_path)
        except Exception:
            # Silently handle config file writing errors - not critical
            pass
        return f"✅ Muscle5 path updated successfully. {message}"
    else:
        return f"❌ Invalid MUSCLE executable. {message}"

def get_max_memory_gb():
    """Returns the available system memory in GB"""
    mem = psutil.virtual_memory()
    # Return 90% of available memory in GB
    return int(mem.total * 0.9 / (1024 * 1024 * 1024))

def check_muscle5():
    """Check if muscle5 is available and return the path"""
    if os.path.exists(MUSCLE5_PATH):
        try:
            subprocess.run([MUSCLE5_PATH, "-version"], 
                          check=False, capture_output=True)
            print(f"Using Muscle5 at: {MUSCLE5_PATH}")
            return MUSCLE5_PATH
        except Exception:
            pass
    
    try:
        subprocess.run(["muscle", "-version"], 
                      check=False, capture_output=True)
        print("Using Muscle5 from PATH")
        return "muscle"
    except Exception:
        return None

def run_muscle5_alignment(fasta_file, use_stratified=False, use_super5=False):
    """
    Runs Muscle5 alignment with maximum CPU and RAM usage
    
    Args:
        fasta_file: Path to the uploaded FASTA file
        use_stratified: Whether to use stratified ensemble
        use_super5: Whether to use super5 for large datasets
    
    Returns:
        Path to the alignment result file and alignment result as string
    """
    # Get the maximum available CPU cores
    max_threads = multiprocessing.cpu_count()
    
    # Create temporary file for output
    fd, output_file = tempfile.mkstemp(suffix=".afa")
    os.close(fd)
    
    try:
        # Check if muscle5 is available
        muscle_cmd = check_muscle5()
        if not muscle_cmd:
            return None, (
                "Error: Muscle5 not found. Please download it from https://drive5.com/muscle/ "
                "and update the MUSCLE5_PATH variable in the code with the correct path."
            )
        
        # FIXED: Using the exact syntax from the help documentation
        if use_super5:
            # Command syntax from help: muscle -super5 seqs.fa -output aln.afa
            cmd = [
                muscle_cmd,
                "-super5", fasta_file,  # Correct syntax based on help
                "-output", output_file,
                "-threads", str(max_threads)
            ]
        else:
            # Command syntax from help: muscle -align seqs.fa -output aln.afa
            cmd = [
                muscle_cmd,
                "-align", fasta_file,  # Correct syntax based on help
                "-output", output_file,
                "-threads", str(max_threads)
            ]
            
            # Add stratified option if selected
            if use_stratified:
                cmd.append("-stratified")  # Changed to append to match help docs
                # Change output file extension for ensembles
                output_file = output_file.replace(".afa", ".efa")
                # Update the output path in the command
                cmd[4] = output_file  # Index is now 4 due to append
        
        # Print the command for debugging
        cmd_str = " ".join(cmd)
        print(f"Running command: {cmd_str}")
        
        # Run muscle5
        process = subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # If using stratified, calculate dispersion
        dispersion_result = ""
        if use_stratified and os.path.exists(output_file):
            try:
                disperse_cmd = [
                    muscle_cmd,
                    "-disperse", output_file
                ]
                disperse_process = subprocess.run(
                    disperse_cmd,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                dispersion_result = "\n\nEnsemble Dispersion Analysis:\n" + disperse_process.stdout
            except Exception as e:
                dispersion_result = f"\n\nError calculating dispersion: {str(e)}"
        
        # Read the alignment output and return as string
        alignment_result = ""
        if os.path.exists(output_file):
            with open(output_file, "r") as f:
                alignment_result = f.read()
        
        # Print stats from muscle5
        print(f"Muscle5 stdout: {process.stdout}")
        print(f"Muscle5 stderr: {process.stderr}")
        
        # Add any stdout messages from Muscle5
        if process.stdout:
            alignment_result = process.stdout + "\n\n" + alignment_result
        
        # Add dispersion results if available
        if dispersion_result:
            alignment_result += dispersion_result
            
        return output_file, alignment_result
    
    except subprocess.CalledProcessError as e:
        return None, f"Error running Muscle5: {e.stderr if e.stderr else str(e)}"
    except Exception as e:
        return None, f"Error: {str(e)}"

def identify_variations(alignment):
    """
    Identify SNPs and conserved regions in the alignment
    
    Args:
        alignment: MultipleSeqAlignment object
    
    Returns:
        Tuple of (SNP positions, conserved positions)
    """
    if not alignment or len(alignment) <= 1:
        return [], []
    
    # Get alignment length
    aln_length = alignment.get_alignment_length()
    
    # Initialize lists to track SNPs and conserved positions
    snp_positions = []
    conserved_positions = []
    
    # Check each column
    for i in range(aln_length):
        # Get all characters in this column
        column = [record.seq[i] for record in alignment]
        
        # Skip columns with any gaps (conserved regions should have no gaps)
        if '-' in column:
            continue
        
        # Skip columns with ambiguous nucleotides like N
        if any(base not in 'ACGT' for base in column):
            continue
        
        # If all characters are the same (conserved)
        if len(set(column)) == 1:
            conserved_positions.append(i)
        
        # If there is variation among characters, it's a SNP
        elif len(set(column)) > 1:
            snp_positions.append(i)
    
    return snp_positions, conserved_positions

def find_conserved_regions(alignment, conserved_positions):
    """
    Find continuous regions of conservation in the alignment
    
    Args:
        alignment: MultipleSeqAlignment object
        conserved_positions: List of conserved positions
    
    Returns:
        List of tuples (start, end, length, sequence)
    """
    if not conserved_positions:
        return []
    
    conserved_regions = []
    
    # Sort positions (should already be sorted, but just to be safe)
    conserved_positions = sorted(conserved_positions)
    
    # Initialize the first region
    start_pos = conserved_positions[0]
    current_pos = start_pos
    
    # Find continuous regions
    for i in range(1, len(conserved_positions)):
        if conserved_positions[i] == current_pos + 1:
            # Continue the current region
            current_pos = conserved_positions[i]
        else:
            # End of a conserved region
            region_length = current_pos - start_pos + 1
            # Get the conserved sequence (from the first record, as all are identical in these positions)
            seq = str(alignment[0].seq[start_pos:current_pos+1])
            conserved_regions.append((start_pos, current_pos, region_length, seq))
            
            # Start a new region
            start_pos = conserved_positions[i]
            current_pos = start_pos
    
    # Don't forget the last region
    region_length = current_pos - start_pos + 1
    seq = str(alignment[0].seq[start_pos:current_pos+1])
    conserved_regions.append((start_pos, current_pos, region_length, seq))
    
    return conserved_regions

def create_conservation_table(conserved_regions):
    """
    Create a DataFrame of conserved regions
    
    Args:
        conserved_regions: List of tuples (start, end, length, sequence)
    
    Returns:
        Pandas DataFrame
    """
    # If no conserved regions, return empty DataFrame with correct columns
    if not conserved_regions:
        return pd.DataFrame(columns=['Start', 'End', 'Length', 'Sequence'])
    
    # Convert to DataFrame
    df = pd.DataFrame(conserved_regions, columns=['Start', 'End', 'Length', 'Sequence'])
    
    # Sort by length (longest first)
    df = df.sort_values('Length', ascending=False)
    
    # Add position index starting from 1
    df['Start'] = df['Start'] + 1
    df['End'] = df['End'] + 1
    
    # Reset index
    df = df.reset_index(drop=True)
    
    # Add index as a column and start from 1
    df.index = df.index + 1
    
    return df

def create_alignment_plot(alignment_file):
    """
    Creates an interactive visualization of the DNA alignment with SNPs and conserved regions highlighted
    
    Args:
        alignment_file: Path to the alignment file
    
    Returns:
        Tuple of (Plotly figure object, conservation table DataFrame)
    """
    try:
        # Read the alignment file
        alignment = AlignIO.read(alignment_file, "fasta")
        
        # Define colors for nucleotides
        color_map = {
            'A': 'green',
            'C': 'blue',
            'G': 'orange',
            'T': 'red',
            '-': 'lightgrey',  # Gap
            'N': 'purple',     # Unknown
        }
        
        # Find SNPs and conserved positions
        snp_positions, conserved_positions = identify_variations(alignment)
        
        # Find conserved regions
        conserved_regions = find_conserved_regions(alignment, conserved_positions)
        
        # Create conservation table
        conservation_table = create_conservation_table(conserved_regions)
        
        # Create a figure
        fig = go.Figure()
        
        # Get alignment dimensions
        num_seqs = len(alignment)
        aln_length = alignment.get_alignment_length()
            
        # For very large alignments, we'll display a subset of sequences
        max_display_seqs = 30
        display_seqs = min(num_seqs, max_display_seqs)
        
        if num_seqs > display_seqs:
            seq_note = f"Note: Showing {display_seqs} of {num_seqs} sequences"
        else:
            seq_note = f"Number of sequences: {num_seqs}"
        
        # For each sequence in the alignment
        for i in range(display_seqs):
            record = alignment[i]
            seq_str = str(record.seq)
            
            # Convert sequence to colors
            colors = [color_map.get(base, 'grey') for base in seq_str]
            
            # Create a scatter plot for this sequence
            fig.add_trace(go.Scatter(
                x=list(range(len(seq_str))),
                y=[i] * len(seq_str),
                mode='markers',
                marker=dict(
                    size=10,
                    color=colors,
                    line=dict(width=1, color='black')
                ),
                name=record.id[:15] + '...' if len(record.id) > 15 else record.id,
                hovertext=[f"Position {j+1}: {seq_str[j]}" for j in range(len(seq_str))],
                hoverinfo='text'
            ))
        
        # Highlight SNP positions
        if snp_positions:
            for pos in snp_positions:
                fig.add_shape(
                    type="rect",
                    x0=pos - 0.5,
                    x1=pos + 0.5,
                    y0=-1,
                    y1=display_seqs,
                    fillcolor="rgba(255, 255, 0, 0.3)",  # Yellow with transparency
                    line=dict(width=0),
                    layer="below"
                )
        
        # Highlight conserved regions
        if conserved_regions:
            for start, end, _, _ in conserved_regions:
                fig.add_shape(
                    type="rect",
                    x0=start - 0.5,
                    x1=end + 0.5,
                    y0=-1,
                    y1=display_seqs,
                    fillcolor="rgba(0, 255, 0, 0.15)",  # Light green with transparency
                    line=dict(width=1, color="green"),
                    layer="below"
                )
        
        # Add annotations
        annotations = [
            dict(
                text=f"Alignment length: {aln_length} positions",
                x=0,
                y=display_seqs + 2,
                showarrow=False,
                xref="x",
                yref="y",
                font=dict(size=12)
            ),
            dict(
                text=seq_note,
                x=0,
                y=display_seqs + 3,
                showarrow=False,
                xref="x",
                yref="y",
                font=dict(size=12)
            ),
            dict(
                text="Color key: A=green, C=blue, G=orange, T=red, gaps=grey",
                x=0,
                y=display_seqs + 4,
                showarrow=False,
                xref="x",
                yref="y",
                font=dict(size=12)
            )
        ]
        
        # Add SNP annotation
        if snp_positions:
            annotations.append(
                dict(
                    text=f"SNPs highlighted in yellow (found {len(snp_positions)} total)",
                    x=0,
                    y=display_seqs + 5,
                    showarrow=False,
                    xref="x",
                    yref="y",
                    font=dict(size=12)
                )
            )
        
        # Add conserved regions annotation
        if conserved_regions:
            annotations.append(
                dict(
                    text=f"Conserved regions highlighted in green (found {len(conserved_regions)} total)",
                    x=0,
                    y=display_seqs + 6,
                    showarrow=False,
                    xref="x",
                    yref="y",
                    font=dict(size=12)
                )
            )
        
        # Default visible range (first 100 positions)
        default_range = [0, min(100, aln_length-1)]
        
        # Update layout with range slider for navigation
        fig.update_layout(
            title="DNA Alignment Visualization",
            xaxis_title="Position",
            yaxis_title="Sequence",
            height=max(400, 25 * display_seqs + 150),
            xaxis=dict(
                range=default_range,
                rangeslider=dict(
                    visible=True,
                    thickness=0.1
                ),
                type="linear",
                tickmode='linear',
                tick0=0,
                dtick=10
            ),
            yaxis=dict(
                tickvals=list(range(display_seqs)),
                ticktext=[alignment[i].id[:15] + '...' if len(alignment[i].id) > 15 else alignment[i].id 
                          for i in range(display_seqs)]
            ),
            showlegend=False,
            margin=dict(l=150, r=20, t=100, b=100),
            annotations=annotations,
            updatemenus=[
                dict(
                    type="buttons",
                    direction="right",
                    x=0.15,
                    y=1.15,
                    buttons=[
                        dict(
                            label="Reset View",
                            method="relayout",
                            args=[{"xaxis.range": default_range}]
                        ),
                        dict(
                            label="Zoom Out",
                            method="relayout",
                            args=[{"xaxis.range": [0, aln_length-1]}]
                        ),
                    ]
                )
            ]
        )
        
        return fig, conservation_table, alignment
    
    except Exception as e:
        # Create an error figure
        fig = go.Figure()
        fig.add_annotation(
            text=f"Error creating visualization: {str(e)}",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=14, color="red")
        )
        fig.update_layout(
            height=300,
            xaxis=dict(showticklabels=False),
            yaxis=dict(showticklabels=False)
        )
        return fig, pd.DataFrame(columns=['Start', 'End', 'Length', 'Sequence']), None

def process_fasta(file, use_stratified, use_super5):
    """
    Process the uploaded FASTA file
    
    Args:
        file: The uploaded file object from Gradio
        use_stratified: Whether to use stratified ensemble
        use_super5: Whether to use super5 for large datasets
    
    Returns:
        The alignment result and statistics, the visualization, the conservation table, and the alignment object
    """
    if file is None:
        return "Please upload a FASTA file.", None, None, None
    
    temp_fasta = None
    output_file = None
    
    try:
        # Save the uploaded file to a temporary location
        temp_fasta = tempfile.NamedTemporaryFile(delete=False, suffix=".fasta")
        temp_fasta.close()
        
        with open(file.name, "rb") as f_in, open(temp_fasta.name, "wb") as f_out:
            f_out.write(f_in.read())
        
        # Check if the file is a valid FASTA file
        try:
            records = list(SeqIO.parse(temp_fasta.name, "fasta"))
            if not records:
                return "The uploaded file does not contain valid FASTA sequences.", None, None, None
            
            # Print statistics about the FASTA file
            seq_count = len(records)
            avg_length = sum(len(record.seq) for record in records) / seq_count
            max_length = max(len(record.seq) for record in records)
            
            stats = f"File contains {seq_count} sequences.\n"
            stats += f"Average length: {avg_length:.1f} bases.\n"
            stats += f"Maximum length: {max_length} bases.\n\n"
            
            # Recommend Super5 for large datasets
            if seq_count > 1000 or (seq_count > 100 and avg_length > 2000):
                stats += "NOTE: This is a large dataset. Super5 method is recommended.\n\n"
            
            # Run the alignment with the selected options
            output_file, result = run_muscle5_alignment(
                temp_fasta.name, 
                use_stratified=use_stratified,
                use_super5=use_super5
            )
            
            # Create visualization and conservation table if alignment was successful
            fig = None
            table = None
            alignment = None
            if output_file and os.path.exists(output_file):
                fig, table, alignment = create_alignment_plot(output_file)
            
            # Return statistics, result, visualization, conservation table, and alignment
            return stats + result, fig, table, alignment
            
        except Exception as e:
            return f"Error parsing FASTA file: {str(e)}", None, None, None
        
    except Exception as e:
        return f"Error processing file: {str(e)}", None, None, None
    finally:
        # Cleanup
        if temp_fasta and os.path.exists(temp_fasta.name):
            try:
                os.remove(temp_fasta.name)
            except:
                pass
        if output_file and os.path.exists(output_file):
            try:
                pass  # Don't delete the output file as we need it for visualization
            except:
                pass

def export_sequences(alignment, format_type, region=None):
    """
    Export sequences in various formats
    
    Args:
        alignment: BioPython MultipleSeqAlignment object
        format_type: String indicating the format (fasta, clustal, nexus, etc.)
        region: Optional tuple (start, end) to export a specific region
    
    Returns:
        String representation of the sequences in the requested format
    """
    if alignment is None:
        return "No alignment available for export"
    
    # Create a temporary file to use AlignIO for format conversion
    fd, temp_file = tempfile.mkstemp(suffix=f".{format_type}")
    os.close(fd)
    
    try:
        # If region is specified, slice the alignment
        if region and len(region) == 2:
            start, end = region
            # Convert to 0-based indexing if needed
            if start > 0:
                start -= 1
            subalignment = alignment[:, start:end]
        else:
            subalignment = alignment
        
        # Write to the specified format
        AlignIO.write(subalignment, temp_file, format_type)
        
        # Read back the formatted content
        with open(temp_file, 'r') as f:
            content = f.read()
        
        return content
    
    except Exception as e:
        return f"Error exporting sequences: {str(e)}"
    
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)

# Create Gradio interface
def create_ui():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Use actual time
    current_user = "Taher Akbari Saeed"  # Updated to real name
    
    with gr.Blocks(title="Muscle5 Sequence Alignment Tool") as app:
        gr.Markdown("# Muscle5 Sequence Alignment Tool")
        gr.Markdown("Upload a FASTA file to align sequences using Muscle5.")
        
        # Store the alignment as a state variable
        alignment_state = gr.State(None)
        
        with gr.Row():
            with gr.Column(scale=1):
                file_input = gr.File(label="Upload FASTA File")
                
                use_stratified = gr.Checkbox(
                    label="Generate Stratified Ensemble", 
                    info="Creates multiple alignments to evaluate quality"
                )
                
                use_super5 = gr.Checkbox(
                    label="Use Super5 Algorithm", 
                    info="Recommended for large datasets (>1000 sequences)"
                )
                
                submit_btn = gr.Button("Run Alignment", variant="primary")
                
                # Display system resources
                cpu_count = multiprocessing.cpu_count()
                memory_gb = get_max_memory_gb()
                gr.Markdown(f"System Resources: {cpu_count} CPU cores will be utilized")
                
                # Add MUSCLE5 executable selector with improved UI
                with gr.Group():
                    gr.Markdown("### MUSCLE5 Executable Configuration")
                    
                    # Check if the current path is valid and display appropriate status
                    is_valid, message = validate_muscle_executable(current_muscle_path)
                    initial_status = f"{'✅ Ready to run' if is_valid else '❌ MUSCLE5 not properly configured'}"
                    initial_color = "green" if is_valid else "red"
                    
                    gr.Markdown("""
                    MUSCLE5 is required for alignment. Select the executable for your operating system:
                    - [Download MUSCLE5](https://drive5.com/muscle/)
                    - [View Setup Guide](MUSCLE5_SETUP.md)
                    """)
                    
                    # Show colored status message
                    muscle_path_status = gr.Markdown(
                        f"<span style='color: {initial_color};'>{initial_status}</span>"
                    )
                    
                    with gr.Row():
                        muscle_file_input = gr.File(
                            label="Select MUSCLE5 Executable",
                            file_types=[".exe", ".out", ""],
                            file_count="single",
                            type="filepath"
                        )
                        muscle_update_btn = gr.Button("Set MUSCLE5 Path", variant="primary")
                    
                    # Connect the update button to the update_muscle_path function
                    def update_and_format_status(file):
                        status_msg = update_muscle_path(file)
                        # Color based on success/failure
                        color = "green" if "✅" in status_msg else "red"
                        return f"<span style='color: {color};'>{status_msg}</span>"
                    
                    muscle_update_btn.click(
                        fn=update_and_format_status,
                        inputs=[muscle_file_input],
                        outputs=[muscle_path_status]
                    )
                    
                    # Remove the update_displayed_path function and the muscle_path_text component
                    # that were previously here
                
                gr.Markdown(f"""
                ## Alignment Options:
                - **Standard Alignment**: Default alignment using the PPP algorithm
                - **Stratified Ensemble**: Creates multiple alignments to evaluate quality
                - **Super5**: Use for very large datasets (>1000 sequences)
                
                ## Current Date/Time: {current_time}
                ## Author: {current_user}
                ### Contact:
                - Email: taherakbarisaeed@gmail.com
                - GitHub: tayden1990
                - Telegram: https://t.me/tayden2023
                
                If you use this tool in your research, please cite:
                ```
                Saeed, T. A. (2023). Muscle5 Sequence Alignment Tool: A Python interface for 
                MUSCLE5 with visualization and conservation analysis.
                ```
                """)
            
            with gr.Column(scale=2):
                # Add tabs for text results, visualization, and conservation table
                with gr.Tabs():
                    with gr.TabItem("Alignment Text"):
                        text_output = gr.Textbox(label="Alignment Result", lines=20)
                    
                    with gr.TabItem("DNA Visualization"):
                        plot_output = gr.Plot(label="DNA Alignment Visualization")
                        gr.Markdown("""
                        ### Visualization Legend:
                        - **Colors**: A=green, C=blue, G=orange, T=red, gaps=grey
                        - **Yellow highlights**: SNP positions (columns with variation)
                        - **Green highlights**: Conserved regions (identical across all sequences)
                        - Use the range slider at the bottom to navigate through the sequence
                        - Click and drag to zoom into specific regions
                        """)
                    
                    with gr.TabItem("Conservation Analysis"):
                        gr.Markdown("""
                        ### Conserved Regions Analysis
                        This table shows continuous regions where all sequences have identical nucleotides.
                        A region is only considered conserved if:
                        1. All sequences have the exact same nucleotide (A, C, G, or T) at each position
                        2. No gaps are present in any sequence
                        3. No ambiguous nucleotides (like N) are present
                        """)
                        conservation_table = gr.DataFrame(label="Conserved Regions")
                        gr.Markdown("""
                        - **Start**: Starting position of the conserved region
                        - **End**: Ending position of the conserved region
                        - **Length**: Number of nucleotides in the conserved region
                        - **Sequence**: The actual conserved sequence
                        
                        Regions are sorted by length (longest first) to highlight the most significant conserved areas.
                        """)
                    
                    with gr.TabItem("Export Options"):
                        gr.Markdown("### Export Sequences")
                        
                        with gr.Row():
                            export_format = gr.Dropdown(
                                label="Export Format",
                                choices=["fasta", "clustal", "phylip", "nexus", "stockholm"],
                                value="fasta"
                            )
                            
                            export_region = gr.Checkbox(
                                label="Export Specific Region",
                                value=False
                            )
                        
                        with gr.Row(visible=False) as region_selector:
                            region_start = gr.Number(label="Start Position", value=1, minimum=1, step=1)
                            region_end = gr.Number(label="End Position", value=100, minimum=1, step=1)
                        
                        export_btn = gr.Button("Generate Export", variant="primary")
                        export_result = gr.Textbox(label="Export Result", lines=15)
                        copy_btn = gr.Button("Copy to Clipboard")
                        download_btn = gr.Button("Download as File")
                        
                        # JavaScript for copying to clipboard
                        copy_btn.click(
                            None,
                            js="""
                            function() {
                                const text = document.querySelector("textarea[data-testid='textbox']").value;
                                navigator.clipboard.writeText(text);
                                return text;
                            }
                            """
                        )
                        
                        # Update region selector visibility
                        export_region.change(
                            fn=lambda x: gr.Row(visible=x),
                            inputs=[export_region],
                            outputs=[region_selector]
                        )
                        
                        # Function to export sequences
                        def export_handler(alignment, format_type, use_region, start, end):
                            if alignment is None:
                                return "Please run an alignment first."
                            
                            if use_region:
                                region = (int(start), int(end))
                            else:
                                region = None
                                
                            return export_sequences(alignment, format_type, region)
                        
                        export_btn.click(
                            fn=export_handler,
                            inputs=[alignment_state, export_format, export_region, region_start, region_end],
                            outputs=[export_result]
                        )
                        
                        # Function to update region end value based on alignment length
                        def update_region_end(alignment):
                            if alignment is None:
                                return 100
                            return alignment.get_alignment_length()
                        
                        # Download handler
                        def download_handler(text, format_type):
                            if not text or text == "Please run an alignment first.":
                                return None
                                
                            # Create a temporary file with the content
                            fd, temp_file = tempfile.mkstemp(suffix=f".{format_type}")
                            os.close(fd)
                            
                            with open(temp_file, 'w') as f:
                                f.write(text)
                                
                            return temp_file
                        
                        download_btn.click(
                            fn=download_handler,
                            inputs=[export_result, export_format],
                            outputs=[gr.File(label="Download")]
                        )
        
        # Connect button to function
        def process_and_store(file, use_stratified, use_super5):
            result, fig, table, alignment = process_fasta(file, use_stratified, use_super5)
            
            # Update region end value if alignment is available
            end_val = alignment.get_alignment_length() if alignment else 100
            
            return result, fig, table, alignment, gr.Number(value=end_val, minimum=1, step=1)
        
        submit_btn.click(
            fn=process_and_store, 
            inputs=[file_input, use_stratified, use_super5], 
            outputs=[text_output, plot_output, conservation_table, alignment_state, region_end]
        )
        
    # Add Codespaces info box if running in Codespaces
    if is_codespaces():
        with gr.Blocks() as app:
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 🌩️ GitHub Codespaces Environment")
                    gr.Markdown("""
                    **You're running in GitHub Codespaces!**
                    
                    - Session will timeout after 30 minutes of inactivity
                    - For large datasets, consider downloading and running locally
                    - Use the share button to get a temporary public URL
                    """)
                with gr.Column(scale=3):
                    # Insert main interface components
                    pass
    else:
        # Regular interface for non-Codespaces environments
        pass
    
    return app

def create_app():
    """
    Create and return the Gradio interface without launching it.
    Used by codespaces_start.py to launch with custom parameters.
    """
    # Create the interface using the existing UI function
    app = create_ui()
    return app

# If this script is run directly (not imported), launch the app normally
if __name__ == "__main__":
    demo = create_app()
    demo.launch()

if __name__ == "__main__":
    # Run MUSCLE5 setup check
    check_and_setup_muscle()
    
    app = create_ui()
    
    # Try to use the compatibility module if available
    try:
        from utils.compatibility import launch_app
        launch_app(app)
    except ImportError:
        # Fall back to the original code if compatibility module isn't available
        codespaces_env = is_codespaces()
        if codespaces_env:
            # GitHub Codespaces requires public=True and needs the host to be 0.0.0.0
            print(f"Running in GitHub Codespaces environment")
            try:
                result = app.launch(server_name="0.0.0.0", share=True, prevent_thread_lock=True)
                if hasattr(result, 'share_url') and result.share_url:
                    print("\n" + "=" * 60)
                    print(f"🌎 PUBLIC SHARING URL: {result.share_url}")
                    print("=" * 60 + "\n")
            except TypeError:
                # Fallback for older Gradio versions or if there's a parameter issue
                result = app.launch(server_name="0.0.0.0", share=True)
                if hasattr(result, 'share_url') and result.share_url:
                    print("\n" + "=" * 60)
                    print(f"🌎 PUBLIC SHARING URL: {result.share_url}")
                    print("=" * 60 + "\n")
        else:
            # Standard local launch
            result = app.launch(share=True)
            if hasattr(result, 'share_url') and result.share_url:
                print("\n" + "=" * 60)
                print(f"🌎 PUBLIC SHARING URL: {result.share_url}")
                print("=" * 60 + "\n")