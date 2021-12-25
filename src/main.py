from camHandler import CamHandler

if __name__ == "__main__":
    handler = CamHandler(60, 200, 200)
    handler.calibrateCenter()
    handler.calibrateRadius()
    handler.mainLoop()
