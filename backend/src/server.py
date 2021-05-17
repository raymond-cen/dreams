import sys
from json import dumps
from flask import Flask, request
from flask_mail import Mail
from flask_mail import Message
from flask_cors import CORS
from src.error import InputError
from src import config
from src.auth import auth_login_v1, auth_register_v1, auth_logout_v1, auth_passwordreset_request_v1, auth_passwordreset_reset_v1
from src.channel import channel_join_v1, channel_messages_v1, channel_addowner_v1, channel_removeowner_v1, channel_details_v1, channel_invite_v1, channel_leave_v1
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
from src.user import users_all_v1, user_profile_v1
from src.user import user_profile_setname_v1, user_profile_setemail_v1, user_profile_sethandle_v1
from src.admin import admin_user_remove_v1, admin_userpermission_change_v1
from src.message import message_send_v2, message_edit_v2, message_remove_v1, message_senddm_v1, message_share_v1, message_unpin_v1
from src.message import message_sendlater_v1, message_sendlaterdm_v1, message_react_v1, message_unreact_v1, message_pin_v1, message_sendlaterdm_v1
from src.dm import dm_create_v1, dm_messages_v1, dm_details_v1, dm_leave_v1, dm_list_v1, dm_remove_v1, dm_invite_v1
from src.other import clear_v1, search_v1, notifications_get_v1
from src.standup import standup_start_v1, standup_active_v1, standup_send_v1
import src.data
from json import loads, dump
#testing git push
def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

def dump_data():
    with open('data.json', 'w') as file:
            file.write(dumps(src.data.data)) 

APP = Flask(__name__)
CORS(APP)


APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)
APP.config['MAIL_SERVER']='smtp.gmail.com'
APP.config['MAIL_PORT'] = 465
APP.config['MAIL_USERNAME'] = 'unswdreamsmessage@gmail.com'
APP.config['MAIL_PASSWORD'] = '123456qwerty!@#$%^'
APP.config['MAIL_USE_TLS'] = False
APP.config['MAIL_USE_SSL'] = True

mail = Mail(APP)
# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

@APP.route("/showdata", methods=['POST'])
def print_data():
    return dumps(src.data.data)

@APP.route("/auth/register/v2", methods=['POST'])
def auth_register():
    payload = request.get_json()
    resp = auth_register_v1(payload['email'], payload['password'], payload['name_first'], payload['name_last'])
    dump_data()
    return dumps(resp)

@APP.route("/auth/login/v2", methods=['POST'])
def auth_login():
    payload = request.get_json()
    resp = auth_login_v1(payload['email'], payload['password'])
    dump_data()
    return dumps(resp)

@APP.route("/auth/logout/v1", methods=['POST'])
def auth_logout():
    payload = request.get_json()
    resp = auth_logout_v1(payload['token'])
    dump_data()
    # print(src.data.data)
    return dumps(resp)

@APP.route("/auth/passwordreset/request/v1", methods=["POST"])
def auth_passwordreset_request():
    payload = request.get_json()

    email = payload['email']
    reset_code = auth_passwordreset_request_v1(email)  

    msg = Message('Password Reset Request', sender = 'unswdreamsmessage@gmail.com', recipients = [email])
    msg.body = f"reset code: {reset_code}" 
    mail.send(msg)
    return {} 
    
@APP.route("/auth/passwordreset/reset/v1", methods = ["POST"])
def auth_passwordreset_reset():
    payload = request.get_json()
    reset_code = payload['reset_code']
    new_password = payload['new_password']
    resp = auth_passwordreset_reset_v1(reset_code, new_password)
    dump_data()
    return dumps(resp)


@APP.route("/channel/join/v2", methods=['POST'])
def channel_join():
    payload = request.get_json()
    resp = channel_join_v1(payload['token'], int(payload['channel_id']))
    dump_data()
    return dumps(resp)

@APP.route("/channel/removeowner/v2", methods=['POST'])
def channel_removerowner():
    payload = request.get_json()   
    resp =  channel_removeowner_v1(payload['token'], int(payload['channel_id']), int(payload['u_id']))
    dump_data()
    return dumps(resp)

@APP.route("/channel/addowner/v1", methods=['POST'])  
def addowner():
    parameters = request.get_json()
    token = parameters['token']
    channel_id = int(parameters['channel_id'])
    u_id = parameters['u_id']
    resp = channel_addowner_v1(token, channel_id, u_id)
    dump_data()
    return dumps(resp)
    
@APP.route("/channels/create/v2", methods=["POST"])
def channel_create():
    payload = request.get_json()
    resp = channels_create_v1(payload["token"], payload["name"], payload["is_public"])
    dump_data()
    return dumps(resp)

@APP.route("/channels/list/v2", methods=["GET"])
def list_v2():
    payload = {
        "token": request.args.get("token")
    }
    channel_list = channels_list_v1(payload['token'])
    dump_data()
    return dumps(channel_list)

@APP.route("/channels/listall/v2", methods=["GET"])
def listall_v2():
    payload = {
        "token": request.args.get("token")
    }
    channel_list = channels_listall_v1(payload['token'])
    dump_data()
    return dumps(channel_list)

@APP.route("/user/profile/v2", methods=['GET'])
def user_profile():
    token = request.args.get("token")
    u_id = request.args.get("u_id")
    users = user_profile_v1(token, u_id)   
    dump_data()
    return dumps(users)

@APP.route("/user/profile/setname/v2", methods=['PUT'])
def profile_setname():
    payload = request.get_json()
    resp = user_profile_setname_v1(payload['token'], payload['name_first'], payload['name_last'])
    dump_data()
    return dumps(resp)

@APP.route("/user/profile/setemail/v2", methods=['PUT'])
def profile_setemail():
    payload = request.get_json()
    resp = user_profile_setemail_v1(payload['token'], payload['email'])
    dump_data()
    return dumps(resp)

@APP.route("/user/profile/sethandle/v1", methods=['PUT'])
def profile_sethandle():
    payload = request.get_json()
    resp = user_profile_sethandle_v1(payload['token'], payload['handle_str'])
    dump_data()
    return dumps(resp)

@APP.route("/users/all/v1", methods=['GET'])
def users_all():
    payload = {
        "token": request.args.get("token")
    }
    users = users_all_v1(payload['token'])
    dump_data()
    return dumps(users)

@APP.route("/admin/user/remove/v1", methods=['DELETE'])
def admin_user_remove():
    payload = request.get_json()
    # uid = []
    # for uid1 in payload['u_id']:
    #     uid.append(int(uid1))
    resp = admin_user_remove_v1(payload['token'], payload['u_id'])
    dump_data()
    return dumps(resp)

@APP.route("/message/send/v2", methods=['POST'])
def message_send():
    payload = request.get_json()
    resp = message_send_v2(payload['token'], int(payload['channel_id']), payload['message'])
    dump_data()
    return dumps(resp)

@APP.route("/message/remove/v1", methods=['DELETE'])
def message_remove():
    payload = request.get_json()
    resp = message_remove_v1(payload['token'], int(payload['message_id']))
    dump_data()
    return dumps(resp)


@APP.route("/message/edit/v2", methods=['PUT'])
def message_edit():
    payload = request.get_json()
    resp = message_edit_v2(payload['token'], int(payload['message_id']), payload['message'])
    dump_data()
    return dumps(resp)

@APP.route("/message/share/v1", methods=['POST'])
def message_share():
    payload = request.get_json()
    resp = message_share_v1(payload['token'], int(payload['og_message_id']), payload['message'],
            int(payload['channel_id']), int(payload['dm_id']))
    dump_data()
    return dumps(resp)

@APP.route("/message/senddm/v1", methods=['POST'])
def message_dm():
    payload = request.get_json()
    resp = message_senddm_v1(payload['token'], int(payload['dm_id']), payload['message'])
    dump_data()
    return dumps(resp)

@APP.route("/dm/create/v1", methods=['POST'])  
def dm_create():
    parameters = request.get_json()
    token = parameters['token']
    uid = []
    for uid1 in parameters['u_ids']:
        uid.append(int(uid1))
    resp = dm_create_v1(token, uid)
    dump_data()
    return dumps(resp)

@APP.route("/channel/messages/v2", methods=['GET'])
def channel_messages():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))
    resp = channel_messages_v1(token, channel_id, start)
    dump_data()
    return dumps(resp)
@APP.route("/dm/messages/v1", methods=["GET"])
def dm_messages():
    token = request.args.get('token')
    dm_id = int(request.args.get('dm_id'))
    start = int(request.args.get('start'))
    resp = dm_messages_v1(token, dm_id, start)
    dump_data()
    return dumps(resp)

@APP.route("/dm/details/v1", methods=["GET"])
def dm_details_v():
    token = request.args.get("token")
    dm_id = int(request.args.get("dm_id"))
    resp = dm_details_v1(token, dm_id)
    dump_data()
    return dumps(resp)


@APP.route("/dm/list/v1", methods=["GET"])
def dm_list():
    payload = {
        "token": request.args.get("token")
    }
    dm_list = dm_list_v1(payload["token"])
    dump_data()
    return dumps(dm_list)

@APP.route("/dm/remove/v1", methods=['DELETE'])
def dm_remove():
    payload = request.get_json()
    resp = dm_remove_v1(payload["token"], int(payload["dm_id"]))
    dump_data()
    return dumps(resp)

@APP.route("/dm/leave/v1", methods=["POST"])
def dm_leave():
    payload = request.get_json()
    token = payload["token"]
    dm_id = int(payload["dm_id"])
    resp = dm_leave_v1(token, dm_id)
    dump_data()
    return dumps(resp)

@APP.route("/clear/v1", methods=["DELETE"])
def clear():
    return clear_v1()

@APP.route("/channel/details/v2", methods=["GET"])
def channel_details():
    payload = {
        "token": request.args.get("token"),
        "channel_id": request.args.get("channel_id")
    }
    resp = channel_details_v1(payload['token'], int(payload['channel_id']))
    return dumps(resp)
    
@APP.route("/channel/invite/v2", methods=["POST"])
def channel_invite():
    payload = request.get_json()
    resp = channel_invite_v1(payload['token'], int(payload['channel_id']), int(payload['u_id']))
    dump_data()
    return dumps(resp)

@APP.route("/channel/leave/v1", methods=["POST"])
def channel_leave():
    payload = request.get_json()
    resp = channel_leave_v1(payload['token'], int(payload['channel_id']))
    dump_data()
    return dumps(resp)

@APP.route("/dm/invite/v1", methods=["POST"])
def dm_invite():
    payload = request.get_json()
    resp = dm_invite_v1(payload['token'], int(payload['dm_id']), int(payload['u_id']))
    dump_data()
    return dumps(resp)

@APP.route("/admin/userpermission/change/v1", methods=["POST"])
def admin_userpermission_change():
    payload = request.get_json()
    resp = admin_userpermission_change_v1(payload['token'], int(payload['u_id']), int(payload['permission_id']))
    dump_data()
    return dumps(resp)

@APP.route("/search/v2", methods=["GET"])
def search():
    payload = {
        "token": request.args.get("token"),
        "query_str": request.args.get("query_str")
    }
    resp = search_v1(payload['token'], payload['query_str'])
    dump_data()
    return dumps(resp)

@APP.route("/notifications/get/v1", methods=["GET"])
def notifications_get():
    payload = {
        "token": request.args.get("token"),
    }
    return dumps(notifications_get_v1(payload['token']))

@APP.route("/standup/start/v1", methods=["POST"])
def standup_start():
    payload = request.get_json()
    resp = standup_start_v1(payload['token'], int(payload['channel_id']), int(payload['length']))
    dump_data()
    return dumps(resp)

@APP.route("/standup/active/v1", methods=["GET"])
def standup_active():
    payload = {
        "token": request.args.get("token"),
        "channel_id": request.args.get("channel_id")
    }
    resp = standup_active_v1(payload['token'], int(payload['channel_id']))
    dump_data()
    return dumps(resp)

@APP.route("/standup/send/v1", methods=["POST"])
def standup_send():
    payload = request.get_json()
    resp = standup_send_v1(payload['token'], int(payload['channel_id']), payload['message'])
    dump_data()
    return dumps(resp)

@APP.route("/message/sendlater/v1", methods=["POST"])
def message_sendlater():
    payload = request.get_json()
    resp = message_sendlater_v1(payload['token'], int(payload['channel_id']), payload['message'], int(payload['time_sent']))
    dump_data()
    return dumps(resp)

@APP.route("/message/sendlaterdm/v1", methods=["POST"])
def message_sendlaterdm():
    payload = request.get_json()
    resp = message_sendlaterdm_v1(payload['token'], int(payload['dm_id']), payload['message'], int(payload['time_sent']))
    dump_data()
    return dumps(resp)

@APP.route("/message/react/v1", methods=["POST"])
def message_react():
    payload = request.get_json()
    resp = message_react_v1(payload['token'], int(payload['message_id']), int(payload['react_id']))
    dump_data()
    return dumps(resp)

@APP.route("/message/unreact/v1", methods=["POST"])
def message_unreact():
    payload = request.get_json()
    resp = message_unreact_v1(payload['token'], int(payload['message_id']), int(payload['react_id']))
    dump_data()
    return dumps(resp)

@APP.route("/message/pin/v1", methods=["POST"])
def message_pin():
    payload = request.get_json()
    resp = message_pin_v1(payload['token'], int(payload['message_id']))
    dump_data()
    return dumps(resp)

@APP.route("/message/unpin/v1", methods=["POST"])
def message_unpin():
    payload = request.get_json()
    resp = message_unpin_v1(payload['token'], int(payload['message_id']))
    dump_data()
    return dumps(resp)


if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port
 
