from wave import open as load
import numpy as np
from os import access, F_OK


class Wav:
    """Let's work with the waves! This class will help you doing some interesting things with them.
    To get started, initialize its object sending the path to the file as an argument!"""

    def __init__(self, path, **params):
        self.path = path
        self.size = 0
        self.compname, self.comptype = None, None
        self.content = np.array([])
        if access(path, F_OK):
            self.load()
        if params:
            self.setparams(**params)
            return
        raise FileNotFoundError('for new files you need to provide params!')

    def load(self):
        with load(self.path, 'rb') as file:
            self.channels, self.bitdepth, self.samprate, self.size, self.comptype, self.compname = file.getparams()
            self.bitdepth *= 8
            self.peak = 2 ** (self.bitdepth - 1)
            self.content = np.fromstring(file.readframes(self.size), dtype=f'int{self.bitdepth}')

    def write(self, data):
        with load(self.path, 'wb') as file:
            file.setnchannels(self.channels)
            file.setsampwidth(self.bitdepth // 8)
            file.setframerate(self.samprate)
            file.writeframesraw(data)
        self.load()

    def setparams(self, **params):
        if 'channels' in params:
            self.channels = params['channels']
        if 'bitdepth' in params:
            self.bitdepth = params['bitdepth']
            self.peak = 2 ** (self.bitdepth - 1)
        if 'samprate' in params:
            self.samprate = params['samprate']

    @property
    def duration(self):
        return self.size / self.samprate
