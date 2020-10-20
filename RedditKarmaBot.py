import requests
import json
import time
from datetime import datetime
from playsound import playsound


def endpoint(username):
    return f"https://www.reddit.com/user/{username}/about.json"

def getJSONUserData(username):
    r = requests.get(endpoint(username), headers = {'User-agent': 'PyKarma'})
    if r.status_code == 200:
        return r.json()['data']

def getUserKarma(username):
    jsonData = getJSONUserData(username)
    if not jsonData:
        return
    l_karma, c_karma = jsonData['link_karma'], jsonData['comment_karma']
    karma = l_karma + c_karma
    return karma




def upvote_event():
    print("Upvote")
    playsound('upvote.mp3', True)


def downvote_event():
    print("Downvote")
    playsound('downvote.mp3', True)


username = input('Please input your username:\n')

max_timestep = 10
min_timestep = 5
fuzzing_cap_cooldown = 270

# Last measured karma/second
karma_rate = 0

last_karma = getUserKarma(username)
karma_difference = 0
max_recent_karma = last_karma
last_max_time = datetime.now()

while True:
    current_timestep = max(min(max_timestep, 15 / ((karma_rate) + 0.0001) ), min_timestep)
    # wait for (second/karma) in seconds    
    print('Waiting', current_timestep)
    print('Difference', karma_difference)
    
    if karma_difference:
        for upvote in range(abs(karma_difference)):
            time.sleep(current_timestep / abs(karma_difference))
            if karma_difference > 0:
                upvote_event()
            else:
                downvote_event()
    else:
        time.sleep(current_timestep)
    karma = getUserKarma(username) or last_karma
    
    def reset_max_karma():
        max_recent_karma = karma
        last_max_time = datetime.now()
        
    if karma > max_recent_karma:
        reset_max_karma()
    
    karma_difference = karma - last_karma
    if karma_difference < 0 and (datetime.now() - last_max_time).seconds > fuzzing_cap_cooldown:
        reset_max_karma()
    else:
        karma_difference = max(0,karma_difference)

    karma_rate = karma_difference / current_timestep
    
    last_karma = karma
    print('Karma', karma)
    
