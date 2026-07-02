"""
routes/chat.py
---------------
The conversation engine for ZeNA AI Assistant.

Design
------
The frontend is a dumb renderer: it keeps track of the *current node id*
and sends it back with every user action. This module is a state machine
that, given (node, type, value), decides what ZeNA says next, which
quick-reply buttons to show, whether to render a lead/collab/session
form, and what the *next* node id is.

Endpoints
---------
POST /api/chat     -> menu clicks & free-text messages (drives the flow)
POST /api/lead      -> form submissions (lead / collaboration / session)
GET  /api/history   -> recent chat_history rows (for admin/debug use)
"""

from flask import Blueprint, request, jsonify

import chatbot_data as data
from database.db import log_chat, get_chat_history
from models.lead import create_lead, create_session_request

chat_bp = Blueprint("chat", __name__)


# ---------------------------------------------------------------------------
# Small response helper so every branch returns a consistent shape
# ---------------------------------------------------------------------------

def reply(messages, node, quick_replies=None, show_form=None,
          form_context=None, links=None):
    if isinstance(messages, str):
        messages = [messages]
    return {
        "bot_messages": messages,
        "quick_replies": quick_replies or [],
        "node": node,
        "show_form": show_form,          # None | "lead" | "collab" | "session"
        "form_context": form_context or {},
        "links": links or [],
    }


def menu_options(items):
    """items: list of dicts with id/label -> quick reply shape."""
    return [{"id": i["id"], "label": i["label"]} for i in items]


def service_menu_items():
    return [{"id": key, "label": val["label"]} for key, val in data.SERVICES.items()]


def yes_no():
    return [{"id": "yes", "label": "Yes"}, {"id": "no", "label": "No"}]


def stay_connected_links_and_replies():
    links = [
        {"label": "Instagram", "url": data.SOCIAL_LINKS["instagram"]},
        {"label": "WhatsApp Community", "url": data.SOCIAL_LINKS["whatsapp_community"]},
        {"label": "LinkedIn", "url": data.SOCIAL_LINKS["linkedin"]},
    ]
    quick_replies = [
        {"id": "instagram", "label": "Instagram"},
        {"id": "whatsapp_community", "label": "WhatsApp Community"},
        {"id": "linkedin", "label": "LinkedIn"},
        {"id": "no_thanks", "label": "No, thanks"},
    ]
    return links, quick_replies


# ---------------------------------------------------------------------------
# Main router
# ---------------------------------------------------------------------------

@chat_bp.route("/chat", methods=["POST"])
def chat():
    body = request.get_json(force=True) or {}
    node = body.get("node", "start")
    msg_type = body.get("type", "menu")   # "menu" | "text"
    value = (body.get("value") or "").strip()

    result = route(node, msg_type, value)

    # Log the turn for analytics / GET /api/history
    user_side = value if value else "(menu opened)"
    bot_side = " | ".join(result["bot_messages"])
    log_chat(user_side, bot_side)

    return jsonify(result)


def route(node, msg_type, value):
    # -------------------- ENTRY POINT --------------------
    if node == "start":
        return reply(data.WELCOME_MESSAGE, "main_menu", menu_options(data.MAIN_MENU))

    # -------------------- MAIN MENU --------------------
    if node == "main_menu":
        return handle_main_menu(value)

    # -------------------- EXPLORE SERVICES --------------------
    if node == "service_menu":
        return handle_service_menu(value)

    if node.startswith("service_discuss_"):
        service_id = node[len("service_discuss_"):]
        return handle_service_discuss(service_id, value)

    if node == "stay_connected":
        return handle_stay_connected(value)

    # -------------------- TRAINING PROGRAMS --------------------
    if node == "training_menu":
        return handle_training_menu(value)

    if node == "skill_up_areas":
        return handle_skill_up_area(value)

    if node == "kirthika_menu":
        return handle_kirthika_menu(value)

    if node == "kirthika_offer_session":
        return handle_kirthika_offer_session(value)

    if node == "hackathon_info":
        return reply(
            "Good luck! Anything else I can help you with?",
            "main_menu", menu_options(data.MAIN_MENU),
        )

    if node == "global_immersion_interest":
        return handle_global_immersion_interest(value)

    # -------------------- BUSINESS COLLABORATION --------------------
    if node == "business_collab_form":
        # Frontend should be rendering the collab form; if the user
        # types instead of submitting, gently redirect.
        return reply(
            "Please fill in the collaboration form above so our "
            "partnerships team can reach out to you.",
            "business_collab_form", show_form="collab",
        )

    # -------------------- OTHER ENQUIRIES (free text + NLP) --------------------
    if node == "other_enquiries":
        return handle_other_enquiries(msg_type, value)

    if node == "tech_support_describe":
        return reply(
            "Thanks, I've logged your issue and our support team will "
            "reach out by email shortly. Anything else I can help with?",
            "main_menu", menu_options(data.MAIN_MENU),
        )

    # -------------------- FALLBACK FOR UNKNOWN NODE --------------------
    return reply(data.WELCOME_MESSAGE, "main_menu", menu_options(data.MAIN_MENU))


# ---------------------------------------------------------------------------
# MAIN MENU
# ---------------------------------------------------------------------------

def handle_main_menu(value):
    if value == "explore_services":
        return reply(
            "Here are our services. Tap one to learn more:",
            "service_menu", service_menu_items(),
        )
    if value == "training_programs":
        return reply(
            "Here are our training programs:",
            "training_menu", menu_options(data.TRAINING_PROGRAMS),
        )
    if value == "business_collaboration":
        return reply(
            data.BUSINESS_COLLAB_INTRO,
            "business_collab_form", show_form="collab",
        )
    if value == "other_enquiries":
        return reply(
            "Sure — ask me anything about ZeAI Soft, or pick a topic below.",
            "other_enquiries", data.FALLBACK_QUICK_REPLIES,
        )
    # Unrecognized value at main menu -> show menu again
    return reply(data.WELCOME_MESSAGE, "main_menu", menu_options(data.MAIN_MENU))


# ---------------------------------------------------------------------------
# EXPLORE SERVICES
# ---------------------------------------------------------------------------

def handle_service_menu(value):
    service = data.SERVICES.get(value)
    if not service:
        return reply(
            "Please choose a service from the list:",
            "service_menu", service_menu_items(),
        )
    messages = [service["description"], data.ASK_DISCUSS_REQUIREMENTS]
    return reply(messages, f"service_discuss_{value}", yes_no())


def handle_service_discuss(service_id, value):
    service = data.SERVICES.get(service_id, {"label": "our service"})
    if value == "yes":
        return reply(
            f"Great! Please share your details for {service['label']} "
            f"and our team will reach out.",
            "stay_connected",  # next node after the form posts to /api/lead
            show_form="lead",
            form_context={"category": service["label"]},
        )
    if value == "no":
        return reply(
            "No problem! Would you like to explore something else?",
            "main_menu", menu_options(data.MAIN_MENU),
        )
    return reply(data.ASK_DISCUSS_REQUIREMENTS, f"service_discuss_{service_id}", yes_no())


def handle_stay_connected(value):
    links, quick_replies = stay_connected_links_and_replies()
    if value in data.SOCIAL_LINKS:
        chosen = next(l for l in links if l["url"] == data.SOCIAL_LINKS[value])
        return reply(
            f"Opening {chosen['label']} for you — see you there! 💜",
            "main_menu", menu_options(data.MAIN_MENU), links=[chosen],
        )
    if value == "no_thanks":
        return reply(
            "Sounds good! Anything else I can help you with?",
            "main_menu", menu_options(data.MAIN_MENU),
        )
    return reply(data.STAY_CONNECTED_PROMPT, "stay_connected", quick_replies, links=links)


# ---------------------------------------------------------------------------
# TRAINING PROGRAMS
# ---------------------------------------------------------------------------

def handle_training_menu(value):
    if value == "skill_up_on_campus":
        return reply(
            [data.SKILL_UP_DESCRIPTION, "Which learning area interests you?"],
            "skill_up_areas", menu_options(data.SKILL_UP_LEARNING_AREAS),
        )
    if value == "global_immersion_program":
        return reply(
            [data.GLOBAL_IMMERSION_DESCRIPTION, "Would you like to register your interest?"],
            "global_immersion_interest", yes_no(),
        )
    if value == "hackathon_2026":
        domains_text = "🏆 Hackathon 2026 Domains:\n" + "\n".join(
            f"• {d}" for d in data.HACKATHON_DOMAINS
        )
        return reply(
            [data.HACKATHON_DESCRIPTION, domains_text,
             f"Register here: {data.HACKATHON_REGISTRATION_URL}"],
            "hackathon_info",
            [{"id": "back", "label": "Back to Main Menu"}],
            links=[{"label": "Register for Hackathon 2026", "url": data.HACKATHON_REGISTRATION_URL}],
        )
    if value == "connect_with_kirthika":
        return reply(
            data.KIRTHIKA_INTRO,
            "kirthika_menu", menu_options(data.KIRTHIKA_FEATURES),
        )
    return reply(
        "Please choose a training program:",
        "training_menu", menu_options(data.TRAINING_PROGRAMS),
    )


def handle_skill_up_area(value):
    area = next((a for a in data.SKILL_UP_LEARNING_AREAS if a["id"] == value), None)
    if not area:
        return reply(
            "Which learning area interests you?",
            "skill_up_areas", menu_options(data.SKILL_UP_LEARNING_AREAS),
        )
    return reply(
        f"Awesome choice! {area['label']} is one of our most popular "
        f"tracks. Share your details and our team will get you onboarded.",
        "stay_connected", show_form="lead",
        form_context={"category": f"ZeAI Skill-Up - {area['label']}"},
    )


def handle_global_immersion_interest(value):
    if value == "yes":
        return reply(
            "Wonderful! Please share your details to register your interest.",
            "stay_connected", show_form="lead",
            form_context={"category": "Global Immersion Program"},
        )
    if value == "no":
        return reply(
            "No problem! Would you like to explore something else?",
            "main_menu", menu_options(data.MAIN_MENU),
        )
    return reply(
        "Would you like to register your interest in the Global Immersion Program?",
        "global_immersion_interest", yes_no(),
    )


# ---------------------------------------------------------------------------
# CONNECT WITH KIRTHIKA
# ---------------------------------------------------------------------------

def handle_kirthika_menu(value):
    if value == "book_session":
        return reply(
            "Sure! Please share a few details and Kirthika's team will "
            "confirm a slot with you.",
            "main_menu", show_form="session",
            form_context={"purpose": "General Mentorship Session"},
        )
    if value == "know_more":
        return reply(
            [data.KIRTHIKA_KNOW_MORE],
            "kirthika_menu", menu_options(data.KIRTHIKA_FEATURES),
        )
    topic_map = {
        "career_guidance": "career guidance",
        "startup_advice": "startup advice",
        "resume_guidance": "resume guidance",
        "project_discussions": "project discussions",
    }
    if value in topic_map:
        return reply(
            f"Kirthika regularly mentors students on {topic_map[value]}. "
            f"Would you like to book a session on this topic?",
            "kirthika_offer_session", yes_no(),
        )
    return reply(
        data.KIRTHIKA_INTRO,
        "kirthika_menu", menu_options(data.KIRTHIKA_FEATURES),
    )


def handle_kirthika_offer_session(value):
    if value == "yes":
        return reply(
            "Great! Please share your details to book the session.",
            "main_menu", show_form="session",
            form_context={"purpose": "Mentorship Session"},
        )
    if value == "no":
        return reply(
            "No problem! Anything else I can help you with?",
            "main_menu", menu_options(data.MAIN_MENU),
        )
    return reply(
        "Would you like to book a session with Kirthika?",
        "kirthika_offer_session", yes_no(),
    )


# ---------------------------------------------------------------------------
# OTHER ENQUIRIES (free text + keyword NLP)
# ---------------------------------------------------------------------------

def handle_other_enquiries(msg_type, value):
    # Quick-reply shortcuts shown alongside the free-text box
    if value == "explore_services":
        return reply(
            "Here are our services. Tap one to learn more:",
            "service_menu", service_menu_items(),
        )
    if value == "training_programs":
        return reply(
            "Here are our training programs:",
            "training_menu", menu_options(data.TRAINING_PROGRAMS),
        )
    if value == "business_collaboration":
        return reply(
            data.BUSINESS_COLLAB_INTRO,
            "business_collab_form", show_form="collab",
        )
    if value == "technical_support":
        return reply(
            "Sure, please describe the issue you're facing and I'll log "
            "it for our support team.",
            "tech_support_describe",
        )

    # Free-text NLP intent matching
    if value:
        intent = data.match_intent(value)
        if intent:
            return reply(intent["response"], "other_enquiries", data.FALLBACK_QUICK_REPLIES)
        return reply(data.FALLBACK_RESPONSE, "other_enquiries", data.FALLBACK_QUICK_REPLIES)

    return reply(
        "Ask me anything about ZeAI Soft, or pick a topic below.",
        "other_enquiries", data.FALLBACK_QUICK_REPLIES,
    )


# ---------------------------------------------------------------------------
# /api/lead  — form submissions (lead / collaboration / session)
# ---------------------------------------------------------------------------

@chat_bp.route("/lead", methods=["POST"])
def submit_lead():
    body = request.get_json(force=True) or {}
    form_type = body.get("formType", "lead")   # "lead" | "collab" | "session"
    name = (body.get("name") or "").strip()
    email = (body.get("email") or "").strip()
    phone = (body.get("phone") or "").strip()

    if not name or not email:
        return jsonify({"error": "Name and email are required."}), 400

    if form_type == "session":
        purpose = body.get("purpose", "Mentorship Session")
        create_session_request(name, email, phone, purpose)
        result = reply(
            f"Thanks, {name}! Your session request has been received. "
            f"Kirthika's team will email you shortly to confirm a time.",
            "main_menu", menu_options(data.MAIN_MENU),
        )
        log_chat(f"[session form] {name}", result["bot_messages"][0])
        return jsonify(result)

    requirement = (body.get("requirement") or "").strip()
    category = (body.get("category") or "General Enquiry").strip()

    if form_type == "collab":
        company_name = (body.get("companyName") or "").strip()
        create_lead(name, email, phone, "Business Collaboration", requirement, company_name)
        links, quick_replies = stay_connected_links_and_replies()
        result = reply(
            [f"Thanks, {name}! Your collaboration request has been sent to "
             f"our partnerships team.", data.STAY_CONNECTED_PROMPT],
            "stay_connected", quick_replies, links=links,
        )
        log_chat(f"[collab form] {name} @ {company_name}", result["bot_messages"][0])
        return jsonify(result)

    # default: regular service / program lead
    create_lead(name, email, phone, category, requirement)
    links, quick_replies = stay_connected_links_and_replies()
    result = reply(
        [f"Thanks, {name}! Our team will reach out to you about "
         f"{category} shortly.", data.STAY_CONNECTED_PROMPT],
        "stay_connected", quick_replies, links=links,
    )
    log_chat(f"[lead form] {name} - {category}", result["bot_messages"][0])
    return jsonify(result)


# ---------------------------------------------------------------------------
# /api/history
# ---------------------------------------------------------------------------

@chat_bp.route("/history", methods=["GET"])
def history():
    limit = request.args.get("limit", default=50, type=int)
    rows = get_chat_history(limit=limit)
    return jsonify({"history": rows})
