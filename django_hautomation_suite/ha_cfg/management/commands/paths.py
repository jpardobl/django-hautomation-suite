import os
import hautomation_x10

def x10_plugin_settings():
    
    p = os.path.join(os.path.dirname(hautomation_x10.__file__), "settings.py")
    if not os.path.isfile(p):
        raise ValueError("Cannot find X10 plugin settings file")
    return p
        
