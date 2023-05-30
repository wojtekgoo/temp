from VT_detections_whitelist import validate_vt_url_ioc
from links import logger, api_key_vt, three_days_expired_domains_carrier, today_expired_domains_carrier, \
    checked_expired_domains, project_path_arc
import argparse
from general_tools import create_json_summary_data, update_domain_csv, move_old_file_to_arc
from check_new_carrier_intel import check_domain_terminal


def main():
    domain_name = {}
    summary_data = {}
    today_new_domains = update_domain_csv(today_expired_domains_carrier, checked_expired_domains)
    three_days_new_domains = update_domain_csv(three_days_expired_domains_carrier, checked_expired_domains)
    new_domains = today_new_domains + three_days_new_domains
    for domain in new_domains:
        check_carrier_intel = check_domain_terminal(domain)
        vt_detections = validate_vt_url_ioc(domain, api_key_vt)
        domain_name["domain_name"] = domain
        summary_data_domain = {**domain_name, **vt_detections, **check_carrier_intel}
        create_json_summary_data(summary_data_domain, domain)
        summary_data[domain] = summary_data_domain

        logger.info("Done : " + domain)
    return summary_data


if __name__ == '__main__':
    main()
    move_old_file_to_arc(today_expired_domains_carrier, project_path_arc)
    move_old_file_to_arc(three_days_expired_domains_carrier, project_path_arc)

