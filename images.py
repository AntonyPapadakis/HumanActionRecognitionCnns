#--------------------------------------------------
#Create image script
#--------------------------------------------------

import scipy 
from os import listdir
import numpy as np
import csv
from scipy.misc import imsave
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy import stats
from scipy.fftpack import dct
from scipy.fftpack import fft
from scipy.interpolate import interp2d
import transformation_directories as td




def readcsv(filename): 
  """ 
  -----------------------------------------------------
  this function reads all the frames from each csv file
  -----------------------------------------------------    
  """

  csvfile = open(filename)
  reader = csv.reader(csvfile, delimiter=',')
  rownum = 0
  signal_img = []

  for row in reader:
      signal_img.append (row)
      rownum += 1
  csvfile.close()
  return signal_img


def create_action_image(camera_case,workdir,verbose,datadir):
  """
  -------------------------------------------------------------------
  this function creates all the action images for the corresponding 
  camera case
  -------------------------------------------------------------------
  """

  num=159 #this is one of the dimensions of the signal image (75x159)
  action_angle=" " #this is the action directory corresponding to each one of the camera angles
  afterinterpolation=" " # this is the directory with the signal images resulting after the interpolation process
  image_directory= " " #this is the directory with the final action images    
  image_counter = 0 #counter used for naming purposes

  td.create_dirs_angles(camera_case,workdir)
  image_directory,model_name,afterinterpolation,action_angle = td.get_values_dirs(camera_case,workdir,datadir)                                
              
  if verbose: print(action_angle)            
  directory_with_actions = listdir( action_angle )
                  
  for csv_file in directory_with_actions: #run all csv files
        
    if verbose: print('repetition:',csv_file[0:len(csv_file)-4])
    picture = readcsv(action_angle+csv_file)

   
    signal_shape= len(picture)

    shape1 = (signal_shape,75)
    signal_img = np.ndarray(shape1)
    signal_img = np.zeros(shape1)

    for j in range(0,signal_shape):
           signal_img[j] =  picture[j][0:75]


    c=signal_img.T


    shape = (75,num)
    d = np.zeros(shape)
    z = []
    b = []

    #interpolation
    for k in range(0,75):
            arr2 = np.array(c[k])
            arr2_interp = interpolate.interp1d(np.arange(arr2.size), arr2)
            arr2_stretch = arr2_interp(np.linspace(0,arr2.size-1,num))
            b = np.concatenate((b, arr2_stretch), axis=0)
    z = np.reshape(b,(75,num))
    znew = z.T

    #saving the afterinterpolation picture
    plt.imsave(afterinterpolation+'images_'+str(image_counter)+'.png',znew)

    #dst transform
    dst_array = scipy.fftpack.dst(znew,norm='ortho')
    dst_shift = np.fft.fftshift(dst_array)
    
            
    #calculating the magnitude
    magnitude_spectrum_dst = 20*np.log(np.abs(dst_shift))
    magnitude = magnitude_spectrum_dst*255
    
    #saving the picture
    plt.imsave(image_directory+ csv_file[0:len(csv_file)-4]+"_"+ str(camera_case) +'.png',magnitude)
    image_counter+=1
