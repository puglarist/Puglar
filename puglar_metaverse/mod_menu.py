from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class ModSetting:
    key: str
    value: Any
    description: str


class ModMenu:
    """Runtime mod menu with multiplayer-safe allowlist."""

    def __init__(self):
        self._allowlist = {
            "fov",
            "weapon_skin_intensity",
            "realism_postfx",
            "hand_tracking_assist",
            "promod_enabled",
        }
        self._settings: Dict[str, ModSetting] = {}

    def set(self, key: str, value: Any, description: str = "") -> None:
        if key not in self._allowlist:
            raise KeyError(f"{key} is not allowed in this mod profile")
        self._settings[key] = ModSetting(key=key, value=value, description=description)

    def get(self, key: str, default: Any = None) -> Any:
        return self._settings.get(key, ModSetting(key, default, "")).value

    def export(self) -> Dict[str, Any]:
        return {name: setting.value for name, setting in self._settings.items()}
