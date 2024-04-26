
import matplotlib.pyplot as plt
import matplotlib.image as img

# get base image
im = img.imread('Figure 5 base edited.png')
plt.imshow(im)
plt.axis('off')

# at rest markers
plt.plot(162,365,'Dk', markersize=4) #P
plt.plot(177,321,'sk', markersize=4) #N
plt.plot(256,204,'ok', markersize=5) #D

# peak contraction markers
plt.plot(98,558,'Dk', markersize=4, markerfacecolor='none') #P
plt.plot(114,510,'sk', markersize=4, markerfacecolor='none') #N
plt.plot(196,268,'ok', markersize=5, markerfacecolor='none') #D

# format and save
plt.legend(('PH - Rest','PL - Rest','D  - Rest','PH - Peak','PL - Peak','D  - Peak'), prop={'size': 6})
plt.savefig('Figure 5.png', dpi=300, bbox_inches='tight', pad_inches=0)
