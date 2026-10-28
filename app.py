import base64
import importlib
import json
import urllib.request
from datetime import date
from html import escape
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

import profile_data

# Streamlit keeps imported modules cached between reruns; reload so edits to
# profile_data.py always show up without restarting the app.
importlib.reload(profile_data)

from profile_data import (
    AFFILIATIONS,
    CERTIFICATIONS,
    COUNTRIES_VISITED,
    EDUCATION,
    EXPERIENCE,
    FLICKR_EMBED,
    FLICKR_PHOTO_COUNT,
    FLICKR_USER_ID,
    HOBBIES,
    LANGUAGES,
    PROFILE,
    PROJECTS,
    PUBLICATIONS,
    SKILLS,
)

ROOT = Path(__file__).parent
CAREER_START_YEAR = 2014

st.set_page_config(
    page_title=f"{PROFILE['name']} | Portfolio",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def html(markup):
    """Render raw HTML. Lines are stripped so Markdown never treats them as code blocks."""
    st.markdown("".join(line.strip() for line in markup.splitlines()), unsafe_allow_html=True)


def find_file(path_str):
    """Return the asset path if it exists, also trying common image extensions."""
    if not path_str:
        return None
    path = ROOT / path_str
    if path.exists():
        return path
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        alt = path.with_suffix(ext)
        if alt.exists():
            return alt
    return None


def image_data_uri(path):
    mime = "image/png" if path.suffix == ".png" else "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


@st.cache_data(ttl=3600, show_spinner=False)
def flickr_photos(user_id, count):
    """Latest public photos from Flickr's public feed (no API key needed)."""
    url = (
        "https://www.flickr.com/services/feeds/photos_public.gne"
        f"?id={user_id}&format=json&nojsoncallback=1"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (portfolio site)"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        raw = resp.read().decode("utf-8").replace("\\'", "'")
    items = json.loads(raw).get("items", [])[:count]
    return [
        {
            "title": item.get("title") or "Untitled",
            "link": item["link"],
            # _m is the small thumbnail; _z is 640px, sharp enough for the grid
            "src": item["media"]["m"].replace("_m.jpg", "_z.jpg"),
        }
        for item in items
    ]


def date_range(start, end):
    return f"{start} – {end}" if start else end


def chips(items):
    return "".join(f'<span class="chip">{escape(t)}</span>' for t in items)


def section_title(anchor, kicker, title):
    html(
        f"""
        <div class="section-head" id="{anchor}">
          <div class="kicker">{escape(kicker)}</div>
          <h2>{escape(title)}</h2>
          <div class="rule"></div>
        </div>
        """
    )


# ---------- Styles ----------
html(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
      :root {
        --navy: #0b1d3a;
        --navy-2: #13294f;
        --gold: #a9b4c6;
        --steel: #5f6f8a;
        --gold-soft: rgba(169, 180, 198, 0.14);
        --ink: #1d2433;
        --muted: #667085;
        --line: #e6e8ee;
        --paper: #f7f6f2;
        --card: #ffffff;
      }
      html, body, [data-testid="stAppViewContainer"] { background: var(--paper); }
      [data-testid="stAppViewContainer"] * { font-family: 'Inter', sans-serif; }
      .brand *, .hero h1 *, .section-head h2 *, .card h3 *, .contact h3 *, .stat .num * {
        font-family: 'Cormorant Garamond', serif !important;
      }
      [data-testid="stHeaderActionElements"], .stMarkdown h1 a, .stMarkdown h2 a, .stMarkdown h3 a { display: none !important; }
      [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu, footer,
      [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
      .block-container { max-width: 1080px; padding: 0 1.25rem 3rem 1.25rem; }
      [data-testid="stMarkdownContainer"] p { color: var(--ink); }
      a { color: var(--navy-2); }

      /* Pinned header */
      .pinbar {
        position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
        background: linear-gradient(135deg, var(--navy) 0%, var(--navy-2) 100%);
        box-shadow: 0 6px 24px -12px rgba(11,29,58,0.6);
      }
      .pinbar-inner {
        max-width: 1080px; margin: 0 auto; padding: 0.6rem 1.25rem;
        display: flex; align-items: center; justify-content: space-between; gap: 1rem;
      }
      .pin-id { display: flex; align-items: center; gap: 0.8rem; min-width: 0; }
      .pin-id img { width: 46px; height: 46px; border-radius: 50%; object-fit: cover; border: 2px solid var(--gold); }
      .pin-name { font-family: 'Cormorant Garamond', serif !important; font-size: 1.35rem; font-weight: 700; color: #fff; line-height: 1.1; }
      .pin-role { font-size: 0.78rem; color: rgba(255,255,255,0.7); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
      .pin-cta { padding: 0.45rem 1.1rem; }
      .pin-wa { background: #25d366; color: #fff !important; display: inline-flex; align-items: center; gap: 0.4rem; }
      .pin-wa:hover { background: #1ebe5b; }

      /* Tabs, pinned under the header */
      .block-container { padding-top: 136px !important; }
      .stTabs [role="tablist"] {
        position: fixed; top: 66px; left: 50%; transform: translateX(-50%); z-index: 900;
        width: min(1080px, 100%); padding: 0.6rem 1.25rem; gap: 0.35rem;
        background: var(--paper); box-shadow: 0 0 0 100vmax var(--paper); clip-path: inset(0 -100vmax);
        border-bottom: 1px solid var(--line);
        overflow-x: auto; scrollbar-width: none; display: flex;
      }
      .stTabs [role="tablist"]::-webkit-scrollbar { display: none; }
      [data-testid="stTabsScrollRight"], [data-testid="stTabsScrollLeft"] { display: none !important; }
      .stTabs [data-testid="stTab"] { box-shadow: none !important; border-bottom: none !important; }
      .stTabs [data-testid="stTab"] {
        height: auto; padding: 0.45rem 1rem; border-radius: 999px; background: transparent;
        white-space: nowrap; transition: background .2s ease; border: none;
      }
      .stTabs [data-testid="stTab"] p { font-size: 0.78rem !important; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: var(--ink); margin: 0; }
      .stTabs [data-testid="stTab"]:hover p { color: var(--gold); }
      .stTabs [data-testid="stTab"][aria-selected="true"] { background: var(--navy) !important; }
      .stTabs [data-testid="stTab"][aria-selected="true"] p { color: #fff !important; }
      .stTabs [role="tablist"] [data-testid="stTab"]::after, .stTabs [role="tablist"] > div:not([data-testid="stTab"]) { display: none !important; }
      .stTabs [role="tabpanel"] { padding-top: 0.5rem; }

      /* Hero */
      .hero {
        position: relative; overflow: hidden;
        display: flex; gap: 2.5rem; align-items: center;
        padding: 3rem 3rem; border-radius: 22px;
        background: radial-gradient(circle at 85% 15%, rgba(169, 180, 198,0.25), transparent 40%),
                    linear-gradient(135deg, var(--navy) 0%, var(--navy-2) 100%);
        color: #fff; box-shadow: 0 25px 60px -25px rgba(11, 29, 58, 0.55);
      }
      .hero::after {
        content: ""; position: absolute; right: -60px; bottom: -60px; width: 260px; height: 260px;
        border: 1px solid rgba(169, 180, 198,0.35); border-radius: 50%;
      }
      .hero img {
        width: 200px; height: 200px; border-radius: 50%; object-fit: cover; flex-shrink: 0;
        border: 4px solid var(--gold); box-shadow: 0 0 0 8px rgba(169, 180, 198,0.15);
      }
      .hero .eyebrow { color: var(--gold); font-size: 0.78rem; letter-spacing: 0.22em; text-transform: uppercase; font-weight: 600; }
      .hero h1 {
        font-family: 'Cormorant Garamond', serif !important; font-weight: 700;
        font-size: 3.4rem; line-height: 1.05; margin: 0.4rem 0 0.6rem 0; color: #fff; padding: 0;
      }
      .hero .role { font-size: 1.15rem; font-weight: 300; color: rgba(255,255,255,0.88); margin: 0; }
      .hero .loc { font-size: 0.9rem; color: rgba(255,255,255,0.6); margin-top: 0.4rem; }
      .btns { margin-top: 1.4rem; display: flex; flex-wrap: wrap; gap: 0.6rem; }
      .btn {
        display: inline-block; padding: 0.55rem 1.2rem; border-radius: 999px; font-size: 0.85rem;
        font-weight: 500; text-decoration: none !important; transition: all .2s ease;
      }
      .btn-gold { background: var(--gold); color: var(--navy) !important; }
      .btn-gold:hover { background: #c3ccd9; }
      .btn-ghost { border: 1px solid rgba(255,255,255,0.4); color: #fff !important; }
      .btn-ghost:hover { border-color: var(--gold); color: var(--gold) !important; }

      /* Stats */
      .stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin: 1.6rem 0 0.5rem 0; }
      .stat { background: var(--card); border: 1px solid var(--line); border-radius: 16px; padding: 1.2rem; text-align: center; }
      .stat .num { font-family: 'Cormorant Garamond', serif !important; font-size: 2.4rem; font-weight: 700; color: var(--navy); line-height: 1; }
      .stat .lbl { font-size: 0.75rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted); margin-top: 0.4rem; }

      /* Sections */
      .section-head { margin: 1.5rem 0 1.5rem 0; }
      .kicker { color: var(--steel); font-size: 0.75rem; letter-spacing: 0.22em; text-transform: uppercase; font-weight: 600; }
      .section-head h2 {
        font-family: 'Cormorant Garamond', serif !important; font-size: 2.4rem; font-weight: 700;
        color: var(--navy); margin: 0.2rem 0 0 0; padding: 0;
      }
      .rule { width: 56px; height: 3px; background: var(--steel); border-radius: 2px; margin-top: 0.7rem; }
      .about { font-size: 1.05rem; line-height: 1.8; color: var(--ink); max-width: 820px; }
      .about p { margin-bottom: 1rem; }

      /* Cards */
      .card {
        background: var(--card); border: 1px solid var(--line); border-radius: 16px;
        padding: 1.4rem 1.6rem; margin-bottom: 1rem; height: calc(100% - 1rem);
        transition: transform .2s ease, box-shadow .2s ease;
      }
      .card:hover { transform: translateY(-3px); box-shadow: 0 18px 40px -22px rgba(11,29,58,0.35); }
      .card h3 { font-family: 'Cormorant Garamond', serif !important; font-size: 1.45rem; font-weight: 700; color: var(--navy); margin: 0 0 0.3rem 0; padding: 0; }
      .card .sub { color: var(--ink); font-weight: 500; font-size: 0.95rem; }
      .card .meta { color: var(--muted); font-size: 0.82rem; margin-top: 0.15rem; }
      .card p, .card li { font-size: 0.93rem; line-height: 1.65; color: var(--ink); }
      .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; }
      .grid .card { margin: 0; height: auto; }

      /* Timeline */
      .timeline { position: relative; padding-left: 2rem; }
      .timeline::before { content: ""; position: absolute; left: 7px; top: 6px; bottom: 6px; width: 2px; background: linear-gradient(var(--gold), var(--line)); }
      .tl-item { position: relative; margin-bottom: 1.2rem; }
      .tl-item::before {
        content: ""; position: absolute; left: -2rem; top: 1.6rem; width: 16px; height: 16px; border-radius: 50%;
        background: var(--paper); border: 3px solid var(--gold);
      }
      .tl-item .card { height: auto; }
      .tl-head { display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; gap: 0.5rem; }
      .badge { background: var(--gold-soft); color: #4a5770; font-size: 0.75rem; font-weight: 600; padding: 0.25rem 0.7rem; border-radius: 999px; white-space: nowrap; }
      .card ul { margin: 0.7rem 0 0 0; padding-left: 1.1rem; }
      .card li::marker { color: var(--gold); }

      /* Chips */
      .chip {
        display: inline-block; padding: 0.35rem 0.85rem; margin: 0.2rem 0.3rem 0.2rem 0;
        border-radius: 999px; font-size: 0.82rem; color: var(--navy);
        background: #fff; border: 1px solid var(--line);
      }
      .card .chip { background: var(--paper); }
      .skill-group h4 { font-size: 0.78rem; letter-spacing: 0.16em; text-transform: uppercase; color: var(--muted); margin: 0 0 0.6rem 0; font-weight: 600; }

      /* Certifications */
      .cert { display: flex; gap: 0.9rem; align-items: flex-start; padding: 0.9rem 0; border-bottom: 1px solid var(--line); }
      .cert:last-child { border-bottom: none; }
      .cert .icon { width: 34px; height: 34px; border-radius: 10px; background: var(--gold-soft); display: flex; align-items: center; justify-content: center; flex-shrink: 0; color: #4a5770; font-size: 0.95rem; }
      .cert .name { font-weight: 600; font-size: 0.93rem; color: var(--ink); }
      .cert .issuer { font-size: 0.83rem; color: var(--muted); }

      /* Language bars */
      .lang { margin-bottom: 0.85rem; }
      .lang .row { display: flex; justify-content: space-between; font-size: 0.88rem; color: var(--ink); }
      .lang .row span:last-child { color: var(--muted); font-size: 0.8rem; }
      .bar { height: 6px; background: var(--line); border-radius: 3px; margin-top: 0.35rem; overflow: hidden; }
      .bar div { height: 100%; background: linear-gradient(90deg, var(--gold), #d3dae4); border-radius: 3px; }

      /* Contact */
      .contact {
        text-align: center; padding: 3rem 2rem; border-radius: 22px; margin-top: 1rem;
        background: linear-gradient(135deg, var(--navy) 0%, var(--navy-2) 100%); color: #fff;
      }
      .contact h3 { font-family: 'Cormorant Garamond', serif !important; font-size: 2rem; color: #fff; margin: 0 0 0.5rem 0; padding: 0; }
      .contact p { color: rgba(255,255,255,0.75) !important; margin-bottom: 1.4rem; }
      .contact .btns { justify-content: center; }
      .mails { display: flex; flex-direction: column; align-items: center; gap: 0.45rem; margin-bottom: 1.4rem; }
      .mails a.mail { color: #fff !important; text-decoration: none !important; font-size: 0.98rem; }
      .mails a.mail:hover { color: var(--gold) !important; }
      iframe { border-radius: 16px; border: 1px solid var(--line) !important; }
      .photo-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.8rem; }
      .photo { position: relative; display: block; aspect-ratio: 1; overflow: hidden; border-radius: 14px; background: var(--line); }
      .photo img { width: 100%; height: 100%; object-fit: cover; transition: transform .4s ease; display: block; }
      .photo:hover img { transform: scale(1.06); }
      .photo span {
        position: absolute; left: 0; right: 0; bottom: 0; padding: 1.6rem 0.8rem 0.6rem;
        background: linear-gradient(transparent, rgba(11,29,58,0.85)); color: #fff; font-size: 0.78rem;
        opacity: 0; transition: opacity .3s ease; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
      }
      .photo:hover span { opacity: 1; }
      .gallery-link { text-align: center; margin-top: 1rem; }
      .hobbies { display: flex; flex-wrap: wrap; gap: 1rem; }
      .hobby { flex: 1 1 200px; align-self: flex-start; text-align: center; padding: 1rem; border-radius: 14px; background: var(--paper); font-weight: 500; color: var(--navy); border: 1px solid transparent; transition: border-color .2s ease, background .2s ease; }
      .hobby:hover { border-color: var(--gold); }
      .hobby[open] { background: #fff; border-color: var(--gold); }
      .hobby summary { cursor: pointer; list-style: none; }
      .hobby summary::-webkit-details-marker { display: none; }
      .hobby .emoji { font-size: 1.8rem; margin-bottom: 0.3rem; }
      .hobby .hint { font-size: 0.72rem; color: var(--muted); font-weight: 400; margin-top: 0.2rem; }
      .hobby[open] .hint { display: none; }
      .hobby .achievement { margin-top: 0.7rem; padding-top: 0.7rem; border-top: 1px solid var(--line); font-size: 0.88rem; color: #4a5770; font-weight: 600; }
      .footer { text-align: center; color: var(--muted); font-size: 0.8rem; margin-top: 2rem; }

      @media (max-width: 760px) {
        .pin-role { display: none; }
        .pin-name { font-size: 1.15rem; }
        .hero { flex-direction: column; text-align: center; padding: 2rem 1.25rem; }
        .hero h1 { font-size: 2.5rem; }
        .hero .btns { justify-content: center; }
        .hero img { width: 150px; height: 150px; }
        .stats { grid-template-columns: repeat(2, 1fr); }
        .grid { grid-template-columns: 1fr; }
        .photo-grid { grid-template-columns: repeat(2, 1fr); }
      }
    </style>
    """
)

contact = PROFILE["contact"]
email = contact.get("email", "")
all_emails = [e for e in [email, *contact.get("other_emails", [])] if e]
photo = find_file(PROFILE.get("photo"))
photo_uri = image_data_uri(photo) if photo else ""

# ---------- Pinned header ----------
whatsapp = "".join(ch for ch in contact.get("whatsapp", "") if ch.isdigit())
if whatsapp:
    pin_cta = (
        f'<a class="btn pin-cta pin-wa" href="https://wa.me/{whatsapp}" target="_blank">'
        f'<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .1-1.3c0-.1-.2-.2-.5-.3z"/></svg>'
        f' WhatsApp</a>'
    )
else:
    pin_cta = f'<a class="btn btn-gold pin-cta" href="mailto:{escape(email)}">Contact</a>'
thumb = f'<img src="{photo_uri}" alt="">' if photo_uri else ""
html(
    f"""
    <div class="pinbar"><div class="pinbar-inner">
      <div class="pin-id">{thumb}
        <div><div class="pin-name">{escape(PROFILE["name"])}</div>
        <div class="pin-role">{escape(PROFILE["headline"])}</div></div>
      </div>
      {pin_cta}
    </div></div>
    """
)

buttons = []
if email:
    buttons.append(f'<a class="btn btn-gold" href="mailto:{escape(email)}">Get in touch</a>')
if contact.get("linkedin"):
    buttons.append(f'<a class="btn btn-ghost" href="{escape(contact["linkedin"])}" target="_blank">LinkedIn</a>')
if contact.get("flickr"):
    buttons.append(f'<a class="btn btn-ghost" href="{escape(contact["flickr"])}" target="_blank">Flickr</a>')
if contact.get("github"):
    buttons.append(f'<a class="btn btn-ghost" href="{escape(contact["github"])}" target="_blank">GitHub</a>')

tab_names = ["Overview", "Experience", "Education", "Expertise", "Research", "Training", "More About Me", "Gallery", "Contact"]
tabs = dict(zip(tab_names, st.tabs(tab_names)))

# ---------- Overview ----------
with tabs["Overview"]:
    photo_html = f'<img src="{photo_uri}" alt="{escape(PROFILE["name"])}">' if photo_uri else ""
    html(
        f"""
        <div class="hero">
          {photo_html}
          <div>
            <div class="eyebrow">Portfolio</div>
            <h1>{escape(PROFILE["name"])}</h1>
            <p class="role">{escape(PROFILE["headline"])}</p>
            <div class="loc">📍 {escape(PROFILE["location"])}</div>
            <div class="btns">{"".join(buttons)}</div>
          </div>
        </div>
        """
    )
    resume = find_file(PROFILE.get("resume"))
    if resume:
        st.download_button("Download CV", data=resume.read_bytes(), file_name=resume.name, mime="application/pdf")
    stats = [
        (f"{date.today().year - CAREER_START_YEAR}+", "Years experience"),
        (str(len(CERTIFICATIONS)), "Professional courses"),
        (str(len(PROJECTS)), "Research works"),
        (str(len(COUNTRIES_VISITED)), "Countries"),
    ]
    html(
        '<div class="stats">'
        + "".join(f'<div class="stat"><div class="num">{n}</div><div class="lbl">{l}</div></div>' for n, l in stats)
        + "</div>"
    )
    section_title("about", "Introduction", "About Me")
    paragraphs = "".join(f"<p>{escape(p)}</p>" for p in PROFILE["about"].split("\n\n"))
    html(f'<div class="about">{paragraphs}</div>')

# ---------- Experience ----------
with tabs["Experience"]:
    section_title("experience", "Career", "Professional Experience")
    items = []
    for job in EXPERIENCE:
        bullets = "".join(f"<li>{escape(h)}</li>" for h in job.get("highlights", []))
        items.append(
            f"""
            <div class="tl-item"><div class="card">
              <div class="tl-head"><h3>{escape(job['title'])}</h3>
                <span class="badge">{escape(date_range(job['start'], job['end']))}</span></div>
              <div class="sub">{escape(job['company'])}</div>
              <div class="meta">{escape(job.get('location', ''))}</div>
              <ul>{bullets}</ul>
            </div></div>
            """
        )
    html(f'<div class="timeline">{"".join(items)}</div>')

# ---------- Education ----------
with tabs["Education"]:
    section_title("education", "Academics", "Education")
    cards = []
    for edu in EDUCATION:
        details = f"<p>{escape(edu['details'])}</p>" if edu.get("details") else ""
        cards.append(
            f"""
            <div class="card">
              <span class="badge">{escape(date_range(edu['start'], edu['end']))}</span>
              <h3 style="margin-top:0.7rem">{escape(edu['degree'])}</h3>
              <div class="sub">{escape(edu['school'])}</div>
              {details}
            </div>
            """
        )
    html(f'<div class="grid">{"".join(cards)}</div>')

# ---------- Expertise ----------
with tabs["Expertise"]:
    section_title("expertise", "Capabilities", "Expertise")
    groups = "".join(
        f'<div class="card skill-group"><h4>{escape(group)}</h4>{chips(items)}</div>'
        for group, items in SKILLS.items()
    )
    html(f'<div class="grid">{groups}</div>')

# ---------- Research ----------
with tabs["Research"]:
    section_title("research", "Publications & Papers", "Research")
    cards = []
    for proj in PROJECTS:
        link = proj.get("link")
        link_html = f'<p><a href="{escape(link)}" target="_blank">Read more →</a></p>' if link else ""
        cards.append(
            f"""
            <div class="card">
              <h3>{escape(proj['name'])}</h3>
              <p>{escape(proj['description'])}</p>
              <div>{chips(proj.get('tags', []))}</div>
              {link_html}
            </div>
            """
        )
    html(f'<div class="grid">{"".join(cards)}</div>')
    if PUBLICATIONS:
        pubs = "".join(f"<li><b>{escape(p['title'])}</b>, <i>{escape(p['venue'])}</i></li>" for p in PUBLICATIONS)
        html(f'<div class="card" style="margin-top:1rem"><h3>Publications</h3><ul>{pubs}</ul></div>')

# ---------- Training ----------
with tabs["Training"]:
    section_title("training", "Training", "Courses & Certifications")
    certs = []
    for cert in CERTIFICATIONS:
        year = f" · {escape(cert['year'])}" if cert.get("year") else ""
        name = escape(cert["name"])
        if cert.get("link"):
            name = f'<a href="{escape(cert["link"])}" target="_blank">{name}</a>'
        certs.append(
            f'<div class="cert"><div class="icon">✦</div><div><div class="name">{name}</div>'
            f'<div class="issuer">{escape(cert["issuer"])}{year}</div></div></div>'
        )
    half = (len(certs) + 1) // 2
    html(
        f'<div class="grid"><div class="card">{"".join(certs[:half])}</div>'
        f'<div class="card">{"".join(certs[half:])}</div></div>'
    )

LEVEL_WIDTH = {"A1": 20, "A2": 35, "B1": 50, "B2": 65, "C1": 85, "C2": 100}


def level_width(level):
    for code, width in LEVEL_WIDTH.items():
        if code in level:
            return width
    return {"native": 100, "elementary": 35, "beginner": 20}.get(level.lower(), 50)


# ---------- More about me ----------
with tabs["More About Me"]:
    section_title("more", "Beyond Work", "More About Me")
    langs = "".join(
        f'<div class="lang"><div class="row"><span>{escape(l)}</span><span>{escape(v)}</span></div>'
        f'<div class="bar"><div style="width:{level_width(v)}%"></div></div></div>'
        for l, v in LANGUAGES.items()
    )
    affs = "".join(f"<p>{escape(a)}</p>" for a in AFFILIATIONS)
    html(
        f"""
        <div class="grid">
          <div class="card skill-group"><h4>Languages</h4>{langs}</div>
          <div>
            <div class="card skill-group" style="margin-bottom:1rem"><h4>Countries visited</h4>{chips(COUNTRIES_VISITED)}</div>
            <div class="card skill-group"><h4>Affiliations</h4>{affs}</div>
          </div>
        </div>
        """
    )
    if HOBBIES:
        hobbies = "".join(
            f'<details class="hobby"><summary><div class="emoji">{h["icon"]}</div>{escape(name)}'
            f'<div class="hint">Tap to see achievement</div></summary>'
            f'<div class="achievement">🏆 {escape(h["achievement"])}</div></details>'
            for name, h in HOBBIES.items()
        )
        html(f'<div class="card skill-group" style="margin-top:1rem"><h4>Hobbies</h4><div class="hobbies">{hobbies}</div></div>')

# ---------- Gallery ----------
with tabs["Gallery"]:
    section_title("gallery", "Photography", "Photo Gallery")
    photos = []
    if FLICKR_USER_ID:
        try:
            photos = flickr_photos(FLICKR_USER_ID, FLICKR_PHOTO_COUNT)
        except Exception:
            photos = []
    if photos:
        tiles = "".join(
            f'<a class="photo" href="{escape(ph["link"])}" target="_blank">'
            f'<img src="{escape(ph["src"])}" alt="{escape(ph["title"])}" loading="lazy">'
            f'<span>{escape(ph["title"])}</span></a>'
            for ph in photos
        )
        html(f'<div class="photo-grid">{tiles}</div>')
    elif FLICKR_EMBED:
        if hasattr(st, "iframe"):
            st.iframe(FLICKR_EMBED, height=520)
        else:
            components.iframe(FLICKR_EMBED, height=520)
    if contact.get("flickr"):
        html(
            f'<div class="gallery-link"><a class="btn btn-gold" href="{escape(contact["flickr"])}" '
            f'target="_blank">View all photos on Flickr →</a></div>'
        )

# ---------- Contact ----------
with tabs["Contact"]:
    section_title("contact", "Contact", "Let's Connect")
    contact_btns = list(buttons)
    if contact.get("phone"):
        contact_btns.append(f'<a class="btn btn-ghost" href="tel:{escape(contact["phone"])}">{escape(contact["phone"])}</a>')
    if contact.get("website"):
        contact_btns.append(f'<a class="btn btn-ghost" href="{escape(contact["website"])}" target="_blank">Website</a>')
    email_links = "".join(f'<a class="mail" href="mailto:{escape(e)}">✉ {escape(e)}</a>' for e in all_emails)
    html(
        f"""
        <div class="contact">
          <h3>Open to new opportunities</h3>
          <p>For collaborations, engineering management roles, or just to say hello.</p>
          <div class="mails">{email_links}</div>
          <div class="btns">{"".join(contact_btns)}</div>
        </div>
        """
    )

html(f'<div class="footer">© {date.today().year} {escape(PROFILE["name"])}</div>')
