#import time
import bge
import sys, select
import time
from math import *
#from numpy import *
from bge import logic
global  controller, car, cube, scene, f,k,initialP,flen,fname,carstate

import os

#initialize the counting index for the file line
k=0
#set the name of the file that contains car positions
fname = 'simdata.txt'


def procline(f):
    global carstate
    #the file for the car should have the following structure:
    # 0         1                   2             3  4  5  6  7     8        9       10     11    12     13        14            15             16        17     18
    # t, steercommand,steerangle, X,U,Y,V,Psi,Psidot, Xdot,Udot,Ydot,Vdot,Psidot,Psiddot, deerspeed,deerpsi,deerx,deery
    line = f.readline()
    linestrip = line.strip()
    linesplit = line.split('\t')
    if(len(linesplit)==19):
        t,carstate = float(linesplit[0]), [float(linesplit[3]),float(linesplit[4]),float(linesplit[5]),float(linesplit[6]),float(linesplit[7]),float(linesplit[8])]
    else:
        print('Uh Oh. The file was not right')

    return t,carstate

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def setup():
    global  controller, car, cube, scene, f, initialP,k,flen,fname,carstate
    carstate = [0,0,0,0,0,0]
    #get the number of lines in this file so we know
    flen = file_len(fname)
    #open a file that will give us vehicle states at 60Hz
    f = open(fname,'r')
    #the file for the car should have the following structure:
    # t, X,U,Y,V,Psi,Psidot
    #get our initial car position out of the file
   t, carstate = procline(f)
    #increment our counter. We will use this to loop through the file again if needed.
    k+=1

    controller = bge.logic.getCurrentController()
    cube = controller.owner
    #keep track of the initial position of the car so that everything is relative to this.
    initialP = cube.worldPosition
    print(initialP)

    cube.worldPosition = [carstate[2],carstate[0],initialP[2]]
    cube.worldOrientation = [0,0,car.x[4]]
    scene = bge.logic.getCurrentScene()

def main():
    global  controller, car, cube, scene, f, initialP,k,flen,fname,carstate
    if(k<flen-1):
        t,carstate = procline(f)
        k+=1
    else:
        k=0
        f.close()
        f.open()
        t,carstate = procline(f)

    cube = controller.owner
    initialP = cube.worldPosition
    cube.worldPosition = [carstate[2],carstate[0],initialP[2]]
    cube.worldOrientation = [0,0,carstate[4]]
    ## #state order is y,v,x,u,psi,r
    