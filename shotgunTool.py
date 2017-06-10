import os, sys
from shotgun_api3 import Shotgun
import os.path
import time

sg = Shotgun("https://upgdl.shotgunstudio.com", "ShotgunTool_Script", "b2d1623aecc4ac178f384f10db7a3fa590eb2f6afb45d73f5797ee8f46c3ef10")

def validateType(userInputType):
	validationType = False
	while validationType == False:
		if userInputType == 'asset':
			return "Asset"
		elif userInputType == 'shot':
			return "Shot"
		else:
			userInputType = raw_input("ERROR, Invalid data. Try again\nWhat do you want to upload?\n->Asset\n->Shot\n").lower()

def validateID(userInputID):
	validationNumber = False
	while validationNumber == False:
		try:
			userInputID = int(userInputID)
			validationNumber = True
		except:
			userInputID = raw_input("ERROR! The Id must be a number")

def validateIDShotgun(validatedID):
	shotgunValidation = False
	shotgunFile = sg.find_one(inputType, [["id", "is", validateID]], ["id", "code"])
	

option = raw_input("What do you want to upload?\n->Asset\n->Shot\n").lower()
inputType = validateType(option)
ID = raw_input("Type the ID of the %s: " %inputType)
validateID(ID)

print "Data correct"
time.sleep(5)