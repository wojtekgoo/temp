import subprocess
import datetime
from links import COMMAND
"""
Quick Guide:
- Create venv as: python3 -m venv bot_venv
- source bot_venv/bin/activate
- pip install slack-sdk
- Keep it in the background with nohup:
    nohup $(python expirationbot.py) &
- OR use crontab -e: 
0 15 * * * /udir/wgusztyl/expiration_bot/bot_venv/bin/python3 /udir/wgusztyl/expiration_bot/expiration_bot.py
"""


# URL = "https://hooks.slack.com/services/{API_KEY}"
# context = ssl._create_unverified_context()
# webhook = WebhookClient(URL, ssl=context)
# COMMAND = [
#     "/usr/local/nom/bin/cat-feed",
#     "--type",
#     "raw",
#     "fresh-milk/alexa-whitelist-additions" ]

# TODO: return reason why domain was added to the whitelist
def retrieve_entries():
    result = subprocess.run(COMMAND, stdout=subprocess.PIPE)
    entries_raw = result.stdout.decode('utf-8')
    entries = entries_raw.split('\n')[:-1]
    entries_dict = {}
    for e in entries:
        entry = e.split()   # split Alexa entry per whitespaces ('reason' will be split into multiple fields)
        domain = entry[0].replace('.', '[.]')
        reason = ' '.join(entry[6:]) # merge 'reason' into one string
        expiration = None
        if entry[1] == "alexa-whitelist-additions":
            expiration = entry[3]
        if entry[2] == "alexa-whitelist-additions":
            expiration = entry[4]
        entries_dict[domain] = list()  # create key
        entries_dict[domain].extend([datetime.datetime\
            .utcfromtimestamp(float(expiration)), reason])  # assign two values (date, reason) to one key (domain)

    sorted_entries = {k: v for k, v in sorted(entries_dict.items(), key=lambda item: item[1][0])}  # sort dict based on date
    today_checks = []
    upcoming_checks = {}

    for k, v in sorted_entries.items():

        today = datetime.datetime.today().date()

        if v[0].date() == today:
            today_checks.append(k)

        elif (v[0].date() - today).days < 10:
            upcoming_checks[k] = list()
            upcoming_checks[k].extend([v[0].strftime('%Y-%m-%d'), v[1]])

    return today_checks, upcoming_checks


# if __name__ == "__main__":
#
#     while True:
#
#         today, upcoming = retrieve_entries()
#         results = ''.join([
#             "Domains expiring today:\n",
#             str(today)[:-1].replace('[', '').replace(',', '\n'),
#             "\nDomains expiring in the next 10 days:\n",
#             str(upcoming)[:-1].replace('{', '').replace("['", "").replace('],', '\n')
#         ])
#
#         response = webhook.send(text=results)
#         assert response.status_code == 200
#         assert response.body == "ok"
