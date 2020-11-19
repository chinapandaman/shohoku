# -*- coding: utf-8 -*-


from app import app
from flask import render_template, url_for
from modules.common import Common


@app.route("/")
def index():
    common = Common()
    events_by_type = common.get_events_grouped_by_type()

    promoted_events = common.get_promoted_events()

    results = []

    for event_type, events in events_by_type.items():
        result_body = {
            "type": event_type,
            "is_active": False,
            "display_name": event_type.split("_")[0].upper(),
            "events": [
                {
                    "event_id": event["event_id"],
                    "event_title": event["event_title"],
                    "event_thumb": url_for(
                        "static",
                        filename="temp/{}/{}.png".format(
                            event["event_type"], event["event_id"]
                        ),
                    ),
                }
                for event in events
            ],
        }
        results.append(result_body)

    results[0]["is_active"] = True

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
        results=results,
    )
