#MULTINOMIAL NAIVE BAYES classifier
from __future__ import division
import glob


#learn from enron1 and enron2
#predict on enron3

spam_mess_count=0
ham_mess_count=0
spam_word_count=0
ham_word_count=0
total_no_of_words=0
data={"bow":{}}
bag_of_words=data['bow']

def learning(sentence,mess_type):
	global spam_mess_count,ham_mess_count,spam_word_count,ham_word_count,total_no_of_words,bag_of_words
 
	words=sentence.split()
	spam_mess_count+=(mess_type)
	ham_mess_count+=(1-mess_type)
	for word in words:
		spam_word_count+=(mess_type)
		ham_word_count+=(1-mess_type)
		try:
			bag_of_words[word][mess_type]+=1
			
		except KeyError:
			bag_of_words[word]=[1-mess_type,mess_type]
			
		
def prediction(sentence):
	#finding priori
	global spam_mess_count,ham_mess_count,spam_word_count,ham_word_count,total_no_of_words,bag_of_words
	#print "spam_mess_count: ",spam_mess_count,"ham_mess_count: ",ham_mess_count
	spam_priori=(spam_mess_count/(ham_mess_count+spam_mess_count))			
	ham_priori=(ham_mess_count/(ham_mess_count+spam_mess_count))		
	#print "spam_priori: ",spam_priori,"ham_priori: ",ham_priori

	p_spam=1
	p_ham=1
	#print "probs"
	#print p_ham,p_spam
	words=sentence.split()
	for word in words:
		yo=0
		if(word in data['bow']):
			p_ham*=(1+bag_of_words[word][0])/(ham_word_count+len(data['bow']))
			p_ham/=(1+bag_of_words[word][1])/(spam_word_count+len(data['bow']))
			p_spam*=(1+bag_of_words[word][1])/(spam_word_count+len(data['bow']))
			#print "probs"
			#print p_ham,p_spam

	p_ham*=ham_priori
	p_ham/=spam_priori	
	p_spam*=spam_priori
	#percent_ham=p_ham/(p_ham+p_spam)
	#percent_spam=p_spam/(p_ham+p_spam)
	#print "---------------------------------------------------"
	#
	#print "ham/spam (ratio)", p_ham
	#print "---------------------------------------------------"
	if (p_ham>1):
		return 0	#ham
	else:
		return 1	#spam

learn_doc_count=0

for z in glob.glob("/home/sid/spam_project/enron1/ham/*.txt"):
	fname=z
	text_file=open(fname,"r")
	x=text_file.read()
	learning(x,0)
	learn_doc_count+=1
for z in glob.glob("/home/sid/spam_project/enron2/ham/*.txt"):
	fname=z
	text_file=open(fname,"r")
	x=text_file.read()
	learning(x,0)
	learn_doc_count+=1

for z in glob.glob("/home/sid/spam_project/enron1/spam/*.txt"):
	fname=z
	text_file=open(fname,"r")
	x=text_file.read()
	learning(x,1)
	learn_doc_count+=1
	
for z in glob.glob("/home/sid/spam_project/enron2/spam/*.txt"):
	fname=z
	text_file=open(fname,"r")
	x=text_file.read()
	learning(x,1)
	learn_doc_count+=1
	
corrects=0
wrongs=0


for z in glob.glob("/home/sid/spam_project/enron3/ham/*.txt"):
	fname=z
	text_file=open(fname,"r")
	x=text_file.read()
	if (prediction(x)==1):
		wrongs+=1
	else:
		corrects+=1
		

print "Ham file testing:"
print "correct predictions: ",corrects," wrong predictions: ",wrongs," accuracy: ",corrects/(corrects+wrongs)
	


corrects=0
wrongs=0


for z in glob.glob("/home/sid/spam_project/enron3/spam/*.txt"):
	fname=z
	text_file=open(fname,"r")
	x=text_file.read()
	if (prediction(x)==1):
		corrects+=1
	else:	
		wrongs+=1
		

print "spam file testing:"
print "correct predictions: ",corrects," wrong predictions: ",wrongs," accuracy: ",corrects/(corrects+wrongs)

'''
fname="hamtest.txt"
text_file=open(fname,"r")
x=text_file.read()	
l=prediction(x)
if (l==1):
	print "spam"
else:
	print "ham"

fname="spamtest.txt"
text_file=open(fname,"r")
x=text_file.read()
l=prediction(x)
if (l==1):
	print "spam"
else:
	print "ham"
'''

#print "dictionary count: ",len(data['bow'])
#for word in data['bow']:
#	print word,bag_of_words[word][0],bag_of_words[word][1] 	


print "distinct vocab :",len(data['bow'])		
print "Total words:",spam_word_count+ham_word_count	
print "Total documents count for learning: ",learn_doc_count
