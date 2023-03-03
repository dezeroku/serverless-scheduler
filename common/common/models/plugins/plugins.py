import importlib
import pkgutil


def discover_plugins(plugins_prefix):
    """
    Find out all installed plugins defining job types.
    Import the modules + return concatenated ENUM_MAPPING and CLASS_MAPPING for
    all the plugins
    """
    # Import only the content from plugin_export module from plugins
    # It's up to the plugin to define proper "*" and include mappings + job types
    # The plugin is expected to provide two dicts:
    # ENUM_MAPPING: {ENUM_FIELD_NAME = enum_string_value}
    # CLASS_MAPPING: {ENUM_FIELD_NAME = ScheduledJobSubclass}
    discovered_plugins = {
        name: importlib.import_module(name + ".plugin_export")
        for _, name, _ in pkgutil.iter_modules()
        if name.startswith(plugins_prefix)
    }
    print(discovered_plugins)
    enum_mapping_all = {}
    class_mapping_all = {}
    for plugin in discovered_plugins.values():
        enum_mapping_all = enum_mapping_all | plugin.ENUM_MAPPING
        class_mapping_all = class_mapping_all | plugin.CLASS_MAPPING

    return enum_mapping_all, class_mapping_all
