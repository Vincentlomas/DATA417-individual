

from gensim.models import Word2Vec
import string
import re
import os
import collections
from os import listdir
from os.path import isfile, join
from joblib import dump, load
import pickle
from io import StringIO
import pandas as pd
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()
from spacy.matcher import PhraseMatcher
from itertools import chain
import textract
from gensim.models import Word2Vec
import string
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import gensim
from gensim.models.phrases import Phraser, Phrases
import nltk
import collections
import re
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
nltk.download('punkt')
nltk.download('stopwords')
     

[nltk_data] Downloading package punkt to /root/nltk_data...
[nltk_data]   Package punkt is already up-to-date!
[nltk_data] Downloading package stopwords to /root/nltk_data...
[nltk_data]   Package stopwords is already up-to-date!

True



def cleanResume(resumeText):
    resumeText = re.sub('http\S+\s*', ' ', resumeText)  
    resumeText = re.sub('RT|cc', ' ', resumeText)  
    resumeText = re.sub('#\S+', '', resumeText) 
    resumeText = re.sub('@\S+', '  ', resumeText) 
    resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', resumeText)
    resumeText = re.sub(r'[^\x00-\x7f]',r' ', resumeText) 
    resumeText = re.sub('\s+', ' ', resumeText)  
    return resumeText
     

def Preprocessfile(filename):
  text = textract.process(filename)
  text= text.decode('utf-8').replace("\n", " ")
  # print(text)
  x=[]
  tokens=word_tokenize(text)
  tok=[w.lower() for w in tokens]
  table=str.maketrans('','',string.punctuation)
  strpp=[w.translate(table) for w in tok]
  words=[word for word in strpp if word.isalpha()]
  stop_words=set(stopwords.words('english'))
  words=[w for w in words if not w in stop_words]
  x.append(words)
  # print(x)
  res=" ".join(chain.from_iterable(x))
  return res
     

x=Preprocessfile('jobtype.txt')
y=Preprocessfile('resume.pdf')
text=[y,x]



#print the similarity score
print("\n Similarity Score: ")
cv = CountVectorizer()
count_matrix = cv.fit_transform(text)
print(cosine_similarity(count_matrix))
matchpercent = cosine_similarity(count_matrix)[0][1]*100
matchpercent = round(matchpercent,2)

print("Your Resume matches about " + str(matchpercent) + "% of the job")
     

 Similarity Score: 
[[1.         0.51460293]
 [0.51460293 1.        ]]
Your Resume matches about 51.46% of the job


#all custom keywords should be in lower case
def find_score(jobdes,filename,customKeywords):   
    resume=Preprocessfile(filename)
    customKeywords = ' '.join(customKeywords)
    jobdes=jobdes + ' ' + customKeywords
    text=[resume,jobdes]
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(text)
    print(cosine_similarity(count_matrix))
    matchpercent = cosine_similarity(count_matrix)[0][1]*100
    matchpercent = round(matchpercent,2)
    print(matchpercent)
    return matchpercent
     


def predictResume(filename):
  text = textract.process(filename)
  text= text.decode('utf-8').replace("\n", " ")
  text=cleanResume(text)
  text=[text]
  text=np.array(text)
  vectorizer = pickle.load(open("vectorizer.pickle", "rb"))
  resume = vectorizer.transform(text)
  model = load('model.joblib') 
  result=model.predict(resume)
  labeldict={
    0:'Arts',
    1:'Automation Testing',
    2:'Operations Manager',
    3:'DotNet Developer',
    4:'Civil Engineer',
    5:'Data Science',
    6:'Database',
    7:'DevOps Engineer',
    8:'Business Analyst',
    9:'Health and fitness',
    10:'HR',
    11:'Electrical Engineering',
    12:'Java Developer',
    13:'Mechanical Engineer',
    14:'Network Security Engineer',
    15:'Blockchain ',
    16:'Python Developer',
    17:'Sales',
    18:'Testing',
    19:'Web Designing'
  }
  return labeldict[result[0]]
     

#FLOW

profile_type=[] # user inputs profile type from the abive 20 options multiple profiles are possible

resume='resumeds.pdf'

#iterate through all resumes here
predictedprofile=predictResume(resume)
print(predictedprofile)   #classifies what type of resume is inputed, if it from the mentioned profile_type keep other wise disgard

#ask user to enter job des
jobdes=Preprocessfile('dsjobdes.txt')  #the job description is preprocessed outside as the same job description is used for the multiple resumes

#askuser to enter custom keywords
customKeywords=['spanish','hindi','opencv']


#iterate through all resumes here
results=find_score(jobdes,resume,customKeywords);


     
