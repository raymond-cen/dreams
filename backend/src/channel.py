import jwt
import time
from src.data import data, mycursor, mydb
from src.error import InputError, AccessError
from src.auth import decode_token
from src.user import find_user

SECRET = 'OURSECRET'

def channel_invite_v1(token, channel_id, u_id):
    '''
    Function invites a user to join a channel
        <auth_user_id> (<int>)  - <uniqiue integer for the authorised user>
        <channel_id> (<int>)    - <unique integer for each channel>
        <u_id> (<int>)    - <unique integer for user>

    Exceptions:
        InputError  - Occurs when channel_id is not valid or u_id does not belong to a user
        AccessError - Occurs when the authorised user is not in the channel

    Return Value:
        Empty dictionary
    '''
    auth_user_id = decode_token(token)
    channel_index = next((index for (index, d) in enumerate(data['channels']) if d["channel_id"] == channel_id), None)
    # Check if channel id exists
    if channel_index is None:
        raise InputError("channel_id does not refer to a valid channel.")
    if auth_user_id == u_id:
        return {}
    user_index = next((index for (index, d) in enumerate(data['users']) if d["auth_user_id"] == u_id), None)  
    if user_index is None:
        raise InputError("u_id does not refer to a valid user")
    if auth_user_id not in data['channels'][channel_index]['members'][0]['members_id']:
        raise AccessError('the authorised user is not already a member of the channel')
    data['channels'][channel_index]['members'][0]['members_id'].append(u_id)
    sqlf = ("""SELECT permission FROM users
            WHERE user_id = %s""")
    value = (u_id,)
    mycursor.execute(sqlf, value)
    result = mycursor.fetchone()

    sqlf = ("""INSERT INTO channel_members
            (channel_id, user_id, owner_permission)
            VALUES (%s, %s, %s)""")

    value = (channel_id, u_id, result[0])
    mycursor.execute(sqlf, value)
    mydb.commit()

    if data['users'][user_index]['permission'] == 1:
        data['channels'][channel_index]['owner_id'].append(u_id)

    return {}

def member_details(auth_user_id):
    """
    helper function that returns a dictionary containing the user's first name, last name and id
    """
    member_info = {}
    # member_index = next((index for (index, d) in enumerate(data['users']) if d["auth_user_id"] == auth_user_id), None)
    member_info['u_id'] = auth_user_id
    # member_info['name_first'] = data['users'][member_index]['name_first']
    # member_info['name_last'] = data['users'][member_index]['name_last']

    sqlf = ("""SELECT name_first, name_last FROM users
            WHERE user_id = %s""")
    values = (auth_user_id,)
    mycursor.execute(sqlf, values)
    result = mycursor.fetchone()
    member_info['name_first'] = result[0]
    member_info['name_last'] = result[1]
    return member_info

def channel_details_v1(token, channel_id):
    '''
    Function takes in a channel with an user and gives information about the users and channel
    Arguments:
        <auth_user_id> (<int>)  - <uniqiue integer for each user>
        <channel_id> (<int>)    - <unique integer for each channel>

    Exceptions:
        InputError  - Occurs when channel_id is not valid or start is greater than total messages in channel
        AccessError - Occurs when the user is not a member of the channel

    Return Value:
        Returns a dictionary containing
    '''
    channel_index = next((index for (index, d) in enumerate(data['channels']) if d["channel_id"] == channel_id), None)
    # Check if channel id exists
    if channel_index is None:
        raise InputError("Channel ID is not a valid channel")
    # Check if user is in channel
    auth_user_id = decode_token(token)
    if auth_user_id not in data['channels'][channel_index]['members'][0]['members_id']:
        raise AccessError("Authorised user is not a member of channel with channel_id")
    owner_info = []
    # for owner_id in data['channels'][channel_index]['owner_id']:
    #     owner_info.append(member_details(owner_id))
    all_members = []
    # for members in data['channels'][channel_index]['members'][0]['members_id']:
    #     all_members.append(member_details(members))

    sqlf = ("""SELECT user_id FROM channel_members
            WHERE channel_id = %s AND owner_permission = %s""")
    values = (channel_id, 1)
    mycursor.execute(sqlf, values)
    result = mycursor.fetchall()

    for owner_id in result:
        owner_info.append(member_details(owner_id[0]))

    sqlf = ("""SELECT user_id FROM channel_members
            WHERE channel_id = %s""")
    values = (channel_id,)
    mycursor.execute(sqlf, values)
    result = mycursor.fetchall()
    for members in result:
        all_members.append(member_details(members[0]))
    all_member_dict = {
        'name': data['channels'][channel_index]['channel_name'],
        'owner_members': owner_info,
        'all_members': all_members
    }
    return all_member_dict

def react_info(u_id, message_info):
    reacts = {
        'react_id': 0,
        'is_this_user_reacted': False,
        'u_ids': []
    }
    for i in message_info['reacts']:
        reacts['u_ids'].append(i['auth_user_id'])
        reacts['react_id'] = i['react_id']
        if u_id == i['auth_user_id']:
            reacts['is_this_user_reacted'] = True
    return reacts

def channel_messages_v1(token, channel_id, start):
    '''
    Function returns a dictionary with the 50 most recent messages starting from the start index
    Arguments:
        <token> (<string>)      - <uniqiue jwt string for each user>
        <channel_id> (<int>)    - <unique integer for each channel>
        <start> (<int>)         - <starting index of messages to be returned>

    Exceptions:
        InputError  - Occurs when channel_id is not valid or start is greater than total messages in channel
        AccessError - Occurs when the user is not a member of the channel

    Return Value:
        Returns a dictionary with a list of messages, starting integer and ending integer
        Ending integer will be start + 50 or -1 if there are no more messages
    '''
    # may have to change start to int from string (not sure yet)
    new_dict = {
        'messages': [],
        'start': start,
        'end': start + 50
        } 
    channel_index = next((index for (index, d) in enumerate(data['channels']) if d["channel_id"] == channel_id), None)
    # Check if channel id exists
    if channel_index is None:
        raise InputError("Channel ID is not a valid channel")
    # check if user is in the channel
    u_id = decode_token(token)
    if u_id not in data['channels'][channel_index]['members'][0]['members_id']: # check new name with megharaj later
        raise AccessError("Authorised user is not a member of channel with channel_id")
    # Create list with all of channel's messages
    message_list = []
    for message_info in data['message']['message_info']:
        if message_info['channel_id'] == channel_id:
            output = {
                'message_id': message_info['message_id'],
                'u_id': message_info['auth_user_id'],
                'message': message_info['message'],
                'time_created': message_info['time_created'],
                'reacts': [react_info(u_id, message_info)],
                'is_pinned': message_info['is_pinned']
            }
            message_list.append(output)

    # check if start index is greater than the amount of messages
    if start > len(message_list):
        raise InputError("Start is greater than the total number of messages in the channel")
    # if start index is equal to total messages, return no messages
    elif start == len(message_list):
        new_dict['end'] = -1
        return new_dict
    message_list.reverse()
    message_index = start
    # Most recent messages will start at the beginning of the list
    for messages in message_list[start:start+50]:
        new_dict['messages'].append(messages)
        message_index += 1
        # Check if we are going outside the range of the list
        if message_index >= len(message_list):
            message_index = -1
            break
    new_dict['end'] = message_index
    return new_dict


def channel_leave_v1(token, channel_id):
    channel_index = next((index for (index, d) in enumerate(data['channels']) if d["channel_id"] == channel_id), None)
    # Check if channel id exists
    if channel_index is None:
        raise InputError("Channel ID is not a valid channel")
    # Check if user is in channel
    auth_user_id = decode_token(token)
    if auth_user_id not in data['channels'][channel_index]['members'][0]['members_id']:
        raise AccessError("Authorised user is not a member of channel with channel_id")
    auth_user_id = decode_token(token)
    data['channels'][channel_index]['members'][0]['members_id'].remove(auth_user_id)

    if auth_user_id in data['channels'][channel_index]['owner_id']: 
        data['channels'][channel_index]['owner_id'].remove(auth_user_id)
    return {
    }


def channel_join_v1(token, channel_id):
    '''<A user join a public or private channel>
    Arguments:
        <token> (<string>)      - <a specific jwt string for each user>
        <channel_id> (<int>)    - <a specific number for each channel>

    Exceptions:
        InputError  - Occurs when 
            not a valid auth_user_id or channel_id
        AccessError - Occurs when 
            a normal member want to join a private channel,
            member want to rejoin same channel

    Return Value:
        Returns <empty dictionary> on <a valid user want to join valid channel with valid access permisstion>
        Returns <empty dictionary> on <global owner want to join valid channel>
    '''
    # get users info from data and store in variable user
    users = data.get('users')
    ids = []
    channel = data.get('channels')
    channel_ids = []
    # check whether the auth_id is valid or not
    for i in range(len(users)):
        ids.append((users[i]['auth_user_id']))
    # raise an error if the auth_id is not valid
    u_id = decode_token(token)    
    print(u_id)

    if u_id not in ids:
        raise InputError("Invalid auth id")
    for i in range(len(channel)):
        channel_ids.append((channel[i]['channel_id']))
    # check whether the channel_id is valid or not
    if channel_id not in channel_ids:
        raise InputError("Invalid channel id")
    for i in range(len(data['channels'])):
        if channel_id is data['channels'][i]['channel_id']:
            member_ls = data['channels'][i]['members'][0]['members_id']
            for mem in member_ls:
                # not allow a member to rejoin a channel they alreay in 
                if mem == u_id:
                    raise AccessError("Already joined this channel")
            # check whether this channel public or not
            if data['channels'][i]['is_public'] == False and data['users'][(u_id - 1)]['permission'] != 1:
                raise AccessError("The channel is private and you are not authorised to join")
            # public channel or global owner
            else:
                member_ls.append(u_id)
                # golbal owner to join both public and private channels as a owner
                if data['users'][(u_id - 1)]['permission'] == 1:
                    data['channels'][i]['owner_id'].append(u_id)
    return {}



def channel_addowner_v1(token, channel_id, u_id):
    '''<Add owner to a channel>
    Arguments:
        <token> (<string>)      - <a specific jwt string for a user>
        <channel_id> (<int>)    - <a specific number for a channel>
        <u_id> (<int>)          - <a specific number for a channel>

    Exceptions:
        InputError  - Occurs when 
            not a valid channel_id,
            user with u_id not a owner of this channel
        AccessError - Occurs when 
            authorised user is not global owner or this channel's owner,
            token given an invalid auth_user_id

    Return Value:
        Returns <empty dictionary> on <valid autherised user with valid permission add another valid owner of this valid channel>
    '''
    auth_user_id = decode_token(token)
    if find_user('auth_user_id', auth_user_id) == -1:
        raise AccessError('Incorrect access')

    #Checking if Channel exists
    channel_found = False
    for i in range(len(data['channels'])):
        if channel_id is data['channels'][i]['channel_id']:
            channel_found = True

    if channel_found == False:
        raise InputError("Channel ID is not valid")

    #User trying to add owner is not part of the channel 
    if auth_user_id not in data['channels'][channel_id - 1]['owner_id']:
        raise AccessError("Authorised user is not a member of channel with channel_id")

    #Checking if Owner is already owner
    if u_id in data['channels'][channel_id - 1]['owner_id']:
            raise InputError('Already a owner of this channel')
       
    #Appending user to owners list
    for i in range(len(data['channels'])):
        if channel_id is data['channels'][i]['channel_id']:
            data['channels'][i]['owner_id'].append(u_id)
    return {}



def channel_removeowner_v1(token, channel_id, u_id):
    '''<Remove owner from a channel>
    Arguments:
        <token> (<string>)      - <a specific jwt string for a user>
        <channel_id> (<int>)    - <a specific number for a channel>
        <u_id> (<int>)          - <a specific number for a channel>

    Exceptions:
        InputError  - Occurs when 
            not a valid channel_id,
            user with u_id not a owner of this channel,
            current user is the only owner
        AccessError - Occurs when 
            authorised user is not global owner or this channel's owner,
            token given an invalid auth_user_id

    Return Value:
        Returns <empty dictionary> on <valid autherised user with valid permission remove another valid owner of this valid channel>
    '''
    # channel id valid or not 
    channel = data.get('channels')
    channel_ids = []
    for i in range(len(channel)):
        channel_ids.append((channel[i]['channel_id']))
    if channel_id not in channel_ids:
        raise InputError("Invalid channel id")
    # how many in owner list
    for i in range(len(data['channels'])):
        if channel_id is data['channels'][i]['channel_id']:
            owner_ls = data['channels'][i]['owner_id']
    
    
    # decode token
    auth_user_id = decode_token(token)
    # token contain invalid id
    if find_user('auth_user_id', auth_user_id) == -1:
        raise AccessError('Incorrect access')

    # check token user id inside owner list or not 
    if auth_user_id not in owner_ls and data['users'][(auth_user_id - 1)]['permission'] == 2:
        raise AccessError("autherised user not an owner of this channel")
    if len(owner_ls) == 1:
        raise InputError("Can't remove the only owner in this channel")
    # u_id in owner list or not 
    if u_id not in owner_ls:
        raise InputError("Not an owner of this channel")
    
    # normal remove
    for i in range(len(data['channels'])):
        if channel_id is data['channels'][i]['channel_id']:
            data['channels'][i]['owner_id'].remove(u_id)


    return {}
