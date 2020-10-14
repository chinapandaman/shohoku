# -*- coding: utf-8 -*-

import os

from pydal import DAL, Field


class Current(object):
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

        self.db.define_table(
            "nfl_event",
            Field("event_id", length=32),
            Field("event_title", length=512),
            Field("event_subtitle", length=512),
            Field("event_datetime", type="datetime"),
            Field("event_home_team", length=64),
            Field("event_away_team", length=64),
            Field("event_description", type="text"),
        )

        self.db.define_table(
            "mlb_event",
            Field("event_id", length=32),
            Field("event_title", length=512),
            Field("event_subtitle", length=512),
            Field("event_datetime", type="datetime"),
            Field("event_home_team", length=64),
            Field("event_away_team", length=64),
            Field("event_description", type="text"),
        )
