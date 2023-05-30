import ssl
from slack_sdk.webhook import WebhookClient
import logging
import time
import datetime

timestamp = str(int(time.time()))
current_date = str(datetime.date.today())

main_path = " /var/nom/feeds/raw/fresh-milk/"
main_path_test = "/Users/gkochner/work/"
project_path = main_path + "carrier_whitelist/"
project_path_arc = project_path + "arc"
today_expired_domains_carrier = project_path + "today_expired_domains" + "_" + current_date + ".txt"
three_days_expired_domains_carrier = project_path + "three_days_expired_domains" + "_" + current_date + ".txt"
checked_expired_domains = project_path + "checked_expired_domains.csv"
carrier_intel = main_path + "tps-malware/"
carrier_intel_command = "/usr/local/nom/bin/cat-feed --type raw fresh-milk/tps-malware fresh-milk/tps-phishing fresh-milk/tps-botnet fresh-milk/tps-spam | grep "
api_key_vt = '1f65e0a384968e78bc332777a6d3152428dca91099fc09617ccf31d117a0c3fd'
virus_total_v3 = "https://www.virustotal.com/api/v3/urls/"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler('carrier_whitelist_log.log')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

keys_to_remove = [
    "favicon",
    "redirection_chain",
    "last_http_response_content_sha256",
    "last_http_response_code",
    "last_analysis_results",
    "last_final_url",
    "last_http_response_content_length",
    "url",
    "last_analysis_date",
    "tags",
    "last_submission_date",
    "last_http_response_headers",
    "last_modification_date",
    "has_content",
    "outgoing_links",
    "first_submission_date",
    "total_votes",
    "type",
    "id",
    "links",
    "trackers",
    "last_http_response_cookies",
    "html_meta",
    "times_submitted"
]

URL = "https://hooks.slack.com/services/{API_KEY}"
context = ssl._create_unverified_context()
webhook = WebhookClient(URL, ssl=context)
COMMAND = [
    "/usr/local/nom/bin/cat-feed",
    "--type",
    "raw",
    "fresh-milk/alexa-whitelist-additions"]