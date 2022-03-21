# RoleBot
RoleBot's current features include:

- An event listener that triggers when a role change happens that will add or remove a role based on whether a user has two other required roles or not.
- A /slash command to manually check all users (suitable for if the bot has downtime or for when it first joins)

# Important
Make sure to change all variables in the file RoleBot.py to their relevant values.

# TOKEN
There are 3 options:
- Edit "token" in bot.run() to manually input the token
- Create a .env file and insert the token with the variable name TOKEN
- Setup AWS Secrets Manager and edit the secret_name variable in get_secret()

# Ubuntu VM (AWS) Setup

1) sudo apt-get install python3.7
2) sudo apt install python3-pip
3) pip install -U discord
4) pip install -U discord-py-slash-command
5) pip install python-dotenv (optional: if using .env)
6) pip install boto3 (optional: if using AWS Secrets Manager)
7) Navigate to the folder with RoleBot.py in it
8) Run python3 RoleBot.py


# Local Setup

1) Install Python 3.7
2) pip install -U discord
3) pip install -U discord-py-slash-command
4) pip install python-dotenv (optional: if using .env)
5) Navigate to the folder with RoleBot.py in it
6) Open a terminal
7) Run py .\RoleBot.py or python .\RoleBot.py or python3 .\RoleBot.py

After a few seconds, to establish the connection, the bot will be active and can be used immediately. 

Other versions of Python should work and if you use a different version, remove the first line in the file.
