from __future__ import annotations

import os
from typing import Any

from hatch.env.collectors.plugin.interface import EnvironmentCollectorInterface
from hatch.plugin.constants import DEFAULT_CUSTOM_SCRIPT
from hatchling.plugin.utils import load_plugin_from_script


class CustomEnvironmentCollector(EnvironmentCollectorInterface):
    PLUGIN_NAME = 'custom'

    def __new__(cls, root: str, config: dict[str, Any], *args: Any, **kwargs: Any) -> EnvironmentCollectorInterface:
        custom_script = config.get('path', DEFAULT_CUSTOM_SCRIPT)
        if not isinstance(custom_script, str):
            raise TypeError(f'Option `path` for environment collector `{cls.PLUGIN_NAME}` must be a string')
        elif not custom_script:
            raise ValueError(
                f'Option `path` for environment collector `{cls.PLUGIN_NAME}` must not be empty if defined'
            )

        path = os.path.normpath(os.path.join(root, custom_script))
        if not os.path.isfile(path):
            raise OSError(f'Plugin script does not exist: {custom_script}')

        hook_class = load_plugin_from_script(
            path, custom_script, EnvironmentCollectorInterface, 'environment_collector'
        )
        hook = hook_class(root, config, *args, **kwargs)

        # Always keep the name to avoid confusion
        hook.PLUGIN_NAME = cls.PLUGIN_NAME

        return hook
