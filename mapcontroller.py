#import time
import bge
from math import *
#from numpy import *
from bge import logic
import os


def setup():
    #this file contains the corner of the map block in XY coordinates.
    fname = "mapsetup.txt"
    f = open(fname,'r')

    
    for line in f:
        linestrip = line.strip()
        linesplit = line.split(" ")
        mapX = float(linesplit[0])
        mapY = float(linesplit[1])


    controller = bge.logic.getCurrentController()
    blockmap = controller.owner
    print("setting map position to "+str(mapX)+","+str(mapY))
    

    blockmap.worldPosition = [mapX,mapY,0]

def main():
    pass
    