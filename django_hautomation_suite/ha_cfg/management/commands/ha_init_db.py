import logging
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from hautomation_x10.deploy import populate_db
from django_thermostat.settings import HEATER_DID, HEATER_PROTOCOL
from django.conf import settings 
from hacore.models import Device, Protocol


class Command(BaseCommand):
    args = ''
    help = 'Once the configuration has been done and applied, this command populates the database'

    def handle(self, *args, **options):
        #logging.basicConfig(level=logging.DEBUG)
        
        #shall we create the database
        
        create_db = (raw_input("Shall create the database? yes|NO: ") == "yes")
            
        if create_db: call_command('syncdb', interactive=True)
        
        populate_x10 = (raw_input("Shall populate X10 protocol? yes|NO: ") == "yes")
        
        if populate_x10: populate_db()
        
        if settings.DJANGO_THERMOSTAT_DEPLOYED:
            populate_heater = (raw_input("Shall populate heater DID to database? yes|NO: ") == "yes")
            if populate_heater:
                Device(protocol=Protocol.objects.get(name=HEATER_PROTOCOL), did=HEATER_DID, device_type="switch", caption="Heater").save()