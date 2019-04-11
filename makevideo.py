import os
import time

def makeVideo():
    print("creating video...")
    os.system("ffmpeg -r 60/1 -i bge_rendered/frame_%04d.png -c:v libx264 -vf fps=60 -pix_fmt yuv420p bge_rendered/video.mp4")
    time.sleep(5)
    print("removing images...")
    os.system("rm bge_rendered/*.png")
    print("done")