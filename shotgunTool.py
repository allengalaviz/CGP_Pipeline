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

option = raw_input("What do you want to upload?\n->Asset\n->Shot\n").lower()
inputType = validateType(option)
ID = raw_input("Type the ID of the %s: " %inputType)
goodID = validateID(ID)
shotgunInfo = validateIDShotgun(goodID)
checkVersionsShotgun(shotgunInfo)

print "Data correct"
time.sleep(10)