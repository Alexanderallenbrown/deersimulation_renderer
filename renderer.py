from bge import render

counter = 0

def grabFrame():
    global counter

    filename = "bge_rendered/frame_" + str(counter).zfill(4) + ".png"
    print("Saving to " + filename)
    render.makeScreenshot(filename)

    counter += 1