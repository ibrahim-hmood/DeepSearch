from debugger import Debugger
from os.path import exists
from xml.etree import ElementTree as Tree
class DeepConfig:
    """
    __init__: constructor that sets configuration data to that from a given path
    @optional param config_path: optional path of configuration file
    """
    def __init__(self, config_path: str = None):
        #Initialize the configuration dataset
        self.__config = dict()
        self.__debugger = Debugger()
        
        #Make sure configuration path is set
        if(config_path is not None):
            #Check if the configuration file exists
            if(exists(config_path)):
                self.__debugger.debug("Trying configuration file at {}".format(config_path))
                #Read the configuration data
                self.__read(config_path)
    
    """
    __read: try to read configuration data from path into config
    @param config_path: configuration file to be read
    """
    def __read(self, config_path: str):
        #Read the configuration data
            #Parse the data using XML
        tree = Tree.parse(config_path)
            #Find all configurations
        configs = tree.findall("Config")
            #Go through them all
        for configuration in configs:
                #Get current configuration attribute and value
                attr = configuration.get("attr", "")
                val = configuration.text
                #And add that to our configuration dictionary
                self.add(attr, val)
    
    """
    add: adds key and value to configuration
    @param key: key to be added
    @param value: value to be added
    """
    def add(self, key: str, value: object):
         self.__config[key] = value
    
    """
    get: returns value of key, if it exists
    @param key: key whose value we want
    @returns value of key if it exists
    """
    def get(self, key: str):
         if(key in list(self.__config.keys())):
              return self.__config[key]
         return None
    
    """
    get_int: gets value of key as integer
    @param key: key whose value we want
    @returns value as integer
    """
    def get_int(self, key: str):
         val = self.get(key)
         if(val is not None):
              return int(val)
         return val
    
    """
    get_bool: gets value of key as boolean
    @param key: key whose value we want
    @returns value as boolean
    """
    def get_bool(self, key: str):
         val = self.get(key)
         if(val is not None):
              val = val.lower()
              return (val == "true")
         return False
    
    """
    get_list: gets value of key as boolean
    @param key: key whose value we want
    @returns value as list
    """
    def get_list(self, key: str):
         val = self.get(key)
         if(val is not None):
              val = val.split(",")
         return val
    
    """
    debugger: gets current debugger
    @returns debugger
    """
    def debugger(self):
         return self.__debugger