# -*- coding: utf-8 -*-

import datetime
import json

import requests
from modules.current import Current


class ExternalIngestion(object):
    def __init__(self):
        self.event_id = 4387

    def load_events(self):
        db = Current().db

        api_response = requests.get(
            "https://www.thesportsdb.com/api/v1/json/1/eventsnextleague.php?id={}".format(
                self.event_id
            )
        )

        if api_response.status_code == 200:
            events = json.loads(api_response.content)["events"]

            db.nba_events.truncate()

            for each in events:
                db.nba_events.insert(
                    **{
                        "event_datetime": datetime.datetime.strptime(
                            "{} {}".format(each["dateEvent"], each["strTime"]),
                            "%Y-%m-%d %H:%M:%S",
                        ),
                        "event_home_team": each["strHomeTeam"],
                        "event_away_team": each["strAwayTeam"],
                    }
                )

        db.commit()


if __name__ == "__main__":
    ExternalIngestion().load_events()
