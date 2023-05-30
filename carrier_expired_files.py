from links import today_expired_domains_carrier, three_days_expired_domains_carrier, webhook
from carrier_expired_domains import retrieve_entries


if __name__ == "__main__":

    while True:

        today, upcoming = retrieve_entries()
        results_today = ''.join([
            str(today)[:-1].replace(',', '\n'),
        ])

        results_upcoming = ''.join([
            str(upcoming)[:-1].replace('{', '').replace("['", "").replace('],', '\n')
        ])

        with open(today_expired_domains_carrier, "w") as file:
            file.write(results_today + "\n")

        with open(three_days_expired_domains_carrier, "w") as file:
            file.write(results_upcoming + "\n")

        response = webhook.send(text=results_today)
        assert response.status_code == 200
        assert response.body == "ok"

        response = webhook.send(text=results_upcoming)
        assert response.status_code == 200
        assert response.body == "ok"


