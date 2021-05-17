import time
from src.data import data
from src.auth import decode_token, check_email
from src.error import InputError, AccessError

# helper functions
def find_user(search_type, search_for):
    ls = []
    for i in range(0, len(data['users'])):
        ls.append(data['users'][i][search_type])

    if search_for not in ls:        
        return -1  
    else:
        return ls.index(search_for)

def user_profile_v1(token, u_id):
    '''<Get a user's profile>

    Arguments:
        <token> (<string>)      - <a specific jwt string for each user>
        <u_id> (<int>)    - <a specific number for each user>
        ...

    Exceptions:
        InputError  - Occurs when 
            User with u_id is not a valid user
        AccessError - Occurs when 
            token given contains a invalid auth_user_id

    Return Value:
        Returns <dict contains user_id, email, first name, last name, and handle> 
        on <valid u_id with a valid token>
    '''    
    auth_id = decode_token(token)    
    if find_user('auth_user_id', auth_id) == -1:
        raise AccessError('Incorrect access')
    if u_id is not None and find_user('auth_user_id', int(u_id)) == -1:
        raise InputError('Not a valid u_id')
    user_index = next((index for (index, d) in enumerate(data['users']) if d["auth_user_id"] == auth_id), None)
    found_user = data['users'][user_index]
    return {
        'user': {
            'u_id': found_user['auth_user_id'],
            'email': found_user['email'],
            'name_first': found_user['name_first'],
            'name_last': found_user['name_last'],
            'handle_str': found_user['handle_str'],
        },
    }

def user_profile_setname_v1(token, name_first, name_last):
    '''
    <Update the authorised user's first and last name>

    Arguments:
        <token> (<string>)          - <a specific jwt string for each user>
        <name_first> (<string>)     - <user's first name>
        <name_last> (<string>)      - <user's last name>

    Exceptions:
        InputError  - Occurs when 
            name_first is not between 1 and 50 characters inclusively in length
            name_last is not between 1 and 50 characters inclusively in length
        AccessError - Occurs when 
            token given contains a invalid auth_user_id

    Return Value:
        Returns <empty dictionary> on <token contains a valid id with valid first and last names>
    '''
    # Invalid long or short first name
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError('Not a valid first name')
    # Invalid long or short last name
    if len(name_last) < 1 or len(name_last) > 50: 
        raise InputError('Not a valid last name')
    # token validation check
    auth_id = decode_token(token)
    num = find_user('auth_user_id', auth_id) 
    if num == -1:
        raise AccessError('token with invalid u_id')
    else:
        data['users'][num]['name_first'] = name_first
        data['users'][num]['name_last'] = name_last
        return {}

def user_profile_setemail_v1(token, email):
    '''
    <Update the authorised user's email address>

    Arguments:
        <token> (<string>)      - <a specific jwt string for each user>
        <email> (<string>)      - <user's email address>

    Exceptions:
        InputError  - Occurs when 
            Email entered is not a valid email 
            Email address is already being used by another user
        AccessError - Occurs when 
            token given contains a invalid auth_user_id

    Return Value:
        Returns <empty dictionary> on <token with a valid id and a valid email not been use by other users>
    '''
    # Invalid email
    if check_email(email) is not True:
        raise InputError('Not a valid email')
    # Search for existance of email         
    if find_user('email', email) > -1:
        raise InputError('Already exist email address for other user')
    # token validation check
    auth_id = decode_token(token)
    num = find_user('auth_user_id', auth_id) 
    if num == -1:
        raise AccessError('token with invalid u_id')
    else:
        data['users'][num]['email'] = email
    return {}

def user_profile_sethandle_v1(token, handle_str):
    '''
    <Update the authorised user's handle>

    Arguments:
        <token> (<string>)         - <a specific jwt string for each user>
        <handle_str> (<string>)    - <display name generated when registered>

    Exceptions:
        InputError  - Occurs when 
            handle_str is not between 3 and 20 characters inclusive
            handle is already used by another user
        AccessError - Occurs when 
            token given contains a invalid auth_user_id

    Return Value:
        Returns <empty dictionary> on <token with a valid id with a valid handle_str not been use by other users>
    '''
    # Invalid long or short handle
    if len(handle_str) < 3 or len(handle_str) > 20: 
        raise InputError('Not a valid ahandle')
    # Search for existance of email         
    if find_user('handle_str', handle_str) > -1:
        raise InputError('Already exist handle for other user')
    # token validation check
    auth_id = decode_token(token)
    num = find_user('auth_user_id', auth_id) 
    if num == -1:
        raise AccessError('token with invalid u_id')
    else:
        data['users'][num]['handle_str'] = handle_str
    return {}

def users_all_v1(token):
    '''
    <Get list of all users and their associated details>

    Arguments:
        <token> (<string>)      - <a specific jwt string for each user>

    Exceptions:
        AccessError - Occurs when 
            token with a invalid auth_user_id

    Return Value:
        Returns <list of all users and their associated details> on <valid token is given>
    '''
    auth_id = decode_token(token)       
    # token contains invalid u_id
    if find_user('auth_user_id', auth_id) == -1:
        raise AccessError('incorrect access')
    ret_ls = []
    for i in range(0, len(data['users'])):
        found_user = data['users'][i]
        new_user = {
            'u_id': found_user['auth_user_id'],
            'email': found_user['email'],
            'name_first': found_user['name_first'],
            'name_last': found_user['name_last'],
            'handle_str': found_user['handle_str'],
        }
        ret_ls.append(new_user)
    return {'users': ret_ls}


