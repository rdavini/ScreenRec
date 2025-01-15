import pyautogui
import os
import cv2 as cv
import sys
import time

def cmpImgs(action_fname, region, threshold = 0.8, max_iter = sys.maxsize):
    i = 0
	
    print(f"{action_fname}")
    print(f"region: {region}")
    if os.path.isfile(f"templates\\{action_fname}") == False:
        print("file could not be read, check with os.path.exists()")
        return False
    
    template = cv.imread(f"templates\\{action_fname}", cv.IMREAD_GRAYSCALE)
    assert template is not None, "file could not be read, check with os.path.exists()"
    while(True):
        pyautogui.screenshot(f"screen.png", region)
        img = cv.imread(f"screen.png", cv.IMREAD_GRAYSCALE)
        assert img is not None, "file could not be read, check with os.path.exists()"

        meth= 'cv.TM_CCOEFF_NORMED' 
        method = eval(meth)
        res = cv.matchTemplate(img, template, method)
        max_val =  cv.minMaxLoc(res)[1]
		
        i += 1
        print(f"max_val: {max_val}")
        
        if max_val > threshold:
            print("Action finished")
            return max_val
        elif i >= max_iter:
            return max_val
        else:
            time.sleep(2)
            print("Trying again ", i)