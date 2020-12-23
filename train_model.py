#auxiliary functions used for the training and testing of our neural netwrok model
import os,shutil
from keras import optimizers
from keras import models
from keras import layers
from keras import regularizers
from keras.preprocessing.image import ImageDataGenerator
from keras.constraints import max_norm
import numpy as np
import neural_network_functions as nnf
import transformation_directories as td
import random


def train(pkudir,times_to_train,model_name,test_cases,where_test_starts,workdir,datadir,verbose,class_scenarios,noval=False):
  """
  ----------------------------------------------------------
  this function conducts our model's training
  ----------------------------------------------------------
  """
  for runs in range(0,times_to_train):

    for num_of_classes in class_scenarios:

      for case in range(0,len(test_cases)):

        basedir = pkudir + str(test_cases[case])+str(num_of_classes)
        model_name_individual = model_name + str(test_cases[case])+str(num_of_classes)

        source_dir,validation_dir,target_dir = nnf.get_base_dirs(basedir)

        if len(test_cases[case])<=3:
          if num_of_classes == 11:
            steps,epochs,batches = 100, 12, 32
          else:
            steps,epochs,batches = 100, 20, 72
        else:
          if num_of_classes == 51:
            steps,epochs,batches = 100, 30, 112
          else:
            steps,epochs,batches = 100, 20, 64


        """
        my_model = models.Sequential()
        my_model = nnf.make_model_sequential(my_model,num_of_classes)
        """
        my_model = nnf.make_model_functional(num_of_classes)
        my_model = nnf.train_model(model_name_individual,my_model,epochs,steps,batches,basedir,noval)
        #nnf.get_individual_accuracies(my_model,target_size,num_of_classes,runs,verbose)
        nnf.test_model(model_name_individual,my_model,num_of_classes,runs,verbose,basedir)
