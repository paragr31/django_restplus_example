#!C:/ProgramData/Anaconda2/python
__author__ = 'parag rajabhoj'

import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
print "Base Directory = ",BASE_DIR
import configs.settings as config
