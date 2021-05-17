"""
Registers user information into data.py through auth_register
and returns the user_id with correct information given through
user_login
"""
import re
import secrets
import jwt
import hashlib
import time 
import string
import random
from src.data import data, add_new_user, mycursor, mydb
from src.error import InputError
from src.data import data, add_new_user
from src.error import InputError, AccessError


# Check for email validation
regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'   
SECRET = 'OURSECRET'

def check_email(email):    
    valid = False
    if(re.search(regex,email)):
        valid = True
    return valid


# Search for specific elements in dictionary with same prefix as given
def prefix_search(list_d, test_for, prefix):
    count = 0
    for d in list_d:
        value = d[test_for]
        if type(value) is not int and value[0: len(prefix)] == prefix:
            count += 1
    
    return count 

''' 
    Generate handle string without whaitespace and '@'
    If full name longer than 20, end at the 20th character
    If other user with same first name and last name 
    add number from 0 to distinct the new user 
 '''
def handle_generate(name_first, name_last, u_ls):
    handle = ""
    length = len(name_first) + len(name_last)
    full_name = name_first.lower() + name_last.lower()
    if full_name.isalnum() == False:
        # Delete the whitespaces and '@'
        full_name = full_name.replace(' ', '')
        full_name = full_name.replace('@','')
        ls = full_name.splitlines()
        spe = ''
        full_name = spe.join(ls)
            
    if length < 20:
        handle = full_name
    else:         
        handle = full_name[0:20]
    #search for same name
    if len(u_ls) != 0:
        counter = prefix_search(u_ls, 'handle_str', handle)
        if counter != 0:
            handle += str(counter)

    return handle

def create_token(auth_user_id, session_num):
    payload = {
        "uid": auth_user_id,
        "session_id": session_num
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

def decode_token(string):
    uid = jwt.decode(string, SECRET, algorithms=["HS256"])
    return uid['uid']

    
def hash(string):
    return hashlib.sha256(string.encode()).hexdigest()


def auth_register_v1(email, password, name_first, name_last):    
    """
    <Register for a new user with given information>
    Arguments:
        <email> (<string>)     - <user's email address>
        <password> (<string>)  - <password of that email>
        <name_first> (<string>)- <user's first name>
        <name_last> (<string>) - <user's last name>

    Exceptions:
        InputError  - Occurs when 
        Email entered is not a valid email 
        Email address is already being used by another user
        Password entered is less than 6 characters long
        name_first is not 1-50 characters inclusively in length
        name_last is not 1-50 characters inclusively in length

    Return Value:
        Returns <auth_user_id> on <valid email, password, name_first and name_last>
    """
    u_ls = data.get('users')
    u_count = len(u_ls)
    # Set permission for global user is 1 and members is 2
    if u_count == 0:
        permission = 1
    else:
        permission = 2
    
    # Invalid email
    if check_email(email) is not True:
        raise InputError('Not a valid email')
    # Search for existance of email
    if u_count != 0:
        count = prefix_search(u_ls, 'email', email)
        if count > 0:
            raise InputError('Already exist email address')
    # Invalid short password
    if len(password) < 6:
        raise InputError('Password too short')
    # Invalid long or short first name
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError('Not a valid first name')
    # Invalid long or short last name
    if len(name_last) < 1 or len(name_last) > 50: 
        raise InputError('Not a valid last name')
    
    u_count += 1
    token = create_token(u_count, 1)

    # Create a new user
    new_user = {
        'auth_user_id' : u_count,
        'session_count': 1,
        'token': [token],        
        'email' : email,
        'password' : hash(password),
        'name_first' : name_first,   
        'name_last' : name_last,
        'permission': permission,
        'handle_str' : handle_generate(name_first, name_last, u_ls), 
    }
    add_new_user(new_user)

    sqlf = ("INSERT INTO users" 
            "(user_id, name_first, name_last, token, email, password, permission, handle_str) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
    user = (u_count, name_first, name_last, token, email, hash(password), permission, handle_generate(name_first, name_last, u_ls))
    mycursor.execute(sqlf, user)
    sqlf = "SELECT MAX(user_id) FROM users"
    mycursor.execute(sqlf)
    u_count1 = mycursor.fetchone()
    print(u_count1)
    sqlf = ("INSERT INTO tokens"
            "(token, user_id)"
            "VALUES (%s, %s)")
    tokens = (token, u_count1[0])
    mycursor.execute(sqlf, tokens)
    mydb.commit()
    return {
        'token': token,
        'auth_user_id': u_count1[0],        
    }


def check_user(email):
    """
    Checks if email exists and returns the password and id
    """
    for index, k in enumerate(data["users"]):
        if k["email"] == email:
            token = create_token(k['auth_user_id'], k['session_count'] + 1)

            return True, k["password"], {
                                        "token": token,
                                        "auth_user_id": k["auth_user_id"]
                                        }, index
    return False, False, False, False

def auth_login_v1(email, password):
    '''
    <Checks for valid and correct email and password and then returns user_id>
    Arguments:
        <email> (<string>)  - <email address of user>
        <password> (<int>)    - <password for user>

    Exceptions:
        InputError  - Occurs when email is in incorrect format or email does not belong to a user
                        or password is not correct

    Return Value:
        Returns the user_id of the user
    '''
    if re.search(regex, email) is None:
        raise InputError("Email entered is not a valid email")
    
    # Check for valid user and their information
    check_email, check_password, user_id, user_index = check_user(email)
    if check_email is False:
        raise InputError("Email entered does not belong to a user")
    if check_password != hash(password):
        raise InputError("Password is not correct")

    data['users'][user_index]['token'].append(user_id['token'])
    data['users'][user_index]['session_count'] += 1

    q = "SELECT user_id, email FROM users WHERE email = %s"
    mycursor.execute(q, (email,))
    myresult = mycursor.fetchone()
    sqlf = ("INSERT INTO tokens"
            "(token, user_id)"
            "VALUES (%s, %s)")
    tokens = (user_id['token'], myresult[0])
    mycursor.execute(sqlf, tokens)
    mydb.commit()
    return user_id

def auth_logout_v1(token):
    '''
    <Invalidates active token to log the user out>
    Arguments:
        <email> (<string>)  - <email address of user>
        <password> (<int>)    - <password for user>

    Exceptions:
        AccessError  - Occurs when invalid token is given

    Return Value:
        Returns <true> on <valid token, successfully logged out>
        Returns <false> on <invalid token is given>        
    '''
    for token_check in data['users']:
        if token in token_check['token']:
            token_check['token'].remove(token)
            sqlf = "DELETE FROM tokens WHERE token = %s"
            mycursor.execute(sqlf, (token,))
            mydb.commit()
            return {"is_success": True}
    raise AccessError


def auth_passwordreset_request_v1(email):
    #check if email is registered and return auth_user_id
    u_id = email_exists(email)
    if u_id != False:
        reset_code = get_random_string() 
        #add random string to that users dictionary

        #adding reset_code to user dictionary
        user_no = len(data['users'])
        i = 0
        while i < user_no:
            if (data['users'][i]['auth_user_id'] == u_id):
                data['users'][i]['password_reset'] = reset_code
            i+=1
        reset_code = str(u_id) + "/" + reset_code
        return reset_code

    else:
        email_list = "emails: "
        user_no = len(data['users'])
        i = 0

        while i < user_no:
            email_list = email_list + data['users'][i]['email']
            i+=1
        return email_list

def email_exists(email):
    user_no = len(data['users'])
    i = 0
    while i < user_no:
        if (data['users'][i]['email'] == email):
            return data['users'][i]['auth_user_id']
        i+=1

    return False

def auth_passwordreset_reset_v1(reset_code, new_password):
    if len(new_password) < 6:
        raise InputError("Password cannot be less than 6 characters")
    auth_id = int(reset_code.split("/")[0]) 

    #Check reset code
    for k in enumerate(data["users"]):
        if k["auth_user_id"] == auth_id:
            k["password"] = hash(new_password)
                                     
    return {}

def get_random_string():
    # choose from all letters
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(8))
    return result_str
