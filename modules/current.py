# -*- coding: utf-8 -*-

import os

from pydal import DAL, Field


class Current(object):
    config = {
        "events": [
            {
                "event_type": "nba",
                "event_external_link": "http://givemenbastreams.com/nba.php?g={}",
            },
            {
                "event_type": "nfl",
                "event_external_link": "https://nflwebcast.com/verses/{}.html",
            },
            {
                "event_type": "mlb",
                "event_external_link": "http://givemenbastreams.com/mlb.php?g={}",
            },
        ]
    }

    def __init__(self):
        self.db = DAL(
            "sqlite://../database/storage.sqlite",
            folder=os.path.join(os.path.dirname(__file__), "..", "database"),
        )

        for each in self.config["events"]:
            self.db.define_table(
                "{}_event".format(each["event_type"]),
                Field("event_id", length=32),
                Field("event_title", length=512),
                Field("event_subtitle", length=512),
                Field("event_datetime", type="datetime"),
                Field("event_home_team", length=64),
                Field("event_away_team", length=64),
                Field("event_description", type="text"),
            )
