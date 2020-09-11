# -*- coding: utf-8 -*-

from app import app
from flask import render_template, url_for
from modules.current import Current


@app.route("/")
def index():
    db = Current().db

    events = db(db.nba_event.id > 0).select()
    promoted_events = events if len(events) <= 2 else events[:2]
    nba_events = events if len(events) <= 6 else events[:6]

    return render_template(
        "index.html",
        promoted_events=[
            {
                "event_id": each["event_id"],
                "event_title": each["event_title"],
                "event_thumb": url_for(
                    "static", filename="temp/{}.png".format(each["event_id"])
                ),
            }
            for each in promoted_events
        ],
        nba_events=[
            {
                "event_id": each["event_id"],
                "event_thumb": url_for(
                    "static", filename="temp/{}.png".format(each["event_id"])
                ),
            }
            for each in nba_events
        ],
    )
