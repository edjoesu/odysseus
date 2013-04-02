import numpy as np
import os

from pluginmanager import VerbosePlugin
import tkMessageBox

class removal_plugin(VerbosePlugin):
    
    def main(self, rawframes, img, roi, name, path):
        cmd = "move " + path + " C:\\junkimg\\"
        os.system(cmd)
