# -*- coding: utf-8 -*-

import datetime
import json
import os

import requests
from pydal import DAL, Field


class ExternalIngestion(object):
    def __init__(self):
        self.db = DAL(
            "sqlite://../database/storage.sqlite",
            folder=os.path.join(os.path.dirname(__file__), "..", "database"),
        )

        self.db.define_table(
            "nba_events",
            Field("event_datetime", type="datetime"),
            Field("event_home_team", length=64),
            Field("event_away_team", length=64),
        )

        self.event_id = 4387
        self.api = "https://www.thesportsdb.com/api/v1/json/1/eventsnextleague.php?id={}".format(
            self.event_id
        )

    def load_events(self):
        db = self.db

        api_response = requests.get(self.api)

        if api_response.status_code == 200:
            events = json.loads(api_response.content)["events"]

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
