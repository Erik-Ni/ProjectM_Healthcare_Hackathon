import argparse
import json
from configparser import ConfigParser
from utils.video_stream import video_stream

############################################################################################################################################

parser = ConfigParser()
parser.read('config.ini')

config = dict()

config['EMOTION_API'] = str(parser.get('NETWORK', 'EMOTION_API'))
config['MOOD_API'] = str(parser.get('NETWORK', 'MOOD_API'))
config['REQUEST_TIMEOUT'] = int(parser.get('NETWORK', 'REQUEST_TIMEOUT'))
config['FRAMES_PER_REQUEST'] = int(parser.get('NETWORK', 'FRAMES_PER_REQUEST'))

config['PROTOTXT_DIRECTORY'] = str(parser.get('DIRECTORIES', 'PROTOTXT_DIRECTORY'))
config['CAFFEMODEL_DIRECTORY'] = str(parser.get('DIRECTORIES', 'CAFFEMODEL_DIRECTORY'))

config['EMOTIONS'] = list(json.loads(parser.get('DATA', 'EMOTIONS')))
config['MOODS'] = list(json.loads(parser.get('DATA', 'MOODS')))

config['FONT_STYLE'] = int(parser.get('OPENCV', 'FONT_STYLE'))
config['FONT_SCALE'] = float(parser.get('OPENCV', 'FONT_SCALE'))
config['EMOTION_COLORS'] = list(json.loads(parser.get('OPENCV', 'EMOTION_COLORS')))
config['MOOD_COLORS'] = list(json.loads(parser.get('OPENCV', 'MOOD_COLORS')))
config['RECTANGLE_THICKNESS'] = int(parser.get('OPENCV', 'RECTANGLE_THICKNESS'))
config['TEXT_THICKNESS'] = int(parser.get('OPENCV', 'TEXT_THICKNESS'))

############################################################################################################################################

video_stream(config)