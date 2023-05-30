import json
from links import logger, project_path, current_date
from datetime import datetime
import pandas as pd
import os
import shutil
from pathlib import Path


def create_json_summary_data(data, domain):
    json_object = json.dumps(data, indent=4)
    file = project_path + "results/summary_" + domain + "_" + current_date + ".json"
    with open(file, "w") as outfile:
        outfile.write(json_object)
    logger.info("crete json done: %s", domain)


def json_summary_data(data):
    json_object = json.dumps(data, indent=4)
    file = project_path + "results/summary_expired_domains_" + current_date + ".json"
    with open(file, "w") as outfile:
        outfile.write(json_object)
    logger.info("crete json done")


def extract_domains_from_text_file(text_file):
    domains = []
    with open(text_file, 'r') as file:
        for line in file:
            if ':' in line:
                domain = line.split(':')[0].strip().strip("'").replace("]", "").replace("[", "")
            else:
                domain = line.strip().strip("'").replace("]", "").replace("[", "")
            domains.append(domain)
    logger.info("domains were extracted from txt files")
    return domains


def update_domain_csv(text_file, csv_file):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # existing_domains = set(pd.read_csv(csv_file, usecols=['Domain'])['Domain'])
    Path(csv_file).touch()

    if Path(csv_file).stat().st_size == 0:
        existing_domains = set()
    else:
        # Read the CSV file
        existing_domains = set(pd.read_csv(csv_file, usecols=['Domain'])['Domain'])

    new_domains = []

    domains = extract_domains_from_text_file(text_file)

    for domain in domains:
        if domain not in existing_domains:
            new_domains.append(domain)
            existing_domains.add(domain)

    new_data = pd.DataFrame({'Domain': new_domains, 'Time Added': current_time})

    # new_data.to_csv(csv_file, mode='a', header=not pd.read_csv(csv_file).empty, index=False)
    new_data.to_csv(csv_file, index=False)
    logger.info("csv with domains was created")
    return new_domains


def move_old_file_to_arc(file_path, destination_folder):
    filename = os.path.basename(file_path)
    destination_path = os.path.join(destination_folder, filename)
    shutil.move(file_path, destination_path)
    logger.info("files were moved to archive")
