#import time
import bge
import sys, select
import time
from math import *
#from numpy import *
from bge import logic
global  suspension,controller, car, cube, scene, f,k,initialP,flen,fname,carstate

import os

#initialize the counting index for the file line
k=0
#set the name of the file that contains car positions
fname = 'simdata.txt'
carstate = [0,0,0,0,0,0]
caray = 0
carax = 0



class Suspension:
    def __init__(self,tauroll,taupitch):
        self.tauroll = tauroll
        self.taupitch = taupitch
        self.roll = 0
        self.pitch = 0

    def update(self,dt,ax,ay):
        self.roll+=dt/self.tauroll*((5.0*3.14/180)*ay/9.81-self.roll)
        self.pitch+=dt/self.taupitch*((2.0*3.14/180)*-ax/9.81-self.pitch)
        return self.roll,self.pitch

suspension = Suspension(.2,.2)

def procline(f):
    global carstate,caray,carax,suspension
    #the file for the car should have the following structure:
    # 0         1                   2             3  4  5  6  7     8        9       10     11    12     13        14            15             16        17     18
    # t, steercommand,steerangle, Y,V,X,U,Psi,Psidot, Ydot,Vdot,Xdot,Udot,Psidot,Psiddot, deerspeed,deerpsi,deerx,deery
    line = f.readline()
    linestrip = line.strip()
    linesplit = line.split('\t')
    if(len(linesplit)==20):
        t,carstate = float(linesplit[0]), [float(linesplit[3]),float(linesplit[4]),float(linesplit[5]),float(linesplit[6]),float(linesplit[7]),float(linesplit[8])]
        carstateder = [float(linesplit[9]),float(linesplit[10]),float(linesplit[11]),float(linesplit[12]),float(linesplit[13]),float(linesplit[14])]
        #ay = Vdot + U*psidot
        caray = carstateder[1]+carstate[3]*carstate[5]
        #ax = Udot - V*psidot
        carax = carstateder[3]-carstate[1]*carstate[5]
        roll,pitch = suspension.update(1.0/60,carax,caray)
    else:
        print('Uh Oh. The file was not right')

    return t,carstate

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def setup():
    global  carax,caray,controller, car, cube, scene, f, initialP,k,flen,fname,carstate
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
    cube.worldOrientation = [0,0,carstate[4]]
    scene = bge.logic.getCurrentScene()

def main():
    global  carax,caray,controller, car, cube, scene, f, initialP,k,flen,fname,carstate
    global suspension
    if(k<flen-1):
        t,carstate = procline(f)
        k+=1
    else:
        k=0
        f.close()
        f=open(fname,'r')
        t,carstate = procline(f)

    cube = controller.owner
    initialP = cube.worldPosition
    cube.worldPosition = [carstate[2],carstate[0],initialP[2]]
    # pitch = -(2.0*3.14/180)*carax/9.81
    # roll = (5.0*3.14/180)*caray/9.81
    cube.worldOrientation = [suspension.roll,suspension.pitch,carstate[4]]
    ## #state order is y,v,x,u,psi,r
    