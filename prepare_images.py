import images as im
import argparse,os

parser = argparse.ArgumentParser()
parser.add_argument("-w","--workdir",default=".",
	help="state the working directory where the images will be created. Default directory is the current one")
parser.add_argument("-v","--verbose",default="False", help="provide an output",
                    action="store_true")
parser.add_argument("-d","--datadir",default=".", 
	help="state the directory where the action data are located. Default directory is the current one")
args = parser.parse_args()

if os.path.exists(args.datadir) == False: 
	print("the data directory you provided does not exist.\n Please provide an existing directory or create one")
	exit()

if os.path.exists(args.workdir) == False and args.workdir not in os.getcwd(): 
	print("the working directory you provided does not exist.\n It will be created")
	os.mkdir(args.workdir)


for theta in range(1,16):
    theta_set.append(theta)
    theta_set.append(theta+0.5)

cases = ["Left","Middle","Right"]    

for theta in theta_set:
    thetaCase = angle_id+"by"+str(theta)
    cases.append(thetaCase)

for case in cases:#,"Leftby90","Leftby45","Middleby45","Middleby-45","Rightby-90","Rightby-45","Middleby90",
                                      #  "Middleby-90","Leftby-45","Leftby-90"
                                       # "Rightby90","Rightby45"}:

  im.create_action_image(case,args.workdir + "/",args.verbose,args.datadir +"/")
