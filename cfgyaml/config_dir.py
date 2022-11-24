import os
from typing import Union
from yaml import safe_load
from pathlib import Path
from argparse import Namespace

class ConfigDir(os.PathLike):
    '''
    A directory of configurations for your project.
    
    Attributes
    ---
        path : pathlib.Path
            The absolute or relative path of the directory.
        default_filename : str
            The default configuration filename of the directory.  
            
    Methods
    ---
        mkdir(mode: int=0o777, parents: bool=False, exist_ok: bool=False)
            Creates this directory.
        load(config_name: str=None, args: Union[dict, Namespace]=None)
            Load a configuration file from this directory and combine extra arguments.
    '''
    
    DEFAULT = None
    ''' The default instance of this class. It represents \'./config/\'. '''
    
    def __init__(self, path: os.PathLike=f'.{os.sep}/config', default_filename: str='default'):
        '''
        Initialize directory by the path and the default configuration filename.
        
        Parameters
        ---
            path : os.PathLike
                The absolute or relative path of the directory.
            default_filename : str
                The name of the default configuration filename.
            
        Usage
        ---
        >>> cfg_dir = ConfigDir()
        ... # By default, './config/default.yaml' is the directory and its configuration file.
        >>> cfg_dir = ConfigDir('./example/config')
        ... # Able to use your own configuration directory.
        >>> cfg_dir = ConfigDir(default_filename='master')
        ... # You may use your preferred filename.
        '''
        self.__path = Path(path)
        self.default_filename = default_filename
        
    def mkdir(self, mode: int=0o777, parents: bool=False, exist_ok: bool=False):
        '''
        Make the directory.
        
        Parameters
        ---
            mode : int
                Required permission to use the directory. Default: 0o777.
            parents : bool
                If set true, makes all parents of the directory. Default: False.
            exist_ok : bool
                If set false, throws FileExistsError when the directory already exists. Default: False.
            
        Usage
        ---
        >>> cfg_dir = ConfigDir()
        ... cfg_dir.mkdir(parents=True, exist_ok=True)
        '''
        self.__path.mkdir(mode=mode, parents=parents, exist_ok=exist_ok)
        return self
        
    def load(self, config_name: str=None, args: Union[dict, Namespace]=None):
        '''
        Load a configuration file and apply an extra arguments to the configuration.
        
        Parameters
        ---
            config_name : str
                The name of the file without extension.
            args : Union[dict, argparse.Namespace]
                The extra configuration informations.
            
        Usage
        ---
        >>> cfg_dir = ConfigDir()
        ... cfg = cfg_dir.load()
        ... cfg = cfg_dir.load('epoch_100')
        ... cfg = cfg_dir.load('epoch_200')
        >>> cfg_dir = ConfigDir()
        ... parser = ArgumentParser()
        ... ~
        ... cfg = cfg_dir.load('epoch_200', parser.parse_args())
        '''
        from .config import Config
        
        # Load default: Level 1
        if self.default_filename is not None:
            with open(self.default_file_fullpath, 'r') as stream:
                default_config = safe_load(stream)
        else:
            default_config = None
        
        # Load superior config: Level 2
        if config_name is None:
            if default_config is not None:
                result = default_config
            else:
                raise RuntimeError('Neither default nor other config are specified.')
        else:
            config_name = config_name.replace('.', os.sep)
            fullname = self.__path.joinpath(f'{config_name}.yaml')
            if fullname.exists():
                with open(fullname, 'r') as stream:
                    other_config = safe_load(stream)
                    
                result = ConfigDir.__inject_dict(default_config, other_config)
            else:
                raise FileNotFoundError(f'Cannot find \'{fullname}\'.')
        
        # Apply extra arguments: Level 3
        if isinstance(args, Namespace):
            result = ConfigDir.__inject_dict(result, vars(args))
        else:
            result = ConfigDir.__inject_dict(result, args)
            
        return Config(result)

    def __fspath__(self):
        return str(self.__path)

    def __str__(self) -> str:
        return str(self.__path)

    @property    
    def path(self) -> Path:
        '''
        The absolute or relative path.
        '''
        return self.__path
        
    @path.setter
    def path(self, path: os.PathLike):
        if path is None:
            raise ValueError('The path must not be none.')
        else:
            self.__path = Path(path)
        
    @property
    def default_file_fullpath(self) -> Path:
        '''
        The full path of the default configuration file.
        '''
        if self.default_filename is None:
            return None
        else:
            return self.__path.joinpath(f'{self.default_filename}.yaml')
        
    @staticmethod
    def __inject_dict(target, source):
        if target is None:
            return source
        if source is None:
            return target
        
        for key, val in source.items():
            if val is None:
                continue
            
            if '.' in key:
                keys = key.split('.')
                for k in keys[:0:-1]:
                    val = {k: val}
                key = keys[0]
            
            if isinstance(val, dict) and key in target:
                target[key] = ConfigDir.__inject_dict(target[key], val)
            else:
                target[key] = val
        return target

ConfigDir.DEFAULT = ConfigDir()
