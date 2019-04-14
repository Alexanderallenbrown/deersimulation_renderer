import os


def createRender(fname='bge_rendered/video.mp4'):
    os.system("blenderplayer DeerVehicleSimulationPlayer_blockmap.blend")
    os.system("mv bge_rendered/video.mp4 "+fname)

if __name__=='__main__':
    createRender()