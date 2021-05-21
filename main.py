import argparse
import json
from configparser import ConfigParser
from utils.video_access import video_access

############################################################################################################################################

parser = ConfigParser()
parser.read('config.ini')

config = dict()

config['EMOTION_API'] = parser.get('NETWORK', 'EMOTION_API')
config['MOOD_API'] = parser.get('NETWORK', 'MOOD_API')
config['REQUEST_TIMEOUT'] = int(parser.get('NETWORK', 'REQUEST_TIMEOUT'))
config['FRAMES_PER_REQUEST'] = int(parser.get('NETWORK', 'FRAMES_PER_REQUEST'))

config['PROTOTXT_DIRECTORY'] = parser.get('DIRECTORIES', 'PROTOTXT_DIRECTORY')
config['CAFFEMODEL_DIRECTORY'] = parser.get('DIRECTORIES', 'CAFFEMODEL_DIRECTORY')

config['EMOTIONS'] = json.loads(parser.get('DATA', 'EMOTIONS'))
config['MOODS'] = json.loads(parser.get('DATA', 'MOODS'))

config['FONT_STYLE'] = int(parser.get('OPENCV', 'FONT_STYLE'))
config['FONT_SCALE'] = float(parser.get('OPENCV', 'FONT_SCALE'))
config['COLOR'] = (int(parser.get('OPENCV', 'BLUE')), int(parser.get('OPENCV', 'GREEN')), int(parser.get('OPENCV', 'RED')))
config['RECTANGLE_THICKNESS'] = int(parser.get('OPENCV', 'RECTANGLE_THICKNESS'))
config['TEXT_THICKNESS'] = int(parser.get('OPENCV', 'TEXT_THICKNESS'))

############################################################################################################################################

video_access(config, 0)