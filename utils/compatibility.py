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
        
        # In Codespaces, we need to use specific settings for Gradio 4.x+
        if GRADIO_VERSION and GRADIO_VERSION.startswith("4."):
            logger.info("Using Codespaces-compatible launch settings for Gradio 4.x")
            
            # Remove any parameters that might not be supported in Gradio 4.x
            if 'prevent_thread_lock' in kwargs:
                del kwargs['prevent_thread_lock']
            if 'show_error' in kwargs:
                del kwargs['show_error']
                
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
            logger.warning(f"Standard launch failed with: {str(e)}")
            # Fallback to simplest launch
            return app.launch(server_name='0.0.0.0', share=True)
