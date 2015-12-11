from psychopy import visual,event,core,gui
import re,csv,random
from myFirstLibrary import *


"""

Future Tasks:

Primary
-finished		
		
secondary tasks
-expand userVars to include age, gender, prior language experience.
-perhaps object definitions should be made to link rectangle, text and draw command.
-ERROR CHECKING- make sure participants can't click through the experiment.
-better dynamic updating for positioning of objects
-dynamic size of passageBox according to text size.
"""

#import generated text content
with open('read1.csv', 'rb') as f:
	reader2=csv.reader(f,delimiter='\t')
	compText=list(reader2)

with open('read2.csv', 'rb') as f:
	reader=csv.reader(f,delimiter='\t')
	paragraphs=list(reader)
	

#user data, generate output fileName
nameTest=False
while nameTest==False:
	userVar = {'part':'Participant number'}
	dlg = gui.DlgFromDict(userVar)
	userVar['part']
	partNum= userVar['part']
	# targetSentence.append(sentences[nameTyped])
	if len(partNum)<3:
		popupError("Please enter your full participant number")
	elif  not 100<int(partNum)<150:
		popupError("Please enter a valid participant number")	
	else:
		nameTest=True

outputFile = open('subj%s.csv' % (str(partNum)),'w')

#global settings
win = visual.Window([1200,800],color="black", units='pix')
timer=core.Clock()

#text variables

for question in compText:
	question[2]+='\n'+question[3]+'\n'+question[4]+'\n'+question[5]
	
setList = [x[0] for x in paragraphs]
newParagraph=set(setList)

#instructions strings
inst=["Welcome, Subject %s, to this study on reading. You will complete two different kinds of tasks, taking approximately 15 minutes. Press 'b' when ready to read about task one." % (str(partNum)),
"You are about to see a series of short passages followed by a question and multiple choice answers. Please read the passage and answer the question with the corresponding letter on your keyboard as quickly and accurately as possible. \nPress [b] when you're ready to begin.",
"Press [b] to advance.",
"Second task\n\nYou will see three short paragraphs each requiring a series of judgments about them. After reading a paragraph, advance to the next screen. Identify, with f or j, which of the bottom two sentences is most clearly a consequence of the top sentence.",
"This concludes the study. Please let the study person know you are finished. Thank you for your participation.\n\n\n[q to exit]",
"This concludes the study. Please let the study person know you are finished. Thank you for your participation.\n\n\n[q to exit]"]
comp2="Identify, with f or j, which of the bottom two sentences is most clearly a consequence of the top sentence."

#reading comprehension 1: visual objects
mainText = visual.TextStim(win,text=compText[0][0], wrapWidth=600, height=20, color='white',pos=[-300,140],alignHoriz='left', alignVert='top')

questionText = visual.TextStim(win,text=compText[0][1], wrapWidth=600, height=20, color='white',pos=[-300,0],alignHoriz='left', alignVert='top')

answersText = visual.TextStim(win,text=compText[0][2], wrapWidth=600, height=20, color='white',pos=[-300,-50],alignHoriz='left', alignVert='top')

instText = visual.TextStim(win,text= inst[0], wrapWidth=600, height=20, color='white',pos=[-280,300],alignHoriz='left', alignVert='top')

	
#reading comprehension 2: visual objects
passagePos=[-380,75]
passageSize=[725,1240]
passageText=paragraphs[0][0]

targetPos=[150,125]
leftPos=[-25,-100]
rightPos=[325,-100]
textSize=[520,320] 
textWrap=((textSize[0]-30)/2)

#text objects
passageText = visual.TextStim(win,text=passageText, wrapWidth=330, height=20, color='white',pos=[passagePos[0],(passagePos[1]+300)],alignHoriz='center', alignVert='top')


targetText = visual.TextStim(win,text=paragraphs[0][1], wrapWidth=textWrap, height=20, color='white',pos=[targetPos[0],(targetPos[1]+80)],alignHoriz='center', alignVert='top')

leftText = visual.TextStim(win,text=paragraphs[0][2], wrapWidth=textWrap, height=20, color='white',pos=[leftPos[0],(leftPos[1]+80)],alignHoriz='center', alignVert='top')

rightText = visual.TextStim(win,text=paragraphs[0][3], wrapWidth=textWrap, height=20, color='white',pos=[rightPos[0],(rightPos[1]+80)],alignHoriz='center', alignVert='top')


#box objects
targetBox = visual.Rect(win,lineColor="white",size=textSize,pos=targetPos)
leftBox = visual.Rect(win,lineColor="white",size=textSize,pos=leftPos)
rightBox = visual.Rect(win,lineColor="white",size=textSize,pos=rightPos)
passageBox = visual.Rect(win,lineColor="white",size=passageSize,pos=passagePos)

#function to streamline visual object rendering
def drawObjects(objectsToDraw):
	for visObj in objectsToDraw:
		visObj.draw()

############
#EXPERIMENT#

#optional headerFile
#headerFile = open(header,'w')
#head=["partNum","trial","targetStim","leftStim","rightStim","leftVal","rightVal","rt","resp","cResp","accuracy","value","margin"]
#writeToFile(headerFile,head,writeNewLine=True)


#Introduction
instText.draw()
win.flip()
event.waitKeys(keyList=['b'])

#Reading Comprehension 1:Instructions and Task

instText.setText(inst[1])
instText.draw()
win.flip()
event.waitKeys(keyList=['b'])


trial=0
instText.setText(inst[2])
reading1Objects=[mainText,questionText,answersText]

for each in compText:	
	#draw reading test and question
	mainText.setText(each[0]+"\n\nPress 'f' for question.")
	questionText.setText(each[1])
	answersText.setText(each[2])

	mainText.draw()
	win.flip()
	event.waitKeys(keyList=['f'])
	
	mainText.setText(each[0])
	drawObjects(reading1Objects)
	
	timer.reset()
	win.flip()
	key=event.waitKeys(keyList=['a','b','c','d'])[0]

	#runtime Vars
	rt=timer.getTime()
	if each[6]==key:
		answer='correct'
	else:
		answer='incorrect'
	targetStim=each[1][0:7]
	forFile=[partNum,(str(trial).zfill(3)),targetStim,"na","na","na","na",rt,key,each[6],answer,"na","na"]
	writeToFile(outputFile,forFile,writeNewLine=True)

	
	trial+=1
	instText.draw()
	win.flip()
	event.waitKeys(keyList=['b'])	

	
#Reading Comprehension 2: Instructions and Task

instText.setText(inst[3])
instText.draw()
win.flip()
event.waitKeys(keyList=['f'])


trial=100
questionText.setPos([-100,300])
questionText.setText(comp2)
readingObjects=[questionText,passageText,passageBox]
trialObjects=[questionText,passageText,targetText,leftText,rightText,passageBox,targetBox,leftBox,rightBox]

for each in paragraphs:
	keyDict={'f':"left",'j':"right"}
	keyValue={'f':float(each[4]),'j':float(each[5])}
	print keyValue['f'],keyValue['j']
	if each[0] in newParagraph:
		paragraphRead=each[0]
		passageText.setText(paragraphRead)
		newParagraph.remove(each[0])
		questionText.setText("Read the passage to the left.\n\nPress ['f' or 'j'] when finished.")
		
		drawObjects(readingObjects)

	else:
		passageText.setText(each[0])
		questionText.setText("Select the bottom sentence that best supports the top sentence.")
		targetText.setText(each[1])
		leftText.setText(each[2])
		rightText.setText(each[3])
		
		drawObjects(trialObjects)		

	timer.reset()
	win.flip()
	key=event.waitKeys(keyList=['f','j'])[0]

	
	#runtime Vars
	rt=timer.getTime()
	if each[4]==each[5]:
		cresp='both'
	elif each[4]>each[5]:
		cresp,ckey="left",'f'
	else:
		cresp,ckey="right",'j'
	if keyDict[key]!=cresp:
		accuracy='incorrect'
	else:
		accuracy='correct'
	targetStim=each[1][0:7]
	leftStim=each[2][0:7]
	rightStim=each[3][0:7]
	margin=keyValue[key]-keyValue[ckey]
	forFile=[partNum,(str(trial).zfill(3)),targetStim,leftStim,rightStim,keyValue['f'],keyValue['j'],rt,keyDict[key],cresp,accuracy,keyValue[key],margin]
	writeToFile(outputFile,forFile,writeNewLine=True)

	trial+=1

#De-brief
instText.setText(inst[5])
instText.draw()
win.flip()
event.waitKeys(keyList=['q'])
	
outputFile.close()
