# -*- coding: utf-8 -*-


from app import app
from flask import render_template, url_for
from modules.common import Common


@app.route("/")
def index():
    common = Common()
    events_by_type = common.get_events_grouped_by_type()

    promoted_events = common.get_promoted_events()
    nba_events_shown = events_by_type["nba_event"]
    nfl_events_shown = events_by_type["nfl_event"]
    mlb_events_shown = events_by_type["mlb_event"]

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
