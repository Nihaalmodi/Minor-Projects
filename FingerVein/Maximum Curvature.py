from bob.bio.vein.preprocessor.mask import LeeMask
from bob.bio.vein.extractor import MaximumCurvature

import numpy,os
from bob.bio.vein.preprocessor import HistogramEqualization
from skimage import color
from bob.io.image import to_bob#,imshow
from skimage import io

# from matplotlib import pyplot as plt

def prepro(addr):
    
    image = to_bob(color.rgb2gray(io.imread(addr)))
    mask = LeeMask()(image)

    image = HistogramEqualization()(image,mask)
    # imshow(image)
    # image = image.astype('float64')/255.
    MC = MaximumCurvature(2.5)
    kappa = MC.detect_valleys(image, mask)
    Vt = MC.eval_vein_probabilities(kappa)
    Cd = MC.connect_centres(Vt)
    G = numpy.amax(Cd, axis=2)
    bina = MC.binarise(G)
    return bina
    # imshow(bina)
    # plt.show()

DATADIR = "./Finger_Vein_Database"
remain = len(os.listdir(DATADIR))
for folder in os.listdir(DATADIR):
    for hand in os.listdir(os.path.join(DATADIR, folder)):
        for image in os.listdir(os.path.join(DATADIR, folder, hand)):
            if image[-3:]==".db":
                continue
            addr = os.path.join(DATADIR, folder, hand, image)
            print(addr)
            filename = "Finger"+"/"+folder+"/"+hand
            if not os.path.exists(filename):
                os.makedirs(filename)
            filename += "/"+"MC_"+image[:-4]+".png"
            io.imsave(filename , prepro(addr))
    print(remain)
    remain -= 1

# mask = mask[1:-1, 1:-1]
# from bob.bio.vein.preprocessor import Preprocessor, NoCrop, LeeMask, HuangNormalization, HistogramEqualization
# processor = Preprocessor(
#     NoCrop(),
#     LeeMask(filter_height=40, filter_width=4),
#     HuangNormalization(padding_width=0, padding_constant=0),
#     HistogramEqualization(),
#     )
# preproc_data = processor(image)

# imshow(preproc_data)