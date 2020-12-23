import os,sys,io,shutil,csv
from decimal import Decimal
#defining and compiling my model
from keras import optimizers
from keras import models
from keras import layers
from keras import regularizers
from keras.preprocessing.image import ImageDataGenerator
from keras.constraints import max_norm
from keras.preprocessing.image import ImageDataGenerator
import numpy as np
from keras.models import load_model
from keras.layers import Flatten, Dense, Dropout
from keras.layers import Input, Concatenate, Conv2D, Flatten, Dense, Convolution2D, Activation
from keras.models import Model, Sequential
import argparse



base_dir = "./my_base"

#check all the different rotation cases
all_the_probability_scores = []
all_the_predicted_actions = []
test_datagen1 = ImageDataGenerator(rescale=1./255)

test_dir = {

	0: "./testRight-2",#"./testMiddle-2",#"./testLeft-2",#"./testMiddle",#"./testRight",#"./testLeft", 
	1: "./testRighttoMiddle-2",#"./testMiddle90-2",#"./testLefttoRight-2",#"./testMiddle90",#"./testRighttoMiddle",#"./testLefttoRight", 
	2: "./testRighttoLeft-2",#"./testMiddle-90-2",#"./testLefttoMiddle-2",#"./testMiddle-90",#"./testRighttoLeft",#"./testLefttoMiddle"
	3: "./testRightby45-2",#"./testMiddletoLeft-2",#"./testLeftby-45-2",#"./testMiddletoLeft",#"./testRightby45",#"./testLeftby-45", 
	4: "./testRightby90-2",#"./testMiddletoRight-2",#"./testLeftby-90-2",#"./testMiddletoRight",#"./testRightby90",#"./testLeftby-90", 

}

for test in range(0,5):


	#test_dir = os.path.join(base_dir, 'test')

	test_generator = test_datagen1.flow_from_directory(test_dir.get(test,"nothing"),target_size=(159, 75),batch_size=32,class_mode='categorical',shuffle=False)

	batches = 32
	num_classes = 51
	my_model = load_model('./modelsRotated/modelMiddle11.h5')



	#history = model.fit_generator(train_generator,steps_per_epoch=73,epochs=3)



	a = my_model.predict_generator(test_generator, steps=test_generator.samples/float(batches))
	y_true = test_generator.classes

	
	#print(a,len(a[0]),len(a))
	#to opio tha to kanoume gia ta ksexorista actions
	#episis kai gia ola ta diaforetika angles
	actions_pred = []
	probabilityScore = []
	temp = []
	for i in range(0,1502): #1502 for 11 and 7151 for 51
		temp = list(a[i])
		probabilityScore.append(max(a[i]))
		actions_pred.append(temp.index(max(a[i])))


	all_the_predicted_actions.append(actions_pred)
	all_the_probability_scores.append(probabilityScore)
	#print(probabilityScore[0]," ",actions_pred[0]," ", len(actions_pred))
	#my_model.summary()


predicted=[]
for score in range(0,len(all_the_probability_scores[0])):
	max_prob = -1
	index_of_max =- 1
	for test in range(0,5):
		if max_prob < all_the_probability_scores[test][score]:
			max_prob = all_the_probability_scores[test][score]
			index_of_max = test

	predicted.append(all_the_predicted_actions[index_of_max][score])

	

for test in range(0,5):
	number_of_correct_predictions=0
	for i in range(0,len(all_the_predicted_actions[test])):
		if all_the_predicted_actions[test][i] == y_true[i]:
			number_of_correct_predictions+=1

	accuracy = number_of_correct_predictions / len(predicted)
	print ("accuracy for test no ",test," is ",accuracy)


number_of_correct_predictions=0
for predictions in range(0,len(predicted)):
	if predicted[predictions] == y_true[predictions]:	#if predicted labels correspond to the true_labels
		number_of_correct_predictions+=1

accuracy = number_of_correct_predictions / len(predicted)		
print("total accuracy is ",accuracy)



























