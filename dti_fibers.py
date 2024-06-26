import numpy as np
import cv2
from scipy.ndimage import binary_erosion


class DtiFiber:
    def __init__(self, name):
        self.name = name


def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        global roi
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
    roi = np.append(roi, [roi[0,:]], axis=0) #close polygon
    return roi


def get_masks(roi_pts, im_size):
    
    # get mask for entire muscle ROI
    muscle_mask = np.zeros((im_size,im_size), dtype=np.uint8)
    cv2.fillPoly( muscle_mask, np.array([roi_pts], dtype=np.int32), 1)
    
    # get muscle top (proximalRegion_proximal) & bottom (distalRegion_distal)
    pr_pr = np.min(roi_pts[:,1])
    di_di = np.max(roi_pts[:,1])
    
    # get proximal region's distal dividing line
    ideal_area = np.sum(muscle_mask) // 3
    y = 30
    region_area = 0
    while region_area < ideal_area:
        pr_di = pr_pr + y
        region_area = np.sum(muscle_mask[pr_pr:pr_di, :])
        y += 1
    
    # get distal region's proximal dividing line
    y = 30
    region_area = 0
    while region_area < ideal_area:
        di_pr = di_di - y
        region_area = np.sum(muscle_mask[di_pr:di_di, :])
        y += 1
    
    # get region mask for each array page: (0) proximal (1) middle (2) distal
    region_masks = np.zeros([3] + list(muscle_mask.shape), dtype=np.uint8)    
    region_masks[0, :pr_di, :] = muscle_mask[:pr_di, :]
    region_masks[1, pr_di:di_pr, :] = muscle_mask[ pr_di:di_pr, :]
    region_masks[2, di_pr:, :] = muscle_mask[di_pr:, :]

    for i in range(3):
        region_masks[i,:,:] = binary_erosion(region_masks[i,:,:], structure=np.ones((3,3)))
    return region_masks


def get_fibers(evx, evy, masks, fa):
    fiber_coords = np.zeros((6,2))
    for p in range(3):
        # get centroids
        mask_indices = np.argwhere(masks[p, :, :] == 1)
        mask_indices[:, [1, 0]] = mask_indices[:, [0, 1]]
        centroid = np.mean(mask_indices, axis=0)
                
        # apply region mask and Fractional Anisotropy filter to eigenvectors
        reg_evx = evx * masks[p,:,:] * (fa > 0.15)
        reg_evy = evy * masks[p,:,:] * (fa > 0.15)
        
        # remove zero values
        reg_evx = reg_evx[reg_evx != 0]
        reg_evy = reg_evy[reg_evy != 0]
        
        # point fibers in same direction (diffusion is 180 deg indeterminate)
        wrong_dir_idx = reg_evy > 0
        reg_evy[wrong_dir_idx] = reg_evy[wrong_dir_idx] * -1
        reg_evx[wrong_dir_idx] = reg_evx[wrong_dir_idx] * -1
        
        # get fiber slope in each region
        fiber_slope = np.mean(reg_evy) / np.mean(reg_evx)
        
        # get x direction pixel numbers
        xmin = np.amin(mask_indices[:,0])
        xmax = np.amax(mask_indices[:,0])
        x = np.linspace(xmin, xmax+1, 250)
        
        # draw fiber lines
        y = centroid[1] + fiber_slope * (x - centroid[0])
        xy = np.array([x,y], dtype=np.int32).transpose()
        
        # determine fiber line points within region
        matches = (xy[:,None] == mask_indices).all(-1).any(-1)
        xy_matches = xy[matches]
        
        # select proximal & distal most coordinates as fiber endpoints
        fiber_coords[2*p, :] = xy_matches[-1,:]
        fiber_coords[2*p+1, :] = xy_matches[0,:]
    return fiber_coords
        
    
def process_dti(name, mag, evx, evy, fa):
    result = DtiFiber(name)
    result.roi = get_roi(mag)
    result.masks = get_masks(result.roi, 256)
    result.fibers = get_fibers(evx, evy, result.masks, fa)
    return result


if __name__ == "__main__":
    print('Import ')
