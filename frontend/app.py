import os

import plotly.graph_objects as go
import requests
import streamlit as st

# ----------------------------------------------------------------------------
# Config
# ----------------------------------------------------------------------------
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
SCORE_MIN, SCORE_MAX = 0.0, 10.0  # change if your model uses a different scale

INK = "#16303B"
MUTED = "#5B7380"
LINE = "#D5E0E6"
CORAL = "#D9644A"
AMBER = "#E3A33B"
TEAL = "#1E8C86"

# Bands: (upper bound, label, colour, tint, message)
BANDS = [
    (
        4.0,
        "Needs attention",
        CORAL,
        "#F6D9D1",
        "Your habits point to a lower score. Sleep, stress and screen time "
        "are usually the quickest things to adjust.",
    ),
    (
        7.0,
        "Moderate",
        AMBER,
        "#F7E6C4",
        "A middle-of-the-road result. Small changes to sleep or daily "
        "screen time could move this up.",
    ),
    (
        SCORE_MAX + 0.001,
        "Healthy",
        TEAL,
        "#CDE7E4",
        "Your habits point to a strong score. Keep your sleep and activity "
        "routines steady.",
    ),
]

COUNTRIES = [
    "India", "USA", "Canada", "Australia", "UK", "Germany", "Mexico", "Turkey",
    "France", "Spain", "Ireland", "Japan", "Denmark", "Switzerland", "Nepal",
    "Italy", "Russia", "Sri Lanka", "Maldives", "Other",
]
PLATFORMS = [
    "Facebook", "LinkedIn", "Instagram", "Snapchat", "Twitter", "YouTube",
    "TikTok", "LINE", "KakaoTalk", "VKontakte", "WhatsApp", "WeChat",
]

# ----------------------------------------------------------------------------
# Page + styling
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Mental Health Predictor",
    page_icon="🧠",
    layout="wide",
)

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Figtree:wght@400;500;600&display=swap');

    html, body, [class*="css"], .stApp {{
        font-family: 'Figtree', sans-serif;
        color: {INK};
    }}
    .stApp {{
        background: #EEF3F6;
    }}
    #MainMenu, footer {{ visibility: hidden; }}
    .block-container {{ padding-top: 2.5rem; max-width: 1180px; }}

    h1.title {{
        font-family: 'Fraunces', serif;
        font-weight: 700;
        font-size: 2.6rem;
        line-height: 1.1;
        letter-spacing: -0.01em;
        margin: 0 0 .5rem 0;
        color: {INK};
    }}
    p.lede {{
        color: {MUTED};
        font-size: 1.05rem;
        max-width: 56ch;
        margin: 0 0 1.8rem 0;
        line-height: 1.55;
    }}

    /* form panel */
    [data-testid="stForm"] {{
        background: #FFFFFF;
        border: 1px solid {LINE};
        border-radius: 18px;
        padding: 1.6rem 1.8rem 1.4rem;
    }}
    .group-title {{
        font-family: 'Fraunces', serif;
        font-weight: 600;
        font-size: 1.15rem;
        margin: .2rem 0 .6rem 0;
        padding-bottom: .4rem;
        border-bottom: 1px solid {LINE};
    }}
    .group-title.spaced {{ margin-top: 1.4rem; }}

    label, [data-testid="stWidgetLabel"] p {{
        font-weight: 500;
        color: {INK};
    }}

    /* primary button */
    [data-testid="stFormSubmitButton"] button {{
        width: 100%;
        background: {INK};
        color: #fff;
        border: none;
        border-radius: 12px;
        padding: .75rem 1rem;
        font-weight: 600;
        font-size: 1rem;
        margin-top: .8rem;
        transition: background .15s ease;
    }}
    [data-testid="stFormSubmitButton"] button:hover {{
        background: {TEAL};
        color: #fff;
    }}
    [data-testid="stFormSubmitButton"] button:focus-visible {{
        outline: 3px solid {AMBER};
        outline-offset: 2px;
    }}

    /* result panel */
    .result-card {{
        background: #FFFFFF;
        border: 1px solid {LINE};
        border-radius: 18px;
        padding: 1.4rem 1.6rem 1.6rem;
    }}
    .result-card h3 {{
        font-family: 'Fraunces', serif;
        font-size: 1.15rem;
        margin: 0 0 .2rem 0;
    }}
    .result-empty {{
        color: {MUTED};
        line-height: 1.55;
        margin: .4rem 0 0 0;
    }}
    .verdict {{
        display: inline-block;
        font-weight: 600;
        padding: .3rem .8rem;
        border-radius: 999px;
        margin: .2rem 0 .8rem 0;
    }}
    .verdict-text {{
        color: {INK};
        line-height: 1.55;
        margin: 0 0 1.2rem 0;
    }}
    .facts {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: .6rem;
    }}
    .fact {{
        background: #F4F8FA;
        border-radius: 12px;
        padding: .7rem .8rem;
    }}
    .fact b {{
        display: block;
        font-family: 'Fraunces', serif;
        font-size: 1.3rem;
    }}
    .fact span {{ color: {MUTED}; font-size: .85rem; }}
    .fine {{
        color: {MUTED};
        font-size: .82rem;
        line-height: 1.5;
        margin-top: 1.1rem;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def band_for(score: float):
    for upper, label, colour, tint, message in BANDS:
        if score < upper:
            return label, colour, tint, message
    return BANDS[-1][1:]


def make_gauge(score: float) -> go.Figure:
    label, colour, _, _ = band_for(score)
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"font": {"size": 54, "family": "Fraunces, serif", "color": INK}, "valueformat": ".1f"},
            gauge={
                "axis": {
                    "range": [SCORE_MIN, SCORE_MAX],
                    "tickwidth": 1,
                    "tickcolor": MUTED,
                    "tickfont": {"color": MUTED, "size": 12},
                },
                "bar": {"color": colour, "thickness": 0.28},
                "bgcolor": "white",
                "borderwidth": 0,
                "steps": [
                    {"range": [SCORE_MIN, BANDS[0][0]], "color": BANDS[0][3]},
                    {"range": [BANDS[0][0], BANDS[1][0]], "color": BANDS[1][3]},
                    {"range": [BANDS[1][0], SCORE_MAX], "color": BANDS[2][3]},
                ],
                "threshold": {
                    "line": {"color": INK, "width": 4},
                    "thickness": 0.8,
                    "value": score,
                },
            },
        )
    )
    fig.update_layout(
        height=290,
        margin=dict(l=24, r=24, t=30, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"family": "Figtree, sans-serif"},
    )
    return fig


def call_api(payload: dict) -> float:
    resp = requests.post(f"{API_URL}/predict", json=payload, timeout=15)
    resp.raise_for_status()
    body = resp.json()

    if "error" in body:
        raise RuntimeError(body["error"])

    value = body.get("response", body.get("Mental_Health_Score"))

    if isinstance(value, (list, tuple)):
        value = value[0]

    if isinstance(value, dict):
        # use the named key if present, otherwise the first value
        value = value.get("Mental_Health_Score", next(iter(value.values())))

    return float(value)

# ----------------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------------
st.markdown('<h1 class="title">How are your daily habits shaping your wellbeing?</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="lede">Tell us about your social media use, sleep and study routine. '
    "The model estimates a mental health score from those habits.</p>",
    unsafe_allow_html=True,
)

left, right = st.columns([1.35, 1], gap="large")

# ----------------------------------------------------------------------------
# Form
# ----------------------------------------------------------------------------
with left:
    with st.form("predict_form", border=False):
        st.markdown('<div class="group-title">About you</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        age = c1.number_input("Age", min_value=10, max_value=100, value=21, step=1)
        gender = c2.selectbox("Gender", ["Male", "Female"])
        c3, c4 = st.columns(2)
        country = c3.selectbox("Country", COUNTRIES)
        academic_level = c4.selectbox("Academic level", ["High School", "Undergraduate", "Graduate"], index=1)

        st.markdown('<div class="group-title spaced">Social media use</div>', unsafe_allow_html=True)
        c5, c6 = st.columns(2)
        platform = c5.selectbox("Most used platform", PLATFORMS, index=2)
        purpose = c6.selectbox("Main purpose", ["Entertainment", "Education", "Networking", "News"])
        usage_hours = st.slider("Average daily use (hours)", 0.0, 24.0, 4.5, 0.5)
        unlocks = st.number_input("Phone unlocks per day", min_value=0, max_value=1000, value=80, step=5)

        st.markdown('<div class="group-title spaced">Daily routine</div>', unsafe_allow_html=True)
        c7, c8 = st.columns(2)
        study_hours = c7.slider("Study hours per day", 0.0, 24.0, 4.0, 0.5)
        activity_hours = c8.slider("Physical activity (hours)", 0.0, 24.0, 1.0, 0.5)
        sleep_hours = c7.slider("Sleep per night (hours)", 0.0, 24.0, 7.0, 0.5)
        stress = c8.select_slider("Stress level", options=["Low", "Medium", "High", "Very High"], value="Medium")

        submitted = st.form_submit_button("Predict my score")

# ----------------------------------------------------------------------------
# Submit -> API
# ----------------------------------------------------------------------------
if submitted:
    payload = {
        "Age": int(age),
        "Gender": gender,
        "Country": country,
        "Academic_Level": academic_level,
        "Most_Used_Platform": platform,
        "Purpose_Of_Use": purpose,
        "Avg_Daily_Usage_Hours": float(usage_hours),
        "Daily_Unlocks": int(unlocks),
        "Study_Hours": float(study_hours),
        "Physical_Activity_Hours": float(activity_hours),
        "Sleep_Hours_Per_Night": float(sleep_hours),
        "Stress_Level": stress,
    }
    try:
        with st.spinner("Calculating…"):
            score = call_api(payload)
        st.session_state["result"] = {
            "score": max(SCORE_MIN, min(SCORE_MAX, score)),
            "usage": usage_hours,
            "sleep": sleep_hours,
            "activity": activity_hours,
        }
        st.session_state.pop("error", None)
    except requests.exceptions.ConnectionError:
        st.session_state["error"] = (
            f"Can’t reach the API at {API_URL}. Start it with "
            "`uvicorn backend.app:app --reload` and try again."
        )
    except requests.exceptions.HTTPError as e:
        st.session_state["error"] = f"The API rejected the input ({e.response.status_code}): {e.response.text}"
    except Exception as e:  # noqa: BLE001
        st.session_state["error"] = f"Something went wrong: {e}"

# ----------------------------------------------------------------------------
# Result panel
# ----------------------------------------------------------------------------
with right:
    if "error" in st.session_state:
        st.error(st.session_state["error"])

    result = st.session_state.get("result")

    if result is None:
        st.markdown(
            """
            <div class="result-card">
                <h3>Your score</h3>
                <p class="result-empty">Fill in the form and select <b>Predict my score</b>.
                Your result will appear here as a gauge.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        score = result["score"]
        label, colour, tint, message = band_for(score)

        st.markdown('<div class="result-card"><h3>Your score</h3>', unsafe_allow_html=True)
        st.plotly_chart(make_gauge(score), width='stretch', config={"displayModeBar": False})
        st.markdown(
            f"""
            <span class="verdict" style="background:{tint}; color:{INK};">
                <span style="color:{colour};">●</span>&nbsp; {label}
            </span>
            <p class="verdict-text">{message}</p>
            <div class="facts">
                <div class="fact"><b>{result["usage"]:g} h</b><span>Social media</span></div>
                <div class="fact"><b>{result["sleep"]:g} h</b><span>Sleep</span></div>
                <div class="fact"><b>{result["activity"]:g} h</b><span>Activity</span></div>
            </div>
            <p class="fine">This is a statistical estimate from a machine-learning model, not a medical
            assessment. If you’re struggling, please talk to a doctor or counsellor.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )