
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pydicom as dcm
from dti_fibers import get_masks
from scipy.io import loadmat
import pickle



class FSE:
    def __init__(self, posn, filename):
        self.posn = posn
        self.filename = filename


def window(path):
    # Load the DICOM image
    ds = dcm.dcmread(path)

    # Get the pixel array from the DICOM image
    pixel_array = ds.pixel_array.astype(np.float32)

    # Set desired window level (center) and width from MicroDicom exploration
    window_level = 144
    window_width = 190

    # Calculate the minimum and maximum values for the new window
    minval = window_level - window_width / 2.0
    maxval = window_level + window_width / 2.0

    # Rescale the pixel values using the new window
    pixel_array = np.clip(pixel_array, minval, maxval)
    pixel_array = (pixel_array - minval) / (maxval - minval)
    pixel_array = np.clip(pixel_array, 0.0, 1.0)
    return pixel_array


def fse_fig():
    folder = r"C:\Users\Brandon\repos\fiber-tracking-py\scirep_figs\figure2"
    figs = [FSE('P', r"\P_IM-0004-0006.dcm"),
            FSE('N', r"\N_IM-0011-0006.dcm"),
            FSE('D', r"\D_IM-0017-0006.dcm")]

    for f in figs:
        f.im = window(folder + f.filename)
        file = open('BC_DTI_'+f.posn, 'rb')
        pkl = pickle.load(file)
        np.savetxt(f"roi_{f.posn}.csv", pkl.roi, delimiter=",")
        f.roi = pkl.roi * 2 #rescale 256 to 512
        f.masks = np.sum(get_masks(f.roi, 512), 0)
        f.fibers = pkl.fibers * 2 #rescale 256 to 512
        f.overlay = f.im + f.masks * 0.6

    fig = np.concatenate((figs[0].overlay, figs[1].overlay, figs[2].overlay), axis=1)

    # plot fibers
    plt.imshow(fig, cmap='gray')
    plt.axis('off')

    # % add
    # arrows
    # clr = 'green';
    # fs = 24;
    # if p == 1
    #     text(275, 170, '→', 'Color', clr, 'FontSize', fs, 'FontWeight', 'bold')
    #     text(295, 255, '→', 'Color', clr, 'FontSize', fs, 'FontWeight', 'bold')
    # elseif
    # p == 2
    # text(270, 155, '→', 'Color', clr, 'FontSize', fs, 'FontWeight', 'bold')
    # text(290, 250, '→', 'Color', clr, 'FontSize', fs, 'FontWeight', 'bold')
    #
    # else
    # text(290, 270, '→', 'Color', clr, 'FontSize', fs, 'FontWeight', 'bold')
    # end

    for i in range(3):
        # plot fibers
        for j in range(0, len(figs[i].fibers[:,0]), 2):
            plt.plot(figs[i].fibers[j:j+2,0] + 511*i, figs[i].fibers[j:j+2,1], '--c', linewidth=0.75)
        plt.text(511 * i + 20, 500, ['PH', 'PL', 'D'][i], color='w', fontsize=8)

    # P arrows
    plt.text(290, 270, '→', color='c', fontsize=8)

    # N arrows
    plt.text(275 + 512, 175, '→', color='c', fontsize=8)
    plt.text(290 + 512, 270, '→', color='c', fontsize=8)

    # D arrows
    plt.text(278 + 512*2, 180, '→', color='c', fontsize=8)
    plt.text(298 + 512*2, 265, '→', color='c', fontsize=8)

    plt.savefig('test.png', dpi=300, bbox_inches='tight', pad_inches=0)




if __name__ == '__main__':
    fse_fig()


