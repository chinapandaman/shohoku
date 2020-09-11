# -*- coding: utf-8 -*-

import datetime
import json
import os
from datetime import timedelta
from io import BytesIO

import requests
from PIL import Image
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

    @staticmethod
    def build_thumb(away_team_badge_url, home_team_badge_url, event_id):
        away_response = requests.get(away_team_badge_url)
        home_response = requests.get(home_team_badge_url)

        away_image = Image.open(BytesIO(away_response.content))
        home_image = Image.open(BytesIO(home_response.content))

        final_image = Image.new(
            "RGB", (away_image.width + home_image.width, away_image.height)
        )
        final_image.paste(away_image, (0, 0))
        final_image.paste(home_image, (away_image.width, 0))
        final_image.save(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "static",
                "temp",
                "{}.png".format(event_id),
            )
        )

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
            for each in os.listdir(
                os.path.join(os.path.dirname(__file__), "..", "static", "temp")
            ):
                os.remove(
                    os.path.join(
                        os.path.join(os.path.dirname(__file__), "..", "static", "temp"),
                        each,
                    )
                )

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

                team_api = (
                    "https://www.thesportsdb.com/api/v1/json/1/lookupteam.php?id={}"
                )

                away_team_badge_url = json.loads(
                    requests.get(team_api.format(each["idAwayTeam"])).content
                )["teams"][0]["strTeamBadge"]
                home_team_badge_url = json.loads(
                    requests.get(team_api.format(each["idHomeTeam"])).content
                )["teams"][0]["strTeamBadge"]

                self.build_thumb(
                    away_team_badge_url, home_team_badge_url, each["idEvent"]
                )

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
