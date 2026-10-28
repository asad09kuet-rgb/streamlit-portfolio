"""
All website content lives here. Edit this file to update the site; you should
not need to touch app.py.

Filled from the top card of https://www.linkedin.com/in/asad09eee/ (name,
headline, organisations, location). The saved page did not include the About,
Experience, Education or Skills sections, so anything marked "TODO" is a
placeholder: copy the real text from your LinkedIn profile into it.
"""

PROFILE = {
    "name": "Hossain Asad",
    "headline": "Bangladesh Air Force · Beihang University · KUET",
    "location": "Dhaka, Bangladesh",
    # Optional: put a square photo at assets/profile.jpg (or .png) and it will show up
    "photo": "assets/profile.jpg",
    # Optional: put your CV at assets/resume.pdf and a download button will appear
    "resume": "assets/resume.pdf",
    # TODO: replace with your LinkedIn "About" section
    "about": (
        "TODO: Write a short summary about yourself here. "
        "Who you are, what you work on, and what you are looking for. "
        "Two or three short paragraphs work best."
    ),
    "contact": {
        "email": "asad09.kuet@gmail.com",
        "linkedin": "https://www.linkedin.com/in/asad09eee/",
        "github": "https://github.com/asad09kuet-rgb",
        # Leave empty ("") to hide
        "phone": "",
        "website": "",
    },
}

# TODO: replace with your real experience (most recent first)
EXPERIENCE = [
    {
        "title": "TODO: Rank / role",
        "company": "Bangladesh Air Force",
        "location": "Dhaka, Bangladesh",
        "start": "TODO: Mon YYYY",
        "end": "Present",
        "highlights": [
            "TODO: What you did and the impact it had.",
            "TODO: Another achievement, ideally with a number.",
        ],
    },
    {
        "title": "TODO: Previous job title",
        "company": "TODO: Company name",
        "location": "TODO: City, Country",
        "start": "TODO: Mon YYYY",
        "end": "TODO: Mon YYYY",
        "highlights": [
            "TODO: Responsibility or achievement.",
        ],
    },
]

# TODO: confirm degrees, years and details
EDUCATION = [
    {
        "degree": "TODO: Degree and field",
        "school": "Beihang University",
        "start": "TODO: YYYY",
        "end": "TODO: YYYY",
        "details": "TODO: Thesis title, research area, or notable coursework.",
    },
    {
        "degree": "B.Sc. in Electrical and Electronic Engineering",  # TODO: confirm
        "school": "Khulna University of Engineering & Technology (KUET)",
        "start": "TODO: YYYY",
        "end": "TODO: YYYY",
        "details": "TODO: CGPA, thesis title, or notable coursework.",
    },
]

# Skill groups: {"Group name": ["skill", ...]}  (TODO: replace with your skills)
SKILLS = {
    "Engineering": ["Power Systems", "Circuit Design", "Control Systems", "TODO"],
    "Tools & Software": ["MATLAB", "AutoCAD", "PSpice", "TODO"],
    "Programming": ["Python", "C", "TODO"],
    "Soft skills": ["Team leadership", "Communication", "TODO"],
}

# TODO: add your projects (set "link" to "" to hide the link)
PROJECTS = [
    {
        "name": "TODO: Project name",
        "description": "TODO: One or two sentences on what it is and what you did.",
        "tags": ["TODO", "Tag"],
        "link": "",
    },
    {
        "name": "TODO: Another project",
        "description": "TODO: Short description.",
        "tags": ["TODO"],
        "link": "",
    },
]

# TODO: certifications, awards, publications. Delete entries you don't need,
# or leave the list empty ([]) to hide the section.
CERTIFICATIONS = [
    {"name": "TODO: Certification name", "issuer": "TODO: Issuer", "year": "TODO", "link": ""},
]

PUBLICATIONS = [
    # {"title": "Paper title", "venue": "Conference / Journal, YYYY", "link": "https://..."},
]
