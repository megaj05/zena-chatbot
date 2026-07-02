"""
chatbot_data.py
----------------
Single source of truth for every piece of static conversational content
used by the ZeNA AI Assistant: menus, service descriptions, training
program details, hackathon domains, social links, and the keyword
dictionary used for free-text intent matching under "Other Enquiries".

Keeping all of this in one module means the chat engine (routes/chat.py)
stays purely about *flow control*, while the actual words ZeNA says live
here and can be edited by a non-developer without touching logic.
"""

# ---------------------------------------------------------------------------
# MAIN MENU
# ---------------------------------------------------------------------------

WELCOME_MESSAGE = (
    "Hi there! 👋 I'm ZeNA, your AI-powered assistant for ZeAI Soft. "
    "I can help you explore our services, training programs, business "
    "collaboration, or answer general questions. What would you like to do?"
)

MAIN_MENU = [
    {"id": "explore_services", "label": "Explore Services"},
    {"id": "training_programs", "label": "Training Programs"},
    {"id": "business_collaboration", "label": "Business Collaboration"},
    {"id": "other_enquiries", "label": "Other Enquiries"},
]

# ---------------------------------------------------------------------------
# EXPLORE SERVICES
# ---------------------------------------------------------------------------

SERVICES = {
    "custom_software_development": {
        "label": "Custom Software Development",
        "description": (
            "We design and build tailor-made software solutions — web apps, "
            "internal tools, and enterprise systems — engineered around your "
            "exact workflows rather than forcing your business into an "
            "off-the-shelf product."
        ),
    },
    "product_engineering_services": {
        "label": "Product Engineering Services",
        "description": (
            "From idea to scale, our product engineering team handles "
            "architecture, full-stack development, QA, and DevOps so your "
            "product is built right the first time and stays maintainable "
            "as it grows."
        ),
    },
    "edtech_solutions": {
        "label": "EdTech Solutions",
        "description": (
            "We build learning platforms, LMS systems, and interactive "
            "e-learning tools that help institutions and ed-tech companies "
            "deliver engaging, measurable learning experiences."
        ),
    },
    "beautytech_solutions": {
        "label": "BeautyTech Solutions",
        "description": (
            "Our BeautyTech suite combines AI-driven try-on, skin analysis, "
            "and personalization engines to help beauty brands offer smart, "
            "data-backed customer experiences online and in-store."
        ),
    },
    "ai_services_manufacturing": {
        "label": "AI Services & Manufacturing",
        "description": (
            "We apply AI to manufacturing workflows — predictive "
            "maintenance, quality inspection, and process automation — to "
            "help manufacturers reduce downtime and improve output quality."
        ),
    },
    "it_ai_infrastructure_support": {
        "label": "IT & AI Infrastructure Support",
        "description": (
            "End-to-end support for cloud infrastructure, AI model "
            "deployment, monitoring, and IT operations, so your systems "
            "stay secure, available, and ready to scale."
        ),
    },
}

ASK_DISCUSS_REQUIREMENTS = "Would you like to discuss your requirements with our team?"

SOCIAL_LINKS = {
    "instagram": "https://www.instagram.com/zeaisoft",
    "whatsapp_community": "https://chat.whatsapp.com/zeaisoft-community",
    "linkedin": "https://www.linkedin.com/company/zeaisoft",
}

STAY_CONNECTED_PROMPT = "Would you like to stay connected with ZeAI Soft?"

# ---------------------------------------------------------------------------
# TRAINING PROGRAMS
# ---------------------------------------------------------------------------

TRAINING_PROGRAMS = [
    {"id": "skill_up_on_campus", "label": "ZeAI Skill-Up On Campus"},
    {"id": "global_immersion_program", "label": "Global Immersion Program"},
    {"id": "hackathon_2026", "label": "Hackathon 2026"},
    {"id": "connect_with_kirthika", "label": "Connect with Kirthika"},
]

SKILL_UP_LEARNING_AREAS = [
    {"id": "ai_ml", "label": "AI & Machine Learning"},
    {"id": "full_stack", "label": "Full Stack Development"},
    {"id": "qa_automation", "label": "QA Automation"},
    {"id": "cloud_infrastructure", "label": "Cloud & Infrastructure"},
]

SKILL_UP_DESCRIPTION = (
    "ZeAI Skill-Up On Campus is our hands-on training program delivered "
    "directly at college campuses, covering in-demand tech skills through "
    "live projects and mentorship from industry engineers."
)

GLOBAL_IMMERSION_DESCRIPTION = (
    "The Global Immersion Program gives students and early professionals "
    "exposure to international tech ecosystems through curated learning "
    "tracks, mentorship, and collaboration with global teams."
)

HACKATHON_DOMAINS = [
    "Artificial Intelligence & Automation",
    "Healthcare & MedTech",
    "Smart Education",
    "Women Safety & Social Impact",
    "Cybersecurity",
    "FinTech & Digital Economy",
    "Smart Mobility & Logistics",
    "Sustainability & Climate Tech",
    "Bharat & Regional Languages",
]

HACKATHON_DESCRIPTION = (
    "Hackathon 2026 is ZeAI Soft's flagship innovation challenge, bringing "
    "together builders to solve real-world problems across nine domains. "
    "Top teams get mentorship, prizes, and incubation support."
)

HACKATHON_REGISTRATION_URL = "https://www.zeaisoft.com/hackathon"

# ---------------------------------------------------------------------------
# CONNECT WITH KIRTHIKA
# ---------------------------------------------------------------------------

KIRTHIKA_INTRO = (
    "Kirthika is ZeAI Soft's lead mentor for students and early-career "
    "professionals. You can book a session with her for guidance on "
    "careers, startups, resumes, or your projects."
)

KIRTHIKA_FEATURES = [
    {"id": "book_session", "label": "Book Session"},
    {"id": "know_more", "label": "Know More"},
    {"id": "career_guidance", "label": "Career Guidance"},
    {"id": "startup_advice", "label": "Startup Advice"},
    {"id": "resume_guidance", "label": "Resume Guidance"},
    {"id": "project_discussions", "label": "Project Discussions"},
]

KIRTHIKA_KNOW_MORE = (
    "Kirthika has mentored 500+ students across AI, full-stack development, "
    "and entrepreneurship, and regularly hosts office hours for the ZeAI "
    "Soft community."
)

# ---------------------------------------------------------------------------
# BUSINESS COLLABORATION
# ---------------------------------------------------------------------------

BUSINESS_COLLAB_INTRO = (
    "Great! Let's get your collaboration request to our partnerships team. "
    "I just need a few details."
)

# ---------------------------------------------------------------------------
# OTHER ENQUIRIES — KEYWORD INTENT MATCHING
# ---------------------------------------------------------------------------
# Each intent has a list of trigger keywords (lowercase) and a canned
# response. The matcher in routes/chat.py scans the user's free-text
# message for any of these keywords. First matching intent wins.

INTENTS = [
    {
        "id": "greeting",
        "keywords": ["hi", "hello", "hey", "good morning", "good afternoon",
                     "good evening", "namaste", "hii", "helo"],
        "response": "Hello! 👋 How can I help you today? You can ask me about "
                    "our services, training programs, or anything else about "
                    "ZeAI Soft.",
    },
    {
        "id": "company_information",
        "keywords": ["about zeai", "about your company", "who are you",
                     "what is zeai", "company info", "about the company"],
        "response": "ZeAI Soft is a technology company building AI-driven "
                    "products and services across software development, "
                    "EdTech, BeautyTech, and AI-powered manufacturing, "
                    "alongside training and mentorship programs for the "
                    "next generation of tech talent.",
    },
    {
        "id": "services",
        "keywords": ["service", "services", "what do you offer", "products",
                     "solutions"],
        "response": "We offer Custom Software Development, Product "
                    "Engineering, EdTech Solutions, BeautyTech Solutions, "
                    "AI Services & Manufacturing, and IT & AI Infrastructure "
                    "Support. Would you like to explore any of these?",
    },
    {
        "id": "internship",
        "keywords": ["internship", "intern", "trainee"],
        "response": "We offer internships through our ZeAI Skill-Up On "
                    "Campus and Global Immersion programs. Would you like to "
                    "know more about our training programs?",
    },
    {
        "id": "careers",
        "keywords": ["career", "job", "jobs", "hiring", "vacancy", "openings"],
        "response": "We're always looking for great talent! Please check our "
                    "careers page at https://www.zeaisoft.com/careers or let "
                    "me connect you with Kirthika for career guidance.",
    },
    {
        "id": "contact_details",
        "keywords": ["contact", "phone number", "email address", "address",
                     "reach you", "support number"],
        "response": "You can reach ZeAI Soft at contact@zeaisoft.com or "
                    "through the WhatsApp Community and social links I can "
                    "share below.",
    },
    {
        "id": "technical_support",
        "keywords": ["bug", "error", "issue", "not working",
                     "technical support", "problem", "support"],
        "response": "Sorry to hear you're facing an issue. Could you briefly "
                    "describe the problem? I'll log it and our support team "
                    "will follow up by email.",
    },
]

FALLBACK_RESPONSE = (
    "I'm here to help you with ZeAI Soft services, programs, and support. "
    "Please select one of the options below."
)

FALLBACK_QUICK_REPLIES = [
    {"id": "explore_services", "label": "Explore Services"},
    {"id": "training_programs", "label": "Training Programs"},
    {"id": "business_collaboration", "label": "Business Collaboration"},
    {"id": "technical_support", "label": "Technical Support"},
]


def match_intent(message: str):
    """Return the first matching intent dict for a free-text message,
    or None if nothing matches (caller should use FALLBACK_RESPONSE)."""
    text = message.lower()
    for intent in INTENTS:
        for kw in intent["keywords"]:
            if kw in text:
                return intent
    return None
