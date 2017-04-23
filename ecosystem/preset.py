
class Preset(object):
    """Defines a preset list of tools"""

    def __init__(self, preset_dictionary):
        self.presets = preset_dictionary.get('presets', None)
        self.tools = preset_dictionary.get('tools', None)

    def resolve_dependencies(self, presets):
        for preset in self.presets:
            if preset in presets:
                self.tools += presets[preset].tools
