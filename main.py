import argparse
import json
from configparser import ConfigParser
from utils.video_access import video_access

############################################################################################################################################

parser = ConfigParser()
parser.read('config.ini')

config = dict()

config['HOST'] = parser.get('DOMAIN', 'HOST')
config['PORT'] = parser.get('DOMAIN', 'PORT')
config['EMOTION_URL'] = parser.get('APIS', 'EMOTION_URL').format(config['HOST'], config['PORT'])
config['MOOD_URL'] = parser.get('APIS', 'MOOD_URL').format(config['HOST'], config['PORT'])
config['PROTOTXT_DIRECTORY'] = parser.get('APIS', 'PROTOTXT_DIRECTORY')
config['CAFFEMODEL_DIRECTORY'] = parser.get('APIS', 'CAFFEMODEL_DIRECTORY')

config['EMOTIONS'] = json.loads(parser.get('DATA_LIST', 'EMOTIONS'))
config['MOODS'] = json.loads(parser.get('DATA_LIST', 'MOODS'))

config['FRAMES_PER_REQUEST'] = int(parser.get('CONFIGURATION', 'FRAMES_PER_REQUEST'))
config['FONT_SCALE'] = float(parser.get('CONFIGURATION', 'FONT_SCALE'))
config['COLOR'] = (int(parser.get('CONFIGURATION', 'BLUE_LEVEL')), int(parser.get('CONFIGURATION', 'GREEN_LEVEL')), int(parser.get('CONFIGURATION', 'RED_LEVEL')))
config['RECTANGLE_THICKNESS'] = int(parser.get('CONFIGURATION', 'RECTANGLE_THICKNESS'))
config['TEXT_THICKNESS'] = int(parser.get('CONFIGURATION', 'TEXT_THICKNESS'))

############################################################################################################################################

video_access(config, 0)