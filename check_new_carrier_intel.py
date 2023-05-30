import pandas as pd
import json
from links import carrier_intel_command, logger
import subprocess


def process_file_csv(file_path, domain_list, output_file):
    # Read the file into a pandas DataFrame
    df = pd.read_csv(file_path, sep='\t', header=None,
                     names=['Domain', 'TPS', 'Val1', 'Val2', 'Val3', 'Val4', 'Description'])

    # Filter the DataFrame based on the domain list
    filtered_df = df[df['Domain'].isin(domain_list)]

    if not filtered_df.empty:
        # Append the filtered DataFrame to the output file
        filtered_df.to_csv(output_file, index=False, mode='a')
    else:
        # Append the original DataFrame to the output file without the header
        df.to_csv(output_file, index=False, mode='a', header=False)


def process_file_json(file_path, domain_name):
    with open(file_path, 'r') as file:
        file_data = file.readlines()

    results = []
    for line in file_data:
        domain, tps, val1, val2, val3, val4, desc = line.strip().split('\t')
        result = {
            'Domain': domain_name,
            'TPS': tps,
            'Val1': val1,
            'Val2': val2,
            'Val3': val3,
            'Val4': val4,
            'Description': desc
        }
        results.append(result)

    json_data = json.dumps(results)
    return json_data


def check_domain_terminal(domain):
    json_data = {}
    command = carrier_intel_command + domain
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.stdout.strip():
        print(result.stdout.strip())
        json_data["Domain in Carrier intel"] = True
        logger.info("the domain " + domain + " exists in carrier intel")
        return json_data
    else:
        json_data["Domain in Carrier intel"] = False
        logger.info("the domain "+domain+" doesn't exist in carrier intel")
        return json_data
