#auxiliary functions used for the training and testing of our neural netwrok model
import os,shutil
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from keras import optimizers
from keras import models
from keras import layers
from keras.models import Model

from keras.layers import Conv2D, MaxPooling2D, Input, Flatten, Dropout, Dense
from keras import regularizers
from keras.preprocessing.image import ImageDataGenerator
from keras.constraints import max_norm
import numpy as np
from keras.callbacks import EarlyStopping, ModelCheckpoint

#paths required for label manipulation
path_labels_dir = "./labelsCSV"   #path to the labels directory
labels = path_labels_dir + "/labelsM.csv" #all the angles have the same labels (L,M,R)


#useful counters
source_size = 0
target_size = 0
validation_size = 0


def get_base_dirs(pkudir):
  """
  -----------------------------------------------------
  this function returns our base directories
  -----------------------------------------------------
  """

  directory_to_use = pkudir


  source_dir = os.path.join(directory_to_use, 'source') #source directory to be used for training
  validation_dir = os.path.join(directory_to_use, 'validation') #directory to be used for validation purposes
  target_dir = os.path.join(directory_to_use, 'target') #directory to be used for testing purposes

  return source_dir,validation_dir,target_dir


#local base directory creation
def __create_base_dirs(dirname,processed_actions):
  """
  -----------------------------------------------------
  this function creates our base directories
  -----------------------------------------------------
  """

  os.mkdir(dirname)
  for i in processed_actions:
      source_class_dirs = os.path.join(dirname, str(i)+'_action')
      if os.path.exists(source_class_dirs) == False:
          os.mkdir(source_class_dirs)
      else:
          shutil.rmtree(source_class_dirs)
          os.mkdir(source_class_dirs)



def make_base(processed_actions,pkudir):
  """
  --------------------------------------------------------------------------
  this function creates the directory containing the source and target data
  within this directory there exist directories corresponding to each one of the action classes
  --------------------------------------------------------------------------
  """

  directory_to_use = pkudir
  if os.path.exists(directory_to_use) == False:
      os.mkdir(directory_to_use)
  else:
      shutil.rmtree(directory_to_use)
      os.mkdir(directory_to_use)

  source_size=0
  validation_size =0
  target_size=0
  #training-validation-and test directories

  source_dir = os.path.join(directory_to_use, 'source') #source directory to be used for training
  validation_dir = os.path.join(directory_to_use, 'validation') #directory to be used for validation purposes
  target_dir = os.path.join(directory_to_use, 'target') #directory to be used for testing purposes


  __create_base_dirs(source_dir,processed_actions)
  __create_base_dirs(validation_dir,processed_actions)
  __create_base_dirs(target_dir,processed_actions)


def make_model_functional(classes):
  """
  ---------------------------------------------------
  this function defines our functional model
  ---------------------------------------------------
  """

  input_image = Input(shape = (159,75,3))
  first_layer_conv = Conv2D(32, (3,3),strides=(2,2), activation='relu',padding='valid',kernel_regularizer=regularizers.l2(0.001),kernel_constraint=max_norm(max_value=2))(input_image)
  #first_layer_pool = MaxPooling2D((2,2), strides=(2,2), padding='valid')(first_layer_conv)
  second_layer_conv = Conv2D(64, (3,3),strides=(2,2),  activation='relu',padding='valid',kernel_regularizer=regularizers.l2(0.001),kernel_constraint=max_norm(max_value=2))(first_layer_conv)
  #second_layer_pool = MaxPooling2D((2,2), strides=(2,2), padding='valid')(second_layer_conv)
  third_layer_conv = Conv2D(128, (3,3),strides=(2,2), activation='relu',padding='valid',kernel_regularizer=regularizers.l2(0.001),kernel_constraint=max_norm(max_value=2))(second_layer_conv)
  #third_layer_pool = MaxPooling2D((2,2), strides=(3,3), padding='valid')(third_layer_conv)

  #flatten
  flattened_layer = Flatten()(third_layer_conv)
  Dropout_layer = Dropout(0.55)(flattened_layer)
  Dense_layer_first = Dense(128, activation = 'relu')(Dropout_layer)
  output = Dense(classes, activation = 'softmax',)(Dense_layer_first)

  model = Model(inputs=input_image, outputs=output)
  model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
  return model


def make_model_sequential(my_model,classes):
  """
  ---------------------------------------------------------
  function that creates our model
  ---------------------------------------------------------
  """

  my_model.add(layers.Conv2D(32, (3, 3),padding='valid',kernel_regularizer=regularizers.l2(0.001),
  kernel_constraint=max_norm(max_value=2), activation='relu',input_shape=(159, 75, 3)))
  my_model.add(layers.MaxPooling2D((2, 2)))
  my_model.add(layers.Conv2D(64, (3, 3), activation='relu',padding='valid',kernel_regularizer=regularizers.l2(0.001),kernel_constraint=max_norm(max_value=2)))
  my_model.add(layers.MaxPooling2D((2, 2)))
  my_model.add(layers.Conv2D(128, (3, 3), activation='relu',padding='valid',kernel_regularizer=regularizers.l2(0.001),kernel_constraint=max_norm(max_value=2)))
  my_model.add(layers.MaxPooling2D((2, 2)))

  #flatten
  my_model.add(layers.Flatten())
  my_model.add(layers.Dropout(0.55))
  my_model.add(layers.Dense(128, activation='relu'))
  my_model.add(layers.Dense(classes, activation='softmax'))
  my_model.compile(loss='categorical_crossentropy',optimizer='rmsprop',metrics=['accuracy'])
  return my_model



def train_model(name,my_model,epochs,steps,batches,pkudir,noval=False):
  """
  ---------------------------------------------------------
  function used to train our model
  ---------------------------------------------------------
  """


  directory_to_use = pkudir

  source_dir = os.path.join(directory_to_use, 'source') #source directory to be used for training
  validation_dir = os.path.join(directory_to_use, 'validation') #directory to be used for validation purposes
  target_dir = os.path.join(directory_to_use, 'target') #directory to be used for testing purposes

  train_datagen = ImageDataGenerator(rescale=1./255)
  test_datagen = ImageDataGenerator(rescale=1./255)


  train_generator = train_datagen.flow_from_directory(source_dir,target_size=(159, 75),batch_size=batches,class_mode='categorical')


  if noval==True:
    early_stopping_callback = EarlyStopping(monitor='loss', patience=2)
    checkpoint_callback = ModelCheckpoint(name+'.h5', monitor='loss', verbose=1, save_best_only=True, mode='min')
    history = my_model.fit_generator(train_generator,steps_per_epoch=train_generator.samples/float(batches),epochs=epochs,shuffle=True,callbacks=[early_stopping_callback, checkpoint_callback])
  else:
    validation_generator = test_datagen.flow_from_directory(validation_dir,target_size=(159, 75),batch_size=batches,class_mode='categorical')
    early_stopping_callback = EarlyStopping(monitor='val_loss', patience=2)
    checkpoint_callback = ModelCheckpoint(name+'.h5', monitor='val_loss', verbose=1, save_best_only=True, mode='min')
    history = my_model.fit_generator(train_generator,steps_per_epoch=train_generator.samples/float(batches),epochs=epochs,validation_data=validation_generator,validation_steps=len(validation_generator), shuffle=True,callbacks=[early_stopping_callback, checkpoint_callback])

  my_model.save(name)
  return my_model




def test_model(name,my_model,num,run,verbose,pkudir):
  """
  -------------------------------------------------------
  function use to test our model
  -------------------------------------------------------
  """


  directory_to_use = pkudir

  source_dir = os.path.join(directory_to_use, 'source') #source directory to be used for training
  validation_dir = os.path.join(directory_to_use, 'validation') #directory to be used for validation purposes
  target_dir = os.path.join(directory_to_use, 'target') #directory to be used for testing purposes

  test_datagen = ImageDataGenerator(rescale=1./255)

  test_generator = test_datagen.flow_from_directory(target_dir,target_size=(159, 75),batch_size=32,class_mode='categorical')

  test_loss, test_acc = my_model.evaluate_generator(test_generator, steps=test_generator.samples/float(32))
  if verbose: print('test acc:', test_acc,'\ntest loss:',test_loss)

  string = "log_multi_method_version51_crossubject_crossview_" +str(run)
  string11="log_multi_method_version11_crossubject_crossview_" +str(run)
  if num == 51 : results = open(string,"a")
  else: results = open(string11,"a")

  results.write("percentages for the model %s are accuracy %f , loss %f \n" % (name,test_acc,test_loss))
  results.close()


def kind_of_rotation(image_name):
  """
  ------------------------------------------------------------
  function returning the kind of rotation of the certain image
  ------------------------------------------------------------
  """

  values = image_name.split("_")
  values1 = values[4].split(".")
  rotation = values1[0]
  return(int(rotation))




def get_individual_accuracies(my_model,size,num,run,verbose,pkudir):
  """
  ----------------------------------------------------
  function returning our individual model accuracies
  ----------------------------------------------------
  """

  directory_to_use = pkudir

  test_datagen = ImageDataGenerator(rescale=1./255)
  test_dir = os.path.join(directory_to_use, 'target')

  my_model.summary()

  test_generator = test_datagen.flow_from_directory(test_dir,target_size=(159, 75),batch_size=1,class_mode='categorical')

  filenames = test_generator.filenames

  predict_generator = test_datagen.flow_from_directory(
          test_dir,
          target_size=(159, 75),
          batch_size=1,
          class_mode=None,  # only data, no labels
          shuffle=False)  # keep data in same order as labels




  predict_generator.reset()
  predictions = my_model.predict_generator(predict_generator,verbose=1,steps=size )
  predictions = np.argmax(predictions, axis=-1)

  filenames = predict_generator.filenames
  filenames2 = []

  for f in filenames: filenames2.append(f.split("/")[1])


  true_positives0deg = 0
  true_positives45deg = 0
  true_positives_45deg = 0
  true_positives_90deg = 0
  true_positives90deg = 0


  label_map = list(predict_generator.class_indices.keys())
  label_map_int=[]
  #label_map = dict((v,k) for k,v in label_map.items())

  for i in range(0,len(label_map)):

      action_str = str(label_map[i])
      values = action_str.split('_')
      label_map_int.append(int(values[0]))




  y_pred = predictions	#predicted labels
  y_true = predict_generator.classes	#true labels

  y_ground_truth = []
  y_prediction = []

  #total = 7151 #51
  #total = 1502 #11
  for i in range(0,len(y_pred)):
      y_prediction.append( label_map_int[y_pred[i]] )

  if verbose: print(len(y_pred),len(y_true))
  for i in range(0,len(y_true)):
      y_ground_truth.append( label_map_int[y_true[i]])
  cc=0
  for i in range(0,len(y_prediction)):
      if y_prediction[i]==y_ground_truth[i]:
          rot = kind_of_rotation(filenames2[i])

          if rot==2: cc+=1
          if(rot == 2 or rot == 1 or rot == 3 ): true_positives0deg+=1
          elif(rot == 6 or rot==5 or rot==15): true_positives45deg+=1
          elif(rot == 7 or rot==9 or rot==12): true_positives_45deg+=1
          elif(rot==14  or rot==10 or rot==4): true_positives90deg+=1
          elif(rot == 11 or rot ==8 or rot==13): true_positives_90deg+=1
  if verbose:
    print(cc)
    print(true_positives0deg/total)
    print(true_positives45deg/total)
    print(true_positives_45deg/total)
    print(true_positives90deg/total)
    print(true_positives_90deg/total)
    print(true_positives0deg)
    print(true_positives45deg)
    print(true_positives_45deg)
    print(true_positives90deg)
    print(true_positives_90deg)

  string = "log_multi_method_version51_crossubject_crossview_" +str(run)
  string11="log_multi_method_version11_crossubject_crossview_" +str(run)

  if num == 51 : results = open(string,"a")
  else: results = open(string11,"a")

  results.write("---- case start -----\n")
  results.write("percentages for the model 1st test are %f \n" % (true_positives0deg/total))
  results.write("percentages for the model 2nd test are %f \n" % (true_positives45deg/total))
  results.write("percentages for the model 3d test are %f \n" % (true_positives_45deg/total))
  results.write("percentages for the model 4th test are %f \n" % (true_positives90deg/total))
  results.write("percentages for the model 5th test are %f \n" % (true_positives_90deg/total))
  results.write("---- case end -----\n")

  results.close()
