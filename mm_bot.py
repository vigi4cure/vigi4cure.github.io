#!/usr/bin/python3.4

## Author Sabane Hosen - GNA-NSO - January 2018
## Modified by ywen@vigilantglobal.com 2018/01/16

# Dependency install
# sudo apt-get update
# sudo apt-get install python3-pip -y --force-yes
# sudo python3.4 -m pip install mattermostdriver
# sudo pip3 install --upgrade requests

#================== example ==================
#from mm_bot import *
#init('shtest002', '61r88z7o9tn6tph1sypfim3joy')
#delete_all_posts('Luna-Bot')
#postmessage('msg', 'http://vgweb/cgi-bin/mattermost/luna-bot-icon.png', 'Luna-Bot')
#=============================================

import json, time
from mattermostdriver import Driver

mm = ''
channel_id = ''

def init(channel, access_token, team_id = 'n1f7ge4biifutrbeq9wdx6sz6y') :
    global mm, channel_id
    # Tuning needed here to switch between GNA and DRW instance may be
    # static override with gna team id to post on gna channels
    # at current time get_team() doesnt return gna team id , only DRW one at index 0 - will need to chat to drw about this.
    # team_id = mm.api['teams'].get_teams()[0]['id']

    url = 'chat.drwholdings.com'
    mm = Driver({
        'url': url,
        'token': access_token,
        'scheme': 'https',
        'port': 443,
        'basepath': '/api/v4',
        'verify': True,
        'timeout': 20
    })
    r = mm.login()
    channel_id = mm.api['channels'].get_channel_by_name(team_id, channel)['id']    
    return r

def postmessage(message, icon, Bot_name):
    global mm, channel_id
    props = {
        'from_webhook': 'true',
        'override_icon_url': icon,
        'override_username': Bot_name
    }
    
    json = mm.api["posts"].create_post(options={
        'credentials': 'same-origin',
        'channel_id' : channel_id,
        'props'      : props,
        'message'    : message
        }
    )        
    # print("Sent post.")        
    return json

def get_posts_in_channels(Bot_name):
    global mm, channel_id

    # print("searching message in posts endpoint")
    json = mm.api["posts"].get_posts_for_channel(channel_id,
        params={
        'page': 0,
        'per_page': 120,
        }
    )
    post_id_collection = {}    
    try:
        for key, post in json['posts'].items():
            try:
                if post['props']['override_username'] == Bot_name:
                    post_id_collection[post['id']] = post
            except:
                pass
    except:
        pass    
    return post_id_collection

def update_this_post(post_id, message):
    global mm
    # print("updating post_id {0}".format(post_id))
    json = mm.api["posts"].update_post(post_id,
        options={
        'message': message,
        }
    )
    return json

def delete_all_posts(Bot_name):
    post_id_collection = get_posts_in_channels(Bot_name)
    for post_id, post in post_id_collection.items():
       r = delete_this_post(post_id)
       time.sleep( 0.5 )
       # print (r)    
    
def delete_this_post(post_id):
    global mm
    # print("deleting post_id {0}".format(post_id))
    json = mm.api["posts"].delete_post(post_id)
    return json
