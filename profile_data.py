"""
All website content lives here. Edit this file to update the site; you should
not need to touch app.py.

Content comes from the 2025 CV and the LinkedIn profile
(https://www.linkedin.com/in/asad09eee/). Phone numbers, date of birth, home
address and referees' contact details are deliberately left off because this
site is public.
"""

PROFILE = {
    "name": "Md. Asad Hossain",
    "headline": "Squadron Leader, Bangladesh Air Force · Electrical & Electronic Engineer (KUET)",
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
        "linkedin": "https://www.linkedin.com/in/asad09eee/",
        "github": "https://github.com/asad09kuet-rgb",
        # Leave empty ("") to hide
        "phone": "",
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
        "degree": "Master's in Space Project Management (in progress)",
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
        "school": "Kaliganj M.U. Degree College, Jhenaidah",
        "start": "",
        "end": "2009",
        "details": "GPA 5.00 / 5.00",
    },
    {
        "degree": "S.S.C., Science",
        "school": "N.B. High School, Jhenaidah",
        "start": "",
        "end": "2007",
        "details": "GPA 5.00 / 5.00",
    },
]

# Skill groups: {"Group name": ["skill", ...]}
SKILLS = {
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
        "Logistics",
    ],
    "Leadership": [
        "Team Leadership",
        "Staff Development & Mentoring",
        "Instruction & Training",
        "Cross-Cultural & Multinational Collaboration",
    ],
}

# Research work, shown as project cards ("link" set to "" hides the link)
PROJECTS = [
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
        "Institute, Cox's Bazar, 2024.",
        "tags": ["Defence", "Disaster Response", "Research"],
        "link": "",
    },
]

# Leave a list empty ([]) to hide it
CERTIFICATIONS = [
    {"name": "No. 125 Junior Command & Staff Course", "issuer": "CSTI BAF, Cox's Bazar", "year": "", "link": ""},
    {"name": "Aviation Risk Management (ARM) Course", "issuer": "UN Global Service Centre", "year": "", "link": ""},
    {"name": "United Nations Peacekeeping Certificate", "issuer": "MINUSMA, Mali", "year": "", "link": ""},
    {"name": "AW119 Helicopter Maintenance Course", "issuer": "Philadelphia, USA", "year": "", "link": ""},
    {"name": "Aviation Safety Course", "issuer": "Civil Aviation Training Centre, Dhaka", "year": "", "link": ""},
    {"name": "Ramp Safety Course", "issuer": "Bangladesh Airlines Training Center, Dhaka", "year": "", "link": ""},
    {"name": "No. 03 Cat D Course", "issuer": "Officers Training School BAF, Jashore", "year": "", "link": ""},
    {"name": "No. 09 PCPT Course", "issuer": "Officers Training School BAF, Jashore", "year": "", "link": ""},
]

PUBLICATIONS = [
    {
        "title": "Optimal On-Grid Hybrid Renewable Energy Model for Coastal Area: Bangladesh Perspective",
        "venue": "IEEE, University of Dhaka, 2014",
        "link": "",
    },
]

AFFILIATIONS = ["Member, Institution of Engineers, Bangladesh (IEB)"]

LANGUAGES = {"English": "Advanced (C1)", "Arabic": "Beginner (A1)", "French": "Beginner (A1)"}

COUNTRIES_VISITED = ["USA", "Canada", "Qatar", "Mali"]
