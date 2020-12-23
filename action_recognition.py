import train_model as trm
import argparse,os

#1st variable is equal to the number of tests you want to run
#the second is a set with number of classes you would like to test
#the set's possible values are 11 or 51

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
print(args.directories)
if args.training==True: trm.train(args.pkudir +"/",3,"model_new_",test_cases,where_test_starts,args.workdir + "/",args.datadir + "/",args.verbose,{11,51})

