# -*- coding: utf-8 -*-

import os

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

MANDATORY_KEYS = ['station-key', 'departure-key']


def load_config(f):
    if not os.path.isfile(f):
        raise IOError('Missing configuration file: %s' % f)

    config = load(open(f), Loader=Loader)

    if not config:
        raise ValueError('Invalid configuration file (wants yaml): %s' % f)

    for key in MANDATORY_KEYS:
        if key not in config:
            raise ValueError('Missing mandatory configration key: %s' % key)
    return config
