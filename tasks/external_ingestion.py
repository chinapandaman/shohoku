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
            Field("event_id", length=32),
            Field("event_title", length=512),
            Field("event_subtitle", length=512),
            Field("event_datetime", type="datetime"),
            Field("event_home_team", length=64),
            Field("event_away_team", length=64),
            Field("event_thumb", type="text"),
        )

        self.event_id = 4387

    def load_events(self):
        db = self.db

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
                        "event_id": each["idEvent"],
                        "event_title": each["strEventAlternate"],
                        "event_subtitle": "{} {}".format(
                            each["strLeague"], each["strSeason"]
                        ),
                        "event_datetime": datetime.datetime.strptime(
                            "{} {}".format(each["dateEvent"], each["strTime"]),
                            "%Y-%m-%d %H:%M:%S",
                        ),
                        "event_home_team": each["strHomeTeam"],
                        "event_away_team": each["strAwayTeam"],
                        "event_thumb": each["strThumb"],
                    }
                )

        db.commit()


if __name__ == "__main__":
    ExternalIngestion().load_events()
