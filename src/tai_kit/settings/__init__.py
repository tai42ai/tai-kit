"""Settings machinery: the base class + the cache-reset registry. Leaf settings
live next to the impl they configure (``tai_kit.llm``, ``tai_kit.clients``,
``tai_kit.logging``)."""

from tai_kit.settings.base import TaiBaseSettings
from tai_kit.settings.cache_registry import (
    register_settings_reset,
    reset_all_settings,
    settings_cache,
)
from tai_kit.settings.registry import (
    SettingsClassInfo,
    SettingsFieldInfo,
    registered_settings,
)

__all__ = [
    "SettingsClassInfo",
    "SettingsFieldInfo",
    "TaiBaseSettings",
    "register_settings_reset",
    "registered_settings",
    "reset_all_settings",
    "settings_cache",
]
