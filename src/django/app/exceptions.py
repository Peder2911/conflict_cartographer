from django.conf import settings

class ConfigurationError(Exception):
    def __init__(self,setting_name):
        setting_value = getattr(settings,setting_name)
        self.message = f"{setting_name} was misconfigured: {setting_value}"
        super().__init__(self.message)
