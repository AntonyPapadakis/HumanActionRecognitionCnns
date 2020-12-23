import argparse,os
import RotateAugment as rot

"""this script is used to create the augmented dataset with all the rotated and 
non-rotated actions"""

parser = argparse.ArgumentParser()
parser.add_argument("-w","--workdir",default=".",
	help="state the working directory where the images will be created. Default directory is the current one")
parser.add_argument("-d","--datadir",default=".", 
	help="state the directory where the skeletal data are located from the PKU-MMD dataset. Default directory is the current one")
parser.add_argument("-l","--labeldir",default=".", 
	help="state the directory where the label data are located from the PKU-MMD dataset. Default directory is the current one")
args = parser.parse_args()


if os.path.exists(args.datadir) == False and args.datadir!="current" and args.datadir!=".." and args.datadir!=".":
	print("the data directory you provided does not exist.\n Please provide an existing directory or create one")
	exit()
if os.path.exists(args.labeldir) == False: 
	print("the label directory you provided does not exist.\n Please provide an existing directory or create one")
	exit()
if os.path.exists(args.workdir) == False and args.workdir not in os.getcwd(): 
	print("the working directory you provided does not exist.\n It will be created")
	os.mkdir(args.workdir)

rot.rotate(args.datadir + '/',args.labeldir+'/',args.workdir+'/')	

