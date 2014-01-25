import logging, re, shutil, pytz, paths
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    args = ''
    help = 'Create a ready to run Django settings file for Home Automation Python Project'

    DISTRO_SETTINGS_PATH = "django_hautomation_suite/settings_distro.py"
    RUNNING_SETTINGS_PATH = "django_hautomation_suite/settings.py"
    CONFIGURED_SETTINGS_PATH = "django_hautomation_suite/settings_configured.py"
    
    HAUTOMATION_X10_PATH = "django_hautomation_suite/hautomation_x10_settings_distro.py"
    
    FQDN_PATTERN = r"(?=^.{4,255}$)(^((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}$)"
    IP_PATTERN = r""
    
    X10_PLUGIN_SETTINGS = ""
    def gen_settings(self):
        shutil.copyfile(Command.DISTRO_SETTINGS_PATH, Command.CONFIGURED_SETTINGS_PATH)
                   
    def apply_settings(self, new_settings, origin_path = None, dest_path = None):
        self.stdout.write("Applying settings...")
        if origin_path is None:
            origin_path = Command.CONFIGURED_SETTINGS_PATH
        with open(origin_path, "r") as fichero:
            content = fichero.read()
        for k, v in new_settings.items():
            logging.debug("Applying setting %s: %s" % (k, v))
            v = str(v)
            content = re.sub(r"%s" % k, v, content)
        if dest_path is None:
            dest_path = Command.CONFIGURED_SETTINGS_PATH
        with open(dest_path, "w") as fichero:
            fichero.write(content)
        
    def database(self):
        """
        Configure the database directives
        """
        
        vals = {}
        while True:
            vals["HA_DB_TYPE"] = raw_input("Choose DB type: ")
            if not re.match(r"postgresql_psycopg2|mysql|sqlite3|oracle", vals["HA_DB_TYPE"]):
                self.stderr.write("Invalid DB type")
                continue
            break

        while True:
            vals["HA_DB_NAME"] = raw_input("Insert DB name: ")
            if len(vals["HA_DB_NAME"]) == 0:
                self.stderr.write("Invalid DB name")
                continue
            break
        
        if vals["HA_DB_TYPE"] == "sqlite3":
            return vals
        
        while True:
            vals["HA_DB_USER"] = raw_input("Insert DB user: ")
            if len(vals["HA_DB_USER"]) == 0:
                self.stderr.write("Invalid DB user")
                continue
            break    
        
        while True:
            vals["HA_DB_PASSWORD"] = raw_input("Insert DB password: ")
            if len(vals["HA_DB_PASSWORD"]) == 0:
                self.stderr.write("Invalid DB password")
                continue
            break 

        while True:
            try:
                vals["HA_DB_HOST"] = raw_input("Insert DB host [localhost]: ")
                if len(vals["HA_DB_HOST"]) == 0:
                    vals["HA_DB_HOST"] = "localhost"
                    break
                
                if not re.match(self.IP_PATTERN, vals["HA_DB_HOST"]) and not re.match(self.FQDN_PATTERN, vals["HA_DB_HOST"]):
                    raise ValueError()
            except ValueError:
                self.stderr.write("Invalid DB host")
                continue            
            break 
        while True:
            try:
                vals["HA_DB_PORT"] = int(raw_input("Insert DB port: "))
            except ValueError:
                self.stderr.write("Invalid DB port")
                continue            
            break
        
        return vals 
        
    def server(self):
        """ Configures the following directives:
        ALLOWED_HOSTS
        """
        
        vals = {}
        while True:
            vals["HA_WEB_SERVER_NAME"] = raw_input("Insert the web server name: ")
            if not re.match(self.FQDN_PATTERN, vals["HA_WEB_SERVER_NAME"]) and not re.match(self.IP_PATTERN, vals["HA_WEB_SERVER_NAME"]):
                self.stderr.write("Invalid value, please insert a valid IP or FQDN")
                continue
            break
        return vals
    
    def time_zone(self):
        """ Configures the following directives:
        HA_TIME_ZONE
        """
         
        vals = {}
        while True:
            vals["HA_TIME_ZONE"] = raw_input("Insert the time zone: ")
            if vals["HA_TIME_ZONE"] not in pytz.all_timezones: 
                self.stderr.write("Invalid time zone")
                continue
            break
        return vals
    
    def x10_plugin(self):
        """ Configures the X10 plugin. It provides the mochad server details """
        
        vals = {}
        while True:
            vals["HA_MOCHAD_HOST"] = raw_input("Insert mochad host [localhost]: ")
            if len(vals["HA_MOCHAD_HOST"]) == 0: 
                vals["HA_MOCHAD_HOST"] = "localhost"
                break
            if not re.match(self.IP_PATTERN, vals["HA_MOCHAD_HOST"]) and not re.match(self.FQDN_PATTERN, vals["HA_MOCHAD_HOST"]):
                    raise ValueError()
            break
        while True:
            vals["HA_MOCHAD_PORT"] = raw_input("Insert mochad port [1099]: ")
            if len(vals["HA_MOCHAD_PORT"]) == 0: 
                vals["HA_MOCHAD_PORT"] = "1099"
                break
            try:
                int(vals["HA_MOCHAD_PORT"])
            except:
                self.stderr.write("Invalid value for a port, please insert a port number")
                continue
            break
        return vals
        
    def handle(self, *args, **options):
        logging.basicConfig(level=logging.DEBUG)
        self.gen_settings()
        #self.apply_settings(self.database())
        #self.apply_settings(self.server())
        #self.apply_settings(self.time_zone())
        self.apply_settings(
                self.x10_plugin(), 
                self.HAUTOMATION_X10_PATH,
                paths.x10_plugin_settings())
            
