"""
Hossain Md Asad: personal portfolio website (single-file version).

Everything the site needs is in this one file: content, styling and layout.
Run it with:

    pip install streamlit "qrcode[pil]"
    streamlit run website_full.py

To deploy on Streamlit Community Cloud, choose this file as the main file path.
"""
import base64
import io
import json
import urllib.request
from datetime import date
from html import escape
from pathlib import Path

import qrcode
import streamlit as st
import streamlit.components.v1 as components

# =====================================================================
# CONTENT: edit everything below to change the website text
# =====================================================================

PROFILE = {
    "name": "Hossain Md Asad",
    "headline": "Squadron Leader, Bangladesh Air Force",
    "location": "Dhaka, Bangladesh",
    # Square photo; app.py also tries .jpg/.png/.webp versions of this path
    "photo": "assets/profile.jpg",
    # Optional: put your CV at assets/resume.pdf and a download button will appear
    "resume": "assets/resume.pdf",
    "about": (
        "I am a Squadron Leader in the Bangladesh Air Force and an Electrical & Electronic "
        "Engineer from KUET, with over ten years of experience in aircraft maintenance, "
        "airfield operations, defence procurement and project management.\n\n"
        "I have commanded aircraft maintenance units, served as a staff officer and instructor, "
        "worked with multinational teams on UN peacekeeping in Mali, and overseen the technical "
        "evaluation and procurement of aerospace equipment.\n\n"
        "I am looking to apply this leadership, engineering and project management experience "
        "in a challenging engineering management role, driving operational excellence, "
        "innovation and organizational growth."
    ),
    "contact": {
        "email": "asad.eee.kuet@gmail.com",
        # Extra addresses listed on the Contact tab
        "other_emails": ["asad09.kuet@gmail.com", "asadspm@buaa.edu.cn", "asad9919@baf.mil.bd"],
        "linkedin": "https://www.linkedin.com/in/asad09eee/",
        "github": "https://github.com/asad09kuet-rgb",
        "flickr": "https://www.flickr.com/photos/0903087/",
        # Leave empty ("") to hide
        "phone": "",
        # WhatsApp number in international format, digits only (e.g. "8801XXXXXXXXX").
        # When set, the top-bar button becomes a WhatsApp button. Leave "" to show email.
        "whatsapp": "8801717146374",
        "website": "",
    },
}

# Most recent first
EXPERIENCE = [
    {
        "title": "Squadron Leader",
        "company": "Bangladesh Air Force",
        "location": "Dhaka, Bangladesh",
        "start": "Dec 2015",
        "end": "Present",
        "highlights": [
            "Served as Officer Commanding, Staff Officer, Officer in Charge of Flight Lines and "
            "instructor at different BAF units.",
            "Led aircraft maintenance units, ensuring operational readiness and compliance with "
            "safety standards.",
            "Directed projects and units, managing logistics and multinational team operations, "
            "including UN peacekeeping service with MINUSMA in Mali.",
            "Mentored and supervised personnel, fostering team cohesion, morale and professional "
            "development.",
            "Oversaw procurement and technical evaluation of aerospace equipment, tenders and "
            "contracts, ensuring regulatory compliance.",
        ],
    },
    {
        "title": "General Manager",
        "company": "Dream71 Bangladesh Ltd",
        "location": "Dhaka, Bangladesh",
        "start": "Aug 2014",
        "end": "May 2015",
        "highlights": [
            "Managed software business operations, liaising with international clients and "
            "company CEOs to ensure timely project delivery.",
            "Led recruitment, partnerships and presentations to support business growth and "
            "team development.",
        ],
    },
]

EDUCATION = [
    {
        "degree": "Master's Degree in Space Project Management",
        "school": "Beihang University, Hangzhou, China",
        "start": "Sep 2026",
        "end": "Present",
        "details": "",
    },
    {
        "degree": "B.Sc. in Electrical & Electronic Engineering",
        "school": "Khulna University of Engineering & Technology (KUET)",
        "start": "",
        "end": "2014",
        "details": "GPA 3.45 / 4.00. Thesis: Design and Feasibility Study of Grid Connected "
        "Hybrid Power Generation for Patenga Coastal Area.",
    },
    {
        "degree": "H.S.C., Science",
        "school": "Kaliganj M.U. Degree College, Jhenaidah, Bangladesh",
        "start": "",
        "end": "2009",
        "details": "GPA 5.00 / 5.00",
    },
    {
        "degree": "S.S.C., Science",
        "school": "N.B. High School, Jhenaidah, Bangladesh",
        "start": "",
        "end": "2007",
        "details": "GPA 5.00 / 5.00",
    },
]

# Skill groups: {"Group name": ["skill", ...]}
SKILLS = {
    "Space": ["Space Project Management", "Space Technology"],
    "Aviation & Engineering": [
        "Aircraft Maintenance",
        "Airfield Operations",
        "Pre-Shipment Inspections",
        "Technical Evaluation",
        "Aviation Safety & Risk Management",
    ],
    "Management": [
        "Project Management & Oversight",
        "Defence Procurement",
        "Contract Negotiation",
        "Logistics Operations",
    ],
    "Programming & Development": ["C", "C++", "Python", "Web Application Development (AI)"],
    "Leadership": [
        "Team Leadership",
        "Staff Development & Mentoring",
        "Instruction & Training",
        "Cross-Cultural & Multinational Collaboration",
    ],
}

# Projects and research work, shown as cards ("link" set to "" hides the link)
PROJECTS = [
    {
        "name": "AI and LLM based Assistant on Celestial Body Reentry and Risk Mitigation",
        "description": "Orbisk: a web app that ranks the risk from satellites and space debris using "
        "public CelesTrak data. It predicts re-entry time and latitude, screens close approaches, "
        "scores the 50 riskiest objects from 0 to 100, and uses a RAG-based LLM assistant to explain "
        "the results in plain language. Role: Product Manager in a five-member team. "
        "Beihang University, Hangzhou, China, 2026.",
        "tags": ["AI & LLM", "RAG", "Space Debris", "Streamlit"],
        "link": "https://satellite-re-entry-debris-tracking-web-app-v2.streamlit.app/",
    },
    {
        "name": "Optimal On-Grid Hybrid Renewable Energy Model for Coastal Area",
        "description": "A Bangladesh-perspective model for an optimal grid-connected hybrid "
        "renewable energy system for coastal areas. IEEE publication, University of Dhaka, 2014.",
        "tags": ["Renewable Energy", "Power Systems", "IEEE"],
        "link": "",
    },
    {
        "name": "Grid Connected Hybrid Power Generation for Patenga Coastal Area",
        "description": "Design and feasibility study of a grid-connected hybrid power plant "
        "for the Patenga coastal area. Undergraduate thesis, KUET, 2014.",
        "tags": ["Thesis", "Hybrid Power", "Feasibility Study"],
        "link": "",
    },
    {
        "name": "Defence Against Chemical Disaster: BAF Capacity Building",
        "description": "Group research paper taking a closer look at Bangladesh Air Force "
        "capacity building for chemical disaster response. Command & Staff Training "
        "Institute, Cox's Bazar, Bangladesh, 2024.",
        "tags": ["Defence", "Disaster Response", "Research"],
        "link": "",
    },
]

# Leave a list empty ([]) to hide it
CERTIFICATIONS = [
    {"name": "Artificial Intelligence and LLM", "issuer": "Beihang University, Hangzhou, China", "year": "", "link": ""},
    {"name": "Intercultural Communication in Space Project", "issuer": "Beihang University, Hangzhou, China", "year": "", "link": ""},
    {"name": "No. 125 Junior Command & Staff Course", "issuer": "CSTI BAF, Cox's Bazar, Bangladesh", "year": "", "link": ""},
    {"name": "Aviation Risk Management (ARM) Course", "issuer": "UN Global Service Centre", "year": "", "link": ""},
    {"name": "United Nations Peacekeeping Certificate", "issuer": "MINUSMA, Mali", "year": "", "link": ""},
    {"name": "Type Trained Helicopter Maintenance Course", "issuer": "Philadelphia, USA", "year": "", "link": ""},
    {"name": "Aviation Safety Course", "issuer": "Civil Aviation Training Centre, Dhaka, Bangladesh", "year": "", "link": ""},
    {"name": "Ramp Safety Course", "issuer": "Bangladesh Airlines Training Center, Dhaka, Bangladesh", "year": "", "link": ""},
    {"name": "No. 03 Cat D Course", "issuer": "Officers Training School BAF, Jashore, Bangladesh", "year": "", "link": ""},
    {"name": "No. 09 PCPT Course", "issuer": "Officers Training School BAF, Jashore, Bangladesh", "year": "", "link": ""},
]

PUBLICATIONS = [
    {
        "title": "Optimal On-Grid Hybrid Renewable Energy Model for Coastal Area: Bangladesh Perspective",
        "venue": "IEEE, University of Dhaka, 2014",
        "link": "",
    },
]

AFFILIATIONS = ["Member, Institution of Engineers, Bangladesh (IEB)"]

LANGUAGES = {"Bangla": "Mother tongue", "English": "Advanced (C1)", "Arabic": "Beginner (A1)", "French": "Beginner (A1)", "Chinese": "Elementary"}

# Country name -> two-letter ISO code (used to show the flag)
COUNTRIES_VISITED = {"China": "cn", "USA": "us", "Canada": "ca", "Qatar": "qa", "Mali": "ml", "Djibouti": "dj"}

# Each hobby card expands on click to show the achievement
HOBBIES = {
    "Photography": {"icon": "📷", "achievement": "1st place, Beihang University Photography Competition 2026"},
    "Volleyball": {"icon": "🏐", "achievement": "Champion team, No. 124 Junior Command & Staff Course"},
    "Badminton": {"icon": "🏸", "achievement": "Professional player"},
}

# Gallery tab: latest public photos from this Flickr user id (set to "" to hide the grid)
FLICKR_USER_ID = "78237795@N08"
FLICKR_PHOTO_COUNT = 12
# Fallback slideshow if the photo feed can't be loaded (set to "" to hide)
FLICKR_EMBED = "https://embedr.flickr.com/photostreams/78237795@N08"

# Insights tab: multinational, intercultural project challenges and how to mitigate them.
# Each challenge card expands on click to show the mitigation measures.
INSIGHTS = {
    "title": "Leading Multinational Projects",
    "intro": (
        "Working with multinational teams on UN peacekeeping in Mali, training abroad, and now "
        "studying Space Project Management in China has shown me that the hardest problems in "
        "international projects are rarely technical. These are the challenges I see most often, "
        "and the measures that help a diverse team deliver as one."
    ),
    "challenges": [
        {
            "icon": "🗣️",
            "title": "Communication & Language",
            "challenge": "Different first languages, accents and jargon lead to misunderstood "
            "instructions and silent disagreement.",
            "mitigation": [
                "Agree on one working language and a shared glossary of technical terms.",
                "Confirm key decisions in writing and use read-backs for critical instructions.",
                "Prefer visuals, checklists and diagrams over long verbal briefings.",
            ],
        },
        {
            "icon": "🧭",
            "title": "Hierarchy & Decision-Making Styles",
            "challenge": "Some cultures expect top-down direction, others consensus; people may "
            "not raise concerns to a senior member.",
            "mitigation": [
                "Make decision rights explicit with a RACI matrix from day one.",
                "Invite input in structured ways, such as round-robin and anonymous feedback.",
                "Leaders model openness by asking for challenge before they decide.",
            ],
        },
        {
            "icon": "⏱️",
            "title": "Work Styles & Time Perception",
            "challenge": "Deadlines, punctuality and 'done' can mean different things across "
            "cultures, putting schedules at risk.",
            "mitigation": [
                "Define clear milestones and acceptance criteria for every deliverable.",
                "Track progress visibly with short, regular check-ins.",
                "Build buffers around cultural and religious holidays in the schedule.",
            ],
        },
        {
            "icon": "🌐",
            "title": "Distance & Time Zones",
            "challenge": "Distributed teams lose overlap hours, slow down decisions and miss "
            "informal information.",
            "mitigation": [
                "Set fixed overlap windows and rotate inconvenient meeting times fairly.",
                "Keep a single source of truth for documents, decisions and status.",
                "Default to asynchronous updates, with clear owners and response times.",
            ],
        },
        {
            "icon": "🤝",
            "title": "Trust & Team Cohesion",
            "challenge": "Stereotypes and sub-groups by nationality weaken collaboration and "
            "information sharing.",
            "mitigation": [
                "Form mixed-nationality working groups and pair members across cultures.",
                "Run early team-building and short cultural awareness sessions.",
                "Recognise contributions publicly and handle conflict early and privately.",
            ],
        },
        {
            "icon": "🛡️",
            "title": "Regulations, Export Control & Security",
            "challenge": "Space and defence projects face export-control rules (e.g. ITAR/EAR), "
            "national security limits and differing laws.",
            "mitigation": [
                "Map applicable regulations and approvals during project planning.",
                "Classify information and control access on a need-to-know basis.",
                "Involve legal and compliance experts early, not at the end.",
            ],
        },
        {
            "icon": "🎯",
            "title": "Stakeholder & National Interests",
            "challenge": "Partner agencies and countries bring different priorities, funding "
            "cycles and political pressures.",
            "mitigation": [
                "Agree a shared mission statement and success criteria at the start.",
                "Use a formal governance board and a clear escalation path.",
                "Keep stakeholders aligned through regular, transparent reporting.",
            ],
        },
        {
            "icon": "📐",
            "title": "Standards & Technical Practices",
            "challenge": "Different engineering standards, units and documentation formats cause "
            "interface errors and rework.",
            "mitigation": [
                "Agree common standards and units in an interface control document.",
                "Hold joint design reviews with clear configuration management.",
                "Verify interfaces early through integration tests and peer checks.",
            ],
        },
    ],
    "closing": (
        "Diversity is a strength when it is managed deliberately: clear structure, open "
        "communication and mutual respect turn many perspectives into better decisions."
    ),
}

# Profile photo embedded so this single file runs on its own.
# If assets/profile.jpg exists next to this file, that file is used instead.
EMBEDDED_PHOTO = "data:image/jpeg;base64,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"

# =====================================================================
# LAYOUT AND STYLE
# =====================================================================

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


def vcard_escape(value):
    return value.replace("\\", "\\\\").replace(",", "\\,").replace(";", "\\;").replace("\n", "\\n")


def build_vcard(full=False):
    """Contact card (vCard 3.0) built from PROFILE, so it always matches the site."""
    contact = PROFILE["contact"]
    title, _, org = PROFILE["headline"].partition(", ")
    city, _, country = PROFILE["location"].partition(", ")
    parts = PROFILE["name"].split()
    lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"N:{vcard_escape(parts[-1])};{vcard_escape(' '.join(parts[:-1]))};;;",
        f"FN:{vcard_escape(PROFILE['name'])}",
        f"TITLE:{vcard_escape(title)}",
    ]
    if org:
        lines.append(f"ORG:{vcard_escape(org)}")
    whatsapp = "".join(ch for ch in contact.get("whatsapp", "") if ch.isdigit())
    if whatsapp:
        lines.append(f"TEL;TYPE=CELL,VOICE:+{whatsapp}")
    if contact.get("phone"):
        lines.append(f"TEL;TYPE=VOICE:{contact['phone']}")
    for i, mail in enumerate([contact.get("email", ""), *contact.get("other_emails", [])]):
        if mail:
            lines.append(f"EMAIL;TYPE=INTERNET{',PREF' if i == 0 else ''}:{mail}")
    lines.append(f"ADR;TYPE=WORK:;;;{vcard_escape(city)};;;{vcard_escape(country)}")
    url = contact.get("website") or contact.get("linkedin")
    if url:
        lines.append(f"URL:{url}")
    # The QR code keeps only the essentials so it stays easy to scan
    for network in ("linkedin", "flickr", "github") if full else ():
        if contact.get(network):
            lines.append(f"X-SOCIALPROFILE;TYPE={network}:{contact[network]}")
    if full:
        photo = find_file(PROFILE.get("photo"))
        data = base64.b64encode(photo.read_bytes()).decode() if photo else EMBEDDED_PHOTO.split(",", 1)[1]
        if data:
            # vCard lines are folded at 75 characters
            folded = "\r\n ".join(data[i : i + 74] for i in range(0, len(data), 74))
            lines.append(f"PHOTO;ENCODING=b;TYPE=JPEG:{folded}")
    lines.append("END:VCARD")
    return "\r\n".join(lines) + "\r\n"


@st.cache_data(show_spinner=False)
def qr_data_uri(text):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=2)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#0b1d3a", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


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
        width: min(1080px, 100%); padding: 0.6rem 1.25rem; gap: 0.1rem; justify-content: space-between;
        background: var(--paper); box-shadow: 0 0 0 100vmax var(--paper); clip-path: inset(0 -100vmax);
        border-bottom: 1px solid var(--line);
        overflow-x: auto; scrollbar-width: none; display: flex;
      }
      .stTabs [role="tablist"]::-webkit-scrollbar { display: none; }
      [data-testid="stTabsScrollRight"], [data-testid="stTabsScrollLeft"] { display: none !important; }
      .stTabs [data-testid="stTab"] { box-shadow: none !important; border-bottom: none !important; }
      .stTabs [data-testid="stTab"] {
        height: auto; padding: 0.45rem 0.7rem; border-radius: 999px; background: transparent;
        white-space: nowrap; transition: background .2s ease; border: none;
      }
      .stTabs [data-testid="stTab"] p { font-size: 0.74rem !important; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; color: var(--ink); margin: 0; }
      .stTabs [data-testid="stTab"]:hover p { color: var(--gold); }
      .stTabs [data-testid="stTab"][aria-selected="true"] { background: var(--navy) !important; }
      .stTabs [data-testid="stTab"][aria-selected="true"] p { color: #fff !important; }
      .stTabs [role="tablist"] [data-testid="stTab"]::after, .stTabs [role="tablist"] > div:not([data-testid="stTab"]) { display: none !important; }
      .stTabs [role="tabpanel"] { padding-top: 0.5rem; }

      /* Hero */
      .hero {
        position: relative; overflow: hidden;
        display: flex; flex-direction: row-reverse; justify-content: space-between;
        gap: 2.5rem; align-items: center;
        padding: 3rem 3.5rem; border-radius: 22px;
        background: radial-gradient(circle at 80% 20%, rgba(169, 180, 198,0.25), transparent 40%),
                    linear-gradient(135deg, var(--navy) 0%, var(--navy-2) 100%);
        color: #fff; box-shadow: 0 25px 60px -25px rgba(11, 29, 58, 0.55);
      }
      .hero::after {
        content: ""; position: absolute; left: -150px; bottom: -150px; width: 260px; height: 260px;
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
      .btn-gmail { background: #fff; color: #1f1f1f !important; display: inline-flex; align-items: center; gap: 0.45rem; }
      .btn-gmail:hover { background: #f1f3f4; }
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
      .flag-chip { display: inline-flex; align-items: center; gap: 0.45rem; }
      .flag-chip img { width: 20px; height: 14px; object-fit: cover; border-radius: 2px; box-shadow: 0 0 0 1px rgba(0,0,0,0.08); }
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
      .vcard { display: flex; align-items: center; gap: 2rem; margin-top: 1.5rem; }
      .vcard .qr { width: 180px; height: 180px; border-radius: 12px; border: 1px solid var(--line); padding: 6px; background: #fff; flex-shrink: 0; }
      .vcard h3 { margin-top: 0.2rem !important; }
      [data-testid="stDownloadButton"] button {
        background: var(--navy) !important; color: #fff !important; border: none !important;
        border-radius: 999px !important; padding: 0.6rem 1.2rem !important; font-weight: 600 !important;
        transition: transform .2s ease, box-shadow .2s ease;
      }
      [data-testid="stDownloadButton"] button:hover { transform: translateY(-2px); box-shadow: 0 14px 30px -16px rgba(11,29,58,0.6); }
      [data-testid="stDownloadButton"] button p { color: #fff !important; }
      .insights-grid { align-items: start; }
      .insight summary { cursor: pointer; list-style: none; }
      .insight summary::-webkit-details-marker { display: none; }
      .insight-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; }
      .insight-icon { font-size: 1.6rem; width: 46px; height: 46px; border-radius: 12px; background: var(--gold-soft); display: inline-flex; align-items: center; justify-content: center; }
      .insight-num { font-family: 'Cormorant Garamond', serif !important; font-size: 1.6rem; font-weight: 700; color: var(--line); }
      .insight-challenge { color: var(--muted) !important; margin-bottom: 0.4rem; }
      .insight .hint { font-size: 0.75rem; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; color: var(--steel); }
      .insight[open] { border-color: var(--gold); }
      .insight[open] .hint { display: none; }
      .insight-fix { margin-top: 0.4rem; padding-top: 0.8rem; border-top: 1px solid var(--line); }
      .insight-label { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: var(--navy); }
      .insight-fix ul { margin-top: 0.4rem !important; }
      .insight-closing {
        margin: 1.6rem auto 0; max-width: 760px; text-align: center; font-family: 'Cormorant Garamond', serif;
        font-size: 1.35rem; font-style: italic; color: var(--navy); line-height: 1.5;
      }
      .footer { text-align: center; color: var(--muted); font-size: 0.8rem; margin-top: 2rem; }

      /* Motion: floating and fade-in */
      @keyframes floaty { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
      @keyframes drift { 0%, 100% { transform: translate(0, 0); } 50% { transform: translate(18px, -14px); } }
      @keyframes rise { from { opacity: 0; transform: translateY(24px); } to { opacity: 1; transform: translateY(0); } }
      @keyframes glow { 0%, 100% { box-shadow: 0 0 0 8px rgba(169,180,198,0.15), 0 20px 40px -20px rgba(0,0,0,0.5); }
                        50% { box-shadow: 0 0 0 14px rgba(169,180,198,0.08), 0 30px 50px -20px rgba(0,0,0,0.55); } }
      @keyframes sheen { 0% { background-position: 0% 50%; } 100% { background-position: 200% 50%; } }
      .hero img { animation: floaty 6s ease-in-out infinite, glow 6s ease-in-out infinite; }
      .hero::after { animation: drift 14s ease-in-out infinite; }
      .hero::before {
        content: ""; position: absolute; top: -80px; right: 22%; width: 180px; height: 180px; border-radius: 50%;
        background: radial-gradient(circle, rgba(169,180,198,0.22), transparent 70%);
        animation: drift 11s ease-in-out infinite reverse; pointer-events: none;
      }
      .hero > div { position: relative; z-index: 1; }
      .hero h1 {
        background: linear-gradient(90deg, #fff 0%, #fff 40%, #d3dae4 50%, #fff 60%, #fff 100%);
        background-size: 200% auto; -webkit-background-clip: text; background-clip: text; color: transparent !important;
        animation: sheen 7s linear infinite;
      }
      .hero h1 * { color: transparent !important; }
      .hero, .stat, .card, .section-head, .about, .photo, .contact, .tl-item {
        animation: rise .7s cubic-bezier(.2,.7,.2,1) both;
      }
      .stats .stat:nth-child(2), .grid > *:nth-child(2), .photo-grid > *:nth-child(2) { animation-delay: .08s; }
      .stats .stat:nth-child(3), .grid > *:nth-child(3), .photo-grid > *:nth-child(3) { animation-delay: .16s; }
      .stats .stat:nth-child(4), .grid > *:nth-child(4), .photo-grid > *:nth-child(4) { animation-delay: .24s; }
      .photo-grid > *:nth-child(n+5) { animation-delay: .32s; }
      .tl-item:nth-child(2) { animation-delay: .12s; }
      .stat { transition: transform .25s ease, box-shadow .25s ease; }
      .stat:hover { transform: translateY(-6px); box-shadow: 0 22px 40px -24px rgba(11,29,58,0.45); }
      .card:hover { transform: translateY(-6px); box-shadow: 0 24px 48px -26px rgba(11,29,58,0.45); }
      .chip { transition: transform .2s ease, border-color .2s ease; }
      .chip:hover { transform: translateY(-2px); border-color: var(--gold); }
      .btn:hover { transform: translateY(-2px); }
      .pin-wa { animation: floaty 3.5s ease-in-out infinite; }
      .hobby .emoji { display: inline-block; transition: transform .3s ease; }
      .hobby:hover .emoji { transform: translateY(-4px) scale(1.12); }
      @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after { animation: none !important; transition: none !important; }
      }

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
        .vcard { flex-direction: column; text-align: center; }
      }
    </style>
    """
)

contact = PROFILE["contact"]
email = contact.get("email", "")
all_emails = [e for e in [email, *contact.get("other_emails", [])] if e]
photo = find_file(PROFILE.get("photo"))
photo_uri = image_data_uri(photo) if photo else EMBEDDED_PHOTO

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
    gmail_icon = (
        '<svg viewBox="0 0 48 48" width="16" height="16" aria-hidden="true">'
        '<path fill="#4285F4" d="M6 40h7V23L4 16v21a3 3 0 0 0 2 3z"/>'
        '<path fill="#34A853" d="M35 40h7a3 3 0 0 0 2-3V16l-9 7z"/>'
        '<path fill="#FBBC04" d="M35 11v12l9-7v-4c0-3.7-4.2-5.8-7.2-3.6z"/>'
        '<path fill="#EA4335" d="M13 23V11l11 8.3L35 11v12l-11 8.3z"/>'
        '<path fill="#C5221F" d="M4 12v4l9 7V11l-1.8-1.6C8.2 7.2 4 9.3 4 12z"/></svg>'
    )
    gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={escape(email)}"
    buttons.append(f'<a class="btn btn-gmail" href="{gmail_url}" target="_blank">{gmail_icon} Gmail</a>')
if contact.get("linkedin"):
    buttons.append(f'<a class="btn btn-ghost" href="{escape(contact["linkedin"])}" target="_blank">LinkedIn</a>')
if contact.get("flickr"):
    buttons.append(f'<a class="btn btn-ghost" href="{escape(contact["flickr"])}" target="_blank">Flickr</a>')
if contact.get("github"):
    buttons.append(f'<a class="btn btn-ghost" href="{escape(contact["github"])}" target="_blank">GitHub</a>')

tab_names = ["Overview", "Experience", "Education", "Expertise", "Project & Research", "Insights", "Training", "More About Me", "Gallery", "Contact"]
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
        (str(len(PROJECTS)), "Projects & research"),
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

# ---------- Project & Research ----------
with tabs["Project & Research"]:
    section_title("research", "Projects, Publications & Papers", "Project and Research")
    cards = []
    for proj in PROJECTS:
        link = proj.get("link")
        link_html = f'<p><a href="{escape(link)}" target="_blank">View project →</a></p>' if link else ""
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

# ---------- Insights ----------
with tabs["Insights"]:
    section_title("insights", "Perspectives", INSIGHTS["title"])
    html(f'<div class="about"><p>{escape(INSIGHTS["intro"])}</p></div>')
    cards = []
    for i, item in enumerate(INSIGHTS["challenges"], 1):
        steps = "".join(f"<li>{escape(m)}</li>" for m in item["mitigation"])
        cards.append(
            f"""
            <details class="card insight">
              <summary>
                <div class="insight-head"><span class="insight-icon">{item['icon']}</span>
                  <span class="insight-num">{i:02d}</span></div>
                <h3>{escape(item['title'])}</h3>
                <p class="insight-challenge">{escape(item['challenge'])}</p>
                <div class="hint">Show mitigation measures ▾</div>
              </summary>
              <div class="insight-fix"><div class="insight-label">Mitigation</div><ul>{steps}</ul></div>
            </details>
            """
        )
    html(f'<div class="grid insights-grid">{"".join(cards)}</div>')
    html(f'<div class="insight-closing">“{escape(INSIGHTS["closing"])}”</div>')

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
    return {"native": 100, "mother tongue": 100, "elementary": 35, "beginner": 20}.get(level.lower(), 50)


# ---------- More about me ----------
with tabs["More About Me"]:
    section_title("more", "Beyond Work", "More About Me")
    if HOBBIES:
        hobbies = "".join(
            f'<details class="hobby"><summary><div class="emoji">{h["icon"]}</div>{escape(name)}'
            f'<div class="hint">Tap to see achievement</div></summary>'
            f'<div class="achievement">🏆 {escape(h["achievement"])}</div></details>'
            for name, h in HOBBIES.items()
        )
        html(f'<div class="card skill-group" style="margin-bottom:1rem"><h4>Hobbies</h4><div class="hobbies">{hobbies}</div></div>')
    langs = "".join(
        f'<div class="lang"><div class="row"><span>{escape(l)}</span><span>{escape(v)}</span></div>'
        f'<div class="bar"><div style="width:{level_width(v)}%"></div></div></div>'
        for l, v in LANGUAGES.items()
    )
    affs = "".join(f"<p>{escape(a)}</p>" for a in AFFILIATIONS)
    flags = "".join(
        f'<span class="chip flag-chip"><img src="https://flagcdn.com/w40/{escape(code)}.png" alt="" '
        f'width="20" height="14">{escape(country)}</span>'
        for country, code in COUNTRIES_VISITED.items()
    )
    html(
        f"""
        <div class="grid">
          <div class="card skill-group"><h4>Languages</h4>{langs}</div>
          <div>
            <div class="card skill-group" style="margin-bottom:1rem"><h4>Countries visited</h4>{flags}</div>
            <div class="card skill-group"><h4>Affiliations</h4>{affs}</div>
          </div>
        </div>
        """
    )

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

    file_name = PROFILE["name"].replace(" ", "_") + ".vcf"
    html(
        f"""
        <div class="card vcard">
          <img class="qr" src="{qr_data_uri(build_vcard())}" alt="QR code with contact details">
          <div>
            <div class="kicker">Digital business card</div>
            <h3>Save my contact</h3>
            <p>Scan the QR code with your phone camera to add me to your contacts instantly, or download the contact card below.</p>
          </div>
        </div>
        """
    )
    st.download_button(
        "⬇ Save contact (vCard)",
        data=build_vcard(full=True),
        file_name=file_name,
        mime="text/vcard",
        use_container_width=True,
    )

html(f'<div class="footer">© {date.today().year} {escape(PROFILE["name"])}</div>')
