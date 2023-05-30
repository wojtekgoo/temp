import requests
import json
import base64
import hashlib
from links import virus_total_v3, keys_to_remove, logger
'''https://github.com/b-fullam/Automating-VirusTotal-APIv3-for-IPs-and-URLs'''


def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature


def validate_vt_url_ioc(entity, api_key):
    summary_vt_entity_data = {}
    target_url = entity
    url_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
    url = virus_total_v3 + url_id
    headers = {
        "Accept": "application/json",
        "x-apikey": api_key
    }
    try:
        response = requests.request("GET", url, headers=headers)
        decoded_response = json.loads(response.text)

        url_unencrypted = ("http://" + target_url + "/")
        sha_signature = encrypt_string(url_unencrypted)
        vt_url_report_link = ("https://www.virustotal.com/gui/url/" + sha_signature)

        filtered_response = (decoded_response["data"]["attributes"])

        for key in keys_to_remove:
            filtered_response.pop(key, None)

        community_score = (decoded_response["data"]["attributes"]["last_analysis_stats"]["malicious"])
        total_vt_reviewers = (decoded_response["data"]["attributes"]["last_analysis_stats"]["harmless"]) + \
                             (decoded_response["data"]["attributes"]["last_analysis_stats"]["malicious"]) + (
                             decoded_response["data"]["attributes"]["last_analysis_stats"]["suspicious"]) + (
                             decoded_response["data"]["attributes"]["last_analysis_stats"]["undetected"]) + (
                             decoded_response["data"]["attributes"]["last_analysis_stats"]["timeout"])

        community_score_info = str(community_score) + "/" + str(total_vt_reviewers) + (
            "  :  security vendors flagged this as malicious")
        filtered_response['last_analysis_stats']['community_score_info'] = community_score_info
        if "last_analysis_stats" in filtered_response:
            summary_vt_entity_data['Virus Total Data'] = filtered_response['last_analysis_stats']
        if "categories" in filtered_response:
            summary_vt_entity_data['Virus Total Categories'] = filtered_response['categories']
        if "threat_names" in filtered_response:
            summary_vt_entity_data['Virus Total Threat Names'] = filtered_response['threat_names']
        if "title" in filtered_response:
            summary_vt_entity_data['Virus Total Page Title'] = filtered_response['title']
        if "reputation" in filtered_response:
            summary_vt_entity_data['Virus Total Reputation'] = filtered_response['reputation']
        summary_vt_entity_data['VT report link'] = vt_url_report_link
        logger.info("virus total Category check DONE: %s", entity)
        return summary_vt_entity_data
    except:
        summary_vt_entity_data = {"Virus Total Data": "domain" + entity + " has no Virus Total data"}
        logger.info("virus total Category check failed %s", entity)
        return summary_vt_entity_data
