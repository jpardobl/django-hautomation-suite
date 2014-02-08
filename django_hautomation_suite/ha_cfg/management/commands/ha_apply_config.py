import logging, re, shutil, pytz
from ha_cfg import paths
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    args = ''
    help = 'Create a ready to run Django settings file for Home Automation Python Project'

    DISTRO_SETTINGS_PATH = "django_hautomation_suite/distro_settings.py"
    RUNNING_SETTINGS_PATH = "django_hautomation_suite/settings.py"
    CONFIGURED_SETTINGS_PATH = "django_hautomation_suite/settings_configured.py"
    
    HAUTOMATION_X10_PATH = "django_hautomation_suite/distro_hautomation_x10_settings.py"
    THERMOSTAT_PATH = "django_hautomation_suite/distro_thermostat_settings.py"
    
    FQDN_PATTERN = r"(?=^.{4,255}$)(^((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}$)"
    IP_PATTERN = r""
    
    def gen_settings(self):
        shutil.copyfile(Command.DISTRO_SETTINGS_PATH, Command.CONFIGURED_SETTINGS_PATH)
                   
    

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.DEBUG)
        logging.info("Applying settings from %s to %s" % (self.CONFIGURED_SETTINGS_PATH, self.RUNNING_SETTINGS_PATH))
        
        shutil.copyfile(self.CONFIGURED_SETTINGS_PATH, self.RUNNING_SETTINGS_PATH)