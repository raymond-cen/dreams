import threading
import time
from json import dumps
from src.data import data
from src.auth import decode_token
from src.error import InputError, AccessError
def standup_off(*args):
    channel_id = args[2]
    u_id = args[1]
    channel_index = args[0]
    
    data['channels'][channel_index]['standup']['active'] = False
    total_string = ''
    for message_info in data['channels'][channel_index]['standup']['messages']:
        total_string = total_string + message_info + '\n'
    # take out last new line
    if total_string != '':
        total_string = total_string[:-1]
    message_info = {
        'message_id': data['message']['most_recent_id'] + 1,
        'message': total_string,
        'time_created': data['channels'][channel_index]['standup']['time'],
        'reacts': [],
        'is_pinned': False,
        'auth_user_id': u_id,
        'channel_id': channel_id,
        'dm_id': -1
    }
    data['message']['message_info'].append(message_info)
    data['message']['most_recent_id'] += 1
    data['channels'][channel_index]['standup']['messages'] = []


def standup_start_v1(token, channel_id, length):
    '''
    <Sets standup to active and allows messages to be sent that will be added onto
    a list. At the end of the timer, all the messages will be compiled onto one and be
    sent as one message by the user who started the standup.>

    Arguments:
        <token> (<string>)      - <a specific jwt string for each user>
        <channel_id> (<int>)      - <unique integer for each channel>
        <length> (<int>)      - <time for how long the standup will be>
        
        
    Exceptions:
        InputError  - Occurs when
            Token is not valid
            channel_id is not valid
            An active standup is already running
        AccessError - Occurs when
            User is not part of channel

    Return Value:
        Returns a dictionary with time_finished>
    '''
    channel_index = next((index for (index, d) in enumerate(data['channels']) if d["channel_id"] == channel_id), None)
    if channel_index is None:
        raise InputError("Channel ID is not a valid channel")
    if data['channels'][channel_index]['standup']['active'] is True:
        raise InputError("An active standup is currently running in this channel")
    u_id = decode_token(token) # decode uid
    if u_id not in data['channels'][channel_index]['members'][0]['members_id']:
        raise AccessError("User not in channel")

    t = threading.Timer(length, standup_off, [channel_index, u_id, channel_id])
    t.start()
    data['channels'][channel_index]['standup']['active'] = True
    data['channels'][channel_index]['standup']['time'] = int(length) + int(time.time())

    return {'time_finished': data['channels'][channel_index]['standup']['time']}

def standup_active_v1(token, channel_id):
    '''
    <Checks if standup is currently active or not>

    Arguments:
        <token> (<string>)      - <a specific jwt string for each user>
        <channel_id> (<int>)      - <unique integer for each channel>
        
    Exceptions:
        InputError  - Occurs when
            Token is not valid
            channel_id is not valid
        AccessError - Occurs when
            User is not part of channel

    Return Value:
        Returns a dictionary with time_finish and bool is_active>
    '''
    channel_index = next((index for (index, d) in enumerate(data['channels']) if d["channel_id"] == channel_id), None)
    if channel_index is None:
        raise InputError("Channel ID is not a valid channel")
    if data['channels'][channel_index]['standup']['active'] is False:
        return {
            'is_active': False,
            'time_finish': None
        }
    return {
        'is_active': True,
        'time_finish': data['channels'][channel_index]['standup']['time']
    }

def standup_send_v1(token, channel_id, message):
    '''
    <Appends a message to the standup list when the standup is active.>

    Arguments:
        <token> (<string>)      - <a specific jwt string for each user>
        <channel_id> (<int>)      - <unique integer for each channel>
        <message> (<str>)      - <message that will be sent>
        
        
    Exceptions:
        InputError  - Occurs when
            Token is not valid
            channel_id is not valid
            messaeg is over 1000 characters
            Standup is inactive
        AccessError - Occurs when
            User is not part of channel

    Return Value:
        Returns {}
    '''
    channel_index = next((index for (index, d) in enumerate(data['channels']) if d["channel_id"] == channel_id), None)
    if channel_index is None:
        raise InputError("Channel ID is not a valid channel")
    u_id = decode_token(token) # decode uid
    user_index = next((index for (index, d) in enumerate(data['users']) if d["auth_user_id"] == u_id), None)  
    if user_index is None:
        raise InputError("Invalid token")
    if u_id not in data['channels'][channel_index]['members'][0]['members_id']:
        raise AccessError("User not in channel")
    if len(message) > 1000:
        raise InputError("Message over 1000 characters")
    if data['channels'][channel_index]['standup']['active'] is False:
        raise InputError('Standup not running currently')
    handle_str = data['users'][user_index]['handle_str']
    total_message = handle_str + ": " + message
    data['channels'][channel_index]['standup']['messages'].append(total_message)
    return {}