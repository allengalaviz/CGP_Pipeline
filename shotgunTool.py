import os, sys
from shotgun_api3 import Shotgun
import os.path
import time
from pprint import pprint

global inputType, goodID, projectID, goodProjectID, savedVersions

codeToUpload = None

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
			return userInputID
		except:
			userInputID = raw_input("ERROR! The Id must be a number\n")

def validateIDShotgun(validatedID):
	shotgunValidation = False
	while shotgunValidation == False:
		try:
			shotgunFile = sg.find_one(inputType, [["id", "is", validatedID]], ["id", "code"])
		except Exception as e:
			print e
		if shotgunFile == None:
			newID = raw_input("No %s founded in the project, try another ID:\n" %inputType)
			try:
				validatedID = validateID(newID)
			except Exception as e:
				print e 
		else:
			print "The %s founded name is: %s \n" %(inputType, shotgunFile['code'])
			return shotgunFile


	print 'Uploaded succesfully'

def checkVersionsShotgun():
	global savedVersions, codeToUpload
	fields = ['id', 'code']
	filters = [['entity', 'is', {'type': inputType, 'id': goodID}]]
	versions = sg.find("Version", filters, fields)
	savedVersions = versions
	print "The versions in this %s are:" %inputType
	for v in versions:
		print 'version: %s \nID: %d' %(v['code'], v['id'])

def asignName(inputName):
	global savedVersions, codeToUpload
	for v in savedVersions:
		if inputName.lower() in v['code'].lower():
			codeToUpload = v['code']
	if codeToUpload == None:
		codeToUpload = inputName + "_v001"
		updateContent(goodID, codeToUpload, inputType)
	else:
		codeToUpload = codeToUpload[:len(codeToUpload) - 4] + ('_v%03d' %(int(codeToUpload[len(codeToUpload) - 3:])+ 1))
		updateContent(goodID, codeToUpload, inputType)

def createContent(id, code, taskType):
    data = {'project': {"type": "Project","id": id}, 'code': code, 'description': 'Open on a beautiful field with fuzzy bunnies', 'sg_status_list': 'ip'}
    result = sg.create(taskType, data)
    pprint(result)
    print "The id of the %s is %d." % (result['type'], result['id'])

def createVersion(inType, ID, code, actionID, mediaPath, description):
	data = { 'project': {'type': 'Project','id': ID}, 'code': code, 'description': description, 'sg_status_list': 'rev', 'entity': {'type': inType, 'id': actionID}}
	result = sg.create('Version', data)
	uploadContent(result['id'], mediaPath)

def deleteContent(inpType, inputID):
	result = sg.delete(inpType, inputID)
	print 'The %s has been deleted succesfully' %inpType

def updateContent(contentID, code, inputType):
	data = {'code': code, 'description': 'Updating...', 'sg_status_list': 'ip'}
	result = sg.update(inputType, contentID, data)

def uploadContent(ID, mediaPath):
	print mediaPath
	result = sg.upload("Version", ID, mediaPath, field_name = "sg_uploaded_movie", display_name = "Latest QT")

#UPLOAD CONTENT
'''option = raw_input("Where do you want to upload your video?\n-> Asset\n-> Shot\n").lower()
inputType = validateType(option)
ID = raw_input("What's the version's ID of the %s:\n" %inputType)
goodID = validateID(ID)
#mediaFile ='/Users/allengalaviz/Desktop/popcornrender.mov'
checkVersionsShotgun()
versionID = raw_input("What's the ID of the version where you want to upload your video:\n")
goodVersionID = validateID(versionID)
try:
	uploadContent(goodVersionID, "c:\\Users\\allengalaviz\\Desktop\\popcornrender.mov")
except Exception as e:
	print e '''


#ASIGN NAME
'''option = raw_input("What you want to upload?\n-> Asset\n-> Shot\n").lower()
inputType = validateType(option)
ID = raw_input("What's the ID of the %s:\n" %inputType)
goodID = validateID(ID)
shotgunInfo = validateIDShotgun(goodID)
checkVersionsShotgun()
Name = asignName(raw_input("\nWhat's the name to asign to your %s \n" %inputType))
print codeToUpload'''

#CREATE CONTENT
'''projectName = raw_input("What's the name of the project you want to create a shot in:\n")
projectID = raw_input("What's the ID of %s:\n" %projectName)
goodID = validateID(projectID)
option = raw_input("What do you want to create?\n-> Asset\n-> Shot\n").lower()
inputType = validateType(option)
code = raw_input("What's the name of the %s:\n" %inputType)
createContent(goodID, code, inputType)'''

#CREATE VERSION
'''projectName = raw_input("What's the name of the project you want to create a shot in:\n")
projectID = raw_input("What's the ID of %s:\n" %projectName)
goodProjectID = validateID(projectID)
option = raw_input("Where do you want to create a new version?\n-> Asset\n-> Shot\n").lower()
inputType = validateType(option)
ID = raw_input("What is the Id of the %s:\n" %inputType)
goodID = validateID(ID)
code = raw_input("What is the version's name of the %s:\n" %inputType)
mediaFile = "/Users/allengalaviz/Documents/[EFECTOS VISUALES]/Particulas y Destruccion/popcornrender.mov"
desc = raw_input("\nType the description:\n")
createVersion(inputType, goodProjectID, code, goodID, mediaFile, desc)'''

#DELETE CONTENT
option = raw_input("What do you want to delete?\n-> Asset\n-> Shot\n").lower()
inputType = validateType(option)
ID = raw_input("What's the ID of the %s:\n" %inputType)
goodID = validateID(ID)
deleteContent(inputType, goodID)

print "Data correct"
time.sleep(10)