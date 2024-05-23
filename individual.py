# -*- coding: utf-8 -*-
"""
Created on Sun May  5 19:01:51 2024

@author: Vincent Lomas
"""

import numpy as np

### THESE ARE THE SLIDERS

prop_subbed = 0.5 # Proportion of subscribed videos in feed
time_slider = 0.02 # 0 is full recomendation based, 1 is new videos
sub_time_slider = 0.9 # 0 is full recomendation based, 1 is new videos (subbed videos)


damp_coeff = 1
time_offset  = 1

# number of values to generate
n =10000
channel_num = 10

time_span = 9**3

np.random.seed(75565885) # Set seeds for consistant results
time_dist = np.random.gamma(2,2,n) # Generate log_9(times) videos are posted from gamma distribution 
time_dist[time_dist>5] = np.random.gamma(2,2,np.sum(time_dist>5)) # Regerate videos that are too old once
time_posted = (9**time_dist)
channel = np.round(np.random.rand(n)*channel_num) # Assign a random channel (up to the number of channels) - channel 1 and 10 are half as likely due to round - change to floor to change this
sub_num = 3 # How many channels subbed to # These are always the first channels, i.e. sub_num = 3, subbed channels are 0,1,2
subbed_channels = np.arange(0,sub_num)
# Generate random scores for each video
a = np.random.rand(n)
b = np.random.rand(n)
c = np.random.rand(n)
d = np.random.rand(n)
e = np.random.rand(n)
# Storage columns for each video to be assigned later
score = np.zeros(n)
ID = np.zeros(n)
adj_score = np.zeros(n)

# Construct matrix holding all videos
video_matrix = np.column_stack((ID,score,time_posted,channel,a,b,c,d,e, adj_score))

# Assign ID num
video_matrix = video_matrix[np.flip(video_matrix[:, 3].argsort())] # Sort videos from oldest to newest
video_matrix[:,0] = np.arange(0,n) # Older videos have a lower ID

### user preference
preference = [0.2,0.5,0.9,0.1,0.4]
p_size = np.linalg.norm(preference)

# Setting up storage arrays
sub_matrix = np.zeros((0,10))
general_matrix = np.zeros((0,10))

### Generate score from cosine similarity and then sort videos into subscribed and unsubscribed matricies
for i in range(len(a)):
    row = video_matrix[i,:]
    row_size = np.linalg.norm(row[4:-1])
    score = np.dot(preference, row[4:-1]) / (row_size*p_size)
    video_matrix[i,1] = score
    row[1] = score
    # Seperate Subbed videos and not
    if row[3] in subbed_channels:
        sub_matrix = np.vstack([sub_matrix, row])
    else:
        general_matrix = np.vstack([general_matrix, row])
    

# Apply equation
sub_matrix[:,-1] = (sub_time_slider+(1-sub_time_slider)*sub_matrix[:,1]) * (1-sub_time_slider+sub_time_slider/(np.log(time_offset + sub_matrix[:,2])/np.log(10)+damp_coeff))
general_matrix[:,-1] = (time_slider+(1-time_slider)*general_matrix[:,1]) * (1-time_slider+time_slider/(np.log(time_offset + general_matrix[:,2])/np.log(10)+damp_coeff))

# Setting up indicies
user_input = ""
i = 0
j = 0



# Sort video matrix according to adjusted score
sub_matrix = sub_matrix[np.flip(sub_matrix[:, -1].argsort())]
general_matrix = general_matrix[np.flip(general_matrix[:, -1].argsort())]


print("")
while user_input != "q":
    print("Subbed?   Time Since Posted     Recommender System Score")
    for i in range(10):
        if prop_subbed > np.random.rand(1): # generate videos according to defined proportion
            print(f" subbed           {sub_matrix[i,2]:9.2f}                      {sub_matrix[i,1]:5.5f}")
            i += 1
        else:
            print(f"                  {general_matrix[j,2]:9.2f}                      {general_matrix[j,1]:5.5f}")
            j+=1
    
    user_input = input("Enter 'q' to quit, or anything else to generate 10 more suggestions: ")
