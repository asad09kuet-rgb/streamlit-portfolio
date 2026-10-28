from html import escape
from pathlib import Path

import streamlit as st

from profile_data import (
    CERTIFICATIONS,
    EDUCATION,
    EXPERIENCE,
    PROFILE,
    PROJECTS,
    PUBLICATIONS,
    SKILLS,
)

ROOT = Path(__file__).parent

st.set_page_config(
    page_title=f"{PROFILE['name']} | Portfolio",
    page_icon="⚡",
    layout="wide",
)

st.markdown(
    """
    <style>
      .block-container { max-width: 1000px; padding-top: 4rem; }
      .hero-headline { font-size: 1.25rem !important; opacity: 0.8; margin-top: 0.3rem; }
      .hero-location { opacity: 0.6; }
      .card {
        border: 1px solid rgba(128,128,128,0.25);
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin-bottom: 1rem;
      }
      .card h4 { margin: 0 0 0.2rem 0; }
      .muted { opacity: 0.65; font-size: 0.92rem; }
      .tag {
        display: inline-block;
        padding: 0.15rem 0.6rem;
        margin: 0.15rem 0.25rem 0.15rem 0;
        border-radius: 999px;
        font-size: 0.82rem;
        background: rgba(255, 140, 0, 0.15);
        border: 1px solid rgba(255, 140, 0, 0.35);
      }
    </style>
    """,
    unsafe_allow_html=True,
)


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


def tags(items):
    return "".join(f'<span class="tag">{escape(t)}</span>' for t in items)


def section(title):
    st.markdown("---")
    st.header(title)


# ---------- Sidebar ----------
contact = PROFILE["contact"]
with st.sidebar:
    st.title(PROFILE["name"])
    st.caption(PROFILE["headline"])
    st.markdown("**Jump to**")
    for name in ["About", "Experience", "Education", "Skills", "Projects", "Certifications", "Contact"]:
        st.markdown(f"- [{name}](#{name.lower()})")
    st.markdown("---")
    if contact.get("linkedin"):
        st.link_button("LinkedIn", contact["linkedin"], use_container_width=True)
    if contact.get("github"):
        st.link_button("GitHub", contact["github"], use_container_width=True)
    if contact.get("email"):
        st.link_button("Email me", f"mailto:{contact['email']}", use_container_width=True)

# ---------- Hero ----------
photo = find_file(PROFILE.get("photo"))
left, right = st.columns([1, 3], vertical_alignment="center") if photo else (None, st.container())
if photo:
    left.image(str(photo), use_container_width=True)
with right:
    st.title(PROFILE["name"], anchor=False)
    st.markdown(f'<p class="hero-headline">{escape(PROFILE["headline"])}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="hero-location">📍 {escape(PROFILE["location"])}</p>', unsafe_allow_html=True)
    resume = find_file(PROFILE.get("resume"))
    if resume:
        st.download_button(
            "📄 Download CV",
            data=resume.read_bytes(),
            file_name=resume.name,
            mime="application/pdf",
        )

# ---------- About ----------
section("About")
st.write(PROFILE["about"])

# ---------- Experience ----------
section("Experience")
for job in EXPERIENCE:
    bullets = "".join(f"<li>{escape(h)}</li>" for h in job.get("highlights", []))
    st.markdown(
        f"""<div class="card">
              <h4>{escape(job['title'])}</h4>
              <div>{escape(job['company'])} · {escape(job.get('location', ''))}</div>
              <div class="muted">{escape(job['start'])} – {escape(job['end'])}</div>
              <ul>{bullets}</ul>
            </div>""",
        unsafe_allow_html=True,
    )

# ---------- Education ----------
section("Education")
for edu in EDUCATION:
    st.markdown(
        f"""<div class="card">
              <h4>{escape(edu['degree'])}</h4>
              <div>{escape(edu['school'])}</div>
              <div class="muted">{escape(edu['start'])} – {escape(edu['end'])}</div>
              <p>{escape(edu.get('details', ''))}</p>
            </div>""",
        unsafe_allow_html=True,
    )

# ---------- Skills ----------
section("Skills")
cols = st.columns(2)
for i, (group, items) in enumerate(SKILLS.items()):
    with cols[i % 2]:
        st.subheader(group)
        st.markdown(tags(items), unsafe_allow_html=True)

# ---------- Projects ----------
section("Projects")
cols = st.columns(2)
for i, proj in enumerate(PROJECTS):
    link = proj.get("link")
    link_html = f'<a href="{escape(link)}" target="_blank">View project →</a>' if link else ""
    with cols[i % 2]:
        st.markdown(
            f"""<div class="card">
                  <h4>{escape(proj['name'])}</h4>
                  <p>{escape(proj['description'])}</p>
                  <div>{tags(proj.get('tags', []))}</div>
                  <p>{link_html}</p>
                </div>""",
            unsafe_allow_html=True,
        )

# ---------- Certifications & publications ----------
if CERTIFICATIONS or PUBLICATIONS:
    section("Certifications")
    for cert in CERTIFICATIONS:
        line = f"**{cert['name']}** · {cert['issuer']} ({cert['year']})"
        if cert.get("link"):
            line += f" · [credential]({cert['link']})"
        st.markdown(f"- {line}")
    if PUBLICATIONS:
        st.subheader("Publications")
        for pub in PUBLICATIONS:
            title = f"[{pub['title']}]({pub['link']})" if pub.get("link") else pub["title"]
            st.markdown(f"- {title}, *{pub['venue']}*")

# ---------- Contact ----------
section("Contact")
st.write("Feel free to reach out for collaborations, opportunities, or just to say hello.")
c1, c2, c3 = st.columns(3)
if contact.get("email"):
    c1.markdown(f"📧 [{contact['email']}](mailto:{contact['email']})")
if contact.get("linkedin"):
    c2.markdown(f"💼 [LinkedIn]({contact['linkedin']})")
if contact.get("github"):
    c3.markdown(f"💻 [GitHub]({contact['github']})")
if contact.get("phone"):
    st.markdown(f"📞 {contact['phone']}")
if contact.get("website"):
    st.markdown(f"🌐 [{contact['website']}]({contact['website']})")

st.markdown("---")
st.caption(f"© {PROFILE['name']} · Built with Streamlit")
