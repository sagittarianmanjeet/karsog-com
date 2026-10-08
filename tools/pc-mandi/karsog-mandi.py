#!/usr/bin/env python3
"""karsog.com mandi rates — PC helper.

Runs on Manjeet's Ubuntu PC (systemd user timer, ~10 min after the PC starts, then every 4 hours while it
stays on). It downloads today's Himachal mandi prices from data.gov.in over the home connection, which
data.gov.in accepts, and hands them to the karsog.com Worker at /api/mandi/ingest.

Needs only Python 3 (standard library). The data.gov.in API key is read from
~/.config/karsog-mandi/key (one line, file readable only by you). The same key authorises the hand-over,
because the Worker already holds it as its DATA_GOV_KEY secret.

Log: ~/.local/state/karsog-mandi/log.txt   Manual run: python3 ~/.local/share/karsog-mandi/karsog-mandi.py
"""
import json
import os
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

RESOURCE_ID = "9ef84268-d588-465a-a308-a864a43d0070"
SOURCES = [
    f"https://www.data.gov.in/backend/dataapi/v1/resource/{RESOURCE_ID}",
    f"https://api.data.gov.in/resource/{RESOURCE_ID}",
]
INGEST_URL = "https://karsog.com/api/mandi/ingest"
STATES = ["Himachal Pradesh"]
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36 "
      "(karsog.com mandi rates; +https://karsog.com/mandi-rates/)")

HOME = Path.home()
KEY_FILE = HOME / ".config/karsog-mandi/key"
STATE_DIR = HOME / ".local/state/karsog-mandi"
LOG_FILE = STATE_DIR / "log.txt"
TRIES = 6            # network may not be up right after boot
WAIT_BETWEEN = 60    # seconds


def log(msg):
    line = time.strftime("%Y-%m-%d %H:%M:%S ") + msg
    print(line, flush=True)
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        old = LOG_FILE.read_text().splitlines()[-300:] if LOG_FILE.exists() else []
        LOG_FILE.write_text("\n".join(old + [line]) + "\n")
    except OSError:
        pass


def get_json(url, timeout=60):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA, "Accept": "application/json", "Referer": "https://www.data.gov.in/"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def pull(base, key):
    records = []
    for state in STATES:
        offset, total = 0, None
        for _ in range(40):
            q = urllib.parse.urlencode({"api-key": key, "format": "json", "limit": "1000",
                                        "offset": str(offset), "filters[state.keyword]": state})
            j = get_json(f"{base}?{q}")
            if j.get("status") not in (None, "ok"):
                raise RuntimeError(f"data.gov.in said: {str(j.get('message') or j.get('status'))[:120]}")
            recs = j.get("records") or []
            total = int(j.get("total") or 0)
            records += recs
            offset += len(recs)
            if not recs or offset >= total:
                break
    return records


def pull_any(key):
    errors = []
    for base in SOURCES:
        host = urllib.parse.urlparse(base).hostname
        try:
            recs = pull(base, key)
            return recs, host
        except urllib.error.HTTPError as e:
            errors.append(f"{host} HTTP {e.code}")
        except Exception as e:  # network down, timeout, bad JSON
            errors.append(f"{host} {type(e).__name__}: {str(e)[:100]}")
    raise RuntimeError(" | ".join(errors))


def hand_over(key, records, host):
    body = json.dumps({"key": key, "from": f"{socket.gethostname()} via {host}", "records": records}).encode()
    req = urllib.request.Request(INGEST_URL, data=body, method="POST", headers={
        "Content-Type": "application/json", "User-Agent": "karsog-mandi-pc/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"karsog.com HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:200]}")


def main():
    try:
        key = KEY_FILE.read_text().strip()
    except OSError:
        log(f"No API key: put your data.gov.in key in {KEY_FILE}")
        return 2
    if not key:
        log(f"Empty API key file: {KEY_FILE}")
        return 2

    last = ""
    for attempt in range(1, TRIES + 1):
        try:
            records, host = pull_any(key)
            if not records:
                log(f"data.gov.in ({host}) returned no Himachal prices yet; will try again next run")
                return 0
            res = hand_over(key, records, host)
            if res.get("ok"):
                log(f"OK: {len(records)} prices from {host}, karsog.com saved {res.get('saved')}")
                return 0
            raise RuntimeError(f"karsog.com answered: {json.dumps(res)[:200]}")
        except Exception as e:
            last = str(e)[:300]
            if attempt < TRIES:
                log(f"try {attempt}/{TRIES} failed ({last}); retrying in {WAIT_BETWEEN}s")
                time.sleep(WAIT_BETWEEN)
    log(f"FAILED after {TRIES} tries: {last}")
    return 1


if __name__ == "__main__":
    if "--once" in sys.argv:   # used by the installer's test run: no retries
        TRIES = 1
    sys.exit(main())
