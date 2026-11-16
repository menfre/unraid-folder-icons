#!/usr/bin/env python3
"""Genererer animerte SVG-mappeikoner for Unraid FolderView2.

Kjør:  python3 generate.py   -> skriver svg/*.svg og preview.html
Alle ikoner deler samme flis (mørk, avrundet, svak glød i aksentfargen),
så det er bare `ICONS` nederst du trenger å endre for å justere et ikon.
"""
from pathlib import Path

OUT = Path(__file__).parent / "svg"

# Unraid-farger: logoen går fra rød til oransje, venstre mot høyre.
# Sett UNIFORM = False for å bruke fargen hvert ikon har i ICONS.
UNIFORM = True
RED, ORANGE = "#e22828", "#ff8c2f"
GLOW = "#f15a2c"      # glød og kantlinje (gradient fungerer ikke der)
LIGHT = "#ffe2cc"     # lys "blink"-farge i animasjonene
TINTS = ["#ede9fe", "#e0f2fe", "#ffe4e6", "#fef3c7", "#ecfdf5", "#eff6ff", "#fdf2f8"]

TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{bg1}"/><stop offset="1" stop-color="{bg2}"/></linearGradient>
<linearGradient id="acc" gradientUnits="userSpaceOnUse" x1="20" y1="30" x2="108" y2="98"><stop offset="0" stop-color="{red}"/><stop offset="1" stop-color="{orange}"/></linearGradient>
<radialGradient id="glow" cx="50%" cy="45%" r="60%"><stop offset="0" stop-color="{glow}" stop-opacity=".38"/><stop offset="1" stop-color="{glow}" stop-opacity="0"/></radialGradient>
</defs>
<style>
*{{transform-box:fill-box;transform-origin:center}}
.s{{fill:none;stroke:{c};stroke-width:7;stroke-linecap:round;stroke-linejoin:round}}
.f{{fill:{c}}}
.glow{{animation:glow 4s ease-in-out infinite}}
@keyframes glow{{50%{{opacity:.45}}}}
{css}
</style>
<rect x="4" y="4" width="120" height="120" rx="28" fill="url(#bg)"/>
<rect class="glow" x="4" y="4" width="120" height="120" rx="28" fill="url(#glow)"/>
<rect x="5" y="5" width="118" height="118" rx="27" fill="none" stroke="{glow}" stroke-opacity=".4" stroke-width="2"/>
{body}
</svg>
"""


def sparkle(cx, cy, r):
    k = r * 0.1
    return (f"M{cx} {cy-r} C{cx+k} {cy-k*3} {cx+k*3} {cy-k} {cx+r} {cy} "
            f"C{cx+k*3} {cy+k} {cx+k} {cy+k*3} {cx} {cy+r} "
            f"C{cx-k} {cy+k*3} {cx-k*3} {cy+k} {cx-r} {cy} "
            f"C{cx-k*3} {cy-k} {cx-k} {cy-k*3} {cx} {cy-r}Z")


ICONS = {
    # ---------------------------------------------------------------- AI
    "ai-tools": dict(c="#a78bfa", css="""
.big{animation:pulse 3s ease-in-out infinite}
.tw{animation:tw 2.4s ease-in-out infinite}
.tw2{animation-delay:1.2s}
@keyframes pulse{50%{transform:scale(.82) rotate(20deg)}}
@keyframes tw{0%,100%{transform:scale(.3);opacity:.2}50%{transform:scale(1);opacity:1}}
""", body=f"""
<path class="f big" d="{sparkle(60, 68, 32)}"/>
<path class="f tw" d="{sparkle(92, 38, 12)}" fill="#ede9fe"/>
<path class="f tw tw2" d="{sparkle(96, 92, 8)}"/>
"""),

    # ---------------------------------------------------- Home Automation
    "home-automation": dict(c="#2dd4bf", css="""
.w{stroke-width:6;animation:wave 2.4s ease-in-out infinite;opacity:.15}
.w2{animation-delay:.4s}
.dot{animation:wave 2.4s ease-in-out infinite;animation-delay:-.4s}
@keyframes wave{0%,15%{opacity:.15}35%,70%{opacity:1}100%{opacity:.15}}
""", body="""
<path class="s" d="M28 66 L64 36 L100 66"/>
<path class="s" d="M40 58 V98 H88 V58"/>
<circle class="f dot" cx="64" cy="88" r="4.5"/>
<path class="s w" d="M55.5 79.5 A12 12 0 0 1 72.5 79.5"/>
<path class="s w w2" d="M48.4 72.4 A22 22 0 0 1 79.6 72.4"/>
"""),

    # ------------------------------------------------------------- Bots
    "bots": dict(c="#38bdf8", css="""
.eye{animation:blink 4s infinite}
.ant{animation:ant 1.6s ease-in-out infinite}
@keyframes blink{0%,44%,52%,100%{transform:scaleY(1)}48%{transform:scaleY(.1)}}
@keyframes ant{50%{fill:#e0f2fe;transform:scale(1.35)}}
""", body="""
<path class="s" d="M64 46 V34"/>
<circle class="f ant" cx="64" cy="29" r="5.5"/>
<rect class="s" x="34" y="46" width="60" height="46" rx="13"/>
<path class="s" d="M26 62 V76 M102 62 V76"/>
<ellipse class="f eye" cx="52" cy="65" rx="5.5" ry="7"/>
<ellipse class="f eye" cx="76" cy="65" rx="5.5" ry="7"/>
<path class="s" d="M55 81 H73" stroke-width="5"/>
"""),

    # ---------------------------------------------------- Media Servers
    "media-servers": dict(c="#fb7185", css="""
.play{animation:play 2.2s ease-in-out infinite}
.bar{animation:bar 1.1s ease-in-out infinite;transform-origin:bottom}
.b2{animation-delay:-.35s}.b3{animation-delay:-.7s}
@keyframes play{50%{transform:scale(1.18);fill:#ffe4e6}}
@keyframes bar{50%{transform:scaleY(.35)}}
""", body="""
<rect class="s" x="26" y="32" width="76" height="54" rx="9"/>
<path class="s" d="M50 100 H78 M64 86 V100"/>
<path class="f play" d="M56 47 L76 59 L56 71Z" stroke="#fb7185" stroke-width="4" stroke-linejoin="round"/>
<rect class="f bar" x="86" y="62" width="4" height="16" rx="2" opacity=".55"/>
<rect class="f bar b2" x="38" y="62" width="4" height="16" rx="2" opacity=".55"/>
<rect class="f bar b3" x="44" y="66" width="4" height="12" rx="2" opacity=".55"/>
"""),

    # ------------------------------------------------- Media Automation
    "media-automation": dict(c="#fbbf24", css="""
.arrow{animation:drop 2s cubic-bezier(.5,0,.5,1) infinite}
.tray{animation:tray 2s ease-out infinite}
@keyframes drop{0%{transform:translateY(-12px);opacity:.25}20%{opacity:1}50%,85%{transform:translateY(0);opacity:1}100%{transform:translateY(4px);opacity:.25}}
@keyframes tray{0%,50%{stroke:#fbbf24}60%{stroke:#fef3c7}80%,100%{stroke:#fbbf24}}
""", body="""
<g class="arrow"><path class="s" d="M64 30 V72 M48 57 L64 73 L80 57"/></g>
<path class="s tray" d="M30 76 V96 H98 V76"/>
"""),

    # ---------------------------------------------------------- Database
    "database": dict(c="#34d399", css="""
.lv{animation:lv 2.4s ease-in-out infinite}
.l2{animation-delay:.3s}.l3{animation-delay:.6s}
@keyframes lv{0%,40%,100%{stroke:#34d399}20%{stroke:#ecfdf5}}
""", body="""
<ellipse class="s lv" cx="64" cy="38" rx="28" ry="10"/>
<path class="s" d="M36 38 V90 M92 38 V90"/>
<path class="s lv l1" d="M36 55 A28 10 0 0 0 92 55"/>
<path class="s lv l2" d="M36 72 A28 10 0 0 0 92 72"/>
<path class="s lv l3" d="M36 90 A28 10 0 0 0 92 90"/>
"""),

    # ----------------------------------------------------------- Network
    "network": dict(c="#60a5fa", css="""
.pk{fill:none;stroke:#eff6ff;stroke-width:6;stroke-linecap:round;stroke-dasharray:6 76;animation:pk 2.6s linear infinite}
.n{animation:n 2.6s ease-in-out infinite}
.n2{animation-delay:.87s}.n3{animation-delay:1.73s}
@keyframes pk{to{stroke-dashoffset:-164}}
@keyframes n{0%,100%{transform:scale(1)}15%{transform:scale(1.25)}}
""", body="""
<path class="s" d="M64 36 L90 86 L38 86 Z" stroke-width="5" stroke-opacity=".55"/>
<path class="pk" d="M64 36 L90 86 L38 86 Z"/>
<circle class="s n" cx="64" cy="36" r="10" fill="#1f2a3c" stroke-width="6"/>
<circle class="s n n2" cx="90" cy="86" r="10" fill="#141b2b" stroke-width="6"/>
<circle class="s n n3" cx="38" cy="86" r="10" fill="#141b2b" stroke-width="6"/>
"""),

    # ------------------------------------------------------ Game Servers
    "game-servers": dict(c="#f472b6", css="""
.btn{animation:btn 1.6s ease-in-out infinite}
.btn2{animation-delay:.8s}
.pad{animation:tilt 3s ease-in-out infinite}
@keyframes btn{0%,100%{fill:#f472b6}50%{fill:#fdf2f8;transform:scale(1.3)}}
@keyframes tilt{25%{transform:rotate(-4deg)}75%{transform:rotate(4deg)}}
""", body="""
<g class="pad">
<path class="s" d="M42 46 H86 C99 46 105 57 107 72 C109 87 103 96 95 96 C89 96 85 90 81 84 H47 C43 90 39 96 33 96 C25 96 19 87 21 72 C23 57 29 46 42 46Z"/>
<path class="s" d="M35 70 H51 M43 62 V78" stroke-width="6"/>
<circle class="f btn" cx="84" cy="64" r="5"/>
<circle class="f btn btn2" cx="94" cy="75" r="5"/>
</g>
"""),

    # ------------------------------------------- Egne apper (hjemmesnekret)
    "egne-apper": dict(c="#a3e635", css="""
.cur{animation:cur 1.1s steps(1) infinite}
.pr{animation:pr 3s ease-in-out infinite}
@keyframes cur{50%{opacity:0}}
@keyframes pr{0%,100%{transform:translateX(0)}50%{transform:translateX(3px)}}
""", body="""
<rect class="s" x="24" y="32" width="80" height="64" rx="11"/>
<path class="s" d="M24 50 H104" stroke-width="5"/>
<circle class="f" cx="36" cy="41" r="3"/><circle class="f" cx="46" cy="41" r="3" opacity=".6"/><circle class="f" cx="56" cy="41" r="3" opacity=".35"/>
<path class="s pr" d="M38 62 L48 71 L38 80"/>
<rect class="f cur" x="56" y="76" width="22" height="6" rx="3"/>
"""),
}

LABELS = {
    "ai-tools": "AI tools", "home-automation": "Home Automation", "bots": "Bots",
    "media-servers": "Media Servers", "media-automation": "Media Automation",
    "database": "Database", "network": "Network", "game-servers": "Game Servers",
    "egne-apper": "Egne apper (ny)",
}


def main():
    OUT.mkdir(exist_ok=True)
    for name, d in ICONS.items():
        d = dict(d, red=RED, orange=ORANGE)
        if UNIFORM:
            for key in ("css", "body"):
                d[key] = d[key].replace(d["c"], "url(#acc)")
                for t in TINTS:
                    d[key] = d[key].replace(t, LIGHT)
                d[key] = d[key].replace("#1f2a3c", "#262626").replace("#141b2b", "#1a1a1a")
            d.update(c="url(#acc)", glow=GLOW, bg1="#2c2c2c", bg2="#141414")
        else:
            d.update(glow=d["c"], bg1="#283246", bg2="#111726")
        (OUT / f"{name}.svg").write_text(TEMPLATE.format(**d))

    cards = "\n".join(
        f'<div class="card"><img src="svg/{n}.svg" width="128"><div class="sm">'
        f'<img src="svg/{n}.svg" width="48"><img src="svg/{n}.svg" width="32"></div>'
        f'<span>{LABELS[n]}</span><code>{n}.svg</code></div>' for n in ICONS)
    (OUT.parent / "preview.html").write_text(f"""<!doctype html><meta charset="utf-8">
<title>Unraid mappeikoner</title>
<style>
body{{font:14px system-ui;margin:0;padding:24px;background:#f2f2f2;color:#222}}
body.dark{{background:#1c1c1c;color:#ddd}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:16px}}
.card{{display:flex;flex-direction:column;align-items:center;gap:8px;padding:16px;border-radius:12px;background:#0001}}
.sm{{display:flex;gap:12px;align-items:center}} code{{opacity:.6;font-size:12px}}
button{{margin-bottom:16px}}
</style>
<button onclick="document.body.classList.toggle('dark')">Bytt lys/mørk bakgrunn</button>
<div class="grid">{cards}</div>
""")
    print(f"Skrev {len(ICONS)} ikoner til {OUT}")


if __name__ == "__main__":
    main()
