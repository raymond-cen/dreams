import json
import time
import mysql.connector

data = {
    'users': [
    ],
   'channels': [
    ],
    'dm': [
    ],
    'message': {
        'most_recent_id': 0,
        'message_info': []
    }
}

# with open('data.json', 'r') as file:
#     data = json.loads(file.read())


def add_new_user(new_user):
    data['users'].append(new_user)

def reset_message():
    new = {
        'most_recent_id': 0,
        'message_info': []
    } 
    data['message'] = new



mydb = mysql.connector.connect(
    host="localhost",
    user = "root",
    passwd="123456qwerty",
    database ="user_id"
)
mycursor = mydb.cursor()

# mycursor.execute('SHOW TABLES')
# SELECT MAX(Id) FROM Table
# for db in mycursor:
#     print(db)

# mycursor.execute("SELECT channel_id, channel_name FROM channels")
# result = mycursor.fetchall()
# for channel_info in result:
#     output = {
#         "channel_id": channel_info[0],
#         "name": channel_info[1]
#     }
#     print(channel_info)