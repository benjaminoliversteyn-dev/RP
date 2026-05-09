import streamlit as st
import json
import random
from datetime import datetime, date, timedelta
import pandas as pd

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Rachel's Pregnancy Journey 🌸",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Lato', sans-serif;
}

/* ── Soft pink background ── */
.stApp {
    background: linear-gradient(160deg, #fff5f7 0%, #fce4ec 40%, #f8bbd0 100%);
    min-height: 100vh;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header {visibility: hidden;}
.block-container {padding-top: 1.5rem; padding-bottom: 4rem; max-width: 480px; margin: auto;}

/* ── App title ── */
.app-title {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    color: #880e4f;
    text-align: center;
    margin-bottom: 0.2rem;
    line-height: 1.2;
}
.app-sub {
    font-family: 'Lato', sans-serif;
    font-size: 0.85rem;
    color: #ad1457;
    text-align: center;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}

/* ── Nav pills ── */
div[data-testid="stHorizontalBlock"] button {
    border-radius: 50px !important;
    border: 2px solid #f48fb1 !important;
    background: white !important;
    color: #880e4f !important;
    font-weight: 700 !important;
    font-size: 0.78rem !important;
    padding: 0.3rem 0.7rem !important;
}

/* ── Cards ── */
.card {
    background: rgba(255,255,255,0.82);
    border-radius: 18px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 20px rgba(136,14,79,0.08);
    border-left: 5px solid #f48fb1;
}
.card h3 {
    font-family: 'Playfair Display', serif;
    color: #880e4f;
    margin: 0 0 0.4rem 0;
    font-size: 1.1rem;
}
.card p, .card li {
    font-size: 0.9rem;
    color: #4a4a4a;
    margin: 0.2rem 0;
}

/* ── Section headers ── */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    color: #880e4f;
    margin: 0.5rem 0 1rem 0;
    border-bottom: 2px solid #f8bbd0;
    padding-bottom: 0.4rem;
}

/* ── Milestone timeline ── */
.milestone {
    display: flex;
    align-items: flex-start;
    gap: 0.8rem;
    margin-bottom: 0.9rem;
}
.ms-dot {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
    font-weight: bold;
}
.ms-done  { background: #e8f5e9; border: 2px solid #66bb6a; color: #2e7d32; }
.ms-now   { background: #fce4ec; border: 2px solid #e91e63; color: #880e4f; animation: pulse 1.8s infinite; }
.ms-future{ background: #f3e5f5; border: 2px solid #ce93d8; color: #6a1b9a; }
@keyframes pulse { 0%,100%{box-shadow:0 0 0 0 rgba(233,30,99,0.3);} 50%{box-shadow:0 0 0 8px rgba(233,30,99,0);} }

.ms-info h4 { margin: 0; font-size: 0.92rem; color: #880e4f; font-weight: 700; }
.ms-info p  { margin: 0.15rem 0 0 0; font-size: 0.82rem; color: #666; }
.ms-bar-bg  { background: #f8bbd0; border-radius: 10px; height: 6px; margin-top: 0.4rem; }
.ms-bar     { background: linear-gradient(90deg,#e91e63,#f06292); border-radius: 10px; height: 6px; }

/* ── Motivational card ── */
.motivational {
    background: linear-gradient(135deg, #880e4f 0%, #ad1457 100%);
    color: white;
    border-radius: 22px;
    padding: 2rem 1.6rem;
    text-align: center;
    box-shadow: 0 8px 30px rgba(136,14,79,0.3);
    margin-bottom: 1.5rem;
}
.motivational .quote {
    font-family: 'Playfair Display', serif;
    font-size: 1.25rem;
    font-style: italic;
    line-height: 1.6;
    margin-bottom: 0.8rem;
}
.motivational .source {
    font-size: 0.82rem;
    opacity: 0.8;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* ── Symptom log ── */
.log-entry {
    background: white;
    border-radius: 14px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.7rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    border-left: 4px solid #f48fb1;
}
.log-date { font-size: 0.75rem; color: #999; margin-bottom: 0.3rem; }
.log-text { font-size: 0.9rem; color: #333; }

/* ── Meal category badge ── */
.badge {
    display: inline-block;
    padding: 0.15rem 0.7rem;
    border-radius: 50px;
    font-size: 0.72rem;
    font-weight: 700;
    margin-right: 0.3rem;
    margin-bottom: 0.4rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.badge-green  { background: #e8f5e9; color: #2e7d32; }
.badge-pink   { background: #fce4ec; color: #880e4f; }
.badge-purple { background: #f3e5f5; color: #6a1b9a; }
.badge-orange { background: #fff3e0; color: #e65100; }

/* ── Shopping list checkbox styling ── */
.stCheckbox label { font-size: 0.9rem !important; color: #333 !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #e91e63, #ad1457) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 0.55rem 2rem !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.05em !important;
    width: 100%;
}
.stButton > button:hover { opacity: 0.9; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.6) !important;
    border-radius: 50px !important;
    padding: 4px !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 50px !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    color: #880e4f !important;
    padding: 0.35rem 0.7rem !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg,#e91e63,#ad1457) !important;
    color: white !important;
}

/* ── Slider ── */
.stSlider { padding: 0 0.5rem; }
</style>
""", unsafe_allow_html=True)

# ── Initialise session state ──────────────────────────────────────────────────
if "symptom_log" not in st.session_state:
    st.session_state.symptom_log = []
if "shopping_done" not in st.session_state:
    st.session_state.shopping_done = {}
if "quote_idx" not in st.session_state:
    st.session_state.quote_idx = 0
if "meal_plan" not in st.session_state:
    st.session_state.meal_plan = {}

# ── Data ─────────────────────────────────────────────────────────────────────

DUE_DATE = date(2025, 12, 28)          # ← update this if needed
CONCEPTION_DATE = date(2025, 3, 23)

def weeks_pregnant():
    delta = date.today() - CONCEPTION_DATE
    return max(0, delta.days // 7)

MILESTONES = [
    {"week": 4,  "emoji": "🌱", "title": "Positive test!",           "desc": "Your tiny miracle implants and begins to grow."},
    {"week": 6,  "emoji": "💓", "title": "Heartbeat detected",        "desc": "A flickering heartbeat appears on scan — magic!"},
    {"week": 8,  "emoji": "🫘", "title": "Size of a kidney bean",     "desc": "Fingers & toes are forming. You're doing amazingly."},
    {"week": 10, "emoji": "🍓", "title": "Size of a strawberry",      "desc": "All major organs in place. Morning sickness may peak."},
    {"week": 12, "emoji": "🌸", "title": "End of first trimester!",   "desc": "Risk drops significantly. Time to share the news! 🎉"},
    {"week": 16, "emoji": "🥑", "title": "Size of an avocado",        "desc": "Baby can hear your voice. Chat away!"},
    {"week": 20, "emoji": "🍌", "title": "Halfway there! 20 weeks",   "desc": "Anatomy scan! You might find out the sex."},
    {"week": 24, "emoji": "🌽", "title": "Viability milestone",       "desc": "Baby could survive outside the womb with support."},
    {"week": 28, "emoji": "🥦", "title": "Third trimester begins",    "desc": "Baby opens its eyes and dreams!"},
    {"week": 32, "emoji": "🥥", "title": "Lungs maturing",            "desc": "Practising breathing movements every day."},
    {"week": 36, "emoji": "🍉", "title": "Almost full term!",         "desc": "Head may engage. Get that hospital bag ready!"},
    {"week": 40, "emoji": "👶", "title": "Due date!",                 "desc": "Welcome to the world, little one! 🌸"},
]

MOTIVATIONAL_QUOTES = [
    ("You are growing a miracle. Every day of discomfort is a testament to your incredible strength.", "For the hard mornings"),
    ("Morning sickness is your body working overtime for your baby. You are extraordinary.", "First trimester"),
    ("Rest is not laziness — it is the most productive thing you can do right now.", "Permission to rest"),
    ("You were made for this. Your body knows exactly what it's doing.", "Trust your body"),
    ("This tiredness you feel? It's the weight of a whole new person being built inside you. You're amazing.", "Energy dip days"),
    ("Some days you'll feel green around the gills. That's okay. You're still a superhero.", "For nausea days"),
    ("Your baby already loves you — they've never known a world without you in it.", "Bonding"),
    ("The sickness will pass. The baby will stay. Hold on, mama.", "Light at the end"),
    ("You don't have to feel radiant to be radiant. You are literally glowing from the inside out.", "Body confidence"),
    ("Every cracker you manage to keep down, every nap you take — it all counts. You're doing it.", "Small wins"),
    ("Pregnancy is not a performance. There is no wrong way to do this.", "Pressure off"),
    ("Talk to your bump. Sing to them. They already know your voice.", "Connection"),
    ("You are building someone's whole world. What could be more powerful than that?", "Purpose"),
    ("On the days you feel awful, remember: you're also the reason someone will one day run toward you with open arms.", "Future love"),
    ("Be patient with yourself. You are learning how to be a mother while already being one.", "Grace"),
]

FOODS = {
    "🥦 Folate-rich (crucial!)": [
        ("Spinach & kale", "Raw in smoothies or lightly wilted — aim for a handful daily"),
        ("Broccoli", "Steam lightly to keep nutrients. Add to pasta or stir-fries"),
        ("Asparagus", "Roast with olive oil. Great folate source"),
        ("Lentils", "Add to soups and dals — also packed with iron"),
        ("Fortified cereals", "Check label for folic acid — easy morning option"),
        ("Edamame", "Snack on these straight from frozen once defrosted"),
    ],
    "🥩 Iron & Protein": [
        ("Lean red meat", "2–3 times a week. Pair with vitamin C to boost iron absorption"),
        ("Chicken & turkey", "Versatile protein — ensure fully cooked"),
        ("Eggs", "Perfect protein. Scrambled, boiled, poached — all great"),
        ("Tofu & tempeh", "Plant-based iron. Marinate and pan-fry for flavour"),
        ("Chickpeas", "Add to curries, salads, or roast as a crunchy snack"),
        ("Oily fish (salmon, sardines)", "2 portions per week max. Omega-3 for brain development"),
    ],
    "🥛 Calcium & Dairy": [
        ("Full-fat yoghurt", "Calcium + protein + probiotics. Add honey and berries"),
        ("Milk", "Opt for full-fat. Great in porridge, smoothies"),
        ("Cheese (hard)", "Cheddar, parmesan — fine to eat. Avoid soft unpasteurised"),
        ("Fortified plant milks", "Oat or almond — check for calcium fortification"),
    ],
    "🍇 Snacks to ease nausea": [
        ("Plain crackers / oatcakes", "Keep by the bed — eat before getting up!"),
        ("Ginger biscuits", "Ginger genuinely helps nausea — have a few with tea"),
        ("Watermelon", "Hydrating and easy on the stomach"),
        ("Banana", "Gentle on the stomach, provides potassium"),
        ("Rice cakes with peanut butter", "Protein + carbs = steady blood sugar"),
        ("Cold fruit & yoghurt", "Cold foods often feel easier when nauseous"),
    ],
    "💧 Hydration": [
        ("Water", "Aim for 8–10 glasses daily. Add cucumber or lemon if plain is off-putting"),
        ("Coconut water", "Natural electrolytes — great if vomiting"),
        ("Ginger tea", "Soothing for morning sickness. Avoid very strong brews"),
        ("Peppermint tea", "Eases nausea and bloating"),
        ("Diluted fruit juice", "If you struggle with plain water"),
    ],
}

SHOPPING_CATEGORIES = {
    "🏥 Pregnancy Essentials": [
        "Folic acid 400mcg (until week 12)",
        "Vitamin D supplement",
        "Pregnancy multivitamin",
        "Omega-3 (DHA) supplement",
        "Pregnancy test (spare)",
        "Maternity notes folder",
    ],
    "🧴 Body & Skin": [
        "Stretch mark oil / bio-oil",
        "Nipple cream (Lansinoh)",
        "Gentle fragrance-free moisturiser",
        "Maternity bra (x2)",
        "Maternity knickers (x3)",
        "Non-slip bath mat",
    ],
    "😴 Sleep & Comfort": [
        "Pregnancy pillow (full-body wedge)",
        "Heartburn pillow wedge",
        "Loose comfortable nightwear",
        "Anti-nausea wristbands (Sea-Bands)",
    ],
    "🍪 Nausea & Morning Sickness": [
        "Plain crackers / oatcakes",
        "Ginger biscuits",
        "Ginger tea bags",
        "Peppermint tea bags",
        "Coconut water (cartons)",
        "Dry cereal / porridge oats",
        "Ice lollies / ice chips",
    ],
    "📚 Reading & Prep": [
        "What to Expect When You're Expecting (book)",
        "Pregnancy journal / diary",
        "Hypnobirthing book or course",
        "Hospital bag list (print off NHS)",
    ],
    "🏠 For the Home": [
        "Pregnancy-safe cleaning products",
        "Carbon monoxide detector",
        "First aid kit refresh",
        "Thermometer",
    ],
}

NHS_INFO = [
    {
        "title": "Morning Sickness — What's Normal",
        "icon": "🤢",
        "body": (
            "Morning sickness affects up to 80% of pregnant women. Despite the name, it can strike at any time of day. "
            "It typically starts around week 6, peaks around weeks 8–10, and usually improves by weeks 12–14 — though for some it lasts longer. "
            "It is caused by the hormone hCG (human chorionic gonadotropin) surging in early pregnancy. Paradoxically, nausea can be a sign your pregnancy is progressing well."
        ),
    },
    {
        "title": "Tips to Manage Nausea",
        "icon": "💡",
        "body": (
            "• Eat little and often — an empty stomach makes nausea worse.\n"
            "• Keep plain crackers by your bed and eat them before sitting up.\n"
            "• Avoid strong smells — cold foods often smell less.\n"
            "• Ginger — biscuits, tea, or ginger ale — has evidence behind it.\n"
            "• Stay hydrated; small sips frequently if large drinks trigger nausea.\n"
            "• Rest as much as you can — fatigue worsens symptoms.\n"
            "• Anti-nausea wristbands (Sea-Bands) work for some women."
        ),
    },
    {
        "title": "When to Call Your Midwife",
        "icon": "📞",
        "body": (
            "Contact your GP or midwife if you:\n"
            "• Cannot keep any food or fluids down for 24 hours\n"
            "• Feel very unwell, dizzy or faint\n"
            "• Are losing weight rapidly\n"
            "• Have dark urine or are not urinating\n"
            "• Have abdominal pain alongside vomiting\n\n"
            "Hyperemesis gravidarum (severe morning sickness) affects ~1% of pregnancies and needs treatment — don't suffer in silence."
        ),
    },
    {
        "title": "First Trimester Appointments",
        "icon": "📅",
        "body": (
            "• **Booking appointment** (8–10 weeks): Long midwife appointment — blood tests, blood pressure, urine, history.\n"
            "• **Dating scan** (8–14 weeks): Confirms due date via ultrasound.\n"
            "• **12-week scan** (11–14 weeks): Combined screening for chromosomal conditions (optional).\n"
            "• **16-week midwife check**: Review screening results, blood pressure, questions.\n"
            "• **20-week anatomy scan**: Detailed check of baby's organs and measurements."
        ),
    },
    {
        "title": "Things to Avoid in Pregnancy",
        "icon": "🚫",
        "body": (
            "**Food**: Avoid raw/undercooked meat, liver, pâté, raw shellfish, unpasteurised cheese (soft mould-ripened like brie, camembert), raw eggs, and shark/swordfish/marlin. Limit tuna to 2 tins/week and oily fish to 2 portions/week.\n\n"
            "**Alcohol**: The NHS advises no alcohol at all during pregnancy.\n\n"
            "**Caffeine**: Limit to 200mg/day (approx. 1–2 coffees or 2–3 teas).\n\n"
            "**Other**: Don't smoke, avoid second-hand smoke, avoid contact sports with risk of falls."
        ),
    },
    {
        "title": "Your Mental Health Matters",
        "icon": "💜",
        "body": (
            "Pregnancy can bring anxiety, low mood, and worry — this is very common and nothing to be ashamed of. "
            "Up to 1 in 5 women experience mental health difficulties during pregnancy or in the first year after birth.\n\n"
            "Speak to your midwife or GP if you're struggling. There is support available including talking therapies, peer support groups, and medication where needed. "
            "You do not have to feel happy all the time to be doing a wonderful job."
        ),
    },
]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="app-title">🌸 Rachel\'s Journey</div>', unsafe_allow_html=True)
wk = weeks_pregnant()
days_to_go = (DUE_DATE - date.today()).days
st.markdown(f'<div class="app-sub">Week {wk} · {days_to_go} days to go · Due {DUE_DATE.strftime("%d %b %Y")}</div>', unsafe_allow_html=True)

# ── Navigation tabs ───────────────────────────────────────────────────────────
tabs = st.tabs(["📅 Timeline", "💬 Boost", "🥗 Food", "🛒 Shopping", "📓 Log", "🏥 NHS Info"])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — TIMELINE
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="section-title">Your Pregnancy Timeline</div>', unsafe_allow_html=True)

    current_week = weeks_pregnant()

    for ms in MILESTONES:
        w = ms["week"]
        if w < current_week:
            dot_class, status = "ms-done", "✓"
        elif w == current_week or (w > current_week and w <= current_week + 1):
            dot_class, status = "ms-now", "NOW"
        else:
            dot_class, status = "ms-future", str(w)

        pct = min(100, int((current_week / w) * 100)) if w >= current_week else 100

        st.markdown(f"""
        <div class="milestone">
          <div class="ms-dot {dot_class}">{ms['emoji']}</div>
          <div class="ms-info" style="flex:1">
            <h4>Week {w} — {ms['title']}</h4>
            <p>{ms['desc']}</p>
            <div class="ms-bar-bg"><div class="ms-bar" style="width:{pct}%"></div></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Custom milestone ──
    st.markdown("---")
    st.markdown("**➕ Add your own milestone**")
    with st.expander("Add a personal milestone"):
        col1, col2 = st.columns([1, 2])
        with col1:
            custom_week = st.number_input("Week", min_value=1, max_value=42, value=12)
        with col2:
            custom_title = st.text_input("Milestone name", placeholder="e.g. First scan!")
        custom_desc = st.text_input("Notes (optional)", placeholder="e.g. Saw the heartbeat!")
        if st.button("Add milestone 🌸"):
            if "custom_milestones" not in st.session_state:
                st.session_state.custom_milestones = []
            st.session_state.custom_milestones.append({
                "week": custom_week, "title": custom_title, "desc": custom_desc
            })
            st.success("Milestone added!")

    if "custom_milestones" in st.session_state and st.session_state.custom_milestones:
        st.markdown("**Your milestones:**")
        for cm in st.session_state.custom_milestones:
            st.markdown(f"""
            <div class="milestone">
              <div class="ms-dot ms-future">⭐</div>
              <div class="ms-info">
                <h4>Week {cm['week']} — {cm['title']}</h4>
                <p>{cm['desc']}</p>
              </div>
            </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — MOTIVATIONAL BOOST
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="section-title">Your Daily Boost 💬</div>', unsafe_allow_html=True)

    idx = st.session_state.quote_idx % len(MOTIVATIONAL_QUOTES)
    quote, source = MOTIVATIONAL_QUOTES[idx]

    st.markdown(f"""
    <div class="motivational">
      <div class="quote">"{quote}"</div>
      <div class="source">— {source}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("✨ Give me another boost"):
        st.session_state.quote_idx = random.randint(0, len(MOTIVATIONAL_QUOTES) - 1)
        st.rerun()

    st.markdown("---")
    st.markdown("**💌 Write yourself a note**")
    st.markdown('<p style="font-size:0.85rem;color:#666">Something to read on a hard day...</p>', unsafe_allow_html=True)

    note_input = st.text_area("Your note to future-you", placeholder="Dear Rachel, on the hard days remember...", height=120, label_visibility="collapsed")
    if st.button("Save note 💾"):
        if note_input.strip():
            if "personal_notes" not in st.session_state:
                st.session_state.personal_notes = []
            st.session_state.personal_notes.append({
                "date": date.today().strftime("%d %b %Y"),
                "text": note_input.strip()
            })
            st.success("Saved! 🌸")

    if "personal_notes" in st.session_state and st.session_state.personal_notes:
        st.markdown("**Your notes:**")
        for n in reversed(st.session_state.personal_notes):
            st.markdown(f"""
            <div class="log-entry">
              <div class="log-date">{n['date']}</div>
              <div class="log-text">{n['text']}</div>
            </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — FOOD & MEAL PLANNING
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="section-title">Pregnancy Nutrition 🥗</div>', unsafe_allow_html=True)

    for category, items in FOODS.items():
        with st.expander(category):
            for name, tip in items:
                st.markdown(f"""
                <div class="card" style="margin-bottom:0.6rem">
                  <h3>🌿 {name}</h3>
                  <p>{tip}</p>
                </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<p class="section-title" style="font-size:1.1rem">🗓️ Quick Meal Planner</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.82rem;color:#666">Tap a day to plan it — ideas pulled from the foods above.</p>', unsafe_allow_html=True)

    MEAL_IDEAS = {
        "Breakfast": [
            "Porridge with banana and honey",
            "Scrambled eggs on wholegrain toast",
            "Fortified cereal with full-fat milk",
            "Greek yoghurt with berries and granola",
            "Smoothie with spinach, banana, milk",
        ],
        "Lunch": [
            "Lentil soup with crusty bread",
            "Grilled chicken salad with spinach and feta",
            "Tuna & cucumber sandwich (wholegrain)",
            "Chickpea and veg stir-fry with rice",
            "Omelette with cheese and salad",
        ],
        "Dinner": [
            "Salmon with sweet potato and broccoli",
            "Chicken and lentil dhal with rice",
            "Beef stir-fry with egg noodles and veg",
            "Pasta with turkey meatballs in tomato sauce",
            "Tofu and vegetable curry with brown rice",
        ],
        "Snacks": [
            "Oatcakes with peanut butter",
            "Apple slices and cheese",
            "Edamame beans",
            "Ginger biscuits and peppermint tea",
            "Rice cakes with hummus",
        ],
    }

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    selected_day = st.selectbox("Plan for:", days)

    if selected_day not in st.session_state.meal_plan:
        st.session_state.meal_plan[selected_day] = {}

    col1, col2 = st.columns(2)
    for i, (meal, ideas) in enumerate(MEAL_IDEAS.items()):
        container = col1 if i % 2 == 0 else col2
        with container:
            current = st.session_state.meal_plan.get(selected_day, {}).get(meal, ideas[0])
            choice = st.selectbox(meal, ideas, index=ideas.index(current) if current in ideas else 0, key=f"meal_{selected_day}_{meal}")
            st.session_state.meal_plan.setdefault(selected_day, {})[meal] = choice

    if st.button("🎲 Shuffle my meals!"):
        for meal, ideas in MEAL_IDEAS.items():
            st.session_state.meal_plan.setdefault(selected_day, {})[meal] = random.choice(ideas)
        st.rerun()

    # Show plan summary
    if st.session_state.meal_plan:
        st.markdown("---")
        st.markdown("**📋 Your week at a glance:**")
        for day in days:
            if day in st.session_state.meal_plan:
                plan = st.session_state.meal_plan[day]
                meals_text = " · ".join([f"{k}: {v}" for k, v in plan.items()])
                st.markdown(f"""
                <div class="log-entry">
                  <div class="log-date">{day}</div>
                  <div class="log-text" style="font-size:0.8rem">{meals_text}</div>
                </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — SHOPPING LIST
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-title">Shopping List 🛒</div>', unsafe_allow_html=True)

    total_items = sum(len(v) for v in SHOPPING_CATEGORIES.values())
    done_count = sum(1 for v in st.session_state.shopping_done.values() if v)
    pct_done = int((done_count / total_items) * 100) if total_items else 0

    st.markdown(f"""
    <div class="card">
      <h3>Progress: {done_count}/{total_items} items ({pct_done}%)</h3>
      <div class="ms-bar-bg"><div class="ms-bar" style="width:{pct_done}%"></div></div>
    </div>""", unsafe_allow_html=True)

    for category, items in SHOPPING_CATEGORIES.items():
        with st.expander(category):
            for item in items:
                key = f"shop_{category}_{item}"
                checked = st.checkbox(item, value=st.session_state.shopping_done.get(key, False), key=key)
                st.session_state.shopping_done[key] = checked

    st.markdown("---")
    st.markdown("**➕ Add your own item**")
    col1, col2 = st.columns([3, 1])
    with col1:
        new_item = st.text_input("Item name", placeholder="e.g. Raspberry leaf tea", label_visibility="collapsed")
    with col2:
        if st.button("Add"):
            if new_item.strip():
                if "custom_shopping" not in st.session_state:
                    st.session_state.custom_shopping = []
                st.session_state.custom_shopping.append(new_item.strip())
                st.rerun()

    if "custom_shopping" in st.session_state and st.session_state.custom_shopping:
        st.markdown("**Your additions:**")
        for ci, citem in enumerate(st.session_state.custom_shopping):
            key = f"custom_shop_{ci}"
            st.checkbox(citem, value=st.session_state.shopping_done.get(key, False), key=key)
            st.session_state.shopping_done[key] = st.session_state.get(key, False)

    if st.button("Clear completed ✓"):
        st.session_state.shopping_done = {k: v for k, v in st.session_state.shopping_done.items() if not v}
        st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 5 — SYMPTOM LOG
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-title">Daily Symptom Log 📓</div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.85rem;color:#666;margin-bottom:1rem">Track how you\'re feeling each day — bring this to midwife appointments.</p>', unsafe_allow_html=True)

    # Input form
    with st.expander("➕ Log today's symptoms", expanded=True):
        log_date = st.date_input("Date", value=date.today())
        week_num = st.number_input("Pregnancy week", min_value=1, max_value=42, value=weeks_pregnant())

        st.markdown("**Nausea level (0 = none, 10 = severe)**")
        nausea = st.slider("Nausea", 0, 10, 3, label_visibility="collapsed")

        st.markdown("**Energy level (0 = exhausted, 10 = great)**")
        energy = st.slider("Energy", 0, 10, 5, label_visibility="collapsed")

        st.markdown("**Mood (0 = very low, 10 = wonderful)**")
        mood = st.slider("Mood", 0, 10, 6, label_visibility="collapsed")

        symptoms_today = st.multiselect(
            "Symptoms today",
            ["Morning sickness", "Nausea all day", "Vomiting", "Food aversions",
             "Cravings", "Fatigue", "Headache", "Bloating", "Heartburn",
             "Breast tenderness", "Spotting", "Cramps (mild)", "Mood swings",
             "Dizziness", "Constipation", "Frequent urination"],
        )

        notes_today = st.text_area("Any notes or observations?", placeholder="e.g. Kept down ginger biscuits today — small win! 🎉", height=90)

        if st.button("Save today's log 💾"):
            entry = {
                "date": log_date.strftime("%d %b %Y"),
                "week": week_num,
                "nausea": nausea,
                "energy": energy,
                "mood": mood,
                "symptoms": symptoms_today,
                "notes": notes_today,
            }
            st.session_state.symptom_log.insert(0, entry)
            st.success("Logged! 🌸 You're doing great.")

    # Past entries
    if st.session_state.symptom_log:
        st.markdown("---")
        st.markdown("**Past entries:**")

        for entry in st.session_state.symptom_log:
            nausea_bar = "🟥" * entry["nausea"] + "⬜" * (10 - entry["nausea"])
            energy_bar = "🟩" * entry["energy"] + "⬜" * (10 - entry["energy"])
            mood_bar   = "💜" * entry["mood"]   + "⬜" * (10 - entry["mood"])
            symp_str   = ", ".join(entry["symptoms"]) if entry["symptoms"] else "None recorded"

            st.markdown(f"""
            <div class="log-entry">
              <div class="log-date">Week {entry['week']} · {entry['date']}</div>
              <div class="log-text">
                <b>Nausea:</b> {nausea_bar} ({entry['nausea']}/10)<br>
                <b>Energy:</b> {energy_bar} ({entry['energy']}/10)<br>
                <b>Mood:</b>   {mood_bar} ({entry['mood']}/10)<br>
                <b>Symptoms:</b> {symp_str}<br>
                {"<b>Notes:</b> " + entry['notes'] if entry['notes'] else ""}
              </div>
            </div>""", unsafe_allow_html=True)

        if st.button("Export log as CSV 📊"):
            df = pd.DataFrame(st.session_state.symptom_log)
            csv = df.to_csv(index=False)
            st.download_button(
                "Download CSV",
                data=csv,
                file_name=f"rachel_symptom_log_{date.today()}.csv",
                mime="text/csv",
            )
    else:
        st.markdown("""
        <div class="card" style="text-align:center;border-left-color:#ce93d8">
          <h3 style="color:#6a1b9a">No entries yet 📓</h3>
          <p>Start logging above — even a quick note each day builds a valuable picture for your midwife.</p>
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 6 — NHS INFO
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="section-title">NHS Advice 🏥</div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.85rem;color:#666;margin-bottom:1rem">Evidence-based guidance from the NHS for early pregnancy.</p>', unsafe_allow_html=True)

    for info in NHS_INFO:
        with st.expander(f"{info['icon']} {info['title']}"):
            # Render markdown inside expander
            st.markdown(info["body"])

    st.markdown("---")
    st.markdown("""
    <div class="card" style="border-left-color:#42a5f5">
      <h3 style="color:#1565c0">🔗 Useful Links</h3>
      <p><a href="https://www.nhs.uk/pregnancy/" target="_blank">NHS Pregnancy Guide</a></p>
      <p><a href="https://www.nhs.uk/pregnancy/related-conditions/common-symptoms/vomiting-and-morning-sickness/" target="_blank">NHS Morning Sickness</a></p>
      <p><a href="https://www.tommys.org/" target="_blank">Tommy's — pregnancy charity</a></p>
      <p><a href="https://www.nct.org.uk/" target="_blank">NCT — antenatal classes & support</a></p>
      <p><a href="https://www.pregnancysicknesssupport.org.uk/" target="_blank">Pregnancy Sickness Support</a></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card" style="border-left-color:#ef5350;margin-top:0.5rem">
      <h3 style="color:#c62828">🆘 Emergency contacts</h3>
      <p><b>GP / Midwife:</b> Your first port of call for any concerns.</p>
      <p><b>NHS 111:</b> For urgent non-emergency advice (call or online).</p>
      <p><b>A&E / 999:</b> Heavy bleeding, severe pain, loss of consciousness.</p>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:2rem;font-size:0.75rem;color:#ad1457;opacity:0.7">
  Made with love 🌸 · Always consult your midwife or GP with medical concerns
</div>
""", unsafe_allow_html=True)
