import sys, os
sys.path.append(os.path.abspath(f'{__file__}/../../'))

from argparse import ArgumentParser
from cfgyaml import ConfigDir

parser = ArgumentParser(description='An example of cfgyaml package.')
parser.add_argument('--env.device', type=int, default=-1, help='The ID of a GPU to use.')

CFG_DIR = ConfigDir('./example/config')

CFG = CFG_DIR.load()
print(CFG)

CFG = CFG_DIR.load(config_name='overlap')
print(CFG)

CFG = CFG_DIR.load(config_name='overlap', args=parser.parse_args())
print(CFG)
