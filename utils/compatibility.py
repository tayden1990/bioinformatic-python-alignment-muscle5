"""
Compatibility utilities to handle different versions of Gradio and other dependencies.
This helps the application run across different environments including GitHub Codespaces.
"""

import os
import sys
import pkg_resources
import importlib
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("compatibility")

def get_package_version(package_name):
    """Get the version of an installed package"""
    try:
        return pkg_resources.get_distribution(package_name).version
    except pkg_resources.DistributionNotFound:
        return None

# Get installed Gradio version
GRADIO_VERSION = get_package_version("gradio")
logger.info(f"Detected Gradio version: {GRADIO_VERSION}")

def is_codespaces():
    """Check if running in GitHub Codespaces environment"""
    return "CODESPACES" in os.environ or "CODESPACE_NAME" in os.environ

def launch_app(app, **kwargs):
    """
    Launch the Gradio app with the appropriate parameters for the environment
    
    Args:
        app: Gradio application object
        **kwargs: Additional arguments to pass to app.launch()
        
    Returns:
        The result of app.launch()
    """
    # Always share the app publicly by default unless explicitly set to False
    if 'share' not in kwargs:
        kwargs['share'] = True
    
    logger.info(f"Launching app with share={kwargs['share']}")
    
    if is_codespaces():
        logger.info("Running in GitHub Codespaces environment")
        kwargs['server_name'] = kwargs.get('server_name', '0.0.0.0')
        
        # In Codespaces, we need to use specific settings to avoid the bool iterable error
        if GRADIO_VERSION and GRADIO_VERSION >= "3.40.0":
            logger.info("Using Codespaces-compatible launch settings for Gradio >= 3.40.0")
            try:
                # Try launching with the workaround for newer Gradio versions
                result = app.launch(
                    show_error=True,
                    prevent_thread_lock=True,
                    **kwargs
                )
                if kwargs['share']:
                    logger.info("----------------------------------------")
                    logger.info("🌎 Public URL: %s", result.share_url)
                    logger.info("----------------------------------------")
                return result
            except TypeError as e:
                if "not iterable" in str(e):
                    logger.warning("Encountered 'not iterable' error, trying with simplified launch")
                    # If we get the 'not iterable' error, try a simpler launch approach
                    return app.launch(quiet=True, **kwargs)
                raise
        else:
            # Older Gradio versions don't have the issue
            return app.launch(**kwargs)
    else:
        # For local environment, use standard launch but still with share=True by default
        logger.info("Running in local environment")
        result = app.launch(**kwargs)
        if kwargs['share']:
            logger.info("----------------------------------------")
            logger.info("🌎 Public URL: %s", result.share_url)
            logger.info("----------------------------------------")
        return result
