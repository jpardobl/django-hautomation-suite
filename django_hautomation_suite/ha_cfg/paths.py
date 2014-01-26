import os



def x10_plugin_settings():
    import hautomation_x10
    p = os.path.join(os.path.dirname(hautomation_x10.__file__), "settings.py")
    if not os.path.isfile(p):
        raise ValueError("Cannot find X10 plugin settings file")
    return p

def django_thermostat_settings():
    import django_thermostat
    p = os.path.join(os.path.dirname(django_thermostat.__file__), "settings.py")
    if not os.path.isfile(p):
        raise ValueError("Cannot find django_thermostat settings file")
    return p
