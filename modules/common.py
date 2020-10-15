# -*- coding: utf-8 -*-

import random

from modules.current import Current


class Common(object):
    def __init__(self):
        self.current = Current()
        db = self.current.db

        self.event_list = []

        for each in self.current.config["events"]:
            query_results = (
                db(db["{}_event".format(each["event_type"])].id > 0).select().as_list()
            )

            for every in query_results:
                every["event_type"] = "{}_event".format(each["event_type"])

            self.event_list += query_results

    def get_promoted_events(self):
        return (
            random.sample(self.event_list, 2)
            if len(self.event_list) > 2
            else self.event_list
        )

    def get_events_grouped_by_type(self):
        results = {
            "{}_event".format(each["event_type"]): []
            for each in self.current.config["events"]
        }

        for each in self.event_list:
            results[each["event_type"]].append(each)

        for k, v in results.items():
            if len(v) > 6:
                results[k] = v[:6]

        return results

    def get_event_by_event_id(self, event_id):
        for each in self.event_list:
            if each["event_id"] == event_id:
                for every in self.current.config["events"]:
                    if every["event_type"] in each["event_type"]:
                        each["event_external_link"] = every["event_external_link"]
                        return each

        return None

    def get_event_other_than_event_id(self, event_id):
        results = []

        for each in self.event_list:
            if each["event_id"] != event_id:
                results.append(each)

        return random.sample(results, 3) if len(results) > 3 else results
