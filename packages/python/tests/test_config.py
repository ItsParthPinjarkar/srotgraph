"""Tests for the shared Python config module."""


from srotgraph_python.config import AppSettings


def test_app_settings_defaults() -> None:
    """Test default settings values."""
    settings = AppSettings()
    
    assert settings.app_name == "SrotGraph"
    assert settings.app_version == "0.1.0"
    assert settings.environment == "development"
    assert settings.debug is False


def test_app_settings_is_production() -> None:
    """Test is_production property."""
    settings = AppSettings()
    
    assert settings.is_production is False
    assert settings.is_development is True
    
    settings.environment = "production"
    assert settings.is_production is True
    assert settings.is_development is False


def test_app_settings_is_development() -> None:
    """Test is_development property."""
    settings = AppSettings()
    
    assert settings.is_development is True
    
    settings.environment = "production"
    assert settings.is_development is False


def test_app_settings_custom_values() -> None:
    """Test custom settings values."""
    settings = AppSettings(
        app_name="CustomApp",
        app_version="1.0.0",
        environment="staging",
        debug=True,
    )
    
    assert settings.app_name == "CustomApp"
    assert settings.app_version == "1.0.0"
    assert settings.environment == "staging"
    assert settings.debug is True
