import time
import threading
from src.data import data
from src.auth import decode_token
from src.error import InputError, AccessError

def raise_inputerrors(token, message_id):
    if next((True for token_list in data['users'] if token in token_list['token']), False) is False:
        raise InputError("Invalid token")
    if message_id is None:
        return
    message_index = next((index for (index, m_id) in enumerate(data['message']['message_info'])
    if message_id == m_id['message_id']), False)
    if message_index is False:
        raise InputError("Invalid message id")
    return message_index
    

def message_send_v2(token, channel_id, message):
    '''
    <Sends a message to a channel>

    Arguments:
        <token> (<string>)      - <a specific jwt string for each user>
        <channel_id> (<int>)      - <unique integer for each channel>
        <message> (<str>)       - message that will be sent
    Exceptions:
        InputError  - Occurs when
            Token is not valid
            Channel_id is not valid
            Message is over 1000 characters
        AccessError - Occurs when
            User is not part of channel

    Return Value:
        Returns a dictionary with the message_id>
    '''
    raise_inputerrors(token, None)
    # Check if channel id exists
    channel_index = next((index for (index, d) in enumerate(data['channels']) if d["channel_id"] == channel_id), None)
    if channel_index is None:
        raise InputError("Channel ID is not a valid channel")
    u_id = decode_token(token) # decode uid
    if u_id not in data['channels'][channel_index]['members'][0]['members_id']:
        raise AccessError("User not in channel")
    if len(message) > 1000:
        raise InputError("Message over 1000 characters")

    message_info = {
        'message_id': data['message']['most_recent_id'] + 1,
        'message': message,
        'reacts': [],
        'is_pinned': False,
        'time_created': int(time.time()),
        'auth_user_id': u_id,
        'channel_id': channel_id,
        'dm_id': -1
    }
    # data['channels'][channel_index]['messages'].append(message_info)
    data['message']['message_info'].append(message_info)
    data['message']['most_recent_id'] += 1
    
    return {
        'message_id': message_info['message_id']
    }

def message_remove_v1(token, message_id):
    '''
    <Removes a message>

    Arguments:
        <token> (<string>)      - <a specific jwt string for each user>
        <message_id> (<int>)      - <unique integer for each channel>

    Exceptions:
        InputError  - Occurs when 
            Token is not valid
            Message_id is not valid
        AccessError - Occurs when 
            User is not part of channel/dm

    Return Value:
        <Returns {}>
    '''
    message_index = raise_inputerrors(token, message_id)
    channel_id = data['message']['message_info'][message_index]['channel_id']
    dm_id = data['message']['message_info'][message_index]['dm_id']
    for channel_index, d in enumerate(data['channels']):
        if d['channel_id'] == channel_id:
            break
    for dm_index, d in enumerate(data['dm']):
        if d['dm_id'] == dm_id:
            break
    # if you sent it or owner of channel you can remove message
    u_id = decode_token(token)

    if u_id != data['message']['message_info'][message_index]['auth_user_id']: # need another case for owner/admin do later
        if channel_id != -1 and u_id not in data['channels'][channel_index]['owner_id']:
            raise AccessError()
        elif dm_id != -1 and u_id not in data['dm'][dm_index]['owner']:
            raise AccessError()
    del data['message']['message_info'][message_index] # remove from data['messages'] key
    return {
    }

def message_edit_v2(token, message_id, message):
    '''
    <Removes a message>

    Arguments:
        <token> (<string>)      - <a specific jwt string for each user>
        <message_id> (<int>)      - <unique integer for each channel>
        <message> (<str>)       - string with a message

    Exceptions:
        InputError  - Occurs when 
            Token is not valid
            new message is over 1000 characters
            Message_id is not valid
        AccessError - Occurs when 
            User is not the original sender or not the owner of channel/dm

    Return Value:
        <Returns {}>
    '''
    message_index = raise_inputerrors(token, message_id)
    channel_id = data['message']['message_info'][message_index]['channel_id']
    dm_id = data['message']['message_info'][message_index]['dm_id']
    for channel_index, d in enumerate(data['channels']):
        if d['channel_id'] == channel_id:
            break

    for dm_index, d in enumerate(data['dm']):
        if d['dm_id'] == dm_id:
            break

    if len(message) > 1000:
        raise InputError("Message over 1000 characters")

    u_id = decode_token(token)
    print(u_id)
    if u_id != data['message']['message_info'][message_index]['auth_user_id']:
        if channel_id != -1 and u_id not in data['channels'][channel_index]['owner_id']:
            raise AccessError()
        if dm_id != -1 and u_id not in data['dm'][dm_index]['owner']:
            raise AccessError()
    # delete message if new message is empty string
    if message == "":
        return message_remove_v1(token, message_id)

    data['message']['message_info'][message_index]['message'] = message
    return {
    }

def message_senddm_v1(token, dm_id, message):
    '''
    <Sends a message to a dm>

    Arguments:
        <token> (<string>)      - <a specific jwt string for each user>
        <dm_id> (<int>)      - <unique integer for each dm>
        <message> (<str>)       - message that will be sent
    Exceptions:
        InputError  - Occurs when
            Token is not valid
            dm_id is not valid
            Message is over 1000 characters
        AccessError - Occurs when
            User is not part of dm

    Return Value:
        Returns a dictionary with the message_id>
    '''
    # assumption raise inputerrors for invalid token and channel_ids
    raise_inputerrors(token, None)
    # Check if channel id exists
    dm_index = next((index for (index, d) in enumerate(data['dm']) if d["dm_id"] == dm_id), None)
    if dm_index is None:
        raise InputError("DM ID is not a valid")
    u_id = decode_token(token) # decode uid
    if u_id not in data['dm'][dm_index]['u_ids']:
        raise AccessError("User not in DM")
    if len(message) > 1000:
        raise InputError("Message over 1000 characters")

    message_info = {
        'message_id': data['message']['most_recent_id'] + 1,
        'message': message,
        'reacts': [],
        'is_pinned': False,
        'time_created': int(time.time()),
        'auth_user_id': u_id,
        'channel_id': -1,
        'dm_id': dm_id
    }
    data['message']['message_info'].append(message_info)
    data['message']['most_recent_id'] += 1

    return {
        'message_id': message_info['message_id']
    }

def message_share_v1(token, og_message_id, message, channel_id, dm_id):
    '''
    <Share a message to a channel or dm>

    Arguments:
        <token> (<string>)      - <a specific jwt string for each user>
        <og_message_id> (<int>)      - <unique integer for each message>
        <message> (<str>)       - message that will be added onto the original message
        <dm_id> (<int>)      - <unique integer for each dm>
        <channel_id> (<int>)      - <unique integer for each channel>
        
    Exceptions:
        InputError  - Occurs when
            Token is not valid
            dm_id is not valid
            channel_id is not valid
        AccessError - Occurs when
            User is not part of new dm/channel
            User is not part of original channel/dm

    Return Value:
        Returns a dictionary with the message_id>
    '''
    if dm_id == -1:
        message_index = next((index for (index, d) in enumerate(data['message']['message_info'])
        if d["message_id"] == og_message_id and dm_id == -1), None)
        if message_index is None:
            raise InputError("Invalid message id")
        channel_index = next((index for (index, d) in enumerate(data['channels']) if d["channel_id"] == channel_id), None)
        if channel_index is None:
            raise InputError("Channel does not exist")
        u_id = decode_token(token)
        if u_id not in data['channels'][channel_index]['members'][0]['members_id']:
            raise AccessError("Not in channel")
        message_id = message_send_v2(token, channel_id, data['message']['message_info'][message_index]['message'] + message)
    else:
        for message_index, d in enumerate(data['message']['message_info']):
            if d["message_id"] == og_message_id and channel_id == -1:
                break
            message_index = None

        if message_index is None:
            raise InputError("Invalid message id")
        dm_index = next((index for (index, d) in enumerate(data['dm']) if d["dm_id"] == dm_id), None)
        if dm_index is None:
            raise InputError("dm does not exist")
        u_id = decode_token(token)
        if u_id not in data['dm'][dm_index]['u_ids']:
            raise AccessError("Not in dm")
        message_id = message_senddm_v1(token, dm_id, data['message']['message_info'][message_index]['message'] + message)

    return {"shared_message_id": message_id['message_id']}

def thread_sendlater():
    return

def message_sendlater_v1(token, channel_id, message, time_sent):
    '''
    <Share a message to a channel or dm>

    Arguments:
        <token> (<string>)      - <a specific jwt string for each user>
        <channel_id> (<int>)      - <unique integer for each channel>
        <message> (<str>)       - message that will be sent
        <time_sent> (<int>)      - <integer with time sent>
        
        
    Exceptions:
        InputError  - Occurs when
            Token is not valid
            channel_id is not valid
            time_sent is in the past
        AccessError - Occurs when
            User is not part of channel

    Return Value:
        Returns a dictionary with the message_id>
    '''
    raise_inputerrors(token, None)
    # Check if channel id exists
    channel_index = next((index for (index, d) in enumerate(data['channels']) if d["channel_id"] == channel_id), None)
    if channel_index is None:
        raise InputError("Channel ID is not a valid channel")
    u_id = decode_token(token) # decode uid
    if u_id not in data['channels'][channel_index]['members'][0]['members_id']:
        raise AccessError("User not in channel")
    if len(message) > 1000:
        raise InputError("Message over 1000 characters")
    if int(time_sent) < int(time.time()):
        raise InputError("time in the past")
    t = threading.Timer(int(time_sent) - int(time.time()), thread_sendlater)
    t.start()
    t.join()
    return message_send_v2(token, channel_id, message)

def message_sendlaterdm_v1(token, dm_id, message, time_sent):
    '''
    <Share a message to a channel or dm>

    Arguments:
        <token> (<string>)      - <a specific jwt string for each user>
        <dm_id> (<int>)      - <unique integer for each dm>
        <message> (<str>)       - message that will be sent
        <time_sent> (<int>)      - <integer with time sent>
        
        
    Exceptions:
        InputError  - Occurs when
            Token is not valid
            dm_id is not valid
            time_sent is in the past
        AccessError - Occurs when
            User is not part of dm

    Return Value:
        Returns a dictionary with the message_id>
    '''
    raise_inputerrors(token, None)
    dm_index = next((index for (index, d) in enumerate(data['dm']) if d["dm_id"] == dm_id), None)
    if dm_index is None:
        raise InputError("DM ID is not a valid")
    u_id = decode_token(token) # decode uid
    if u_id not in data['dm'][dm_index]['u_ids']:
        raise AccessError("User not in DM")
    if len(message) > 1000:
        raise InputError("Message over 1000 characters")
    if int(time_sent) < int(time.time()):
        raise InputError("time in the past")
    t = threading.Timer(int(time_sent) - int(time.time()), thread_sendlater)
    t.start()
    t.join()
    return message_senddm_v1(token, dm_id, message)

def message_react_v1(token, message_id, react_id):
    message_index = raise_inputerrors(token, message_id)
    u_id = decode_token(token)
    if react_id != 1:
        raise InputError("invalid react id")
    if data['message']['message_info'][message_index]['channel_id'] != -1:
        channel_id = data['message']['message_info'][message_index]['channel_id']
        channel_index = next((index for (index, d) in enumerate(data['channels']) if d["channel_id"] == channel_id), None)
        if u_id not in data['channels'][channel_index]['members'][0]['members_id']:
            raise AccessError("User not in channel")

        if next((True for d in data['message']['message_info'][message_index]['reacts'] 
        if d['auth_user_id'] == u_id if d['react_id'] == react_id), False) is True:
            raise InputError('already reacted')
        react_info = {
                'react_id': react_id,
                'auth_user_id': u_id
            }
        data['message']['message_info'][message_index]['reacts'].append(react_info)
        return {}
    dm_id = data['message']['message_info'][message_index]['dm_id']
    dm_index = next((index for (index, d) in enumerate(data['dm']) if d["dm_id"] == dm_id), None)
    if dm_index is None:
        raise InputError("DM ID is not a valid")
    u_id = decode_token(token) # decode uid
    if u_id not in data['dm'][dm_index]['u_ids']:
        raise AccessError("User not in DM")
    if next((True for d in data['message']['message_info'][message_index]['reacts']
    if d['auth_user_id'] == u_id and d['react_id'] == react_id), False) is True:
        raise InputError("already reacted")
    react_info = {
        'react_id': react_id,
        'auth_user_id': u_id
    }
    data['message']['message_info'][message_index]['reacts'].append(react_info)
    return {}

def message_unreact_v1(token, message_id, react_id):
    message_index = raise_inputerrors(token, message_id)
    u_id = decode_token(token)
    if react_id != 1:
        raise InputError("invalid react id")
    if data['message']['message_info'][message_index]['channel_id'] != -1:
        channel_id = data['message']['message_info'][message_index]['channel_id']
        channel_index = next((index for (index, d) in enumerate(data['channels']) if d["channel_id"] == channel_id), None)
        if u_id not in data['channels'][channel_index]['members'][0]['members_id']:
            raise AccessError("User not in channel")
        react_index = next((index for index, d in enumerate(data['message']['message_info'][message_index]['reacts']) 
        if d['auth_user_id'] == u_id if d['react_id'] == react_id), None)
        if react_index is None:
            raise InputError('has not reacted')
        del data['message']['message_info'][message_index]['reacts'][react_index]
        return {}
    
    dm_id = data['message']['message_info'][message_index]['dm_id']
    dm_index = next((index for (index, d) in enumerate(data['dm']) if d["dm_id"] == dm_id), None)

    if u_id not in data['dm'][dm_index]['u_ids']:
        raise AccessError("User not in DM")
    react_index = next((index for index, d in enumerate(data['message']['message_info'][message_index]['reacts']) 
    if d['auth_user_id'] == u_id if d['react_id'] == react_id), None)
    if react_index is None:
        raise InputError('has not reacted')
    del data['message']['message_info'][message_index]['reacts'][react_index]
    return {}


def message_pin_v1(token, message_id):
    message_index = raise_inputerrors(token, message_id)
    if data['message']['message_info'][message_index]['is_pinned'] is True:
        raise InputError('message already pinned')
    u_id = decode_token(token)
    if data['message']['message_info'][message_index]['channel_id'] != -1:
        channel_id = data['message']['message_info'][message_index]['channel_id']
        channel_index = next((index for (index, d) in enumerate(data['channels']) if d["channel_id"] == channel_id), None)
        if u_id not in data['channels'][channel_index]['members'][0]['members_id']:
            raise AccessError("User not in channel")
        if u_id not in data['channels'][channel_index]['owner_id']:
            raise AccessError("not owner of channel")
        data['message']['message_info'][message_index]['is_pinned'] = True

        return {}

    dm_id = data['message']['message_info'][message_index]['dm_id']
    dm_index = next((index for (index, d) in enumerate(data['dm']) if d["dm_id"] == dm_id), None)
    if dm_index is None:
        raise InputError("DM ID is not a valid")
    u_id = decode_token(token) # decode uid
    if u_id not in data['dm'][dm_index]['u_ids']:
        raise AccessError("User not in DM")
    if u_id not in data['dm'][dm_index]['owner']:
        raise AccessError("not owner of dm")
    data['message']['message_info'][message_index]['is_pinned'] = True

    return {}

def message_unpin_v1(token, message_id):
    message_index = raise_inputerrors(token, message_id)
    if data['message']['message_info'][message_index]['is_pinned'] is False:
        raise InputError('message already unpinned')
    u_id = decode_token(token)

    if data['message']['message_info'][message_index]['channel_id'] != -1:
        channel_id = data['message']['message_info'][message_index]['channel_id']
        channel_index = next((index for (index, d) in enumerate(data['channels']) if d["channel_id"] == channel_id), None)
        if u_id not in data['channels'][channel_index]['members'][0]['members_id']:
            raise AccessError("User not in channel")
        if u_id not in data['channels'][channel_index]['owner_id']:
            raise AccessError("not owner of channel")
        data['message']['message_info'][message_index]['is_pinned'] = False
        return {}

    dm_id = data['message']['message_info'][message_index]['dm_id']
    dm_index = next((index for (index, d) in enumerate(data['dm']) if d["dm_id"] == dm_id), None)
    if dm_index is None:
        raise InputError("DM ID is not a valid")
    u_id = decode_token(token) # decode uid
    if u_id not in data['dm'][dm_index]['u_ids']:
        raise AccessError("User not in DM")
    if u_id not in data['dm'][dm_index]['owner']:
        raise AccessError("not owner of dm")
    data['message']['message_info'][message_index]['is_pinned'] = False
    return {}