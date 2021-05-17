import time
from src.data import data
from src.error import InputError, AccessError
from src.auth import decode_token
from src.channel import react_info

def dm_create_v1(token, u_id):
    dm_id = len(data['dm']) + 1
    #Finding owner handle
    decode = decode_token(token)
    dm_id = len(data['dm']) + 1
    for i in range(len(data['users'])):
        if decode == data['users'][i]['auth_user_id']:
            fname1 = data['users'][i]['name_first']
            lname1 = data['users'][i]['name_last']
            name1 = fname1 + lname1

    #handle for users + owner
    user_handles = [name1]
    name2 = ""
    for auth_user_id in u_id:
        name2 = find_user_handles(auth_user_id)
        user_handles.append(name2)
    
    #sorting user handles
    user_handles = sorted(user_handles)

    dm_name = ",".join(user_handles)
    u_id.append(decode)
    dms = {
        'dm_id': dm_id,
        'dm_name': dm_name,
        'u_ids': u_id,
        'owner': [decode]
        }
    data['dm'].append(dms)

    return {'dm_id': dm_id, 'dm_name': dm_name}

def find_user_handles(u_id):
    for i in range(len(data['users'])):
        if u_id == data['users'][i]['auth_user_id']:
            fname2 = data['users'][i]['name_first']
            lname2 = data['users'][i]['name_last']
            return fname2 + lname2
    
    else:
        raise AccessError("user not found")

def dm_messages_v1(token, dm_id, start):
    '''
    Function returns a dictionary with the 50 most recent messages starting from the start index
    Arguments:
        <token> (<string>)      - <uniqiue jwt string for each user>
        <dm_id> (<int>)    - <unique integer for each dm>
        <start> (<int>)         - <starting index of messages to be returned>

    Exceptions:
        InputError  - Occurs when dm_id is not valid or start is greater than total messages in dm
        AccessError - Occurs when the user is not a member of the dm

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
    dm_index = next((index for (index, d) in enumerate(data['dm']) if d["dm_id"] == dm_id), None)
    # Check if dm id exists
    if dm_index is None:
        raise InputError("dm ID is not a valid dm")
    # check if user is in the dm
    u_id = decode_token(token)
    if u_id not in data['dm'][dm_index]['u_ids']:
        raise AccessError("Authorised user is not a member of dm with dm_id")
    # Create list with all of dm's messages
    message_list = []
    for message_info in data['message']['message_info']:
        if message_info['dm_id'] == dm_id:
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
        raise InputError("Start is greater than the total number of messages in the dm")
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

def dm_details_v1(token, dm_id):
    '''
    This function takes gives us the details of a particular user who is a member of a dm
    Arguments:
        <token> (string) ----token is an encoded version of auth user id
        <dm id> (integer) ---dm_id is the unique id for each dm
    Exceptions:
        InputError -- occurs when your dm id is invalid
        AccessError -- occurs when you are not a member of this dm
    Return value:
        returns the nane of the dm
        returns list of members' auth id
    '''
    decoded = decode_token(token)
    decoded = int(decoded)
    dms_aid = data['dm']
    dm_ids = []

    details = {}
    for i in range(len(dms_aid)):
        dm_ids.append(dms_aid[i]['dm_id'])
    if int(dm_id) not in dm_ids:
        raise InputError("Invalid dm_id")
    for users in dms_aid:
        if dm_id == users['dm_id'] and decoded not in users['u_ids']:
            raise AccessError("not a member")

    for i in range(len(data['dm'])):
        if dm_id == data['dm'][i]['dm_id']:
            details['name'] = data['dm'][i]['dm_name']
            out = []
            for m in data['dm'][i]['u_ids']:
                auth_index = next((index for (index, d) in enumerate(data['users']) if d["auth_user_id"] == m), None)
                member_info = {
                    'u_id': data['users'][auth_index]['auth_user_id'],
                    'email': data['users'][auth_index]['email'],
                    'name_first': data['users'][auth_index]['name_first'],
                    'name_last': data['users'][auth_index]['name_last'],
                    'handle_str': data['users'][auth_index]['handle_str'],
                }
                out.append(member_info)
            details['members'] = out
    return details


def dm_list_v1(token):
    '''
    This function gives out the list of dms the user is part. The function takes an encoded token decodes it
    and gives us the list of dms after checking the data structure.

    Arguments:
        <token> (string) --- token is an encoded version of auth user id

    Exceptions:
        AccessError -- occurs when the token is invalid
    Return Value:
        return list of dm ids that the user is member of
    '''
    decoded = decode_token(token)
    dms_id = data.get('dm')
    dm_ids = []
    dm_info = []
    for i in range(len(dms_id)):
        dm_ids.append(dms_id[i]['u_ids'])
    # if next((True for token_list in data['users'] if decoded in token_list['token']), False) is False:
    #     raise InputError("Invalid token")
    for i in range(len(data['dm'])):
        if decoded in data['dm'][i]['u_ids']:
            out = {
                "dm_id": data['dm'][i]['dm_id'],
                "name": data['dm'][i]['dm_name']
            }
            dm_info.append(out)
    return {'dms': dm_info}


def dm_remove_v1(token, dm_id):
    '''
    This function removes the entire dm or deletes it. but only the user who created it can delete a particular
    dm.
    Arguments:
        <token> (string) -----token is an encoded version of auth user id
        <dm_id> (integer) ----dm_id is the unique id for each dm
    Exceptions:
        InputError -- occurs when your dm id is invalid
        AccessError -- occurs when you are not a creator but want to delete this dm
    Return Value:
        This function does not return anything
    '''
    decode = decode_token(token)
    vdm = []
    ids = data.get('dm')
    for i in range(len(data['dm'])):
        vdm.append(ids[i]['dm_id'])
    if dm_id not in vdm:
        raise InputError("not a valid dm id")
    for i in range(len(data['dm'])):
        if dm_id == data['dm'][i]['dm_id']:
            if decode in data['dm'][i]['owner']:
                del data['dm'][i]
            else:
                raise AccessError("not owner")
    return {}


def dm_leave_v1(token, dm_id):
    '''
    This function provides you with the service of leaving a dm.
    Arguments:
        <token> (string) -----token is an encoded version of auth user id
        <dm_id> (integer) ----dm_id is the unique id for each dm

    Exceptions:
        InputError -- occurs when your dm id is invalid
        AccessError -- occurs when you are not a member of a particular dm

    Return Value:
        This function does not return anything

    '''
    decode = decode_token(token)
    vdm = []
    udm = []
    ids = data.get('dm')
    for i in range(len(data['dm'])):
        vdm.append(ids[i]['dm_id'])
        uid = udm+(ids[i]['u_ids'])
    if dm_id not in vdm:
        raise InputError("not a valid dm id")
    if decode not in uid:
        raise AccessError("You are not a member")
    for i in range(len(data['dm'])):
        if decode in data['dm'][i]['u_ids'] and decode != data['dm'][i]['owner']:
            data['dm'][i]['u_ids'].remove(decode)
    return {}

def dm_invite_v1(token, dm_id, u_id):
    auth_user_id = decode_token(token)
    dm_index = next((index for (index, d) in enumerate(data['dm']) if d["dm_id"] == dm_id), None)
    # Check if channel id exists
    if dm_index is None:
        raise InputError("dm_id does not refer to an existing dm.")
    if auth_user_id == u_id:
        return {}
    user_index = next((index for (index, d) in enumerate(data['users']) if d["auth_user_id"] == u_id), None)  
    if user_index is None:
        raise InputError("u_id does not refer to a valid user")
    if auth_user_id not in data['dm'][dm_index]['u_ids']:
        raise AccessError('the authorised user is not already a member of the channel')
    
    data['dm'][dm_index]['u_ids'].append(u_id)
    if data['users'][user_index]['permission'] == 1:
        data['dm'][dm_index]['owner'].append(u_id)
    return {}
