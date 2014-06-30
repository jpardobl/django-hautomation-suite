import logging, os
from ha_cfg import paths
from django.core.management.base import BaseCommand

logger = logging.getLogger("backup_config")


class Command(BaseCommand):
    args = ''
    help = 'Create a ready to run Django settings file for Home Automation Python Project'

    def handle(self, *args, **options):
        cwd = os.getcwd()
        logger.info("Backing up settings from every involved module to %s" % cwd)
        
        shutil.copyfile(paths.x10_plugin_settings(), os.path.join(cwd, "x10_plugin_settings.bak"))
        logger.info("Backed up file: %s" % os.path.join(cwd, "x10_plugin_settings.bak"))
        shutil.copyfile(paths.django_thermostat_settings(), os.path.join(cwd, "django_thermostat_settings.bak"))
        logger.info("Backed up file: %s" % os.path.join(cwd, "django_thermostat_settings.bak"))
