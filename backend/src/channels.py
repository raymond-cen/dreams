from src.data import data, mycursor, mydb
from src.auth import decode_token
from src.error import InputError
from src.error import AccessError
import time
import itertools

def channels_list_v1(token):
    # channel info for storing the sliced dictionaries from a list
    d = decode_token(token)
    channelinfo = []
    # get the list of dictionaries of key:users to know how many times you need to iterate
    user = data.get('users')
    ids = []
    # check whether the input argument (auth_user_id) exists in the data or not
    for i in range(len(user)):
        ids.append((user[i]['auth_user_id']))
    if d not in ids:
        # raise an error if the auth_id is not valid
        raise AccessError("Invalid auth id")
    # iterate through the list of dictionaries (channels) that has 'channels' as key
    for i in range(len(data['channels'])):
        # check each item (channel) in the list if the given user exists in the members
        # list of that channel
        if d in (data['channels'][i]['members'][0]['members_id']):
            # if the id is a member of the channel then store the associated details of the
            # channel in variable out
            # out = dict(itertools.islice(data['channels'][i].items(), 2))
            out = {
                "channel_id": data['channels'][i]['channel_id'],
                "name": data['channels'][i]["channel_name"]
                }
            # append the info from out to channelinfo
            channelinfo.append(out)
    return {'channels': channelinfo}


def channels_listall_v1(token):
    d = decode_token(token)
    # channel info for storing the sliced dictionaries from a list
    channel_listall = []
    # get the list of dictionaries of key:users to know how many times you need to iterate
    user = data.get('users')
    ids = []
    # check whether the input argument (auth_user_id) exists in the data or not
    for i in range(len(user)):
        # append the list of dictionaries into ids
        ids.append((user[i]['auth_user_id']))
    if d not in ids:
        # raise an error if the auth_id is not valid ie if it does not exist in ids
        raise AccessError("Invalid auth id")
    # iterate over all the channels and slice out the associated details and append to channel_listall
    for i in range(len(data['channels'])):
        out = dict(itertools.islice(data['channels'][i].items(), 2))
        out = {
        "channel_id": data['channels'][i]['channel_id'],
        "name": data['channels'][i]["channel_name"]
        }
        channel_listall.append(out)
    return {'channels': channel_listall}


def channels_create_v1(token, name, is_public):
    # get users info from data and store in variable user
    d = decode_token(token)
    user = data.get('users')
    ids = []
    # check whether the auth_id is valid or not
    for i in range(len(user)):
        ids.append((user[i]['auth_user_id']))
    # raise an error if the auth_id is not valid
    if d not in ids:
        raise AccessError("Invalid authi id")
    # raise an error if the channel name is more than 20 characters long
    if len(name) > 20:
        raise InputError("Error input name too long")
    # to create the channel_id we need to know how many channels already exist in our data
    num_of_channels = len(data['channels'])
    # the current channel_id will be how many already are there plus one
    channel_id = num_of_channels + 1
    # information of the channel will be stored in this format
    channels = {'channel_id': channel_id, 'channel_name': name, 'is_public': is_public, 'owner_id': [d],
                'members': [{'members_id': [d]}], 'standup': {'active': False, 'time': 0 ,'messages': []}}
    # append the channel information to the data
    data['channels'].append(channels)
    sqlf = ("INSERT INTO channels"
            "(channel_id, channel_name, is_public)"
            "VALUES (%s, %s, %s)")

    values = (channel_id, name, 1)
    
    mycursor.execute(sqlf, values)

    sqlf = ("INSERT INTO channel_members"
            "(channel_id, user_id, owner_permission)"
            "VALUES (%s, %s, %s)")
    values = (channel_id, d, 1)
    mycursor.execute(sqlf, values)
    mydb.commit()
    return {'channel_id': channel_id}
