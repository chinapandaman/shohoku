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
            "nba_events",
            Field("event_datetime", type="datetime"),
            Field("event_home_team", length=64),
            Field("event_away_team", length=64),
        )
