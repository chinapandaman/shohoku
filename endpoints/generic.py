# -*- coding: utf-8 -*-

from app import app
from flask import abort, render_template, url_for
from modules.current import Current


@app.route("/generic/<event_id>")
def generic(event_id):
    db = Current().db

    nba_event = db(db.nba_event.event_id == event_id).select().first()
    nfl_event = db(db.nfl_event.event_id == event_id).select().first()
    mlb_event = db(db.mlb_event.event_id == event_id).select().first()

    external_link = "http://givemenbastreams.com/nba.php?g={}"

    if nfl_event:
        external_link = "https://nflwebcast.com/verses/{}.html"

    if mlb_event:
        external_link = "http://givemenbastreams.com/mlb.php?g={}"

    event = nba_event or nfl_event or mlb_event

    more_nba_events = db(db.nba_event.event_id != event_id).select().as_list()
    more_nfl_events = db(db.nfl_event.event_id != event_id).select().as_list()
    more_mlb_events = db(db.mlb_event.event_id != event_id).select().as_list()

    for each in more_nba_events:
        each["event_type"] = "nba_event"

    for each in more_nfl_events:
        each["event_type"] = "nfl_event"

    for each in more_mlb_events:
        each["event_type"] = "mlb_event"

    more_events = more_nba_events + more_nfl_events + more_mlb_events

    if len(more_events) > 3:
        more_events = more_events[:3]

    if not event:
        abort(404)

    return render_template(
        "generic.html",
        event_title=event["event_title"],
        event_subtitle=event["event_subtitle"],
        event_link=external_link.format(
            event["event_home_team"].lower().split(" ")[-1]
        ),
        event_description=event["event_description"],
        more_events=[
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
            for each in more_events
        ],
    )
