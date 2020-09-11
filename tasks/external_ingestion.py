# -*- coding: utf-8 -*-

import datetime
import json
import os
from datetime import timedelta

import requests
from pydal import DAL, Field


class ExternalIngestion(object):
    def __init__(self):
        self.db = DAL(
            "sqlite://../database/storage.sqlite",
            folder=os.path.join(os.path.dirname(__file__), "..", "database"),
        )

        self.db.define_table(
            "nba_event",
            Field("event_id", length=32),
            Field("event_title", length=512),
            Field("event_subtitle", length=512),
            Field("event_datetime", type="datetime"),
            Field("event_home_team", length=64),
            Field("event_away_team", length=64),
            Field("event_description", type="text"),
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

            db.nba_event.truncate()

            for each in events:
                event_datetime = datetime.datetime.strptime(
                    "{} {}".format(each["dateEvent"], each["strTime"]),
                    "%Y-%m-%d %H:%M:%S",
                )

                if event_datetime < datetime.datetime.utcnow():
                    continue

                next_day = (datetime.datetime.utcnow() + timedelta(days=1)).replace(
                    hour=7, minute=0, second=0, microsecond=0
                )

                if event_datetime > next_day:
                    continue

                db.nba_event.insert(
                    **{
                        "event_id": each["idEvent"],
                        "event_title": each["strEventAlternate"],
                        "event_subtitle": "{} Season {}".format(
                            each["strLeague"], each["strSeason"]
                        ),
                        "event_datetime": event_datetime,
                        "event_home_team": each["strHomeTeam"],
                        "event_away_team": each["strAwayTeam"],
                        "event_description": each["strFilename"],
                    }
                )

        db.commit()


if __name__ == "__main__":
    ExternalIngestion().load_events()
