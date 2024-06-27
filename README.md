[Return home](https://bcunnane.github.io/)

This project develops MRI image processing methods to study strain in the medial gastrocnemius (MG) muscle of the human calf. Specifically, it examines the effects of different ankle angles and exertion levels to identify the dependence of muscle force on muscle architecture.

It was published in [Nature's Scientific Reports](https://www.nature.com/articles/s41598-023-41127-z).

# Collect Data
Data was collected for 6 subjects in a 1.5T MRI scanner as shown in Figures 1 and 2. The subject’s foot was positioned in a foot pedal fixture that recorded their pressing force. A projector prompted them to repeatedly press the pedal at a certain percentage of their maximum voluntary contraction (% MVC). This procedure was repeated for high (50% MVC) and low (25% MVC) pressing forces at three foot positions: dorsiflexion (D), low plantar flexio (PL), and high plantar flexion (PH). Several different MRI sequences were utilzed to collect different image types, including:
1. Large FOV images to measure subject's ankle position (see Figure 3)
2. High-res images to scout for slice with clear fibers (see Figure 5)
3. Diffusion Tensor images for the chosen slice (see Figure 4)
4. Dynamic (i.e. video) velocity images for the chosen slice (see Figure 6)

![Experimental Setup](files/Research_experimental_setup.png)
> *Figure 1. Experimental Setup*

![Imaging Flowchart](files/Imaging_Flowchart.png)
> *Figure 2. Experimental Setup*

![Ankle Angles](files/Foot_Angles.png)
> *Figure 3. Ankle angle measurements for single subject*

# Identify Muscle Fibers from Diffusion Tensor Imaging (DTI)
Diffusion tensors are calculated from the diffusion images. Since the primary direction of water diffusion within skeletal muscle is along the muscle fiber, the diffusion tensor's principal eigenvector follows the muscle fibers' direction (see Figure 4). An outline of the MG muscle was manually identified, then split into three equal-size regions: proximal, middle, and distal. Then the principal eigenvectors in each region were extracted and averaged to form representative fibers (see Figure 5).

![DTI image](files/DTI_colormaps_with_outline.png)
> *Figure 4. Colormaps of the lead eigenvector are generated as follows: x-component of the eigenvector determines the red, the y-component of the eigenvector determines the green while the z-component of the eigenvector determines the blue hue in each voxel. The colormap of the MG (outlined in white) shows predominantly proximo-distal*

![Muscle Fiber image](files/Fibers.png)
> *Figure 5. The fibers identified by the proposed method using the DTI leading eigenvector data are shown in blue dashed lines in the proximal, middle, and distal regions of the muscle superposed on the high-resolution images. A few fascicles in the MG can be seen in white and are approximately aligned with the DTI derived fibers (identified by blue arrows). It can be seen that not many fascicles are visible in the MG while the proposed technique using DTI is effective in identifying the muscle fibers.*

# Track and Analyze Muscle Fibers
The endpoints of the DTI-identified muscle fibers were tracked through each frame of the dynamic study (see Figure 6). Changes in fiber angle were calculated with respect to the vertical in the image. Changes in fiber length were calculated with respect to initial length, leading to changes in Lagrangian strain. The results of the three muscle fibers were averaged together (see Figure 7). 

![Fiber Gif](files/Supplemental_Video.gif)
> *Figure 6. Average muscle fibers identified from diffusion tensor data for the proximal, middle, and distal regions of the MG muscle. Cine image shows change in fiber length and angle over contraction cycle for all exertion levels and ankle angles of a single subject.*

![Result Plot](files/Temporal_Plots.png)
> *Figure 7. Change in fiber angle, length, and strain vs temporal cycle for the three foot positions. Determined from tracking change in position of the DTI-identified fibers throughout the muscle contraction cycle. The results for the fibers in the proximal, middle, and distal regions of the MG muscle were averaged for each percent MVC.*

# Statistical Analysis and Results
Normality of data was tested using both the Shapiro-Wilk test and visual inspection of Q-Q plots. Fiber strain and normalized fiber strains were normally distributed.
Two-way factorial ANOVA assessed differences between ankle angles and % MVC, as well as potential interaction effects. In case of significant ANOVA results for the factor ‘ankle angles’, Bonferroni-adjusted paired t-tests were used for post hoc analyses.

Fiber lengths and pennation angles at rest and peak contraction were not normally distributed, therefore, non-parametric testing was used. The Mann-Whitney U-test was used to compare the %MVC. Kruskal-Wallis tests were used to compare the ankle angles. Bonferroni-adjusted U-tests were also used for the post-hoc analysis. Table 1b lists the median and interquartile range (over all subjects) of fiber architecture (length and pennation angle) at rest and at peak contraction.

# Discussion
The dorsiflexed ankle position showed significantly lower normalized strains at both %MVCs than the normal and plantarflexed ankle positions. This demonstrates that the dorsiflexed ankle position is at the optimum position for force production, followed by low plantar flexioni, then high plantar flexion. Dorsiflexion producing a high force with low strain could be of interest in rehabilitation paradigms and in optimizing athletic performance. Strain injury in skeletal muscle occurs when regions of a muscle experience localized strains that exceeds a threshold, so dorsiflexion yeilding overall lower strains indicates that high regional strains exceeding the threshold are less likely than in the plantarflexed positions.

In addition, strain increased less than linearly with %MVC. This departure from linearity is most pronounced in the high plantarflexed ankle position, implying that with increasing contraction required to generate higher forces, the MG muscle may be approaching the critical length where further contraction becomes more difficult.