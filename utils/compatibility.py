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

def is_key_in_dict(d, key):
    """Safely check if a key is in a dictionary, handling non-dict types"""
    try:
        return key in d
    except TypeError:
        # If d is not iterable or not a dictionary
        return False

def has_pyobjc():
    """Check if PyObjC is installed and available"""
    try:
        import pyobjc_framework_Cocoa
        return True
    except ImportError:
        return False

def is_compatible_python_version():
    """Check if the current Python version is compatible with all dependencies"""
    major = sys.version_info.major
    minor = sys.version_info.minor
    
    # PyObjC requires Python 3.9+
    if sys.platform == "darwin" and (major, minor) < (3, 9):
        return False
    
    return True

def launch_app(app, **kwargs):
    """
    Launch a Gradio app with appropriate settings for the environment.
    Handles different Gradio versions and environments like GitHub Codespaces.
    
    Args:
        app: The Gradio app to launch
        **kwargs: Additional arguments to pass to app.launch()
    
    Returns:
        The result of app.launch()
    """
    # Default to share=True if not specified
    if 'share' not in kwargs:
        kwargs['share'] = True
        
    # For GitHub Codespaces, we need specific settings
    if is_codespaces():
        logger.info("Running in GitHub Codespaces environment")
        # Set server_name to 0.0.0.0 for Codespaces
        kwargs['server_name'] = '0.0.0.0'
        
        # Check which version of Gradio we're using
        if GRADIO_VERSION and GRADIO_VERSION.startswith('4.'):
            logger.info("Using Gradio 4.x in Codespaces")
            # For Gradio 4.x, cleanup potentially incompatible parameters
            if 'height' in kwargs:
                del kwargs['height']
            if 'prevent_thread_lock' in kwargs:
                del kwargs['prevent_thread_lock']
            if 'show_error' in kwargs:
                del kwargs['show_error']
            # Remove host parameter that's causing issues
            if 'host' in kwargs:
                del kwargs['host']
                
            try:
                # Basic launch for Gradio 4.x
                result = app.launch(**kwargs)
                # Safely try to log the share URL if available
                try:
                    if hasattr(result, 'share_url') and result.share_url:
                        logger.info("----------------------------------------")
                        logger.info("🌎 Public URL: %s", result.share_url)
                        logger.info("----------------------------------------")
                except AttributeError:
                    # If we can't access share_url attribute, don't crash
                    pass
                return result
            except Exception as e:
                logger.warning(f"Launch failed with error: {str(e)}")
                # Try a simpler approach
                return app.launch(server_name='0.0.0.0', share=True)
        else:
            # For Gradio 3.x
            logger.info("Using Codespaces-compatible launch settings for Gradio 3.x")
            try:
                # Try launching with compatible settings for older Gradio
                result = app.launch(
                    show_error=True,
                    prevent_thread_lock=True,
                    **kwargs
                )
                if kwargs['share']:
                    try:
                        if hasattr(result, 'share_url') and result.share_url:
                            logger.info("----------------------------------------")
                            logger.info("🌎 Public URL: %s", result.share_url)
                            logger.info("----------------------------------------")
                    except AttributeError:
                        pass
                return result
            except TypeError as e:
                if "not iterable" in str(e):
                    logger.warning("Encountered 'not iterable' error, trying with simplified launch")
                    # If we get the 'not iterable' error, try a simpler launch approach
                    return app.launch(quiet=True, **kwargs)
                raise
    else:
        # For local environment, use standard launch but still with share=True by default
        logger.info("Running in local environment")
        try:
            result = app.launch(**kwargs)
            if kwargs['share']:
                try:
                    if hasattr(result, 'share_url') and result.share_url:
                        logger.info("----------------------------------------")
                        logger.info("🌎 Public URL: %s", result.share_url)
                        logger.info("----------------------------------------")
                except AttributeError:
                    pass
            return result
        except Exception as e:
            logger.warning(f"Standard launch failed with error: {str(e)}")
            logger.info("Trying simplified launch approach...")
            return app.launch(share=True, server_name='0.0.0.0')
