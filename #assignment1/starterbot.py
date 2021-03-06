import os
import threading
import time
import re
from threading import Timer
from slackclient import SlackClient
import tweepy
from tweepy import OAuthHandler
import json
import schedule

# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "Show trends"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

consumer_key = 'Pqa4IkRATQIQI5cmeoku9uSmc'
consumer_secret = 'sQ0RfURq56xQIxU4Zo3EbsMtYuN127YeujlR5aXnznwatkUkYr'
access_token = '878801066749378560-xxVM1tzuOBSSwlPVYrtEGcpHuPFSWzO'
access_secret = '51qMwcwcOoBZwQqtWIpIKFOROGgjphpdZTAR80DhvbRwD'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

# Where On Earth ID for Global is 1.
WOE_ID = 1

trends = api.trends_place(WOE_ID)

trends = json.loads(json.dumps(trends, indent=1))

trendy = []
for trend in trends[0]["trends"]:
    trendy.append(trend["name"])

trending = ' \n'.join(trendy[:10])


def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None


def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def output(command, channel):
    """
        Executes bot command if the command is known
    """

    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    if command.startswith(EXAMPLE_COMMAND):
        response = "Today's top ten trending are: \n"+ trending
    else:
        response = "Sorry, please ask something else."

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

    threading.Timer(600, output1).start()
    threading.Timer(600, output2).start()

def output1():
    """
        Executes bot command if the command is known
    """

    command = "Top Ten trends in Philippines."

    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sorry, please ask something else."
    else:
        response = "Today's top ten trending are: \n"+trending

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel='general',
        text=response or default_response
    )

    threading.Timer(600, output1).start()
    threading.Timer(600, output2).start()

#t = Timer(600, output1)
#t.start()
#schedule.every(10).minutes.do(output1)
#threading.Timer(600, output1).start()

def output2():
    """
        Executes bot command if the command is known
    """

    command = "Top Ten trends in Philippines."

    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sorry, please ask something else."
    else:
        response = "Today's top ten trending are: \n"+trending

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel='assignment1',
        text=response or default_response
    )

    threading.Timer(600, output1).start()
    threading.Timer(600, output2).start()


#t2 = Timer(600, output2)
#t2.start()
#schedule.every(10).minutes.do(output2)
#threading.Timer(600, output2).start()

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        threading.Timer(600, output1).start()
        threading.Timer(600, output2).start()
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                output(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
