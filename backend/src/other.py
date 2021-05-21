from src.data import data, reset_message, mycursor, mydb
from src.auth import decode_token
from src.error import AccessError, InputError
from json import dumps
import time
def clear_v1():
    data['users'] = []
    data['channels'] = []
    data['dm'] = []    
    reset_message()
    sqld = "DELETE FROM users"
    mycursor.execute(sqld)
    sqld = "DELETE FROM tokens"
    mycursor.execute(sqld)
    sqld = "DELETE FROM channels"
    mycursor.execute(sqld)
    sqld = "DELETE FROM channel_members"
    mycursor.execute(sqld)
    mydb.commit()


def search_v1(token, query_str):
    if next((True for token_list in data['users'] if token in token_list['token']), False) is False:
        raise InputError("Invalid token")
    auth_user_id = decode_token(token)
    if len(query_str) > 1000:
        raise InputError('above 1000 characters')
    messages_list = []
    for message in data['message']['message_info']:
        if query_str in message['message']:
            if message['channel_id'] != -1:
                channel_index = next((index for (index, d) in enumerate(data['channels'])
                if d["channel_id"] == message['channel_id']), None)
                if auth_user_id in data['channels'][channel_index]['members'][0]['members_id']:
                    messages_list.append(message)
            else:
                dm_index = next((index for (index, d) in enumerate(data['dm']) 
                if d["dm_id"] == message['dm_id']), None)
                if auth_user_id in data['dm'][dm_index]['u_ids']:
                    messages_list.append(message)
    return {
        'messages': messages_list
    }

def notifications_get_v1(token):
    return {
        'notifications': [token]
    }
    