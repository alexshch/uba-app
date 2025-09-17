# utils.py
import json
from datetime import datetime
from typing import List, Dict
import math

def read_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)

def iso_to_dt(s):
    # безопасно парсит ISO
    try:
        return datetime.fromisoformat(s.replace("Z","+00:00"))
    except Exception:
        return None

def time_of_day(dt):
    if dt is None: return None
    return dt.hour + dt.minute/60.0

def is_night(dt):
    if dt is None: return False
    return dt.hour < 6 or dt.hour >= 22

def sessionize(events):
    """
    aggregates events by session_id into a list of session dicts
    """
    sessions = {}
    for e in events:
        sid = e.get("session_id") or f"{e.get('user')}-{e.get('host')}"
        if sid not in sessions:
            sessions[sid] = {
                "session_id": sid,
                "user": e.get("user"),
                "host": e.get("host"),
                "events": []
            }
        # enrich time
        dt = iso_to_dt(e.get("timestamp"))
        e["_dt"] = dt.isoformat() if dt else None
        e["_hour"] = dt.hour if dt else None
        e["_is_night"] = is_night(dt)
        sessions[sid]["events"].append(e)
    # compute session-level meta
    out = []
    for sid, s in sessions.items():
        evs = sorted(s["events"], key=lambda x: x.get("timestamp") or "")
        start = iso_to_dt(evs[0].get("timestamp"))
        end = iso_to_dt(evs[-1].get("timestamp"))
        s["start"] = start.isoformat() if start else None
        s["end"] = end.isoformat() if end else None
        s["duration_sec"] = (end - start).total_seconds() if start and end else 0
        out.append(s)
    return out
