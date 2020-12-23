# AntonisActions

Code for human action recognition developed by Antonis Papadakis

To this point this repository includes code used for human action recognition on the PKU-MMD dataset. We used a CNN for the recognition purposes.

when using the create_actions.py make sure you use the original skeleton and
label data provided by the PKU_MMD dataset.

------------------------------------------------------------------------------------------------------------

Below you can find information about each one of the code files provided 

ATTENTION when inputting directories in code take CARE!!: 

input directory as such ./mydocs/labelsCSV not as ./mydocs/labelsCSV/



------------------------------action_recognition.py---------------------------------------------------------

this script is used to train an action recognition model

flags and their use:

-w == -workdir [enter the directory where the action image dataset (e.g. dst_images) is located]-- optional with default value the current directory

-d == -datadir [state the directory where the skeletal data are located (actions)] --optional with current as default value

-l == -labeldir [state the directory where the label data are located IMPORTANT when we need different actions from each angle]--optional with current as default value

-p == -pkudir [state the directory where the source and target dirs will be created]--optional with current as default value

-testCases [state the image angles used for train and testing (e.g -testCases Left Right] --mandatory

-whereTestStarts [state the indentation of the testCases]--mandatory 

example of use :-testCases Left Right -whereTestStarts 1 means that Right will be used as target (test) and Left as source (train) since index of Left is 0 and index of Right is 1


also this is correct too: -testCases Left Right -testCases Left Leftby45 Leftby90 Right -whereTestStarts 1 3

-v == verbose

------------------------------create_actions.py--------------------------------------------------------------

creates the initial csv files using raw PKU_MMD data

flags:

-w == workdir

-d == datadir

-l == labeldir


------------------------------create_different_frame_tests.py-------------------------------------------------

this script can create the source and target directories if used with the -dirs flag and can train an action recognition model if used with the train flag

flags and their use:

-w == -workdir [enter the directory where the action image dataset (e.g. dst_images) is located]-- optional with default value the current directory

-d == -datadir [state the directory where the skeletal data are located (actions)] --optional with current as default value

-l == -labeldir [state the directory where the label data are located IMPORTANT when we need different actions from each angle]--optional with current as default value

-p == -pkudir [state the directory where the source and target dirs will be created]--optional with current as default value

-testCases [state the image angles used for train and testing (e.g -testCases Left Right] --mandatory

-whereTestStarts [state the indentation of the testCases]--mandatory 

example of use :-testCases Left Right -whereTestStarts 1 means that Right will be used as target (test) and Left as source (train) since index of Left is 0 and index of Right is 1


also this is correct too: -testCases Left Right -testCases Left Leftby45 Leftby90 Right -whereTestStarts 1 3

-v == verbose

-dirs == -directories

-train == -training

-noval == -novalidation if you dont want data to be added to the validation directory -- e.g. for domain adaptation


------------------------------create_tests.py-----------------------------------------------------------------



similar use with create_different_frame_tests.py without the novalidation option.


------------------------------prepare_images.py---------------------------------------------------------------

script to create action images using the dst transform from the actions of the PKU_MMD dataset. Adictionary is provided in the code with the angle cases.

-----------------------------neural_network_functions.py------------------------------------------------------

code with all the functions needed for the creation, train and testing of our supervised learning method for human action recognition with neural networks.

-----------------------------transformation_directories.py----------------------------------------------------

code for the manipulation of the neccesary directories


-------------------------------images.py----------------------------------------------------------------------

code that executes the transformation from signal to action image

-------------------------------Rotate.py----------------------------------------------------------------------

code that executes all the rotation transformations and creates all the action directories from raw PKU data

-------------------------------train_model.py-----------------------------------------------------------------

code that calls the neural network functions






























