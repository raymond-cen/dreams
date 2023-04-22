# Messaging Platform
This is a messaging platform written in Python that allows users to create their own accounts and directly message other users in channels. Some users are given admin powers that can delete other people's messages, join channels, and more.

## Installation
Clone the repository using git clone https://github.com/your-username/messaging-platform.git
Install the required dependencies using pip install -r requirements.txt
Run the server using python server.py
## Usage
The messaging platform has the following functionalities:

1. Create a new account: Users can create their own accounts by providing their username and password. Passwords are hashed for security purposes.

2. Log in: Users can log in to their account by providing their username and password. Upon successful login, users are given a token that allows them to use the server's functionalities.

3. Send a direct message: Users can send direct messages to other users by providing the recipient's username and the message.

4. Join a channel: Users can join a channel by providing the channel's name. Once a user joins a channel, they can see all messages sent to that channel.

5. Leave a channel: Users can leave a channel by providing the channel's name. Once a user leaves a channel, they will no longer see any messages sent to that channel.

6. Send a message to a channel: Users can send messages to a channel by providing the channel's name and the message.

7. Delete a message: Admin users can delete other people's messages by providing the message ID.

8. Log out: Users can log out of their account by removing their token from their cache or logging in from another window. Upon logout, users will need to re-login to use the server's functionalities.
