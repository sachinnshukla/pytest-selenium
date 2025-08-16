"""
Configuration module - provides environment-specific settings
Usage:
    from config import config
    
    # Access configuration values
    driver.get(config.BASE_URL)
    login_page.enter_username(config.USERNAME)
"""

from config.environment_manager import environment_manager


class ConfigProxy:
    """Proxy class to provide lazy loading of configuration"""
    
    def __init__(self):
        self._config = None
    
    def _get_config(self):
        if self._config is None:
            self._config = environment_manager.config
        return self._config
    
    @property
    def BASE_URL(self):
        return self._get_config().base_url
    
    @property
    def USERNAME(self):
        return self._get_config().username
    
    @property
    def PASSWORD(self):
        return self._get_config().password
    
    @property
    def TIMEOUT(self):
        return self._get_config().timeout
    
    @property
    def BROWSER(self):
        return self._get_config().browser
    
    @property
    def HEADLESS(self):
        return self._get_config().headless
    
    @property
    def WINDOW_WIDTH(self):
        return self._get_config().window_size.width
    
    @property
    def WINDOW_HEIGHT(self):
        return self._get_config().window_size.height
    
    @property
    def IMPLICIT_WAIT(self):
        return self._get_config().implicit_wait
    
    @property
    def PAGE_LOAD_TIMEOUT(self):
        return self._get_config().page_load_timeout
    
    @property
    def ENVIRONMENT(self):
        return self._get_config().environment


# Create proxy instance and expose it
config = ConfigProxy()

# For backward compatibility, expose common values as module attributes
def __getattr__(name):
    """Dynamic attribute access for backward compatibility"""
    if hasattr(config, name):
        return getattr(config, name)
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")