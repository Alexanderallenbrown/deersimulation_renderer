#import time
import bge
import sys, select
import time
from math import *
from bge import logic
global  controller, Deer, cube, scene, f,k,initialP,flen,fname,deerstate

fname = 'simdata.txt'

def procline(f):
    global deerstate
    #the file for the car should have the following structure:
    # 0         1                   2             3  4  5  6  7     8        9       10     11    12     13        14            15             16        17     18
    # t, steercommand,steerangle, X,U,Y,V,Psi,Psidot, Xdot,Udot,Ydot,Vdot,Psidot,Psiddot, deerspeed,deerpsi,deerx,deery
    line = f.readline()
    linestrip = line.strip()
    linesplit = line.split('\t')
    if(len(linesplit)==19):
        t,deerstate = float(linesplit[0]), [float(linesplit[15]),float(linesplit[16]),float(linesplit[17]),float(linesplit[18])]
    else:
        print('Uh Oh. The file was not right')

    return t,deerstate

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def setup():
    global  controller, Deer, deerstate, scene, f,k,initialP,flen,fname
    deerstate = [0,0,0,0]
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
    Deer = controller.owner
    initialP = Deer.worldPosition
    scene = bge.logic.getCurrentScene()



def main():
    global  controller, Deer, deerstate, scene, f,k,initialP,flen,fname

    if(k<flen-1):
        t,deerstate = procline(f)
        k+=1
    else:
        k=0
        f.close()
        f.open()
        t,deerstate = procline(f)

    Deer = controller.owner
    initialP = Deer.worldPosition

    Deer.worldPosition = [deerstate[2],deerstate[3],.7]
    Deer.worldOrientation = [3.14/2,0,deerstate[1]]

def Running():
    global  controller, Deer, deerstate, scene, f,k,initialP,flen,fname
    controller = bge.logic.getCurrentController()
    scene = bge.logic.getCurrentScene()
    if deerstate[0] > 0:
        print('RUNNING ANIMATION')
        controller.activate('Running')
        controller.deactivate('Standing')
    else:
        print('NO RUNNING ANIMATION')
        controller.activate('Standing')
        controller.deactivate('Running')