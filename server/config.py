import pkgsettings
import settings_vial


DEFAULT_SETTINGS = {
    "HOST": "0.0.0.0",
    "PORT": 8000,
    "DATABASE_URL": "sqlite:///./shortlinks.db",
    "ALLOWED_HOSTS": ["*"],
}

def configure_settings(settings: pkgsettings.Settings) -> pkgsettings.Settings:
    settings.configure(**DEFAULT_SETTINGS)

    env_settings = settings_vial.Settings(env_prefix="S_")
    env_settings.load_env()
    settings.configure(env_settings)
    return settings

settings = configure_settings(pkgsettings.Settings())

__all__ = ["settings"]