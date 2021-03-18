from datetime import datetime
from dataclasses import dataclass
from dataclasses_json import dataclass_json
import json
import os

from requests_html import HTMLSession
import requests


@dataclass_json
@dataclass
class Program:
    station: str
    start_at: datetime
    end_at: datetime
    title: str
    act: str


SKIP = ("JOCK", "JOAK-FM", "RN1", "RN2", "HOUSOU-DAIGAKU")

now = datetime.now()
ses = HTMLSession()


def nhk():
    r = requests.get(
        f"https://api.nhk.or.jp/r5/pg/list/4/230/all/{now.date().isoformat()}.json"
    )
    stations = r.json()["list"]
    r1 = stations["r1"]
    r2 = stations["r2"]
    fm = stations["r3"]
    all = r1 + r2 + fm

    def extract(item):
        return Program(
            station=item["service"]["name"],
            start_at=datetime.fromisoformat(item["start_time"]),
            end_at=datetime.fromisoformat(item["end_time"]),
            title=item["title"],
            act=item["act"],
        )

    return [extract(item) for item in all]


def datetime_from_h_m(hour: str, minute: str):
    hour, minute = int(hour), int(minute)
    exceeds = hour >= 24
    hour = hour - 24 if exceeds else hour
    day = now.day + 1 if exceeds else now.day
    return now.replace(day=day, hour=hour, minute=minute, second=0, microsecond=0)


def radiko_time(time: str):
    start, end = time.split(" ～ ")
    start_h, start_m = start.split(":")
    end_h, end_m = end.split(":")
    return datetime_from_h_m(start_h, start_m), datetime_from_h_m(end_h, end_m)


def radiko():
    r = ses.get("https://radiko.jp/index/JP23/")
    rows_container = r.html.find(".program-table__items", first=True)
    stations = rows_container.find(".item-outer")
    programs: list[Program] = []
    for s in stations:
        station_name = s.attrs["data-station_id"]
        if station_name in SKIP:
            continue
        items = s.find(".item a")
        for item in items:
            title = item.find(".title", first=True).text
            cast = item.find(".cast", first=True).text
            time = item.find(".time", first=True).text
            start_at, end_at = radiko_time(time)
            programs.append(
                Program(
                    station=station_name,
                    start_at=start_at,
                    end_at=end_at,
                    title=title,
                    act=cast,
                )
            )
    return programs


def scrape():
    all = nhk() + radiko()
    with open(
        os.path.join("server", "data", now.date().isoformat() + ".json"), "w"
    ) as f:
        f.write(json.dumps([prog.to_dict() for prog in all], default=str))


if __name__ == "__main__":
    scrape()
