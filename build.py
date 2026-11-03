#!/usr/bin/env python3
"""Rebuilds index.html (the archive) from editions.json. Run: python3 build.py"""
import json, html, pathlib

root = pathlib.Path(__file__).parent
eds = sorted(json.loads((root / "editions.json").read_text()), key=lambda e: e["date"], reverse=True)

def item(e, latest=False):
    h = html.escape(e["headline"]); c = html.escape(e.get("category", "")); l = html.escape(e["label"])
    cls = "item latest" if latest else "item"
    tag = "Latest edition" if latest else l
    return f'''<a class="{cls}" href="{e["date"]}/">
  <span class="label">{tag}{" · " + c if c else ""}</span>
  <span class="h">{h}</span>
  <span class="meta">{l if latest else ""}{" · " if latest else ""}{e.get("minutes", 5)} min read</span>
</a>'''

items = "\n".join(item(e, i == 0) for i, e in enumerate(eds)) or "<p>No editions yet.</p>"

page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI Brief</title>
<meta name="robots" content="noindex,nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&family=Inter:wght@400;500;600&display=swap">
<style>
:root{{--bg:#fff;--fg:#1a1a1a;--muted:#6b6b6b;--rule:#e6e6e3;--soft:#f6f6f3;--accent:#1f5f5b;
--serif:"Source Serif 4",Charter,Georgia,serif;--sans:Inter,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color-scheme:light}}
@media (prefers-color-scheme:dark){{:root{{--bg:#121414;--fg:#e8e8e5;--muted:#9a9e9c;--rule:#2a2e2d;--soft:#1b1f1e;--accent:#7cc4bc;color-scheme:dark}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font-family:var(--serif);padding:32px 16px 64px}}
main{{max-width:680px;margin:0 auto}}
.mast{{font-family:var(--sans);border-bottom:1px solid var(--rule);padding-bottom:14px;margin-bottom:36px;display:flex;justify-content:space-between;align-items:baseline;gap:8px;flex-wrap:wrap}}
.mast b{{font-size:17px;font-weight:600}} .mast span{{font-size:13px;color:var(--muted)}}
.item{{display:block;text-decoration:none;color:inherit;padding:22px 0;border-bottom:1px solid var(--rule)}}
.item:hover .h{{color:var(--accent)}}
.label{{display:block;font-family:var(--sans);font-size:12px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);margin-bottom:8px}}
.h{{display:block;font-size:22px;line-height:1.3;font-weight:600;text-wrap:balance}}
.latest .h{{font-size:clamp(28px,5.5vw,38px);line-height:1.15;font-weight:700;letter-spacing:-.01em}}
.meta{{display:block;font-family:var(--sans);font-size:13px;color:var(--muted);margin-top:8px}}
</style></head><body><main>
<header class="mast"><b>AI Brief</b><span>A daily AI briefing · five-minute read</span></header>
{items}
</main></body></html>
'''
(root / "index.html").write_text(page)
print(f"index.html rebuilt with {len(eds)} edition(s)")
