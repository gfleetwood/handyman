import matplotlib.pyplot as plt
from skimage.io import imsave, imread
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu
import skimage.exposure
from scipy.signal import find_peaks

def get_circle(im, x, y, r):
  '''
  https://stackoverflow.com/questions/31519197/python-opencv-how-to-crop-circle/43835120#43835120
  '''
  rectX = (x - r) 
  rectY = (y - r)
  crop_im = im[y:(y+2*r), x:(x+2*r)]

  return(crop_im)
  
  
def plot_hist(im):

  hist, bins = skimage.exposure.histogram(im)
  peaks, _ = find_peaks(hist, threshold = 20000)
  im = im*(im < max(peaks))

  plt.plot(bins, hist, linewidth = 1)
  plt.xlabel('pixel value (a.u.)')
  plt.ylabel('counts')
  plt.imshow(im, cmap = plt.cm.Greys_r)
  plt.show()
  
  return(True)
