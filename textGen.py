import os, csv, re, itertools,random
from myFirstLibrary import *
"""Things to think about:

future tasks

solve puzzle of creating upperbound limit for iterables.
-solve GUI for text structure encoding
-build error protection for above.
-implement algorithm for item-pair selection.
-more robust text scrubbing/stripping.
-improve readability of labels (especially > line 89)
"""


#open read and write files
#1st textGen
with open('readInput1.csv', 'rb') as f:
	reader=csv.reader(f,delimiter='\t')
	compText=list(reader)

#2nd textGen
with open('readInput2.csv', 'rb') as f:
	reader=csv.reader(f,delimiter='\n')
	paragraphs=list(reader)

#write files
rCompFile = open('read1.csv','w')
outputFile = open('read2.csv','w')	


#text generation
#1st textGen
random.shuffle(compText)
for each in compText:
	writeToFile(rCompFile,each,writeNewLine=True) 
rCompFile.close()


#2nd textGen
for i, curParagraph in enumerate(paragraphs):
	thesis=[]
	#cleans up sentences
	paragraph=str(curParagraph[0]).replace("\"","").replace("[","").replace(",","")
	sentences = re.split(r' *[\.\?!][\'"\)\]]* *', str(paragraph))
	emptyItm=sentences.pop(-1)
	targetValues=[0]*len(sentences)

	#pop-up entry records target sentence
	textEval= "\n\nPlease enter the number corresponding to the target sentence for paragraph "+str(i)+":\n\n"
	for index,each in enumerate(sentences):
		textEval+= " \n"+str(index)+"- "+str(each)
	print textEval
		
	targetTest=False
	while targetTest==False:
		userVar = {'targetSent':'Enter your value'}
		dlg = gui.DlgFromDict(userVar)
		userVar['targetSent']
		targetSent= int(userVar['targetSent'])
		if targetSent in range(len(sentences)):
			targetTest=True
		else:
			popupError("Index value is out of range.")
	print "\n\n\nNow enter indexes of sentence dependencies. enter 'x' in the first box when finished.\n\n"
	dependent=01
	dependSet=[]
	indices=[]
	while not dependent=="x":
		userVar = {'dependent':'dependent','parent':'parent'}
		dlg = gui.DlgFromDict(userVar)
		dependent,parent= str(userVar['dependent']),str(userVar['parent'])
		try:
			dependSet.append((sentences[int(dependent)],sentences[int(parent)]))
			indices.append((dependent,parent))
			print indices
		except:
			pass
	print dependSet
	
	#Here's the nifty efficient wt. adjuster tool. I saw something like this in looking at how LSA networks are programmed.
	dependWt=-.5
	parentWt=1
	for (dependent,parent) in indices:
		targetValues[int(dependent)]+=dependWt
		targetValues[int(parent)]+=parentWt

	print targetValues
	
	#generate combinations of sentences
	fullSentences=sentences
	thesis=sentences.pop(targetSent)
	iterations= list(itertools.combinations(sentences, 2))
	fullset=[(thesis,a,b) for (a,b) in iterations]

	random.shuffle(fullset)
	targetSet=fullset[0:(len(sentences)+4)]
	print "len sentences"+str(len(sentences))
	print "len targetSet"+str(len(targetSet))
	
	#append values for each sentence in pair	
	for (a,b,c) in targetSet:
		bValue=targetValues[fullSentences.index(b)]
		cValue=targetValues[fullSentences.index(c)]
		print (bValue,cValue)
		writeToFile(outputFile,[paragraph,a,b,c,bValue,cValue],writeNewLine=True)

outputFile.close()
