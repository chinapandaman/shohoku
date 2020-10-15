# -*- coding: utf-8 -*-

from app import app
from flask import abort, render_template, url_for
from modules.common import Common


@app.route("/generic/<event_id>")
def generic(event_id):
    common = Common()

    event = common.get_event_by_event_id(event_id)

    more_events = common.get_event_other_than_event_id(event_id)

    if not event:
        abort(404)

    return render_template(
        "generic.html",
        event_title=event["event_title"],
        event_subtitle=event["event_subtitle"],
        event_link=event["event_external_link"].format(
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
