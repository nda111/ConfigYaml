import os
from pathlib import Path
from yaml import safe_dump

class Config(dict):
    '''
    A hierarchical configuration data.
            
    Methods
    ---
        to_dict()
            Change the configuration into a python ```dict``` instance.
        save(name: str, directory: os.PathLike)
            Save the configuration into a file in yaml format.
    '''
    
    def __init__(self, original: dict=None):
        if original is not None:
            for key, val in original.items():
                if isinstance(val, dict) and not isinstance(val, Config):
                    self[key] = Config(val)
                else:
                    self[key] = val
                    
    def __set_value(self, key: str, value):
        if isinstance(value, dict) and not isinstance(value, Config):
            value = Config(value)
            
        keys = key.split('.')
        node = self
        for k in keys[:-1]:
            node = dict.__getitem__(node, k)
            
        dict.__setattr__(node, keys[-1], value)
        dict.__setitem__(node, keys[-1], value)
                    
    def __setitem__(self, key: str, value):
        self.__set_value(key, value)
    
    def __setattr__(self, name: str, value):
        self.__set_value(name, value)
    
    def __getitem__(self, key: str):
        keys = key.split('.')
        node = self
        for k in keys:
            node = dict.__getitem__(node, k)
        return node
    
    def __repr__(self) -> str:
        return self.to_dict().__repr__()
            
    def to_dict(self):
        '''
        Change the configuration into a python ```dict``` instance.
        '''
        result = {}
        for key, val in self.items():
            if isinstance(val, Config):
                val = val.to_dict()
            result[key] = val
        return result
    
    def save(self, name: str, directory: os.PathLike):
        '''
        Save the configuration into a file in yaml format.
        
        Parameters
        ---
            name: str
                The name of the file without extension.
            directory: os.PathLike
                A directory to save the file. ```ConfigDir``` directory is preferred.
        '''
        name = name.replace('.', os.sep) + '.yaml'
        directory = Path(str(directory))
        
        fullname = directory.joinpath(name)
        directory.mkdir(parents=True, exist_ok=True)
        
        with open(fullname, 'w') as file:
            safe_dump(self.to_dict(), file)
