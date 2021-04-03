import os
import json
import argparse

from get_elevation import getElevation

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('sondenumber', metavar='S', type=str, nargs='+',
                    help='Radiosonde number')
args = parser.parse_args()                 
                    
print(args.sondenumber[0], "argument parsing is done :)")