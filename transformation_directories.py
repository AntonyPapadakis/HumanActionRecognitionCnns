import os,shutil

def create_dirs_angles(camera_case,workdir):
  """
  -------------------------------------------------------------------
  this function creates or reinitializes the directories required for
  the action image creation
  -------------------------------------------------------------------
  """

  suffix = camera_case
  if workdir=="current" or workdir in os.getcwd():
    workdir = "./"

  if os.path.exists(workdir+"afterinterpolation_" + suffix) == False: os.mkdir(workdir+"afterinterpolation_" + suffix)
  else:
      shutil.rmtree(workdir+"afterinterpolation_" + suffix)
      os.mkdir(workdir+"afterinterpolation_" + suffix)

  if os.path.exists(workdir+"dstimages_" + suffix) == False: os.mkdir(workdir+"dstimages_" + suffix)
  else:
      shutil.rmtree(workdir+"dstimages_" + suffix)
      os.mkdir(workdir+"dstimages_" + suffix)


def get_values_dirs(camera_case,workdir,datadir,model_name = "no_model_"):
  """
  -------------------------------------------------------------------
  this function returns the directory names needed to perform either the
  action image cretion or the training of our model
  -------------------------------------------------------------------
  """

  if workdir=="current" or workdir in os.getcwd():
    workdir = "./"

  if datadir=="current" or datadir in os.getcwd():
    datadir = "./"


  suffix = camera_case
  action_angle = datadir + 'actions' + suffix+'/'
  afterinterpolation = workdir + 'afterinterpolation_'+ suffix+'/'
  image_directory = workdir + 'dstimages_'+ suffix+'/'
  model_name += suffix

  print(image_directory)

  if os.path.exists(image_directory) == False:
      print ("----------- ERROR ------------- \n THERE IS NO SUCH IMAGE DIRECTORY\n please create one to precede with training \n")
      exit()

  return image_directory,model_name,afterinterpolation,action_angle
