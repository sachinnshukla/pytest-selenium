import json
import os
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class WindowSize:
    width: int
    height: int


@dataclass
class EnvironmentConfig:
    environment: str
    base_url: str
    username: str
    password: str
    timeout: int
    browser: str
    headless: bool
    window_size: WindowSize
    implicit_wait: int
    page_load_timeout: int
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EnvironmentConfig':
        window_size_data = data.get('window_size', {'width': 1920, 'height': 1080})
        window_size = WindowSize(**window_size_data)
        
        return cls(
            environment=data.get('environment', 'prod'),
            base_url=data.get('base_url', 'https://www.saucedemo.com/'),
            username=data.get('username', 'standard_user'),
            password=data.get('password', 'secret_sauce'),
            timeout=data.get('timeout', 10),
            browser=data.get('browser', 'chrome'),
            headless=data.get('headless', False),
            window_size=window_size,
            implicit_wait=data.get('implicit_wait', 3),
            page_load_timeout=data.get('page_load_timeout', 20)
        )


class EnvironmentManager:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.environments_dir = self.project_root / "environments"
        self._config: Optional[EnvironmentConfig] = None
    
    def get_available_environments(self) -> list:
        """Get list of available environment configuration files"""
        if not self.environments_dir.exists():
            return []
        
        env_files = list(self.environments_dir.glob("*.json"))
        return [f.stem for f in env_files]
    
    def load_environment(self, env_name: str = None) -> EnvironmentConfig:
        """Load environment configuration"""
        # Priority: Command line -> Environment variable -> Default (prod)
        if env_name is None:
            env_name = os.getenv('TEST_ENV', 'prod')
        
        config_file = self.environments_dir / f"{env_name}.json"
        
        if not config_file.exists():
            available_envs = self.get_available_environments()
            raise FileNotFoundError(
                f"Environment config '{env_name}' not found. "
                f"Available environments: {available_envs}"
            )
        
        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
            
            self._config = EnvironmentConfig.from_dict(config_data)
            return self._config
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {config_file}: {e}")
        except Exception as e:
            raise RuntimeError(f"Error loading environment config: {e}")
    
    @property
    def config(self) -> EnvironmentConfig:
        """Get current configuration, load default if not loaded"""
        if self._config is None:
            self.load_environment()
        return self._config
    
    def get_config_value(self, key: str, default=None):
        """Get specific configuration value"""
        return getattr(self.config, key, default)
    
    def print_config(self):
        """Print current configuration for debugging"""
        if self._config is None:
            print("No configuration loaded")
            return
        
        print(f"\n=== Environment Configuration ===")
        print(f"Environment: {self._config.environment}")
        print(f"Base URL: {self._config.base_url}")
        print(f"Browser: {self._config.browser}")
        print(f"Headless: {self._config.headless}")
        print(f"Timeout: {self._config.timeout}s")
        print(f"Window Size: {self._config.window_size.width}x{self._config.window_size.height}")
        print(f"==================================\n")


# Global instance
environment_manager = EnvironmentManager()
