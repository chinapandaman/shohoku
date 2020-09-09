# -*- coding: utf-8 -*-

from app import app
from flask import render_template
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
                "event_thumb": "https://hhsvoyager.org/wp-content/uploads/2020/01/New-NBA-Logo-1.png",
            }
            for each in promoted_events
        ],
        nba_events=[
            {
                "event_id": each["event_id"],
                "event_thumb": "https://hhsvoyager.org/wp-content/uploads/2020/01/New-NBA-Logo-1.png",
            }
            for each in nba_events
        ],
    )
