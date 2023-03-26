from configparser import ConfigParser
import os

FILE_NAME = 'configuration.ini'
_value = None


def setup():
    if not os.path.exists(FILE_NAME):
        _write_default()
    _read()

def _write_default():
    cp = ConfigParser()

    cp['settings'] = {
        'voice activated': 'yes',
        'realistic voice': 'yes'
        }

    with open('configuration.ini', 'w') as f:
        cp.write(f)

def _read():
    cp = ConfigParser()
    cp.read(FILE_NAME)
    global _value
    _value = cp


def voice_activated():
    _read()
    realistic_voice = _value['settings']['realistic voice'].lower()
    voice = _value['settings']['voice activated'].lower()
    return voice == 'yes', voice == 'yes' and realistic_voice == 'yes'

