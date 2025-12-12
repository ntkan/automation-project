from SeleniumLibrary import SeleniumLibrary
from .keywords import Common
import sys

class Share(SeleniumLibrary):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        SeleniumLibrary.__init__(self, 30)
        self.add_library_components(
            [
                Common(self)
            ]
        )
        ####################################################################################
        # Make sure pydevd installed: pip install pydevd
        # AND Uncomment following codes to enable debug mode
        # sys.path.append("pycharm-debug-py3k.egg")
        # import pydevd_pycharm
        # pydevd_pycharm.settrace('localhost', port=8001, stdoutToServer=True, stderrToServer=True)
        ####################################################################################
