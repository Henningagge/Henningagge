#!/usr/bin/env python3
"""Render a Boot.dev profile card as SVG from the public profile API."""
import base64
import json
import sys
import urllib.request
from html import escape

HANDLE = "henningagge"
API = f"https://api.boot.dev/v1/users/public/{HANDLE}"
OUT = "assets/bootdev-card.svg"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "profile-card"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read()


def main():
    user = json.loads(fetch(API))["data"]
    stats = json.loads(fetch(f"{API}/stats"))["data"]

    avatar = base64.b64encode(fetch(user["profileImageURL"])).decode()
    xp_in_level = user["xpTotalForLevel"] - user["xpForLevel"]
    progress = max(0.0, min(1.0, xp_in_level / user["xpTotalForLevel"]))
    bar_w = 240

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="400" height="172" viewBox="0 0 400 172" role="img" aria-label="Boot.dev profile of {escape(user['firstName'])}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#1b2438"/>
      <stop offset="1" stop-color="#0f1626"/>
    </linearGradient>
    <clipPath id="av"><circle cx="64" cy="64" r="36"/></clipPath>
  </defs>
  <style>
    text {{ font-family: 'Segoe UI', Ubuntu, Helvetica, Arial, sans-serif; fill: #ffffff; }}
    .muted {{ fill: #8b95a9; font-size: 12px; }}
    .name {{ font-size: 20px; font-weight: 700; }}
    .role {{ fill: #E4A11B; font-size: 13px; font-weight: 600; }}
    .stat {{ font-size: 15px; font-weight: 600; }}
  </style>
  <rect width="400" height="172" rx="10" fill="url(#bg)"/>
  <text x="20" y="24" class="muted">boot.dev</text>
  <circle cx="64" cy="76" r="39" fill="none" stroke="#E4A11B" stroke-width="2"/>
  <g transform="translate(0,12)"><image href="data:image/png;base64,{avatar}" x="28" y="28" width="72" height="72" clip-path="url(#av)" preserveAspectRatio="xMidYMid slice"/></g>
  <text x="124" y="62" class="name">{escape(user['firstName'])} {escape(user['lastName'])}</text>
  <text x="124" y="82" class="role">{escape(user['role'])} · Level {user['level']}</text>
  <rect x="124" y="94" width="{bar_w}" height="6" rx="3" fill="#2a3550"/>
  <rect x="124" y="94" width="{bar_w * progress:.1f}" height="6" rx="3" fill="#E4A11B"/>
  <text x="124" y="116" class="muted">{user['xp']:,} XP</text>
  <text x="124" y="148" class="stat">{stats['lessonsCompleted']:,}</text>
  <text x="124" y="162" class="muted" style="font-size:10px">lessons</text>
  <text x="214" y="148" class="stat">Top {stats['leaderboardXPPercentileAlltime']}%</text>
  <text x="214" y="162" class="muted" style="font-size:10px">all-time XP</text>
</svg>
"""
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    sys.exit(main())
