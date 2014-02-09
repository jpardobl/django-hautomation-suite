import logging, os
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.conf import settings 


class Command(BaseCommand):
    args = ''
    help = 'Deploy static assets into location chosen by the user'

    def handle(self, *args, **options):
        #logging.basicConfig(level=logging.DEBUG)
        deploy_statics = (raw_input("Shall deploy statics? yes|NO: ") == "yes")
        
        if deploy_statics:
            if not os.path.isdir(settings.STATIC_ROOT): os.makedirs(settings.STATIC_ROOT)
            call_command('collectstatic', interactive=True)
        
        