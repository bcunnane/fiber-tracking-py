import numpy as np
import matplotlib.pyplot as plt
import cv2


class DtiFiber:
    def __init__(self):
        self.roi = []


def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        roi = np.append(roi, [[x,y]], axis=0)
        
        

def get_roi(img):
    # initiate roi points
    global roi
    roi = np.empty((0,2), int)
    
    # ensure image is in correct data type, uint8
    img = np.array(img, dtype = np.uint8 )
    print(type(img))
    
    #get roi points
    cv2.imshow('Select MG muscle',img)
    cv2.setMouseCallback('Select MG muscle', click_event)
    cv2.waitKey(0)        
    cv2.destroyAllWindows()
    
    plt.imshow(img)
    plt.plot(roi[:,0], roi[:,1],'ob')
    return roi


def get_dti_fibers(mag, evx, evy, fa):
    result = DtiFiber()
    result.roi = get_roi(mag)
    
    return result


# test
import scipy.io
dti = scipy.io.loadmat('BC_DTI_D.mat')
data = get_dti_fibers(dti['M'], dti['X'], dti['Y'], dti['FA'])