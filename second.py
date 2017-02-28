import csv
import random
import math
def loadcsv(filename):
	lines=csv.reader(open(filename,"rb"))
	dataset=list(lines)
	for i in range(len(dataset)):
			dataset[i]=[float(x)for x in dataset[i]]
	return dataset
filename="/home/sukhad/diabetes.csv"
dataset=loadcsv(filename)


def splitDataset(dataset,splitratio):
	trainsize=int(len(dataset)*splitratio)
	trainset=[]
	copy=list(dataset)
	while(len(trainset)<trainsize):
		index=random.randrange(len(copy))
		trainset.append(copy.pop(index))
	return trainset,copy

def seperateByClass(dataset):
	seperated={}
	for i in range(len(dataset)):
		vector=dataset[i]
		if vector[-1] not in seperated:
			seperated[vector[-1]]=[]
		seperated[vector[-1]].append(vector)
	return seperated
def mean(numbers):
	sum=0
	for i in range(len(numbers)):
		sum=sum+numbers[i]
	mean1=sum/len(numbers);
	return mean1

def stddev(numbers):
	mean1=mean(numbers)
	sum=0
	for i in range(len(numbers)):
		sum=sum+(numbers[i]-mean1)*(numbers[i]-mean1)
	len1=float(len(numbers)-1)
	var=sum/len1
	std=math.sqrt(var)
	return std

def summarize(dataset):
	summaries=[(mean(attribute),stddev(attribute)) for attribute in zip(*dataset)]
	del summaries[-1]
	return summaries
def summarizeByClass(dataset):
	seperated={}
	seperated=seperateByClass(dataset)
	summaries={}
	for classvalue,instances in seperated.iteritems():
		summaries[classvalue]=summarize(instances)
	return summaries
def calculateProbability(x,mean,stddev):
	exponent=math.exp(-((math.pow(x-mean,2))/(2*stddev*stddev)))
	return (1.0/(math.sqrt(math.pi*2)*stddev)*exponent)
def classprob(summaries,input):
	probabilities={}
	for classvalue,classsum in summaries.iteritems():
			probabilities[classvalue]=1
			for i in range(len(classsum)):
				mean,stddev=classsum[i]
				x=input[i]
				probabilities[classvalue]*=calculateProbability(x,mean,stddev)
	return probabilities

def predict(summaries,inputVector):
	prob=classprob(summaries,inputVector)
	bestlabel,bestProb=None,-1
	for classvalue,probability in prob.iteritems():
		if bestlabel is None or probability>bestProb:
			bestlabel=classvalue
			bestProb=probability
	return bestlabel
def getPredictions(summaries,testSet):
	predictions=[]
	for i in range (len(testSet)):
		result=predict(summaries,testSet[i])
		predictions.append(result)
	return predictions
def getAccuracy(testSet,predictions):
	correct=0
	for i in range(len(testSet)):
		if testSet[i][-1]==predictions[i]:
			correct+=1
	return (correct/float(len(predictions)))*100.0

def main():
	filename="filename"
	split=0.67
	dataset=loadcsv(filename)
	train,test=splitDataset(dataset,split)
	summ=summarizeByClass(train)
	predictions=getPredictions(summ,test)
	accuracy=getAccuracy(test,predictions)
	print accuracy
main()
