# -*- coding: utf-8 -*-


import random

from app import app
from flask import render_template, url_for
from modules.current import Current


@app.route("/")
def index():
    db = Current().db

    nba_events = db(db.nba_event.id > 0).select().as_list()
    nfl_events = db(db.nfl_event.id > 0).select().as_list()
    mlb_events = db(db.mlb_event.id > 0).select().as_list()

    for each in nba_events:
        each["event_type"] = "nba_event"

    for each in nfl_events:
        each["event_type"] = "nfl_event"

    for each in mlb_events:
        each["event_type"] = "mlb_event"

    event_list = nba_events + nfl_events + mlb_events

    promoted_events = (
        random.sample(event_list, 2) if len(event_list) > 2 else event_list
    )
    nba_events_shown = nba_events if len(nba_events) <= 6 else nba_events[:6]
    nfl_events_shown = nfl_events if len(nfl_events) <= 6 else nfl_events[:6]
    mlb_events_shown = mlb_events if len(mlb_events) <= 6 else mlb_events[:6]

    return render_template(
        "index.html",
        promoted_events=[
            {
                "event_id": each["event_id"],
                "event_title": each["event_title"],
                "event_thumb": url_for(
                    "static",
                    filename="temp/{}/{}.png".format(
                        each["event_type"], each["event_id"]
                    ),
                ),
            }
            for each in promoted_events
        ],
        nba_events=[
            {
                "event_id": each["event_id"],
                "event_thumb": url_for(
                    "static",
                    filename="temp/{}/{}.png".format(
                        each["event_type"], each["event_id"]
                    ),
                ),
            }
            for each in nba_events_shown
        ],
        nfl_events=[
            {
                "event_id": each["event_id"],
                "event_thumb": url_for(
                    "static",
                    filename="temp/{}/{}.png".format(
                        each["event_type"], each["event_id"]
                    ),
                ),
            }
            for each in nfl_events_shown
        ],
        mlb_events=[
            {
                "event_id": each["event_id"],
                "event_thumb": url_for(
                    "static",
                    filename="temp/{}/{}.png".format(
                        each["event_type"], each["event_id"]
                    ),
                ),
            }
            for each in mlb_events_shown
        ],
    )
