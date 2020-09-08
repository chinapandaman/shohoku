# -*- coding: utf-8 -*-

from app import app
from flask import abort, render_template
from modules.current import Current


@app.route("/generic/<event_id>")
def generic(event_id):
    db = Current().db

    event = db(db.nba_event.event_id == event_id).select().first()

    more_events = db(db.nba_event.event_id != event_id).select()

    if len(more_events) > 3:
        more_events = more_events[:3]

    if not event:
        abort(404)

    return render_template(
        "generic.html",
        event_title=event["event_title"],
        event_subtitle=event["event_subtitle"],
        event_link="http://givemenbastreams.com/nba.php?g={}".format(
            event["event_home_team"].lower()
        ),
        event_description=event["event_description"],
        more_events=[
            {
                "event_id": each["event_id"],
                "event_title": each["event_title"],
                "event_thumb": "https://hhsvoyager.org/wp-content/uploads/2020/01/New-NBA-Logo-1.png",
            }
            for each in more_events
        ],
    )
