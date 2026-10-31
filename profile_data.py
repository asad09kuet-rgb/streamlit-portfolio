"""
All website content lives here. Edit this file to update the site; you should
not need to touch app.py.

Content comes from the 2025 CV and the LinkedIn profile
(https://www.linkedin.com/in/asad09eee/). Phone numbers, date of birth, home
address and referees' contact details are deliberately left off because this
site is public.
"""

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
