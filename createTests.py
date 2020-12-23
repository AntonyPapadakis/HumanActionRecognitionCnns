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
import argparse
import train_model as trm


def create_base_dirs(pkudir,test_cases,where_test_starts,workdir,datadir,verbose,class_scenarios):
  """
  ----------------------------------------------------------
  this function conducts our model's training
  ----------------------------------------------------------
  """


  for num_of_classes in class_scenarios:

    #becomes true when we start inserting in training set
    if verbose : print(class_scenarios)

    #actions we are going to use
    if num_of_classes == 51: #51 classes
        processed_actions = list(range(1,52))
        entries = 7151
    else:                    #11 classes
        processed_actions = [10,11,14,16,20,23,30,33,34,46,48]
        entries = 1502

    image_count=0

    #validation set percentage - we'll use 20 %
    #total number of entries used for validation - must be an integer- 51
    #"Left","Middle","Right","Leftby90","Leftby45","Middleby45",
    #                            "Middleby-45","Rightby-90","Rightby-45","Middleby90",
    #                            "Middleby-90","Leftby-45","Leftby-90"
    #                            "Rightby90","Rightby45"




    #getting action data in the action directory
    for case in range(0,len(test_cases)):

      basedir = pkudir + str(test_cases[case])+str(num_of_classes)

      source = test_cases[case][0:int(where_test_starts[case])]
      target = test_cases[case][int(where_test_starts[case]):len(test_cases[case])]

      #prints
      if verbose:
        print("\n ####################################################### \n")
        print("Evaluating case: ",test_cases[case]," where source angles are ",
              source," and the target angles are: ", target )
        print("\n ####################################################### \n ")

      #model name initialization
      if num_of_classes==51: model_name = 'augmented_51_multiangle_'
      else: model_name = 'augmented_11_multiangle_'


      #creates the ./PKU directory containing the source and target directories to be used for training
      nnf.make_base(processed_actions,basedir)

      source_dir,validation_dir,target_dir = nnf.get_base_dirs(basedir)


      for camera_case in test_cases[case]:

        same_camera_test_train = False
        #counts total entries moved
        count_entries=0

        target_size=0
        source_size=0
        validation_size=0


        image_directory,model_name,afterinterpolation,action_angle = td.get_values_dirs(camera_case,workdir,datadir,
                                                         model_name)


        #using the image directory
        dirI = os.listdir( image_directory )


        for image in dirI:

          values = image.split('_')
          filenum = int(values[0])
          #values1 = values[3]

          #51 classes
          #action_num = values1[0]

          #11 classes
          action_num = values[3]

          #11 needs int()
          if (action_num in processed_actions) or (int(action_num) in processed_actions):

            count_entries+=1

            train_labels=[]
            test_labels=[]
            val_labels=[]


            if (camera_case not in target) and (camera_case in source): #for the training and validation sets

              if validation_size / entries < 0.1 : #using 10% of the data for validation

                #directory from which we move the imagesz used for training
                starting_image_dir = image_directory+image

                #destination directory
                destination = validation_dir+"/"+action_num+'_action'+'/'+image
                val_labels.append(action_num)
                validation_size+=1
                shutil.copyfile(starting_image_dir,destination)

              else:
                starting_image_dir = image_directory+image
                destination = source_dir+"/"+action_num+'_action'+'/'+image
                train_labels.append(action_num)
                source_size+=1
                shutil.copyfile(starting_image_dir,destination)


            elif (camera_case in target) and (camera_case not in source): #for the testing set

              starting_image_dir = image_directory+image
              destination = target_dir+"/"+action_num+'_action'+'/'+image
              test_labels.append(action_num)
              target_size+=1
              shutil.copyfile(starting_image_dir,destination)

            elif (camera_case in target) and (camera_case in source):

              same_camera_test_train = True

              r1 = random.randint(0, 4)

              if validation_size / entries < 0.1 and r1==2: #using 10% of the data for validation

                #directory from which we move the imagesz used for training
                starting_image_dir = image_directory+image

                #destination directory
                destination = validation_dir+"/"+action_num+'_action'+'/'+image
                val_labels.append(action_num)
                validation_size+=1
                shutil.copyfile(starting_image_dir,destination)

              elif target_size / entries < 0.1 and r1>=3:
                starting_image_dir = image_directory+image
                destination = target_dir+"/"+action_num+'_action'+'/'+image
                test_labels.append(action_num)
                target_size+=1
                shutil.copyfile(starting_image_dir,destination)

              else:
                starting_image_dir = image_directory+image
                destination = source_dir+"/"+action_num+'_action'+'/'+image
                train_labels.append(action_num)
                source_size+=1
                shutil.copyfile(starting_image_dir,destination)




          image_count+=1
        if  same_camera_test_train: break



parser = argparse.ArgumentParser()
parser.add_argument("-w","--workdir",default="current",
  help="state the working directory where the images are located. Default directory is the current one")
parser.add_argument("-d","--datadir",default="current", 
  help="state the directory where the skeletal data are located from the PKU-MMD dataset. Default directory is the current one")
parser.add_argument("-l","--labeldir",default="current", 
  help="state the directory where the label data are located from the PKU-MMD dataset. Default directory is the current one")
parser.add_argument("-p","--pkudir",default="./PKU", 
  help="state the base directory where the source and target dirs will be created. Default directory is ./PKU which will be created if it does not exist")
parser.add_argument("-testCases",type=str, nargs='+', action='append', help="state the test cases for your experiment. Appropriate directories will be created. Test case format [[train_angle11, ... ,train_angle1N, test_angle12, ... ,test_angle1N],[train_angle21...,test_angle21...]]")
parser.add_argument("-whereTestStarts",nargs='+', type=int,help="state the indentation of the angle from which your test angles start for each case")
parser.add_argument("-v","--verbose",default="False", help="provide an output",
                    action="store_true")
parser.add_argument("-dirs","--directories",default="False", help="if true then all base directories are created",
                    action="store_true")
parser.add_argument("-train","--training",default="False", help="if true then model percedes to training",
                    action="store_true")

args = parser.parse_args()

if os.path.exists(args.workdir) == False and args.workdir!="current" and args.workdir!="../" and args.workdir!="./":
  print("the image working directory you provided does not exist.\n Please provide an existing directory or create one")
  exit()
if os.path.exists(args.datadir) == False and args.datadir!="current" and args.datadir!="../" and args.datadir!="./":
  print("the data directory you provided does not exist.\n Please provide an existing directory or create one")
  exit()
if os.path.exists(args.pkudir) == False: 
  print("the working directory you provided will be created")
  args.pkudir=args.pkudir


#below define all the test cases you want to check
test_cases= list(args.testCases) #[["Left","Middle"],["Middle","Right"],["Left","Right"],["Right","Left"],["Middle","Middle"],["Left","Left"],["Right","Right"],["Right","Left","Middle"]]

#start ident for test data, the other ones are used for train and validation
where_test_starts = args.whereTestStarts #[1,1,1,1,1,1,1,2]

if args.verbose == True: print(args.directories)
if args.directories==True : create_base_dirs(args.pkudir,test_cases,where_test_starts,args.workdir+"/",args.datadir+"/",args.verbose,{11,51})
if args.training==True: trm.train(args.pkudir+"/",3,"model_new_",test_cases,where_test_starts,args.workdir+"/",args.datadir+"/",args.verbose,{11,51})
