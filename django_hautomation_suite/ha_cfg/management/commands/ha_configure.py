import logging, re, shutil, pytz, os
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
    
    SUPERVISOR_HASUITE_PATH = "django_hautomation_suite/distro_hasuite.conf"
    SUPERVISOR_EVAL_HASUITE_THERM_PATH = "django_hautomation_suite/distro_eval_hasuite_therm.conf"
    
    SUPERVISOR_HASUITE_PATH_DEST = "supervisor_hasuite.conf"
    SUPERVISOR_EVAL_HASUITE_THERM_PATH_DEST = "supervisor_eval_hasuite_therm.conf"
    
    FQDN_PATTERN = r"(?=^.{4,255}$)(^((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}$)"
    IP_PATTERN = r""
    
    applied_vals = {}
    
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
        for key, val in new_settings.items():
            self.applied_vals[key] = val
        
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
    
    def statics(self):
        """ Configures the following directives:
        HA_STATIC
        """
        vals = {}

        default = os.path.join(os.getcwd(), "static/")
        vals["HA_STATIC"] = raw_input("Where do you want to static assets? [%s]:" % default)
        if len(vals["HA_STATIC"]) == 0: vals["HA_STATIC"] = default
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
                self.stderr.write("Must be a IP or a valid FQDN")
                continue
            break
        while True:
            vals["HA_MOCHAD_PORT"] = raw_input("Insert mochad port [1099]: ")
            if len(vals["HA_MOCHAD_PORT"]) == 0: 
                vals["HA_MOCHAD_PORT"] = 1099
                break
            try:
                int(vals["HA_MOCHAD_PORT"])
            except:
                self.stderr.write("Invalid value for a port, please insert a port number")
                continue
            break
        return vals
        
    def ha_web(self):
        """Configures every directive needed by the django_haweb module"""
        vals = {}
        while True:
            vals["HA_REST_API_HOST"] = raw_input("Insert Home Automation Python Project REST API host [http://%s:8000]: " % self.applied_vals["HA_WEB_SERVER_NAME"])
            if len(vals["HA_REST_API_HOST"]) == 0: 
                vals["HA_REST_API_HOST"] = "http://%s:8000" % self.applied_vals["HA_WEB_SERVER_NAME"]
                break
            if not re.match(self.IP_PATTERN, vals["HA_REST_API_HOST"]) and not re.match(self.FQDN_PATTERN, vals["HA_REST_API_HOST"]):
                self.stderr.write("Must be a IP or a valid FQDN")
                continue
            break
        while True:
            vals["HA_REST_API_USERNAME"] = raw_input("Insert Home Automation Python Project REST API username: ")
            if len(vals["HA_REST_API_USERNAME"]) == 0: 
                self.stderr.write("Must be a valid username")
                continue
            break
        while True:
            vals["HA_REST_API_PASSWORD"] = raw_input("Insert Home Automation Python Project REST API password: ")
            if len(vals["HA_REST_API_PASSWORD"]) == 0: 
                self.stderr.write("Must be a valid password")
                continue
            break       
        return vals
    
    def django_thermometer(self):
        pass
    
    def django_thermostat(self):
        vals = {}
        while True:
            vals["HA_HEATER_PROTOCOL_X10"] = raw_input("Insert the Heater domotic protocol: ")
            if len(vals["HA_HEATER_PROTOCOL_X10"]) == 0: 
                self.stderr.write("Must be a valid protocol name")
                continue
            break
        
        while True:
            vals["HA_HEATER_DID"] = raw_input("Insert the Heater domotic address: ")
            if len(vals["HA_HEATER_DID"]) == 0: 
                self.stderr.write("Must be a valid address")
                continue
            break
        
        while True:
            default = "http://localhost:8000"
            if "HA_REST_API_HOST" in self.applied_vals and self.applied_vals["HA_REST_API_HOST"] is not None:
                default = self.applied_vals["HA_REST_API_HOST"]
            
            vals["HA_HEATER_API"] = raw_input("Insert the Home Automation Python Project REST API server [%s]: " % default)
            if len(vals["HA_HEATER_API"]) == 0:
                vals["HA_HEATER_API"] = default
            if not re.match(self.IP_PATTERN, vals["HA_HEATER_API"]) and not re.match(self.FQDN_PATTERN, vals["HA_HEATER_API"]):
                self.stderr.write("Must be a IP or a valid FQDN")
                continue
            break
        
        while True:
            default = ""
            if "HA_REST_API_USERNAME" in self.applied_vals and self.applied_vals["HA_REST_API_USERNAME"] is not None:
                default = self.applied_vals["HA_REST_API_USERNAME"]
            vals["HA_HEATER_USERNAME"] = raw_input("Insert the Home Automation Python Project REST API username [%s]: " % default)
            if len(vals["HA_HEATER_USERNAME"]) == 0:
                if default == "":
                    self.stderr.write("Must be a valid username")
                    continue                     
                vals["HA_REST_API_USERNAME"] = default
                
            break
        
        while True:
            if "HA_REST_API_PASSWORD" in self.applied_vals and self.applied_vals["HA_REST_API_PASSWORD"] is not None:
                default = self.applied_vals["HA_REST_API_PASSWORD"]
            vals["HA_HEATER_PASSWORD"] = raw_input("Insert the Home Automation Python Project REST API password [%s]: " % default)
            if len(vals["HA_HEATER_PASSWORD"]) == 0: 
                vals["HA_HEATER_PASSWORD"] = default
            break   
            
        while True:
            vals["HA_HEATER_MARGIN"] = raw_input("Insert the margin to add/substract when comparing temperatures : ")
            try:
                vals["HA_HEATER_MARGIN"] = float(vals["HA_HEATER_MARGIN"])
            except:
                self.stderr.write("Must be a float number")
                continue
            break
        while True:
            vals["HA_HEATER_INCREMENT"] = raw_input("Insert the increment of the Confort and Economic web controls : ")
            try:
                vals["HA_HEATER_INCREMENT"] = float(vals["HA_HEATER_INCREMENT"])
            except:
                self.stderr.write("Must be a float number")
                continue
            break
        while True:
            vals["HA_FLAME_STATS_ENABLE"] = raw_input("Activate flaming reports Yes|No: ")
            if vals["HA_FLAME_STATS_ENABLE"] not in ("No", "Yes"):
                self.stderr.write("Answer not valid. Yes or No?")
                continue
            vals["HA_FLAME_STATS_ENABLE"] = (vals["HA_FLAME_STATS_ENABLE"] == "Yes")
            break
        if vals["HA_FLAME_STATS_ENABLE"]:
            while True:
                vals["HA_FLAME_STATS_PATH"] = raw_input("Insert the flaming report path: ")
                if len(vals["HA_FLAME_STATS_PATH"]) == 0: 
                    self.stderr.write("Must be a valid path")
                    continue
                break
            
        while True:
            default = "http://localhost"
            if "HA_REST_API_HOST" in self.applied_vals and self.applied_vals["HA_REST_API_HOST"] is not None:
                default = self.applied_vals["HA_REST_API_HOST"]
                
            vals["HA_TERMOMETER_SERVER"] = raw_input("Insert the thermometer API server [%s]: " % default)
            if len(vals["HA_TERMOMETER_SERVER"]) == 0:
                vals["HA_TERMOMETER_SERVER"] = default
                break
            if not re.match(self.IP_PATTERN, vals["HA_TERMOMETER_SERVER"]) and not re.match(self.FQDN_PATTERN, vals["HA_TERMOMETER_SERVER"]):
                self.stderr.write("Must be a IP or a valid FQDN")
                continue

            break
        return vals

    def supervisor(self):
        """ Configures the following directives:
        PROCESS_WORKING_DIR
        PROCESS_USER
        """
         
        vals = {}

        vals["PROCESS_WORKING_DIR"] = os.getcwd()
        while True:
            vals["PROCESS_USER"] = raw_input("Please enter the user that must be used to run the daemon process: ")
            if len(vals["PROCESS_USER"]) == 0:
                self.stderr.write("Invalid user")
                continue
            break
        while self.applied_vals["HA_DJANGO_THERMOSTAT_DEPLOYED"]:
            vals["SECONDS_INTERVAL"] = raw_input("PLease enter the seconds to wait before next thermostat loop: ")
            try:
                s = int(vals["SECONDS_INTERVAL"])
                if s < 10: raise Exception("To high")
                break
            except:
                self.stderr.write("Invalid number of seconds, must be over 10s")
                continue
        return vals

    def nginx(self):
        """ Configures the following directives:
        PROCESS_WORKING_DIR
        PROCESS_USER
        """
         
        vals = {}

        vals["PROCESS_WORKING_DIR"] = os.getcwd()
        while True:
            vals["PROCESS_USER"] = raw_input("Please enter the user that must be used to run the daemon process: ")
            if len(vals["PROCESS_USER"]) == 0:
                self.stderr.write("Invalid user")
                continue
            break
        while True:
            vals["SECONDS_INTERVAL"] = raw_input("PLease enter the seconds to wait before next thermostat loop: ")
            try:
                s = int(vals["SECONDS_INTERVAL"])
                if s < 10: raise Exception("To high")
                break
            except:
                self.stderr.write("Invalid number of seconds, must be over 10s")
                continue
        return vals
    
    def handle(self, *args, **options):
        #logging.basicConfig(level=logging.DEBUG)
        self.gen_settings()
        self.apply_settings(self.database())
        self.apply_settings(self.server())
        self.apply_settings(self.time_zone())
        self.apply_settings(self.statics())
        
        while True:
            harest = raw_input("Want to deploy the Home Automation Python Project REST API server (module django_hautomation)? Yes|No: ")
            if harest not in ("No", "Yes"):
                self.stderr.write("Answer not valid. Yes or No?")
                continue
            harest = (harest == "Yes")
            break
        if harest:
            self.apply_settings(
                self.x10_plugin(), 
                self.HAUTOMATION_X10_PATH,
                paths.x10_plugin_settings())
            #marking as activated the django_hautomation module
        self.apply_settings({"HA_DJANGO_HAUTOMATION_DEPLOYED": harest})
                                 
        while True:
            haweb = raw_input("Want to deploy the Home Automation Python Project Domotic Web (module django_haweb)? Yes|No: ")
            if haweb not in ("No", "Yes"):
                self.stderr.write("Answer not valid. Yes or No?")
                continue
            haweb = (haweb == "Yes")
            break
        if haweb:
            self.apply_settings(self.ha_web())
        self.apply_settings({"HA_DJANGO_HAWEB_DEPLOYED": haweb})

            
        while True:
            hathermometer = raw_input("Want to deploy the Home Automation Python Project Thermometer (module django_thermometer)? Yes|No: ")
            if hathermometer not in ("No", "Yes"):
                self.stderr.write("Answer not valid. Yes or No?")
                continue
            hathermometer = (hathermometer == "Yes")
            break
        if hathermometer:
            self.django_thermometer()
        self.apply_settings({"HA_DJANGO_THERMOMETER_DEPLOYED": hathermometer})
       
        while True:
            hathermostat = raw_input("Want to deploy the Home Automation Python Project Thermostat (module django_thermostat)? Yes|No: ")
            if hathermostat not in ("No", "Yes"):
                self.stderr.write("Answer not valid. Yes or No?")
                continue
            hathermostat = (hathermostat == "Yes")
            break
        if hathermostat:
            self.apply_settings(
                self.django_thermostat(),
                self.THERMOSTAT_PATH,
                paths.django_thermostat_settings()
                )
        self.apply_settings({"HA_DJANGO_THERMOSTAT_DEPLOYED": hathermostat})
        
        supervisor = self.supervisor()
        self.apply_settings(supervisor, self.SUPERVISOR_EVAL_HASUITE_THERM_PATH, self.SUPERVISOR_EVAL_HASUITE_THERM_PATH_DEST)
        self.apply_settings(supervisor, self.SUPERVISOR_HASUITE_PATH, self.SUPERVISOR_HASUITE_PATH_DEST)
       