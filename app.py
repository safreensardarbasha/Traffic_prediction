import streamlit as st
import pandas as pd
import joblib
import folium
from streamlit_folium import st_folium

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="TrafficAI - Smart City",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# LOAD DATA + MODEL - CACHED
# =========================================================
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")


@st.cache_resource
def load_model():
    return joblib.load("traffic_model.pkl")


data = load_data()
model = load_model()


# =========================================================
# SALEM + SURROUNDING AREAS + COLLEGES
# =========================================================
raw_profiles = {
    "Salem Junction": (1100,30,1900,8.0,11.6640,78.1460),
    "Five Roads": (350,50,1800,6.0,11.6710,78.1390),
    "Cherry Road": (500,45,1700,6.5,11.6780,78.1510),
    "Fairlands": (650,40,1700,7.0,11.6810,78.1310),
    "Alagapuram": (580,43,1750,6.8,11.6750,78.1280),
    "Alagapuram Pudur": (500,45,1700,7.0,11.6820,78.1240),
    "Jagir Ammapalayam": (620,42,1700,7.5,11.6960,78.1160),
    "Suramangalam": (700,41,1700,8.0,11.6530,78.1200),
    "Meyyanur": (850,36,1700,7.2,11.6550,78.1350),
    "Hasthampatti": (450,47,1800,7.2,11.6740,78.1580),
    "Kannankurichi": (520,44,1650,8.0,11.6860,78.1730),
    "Gorimedu": (480,46,1700,7.5,11.6800,78.1650),
    "Chinnakollapatti": (420,48,1650,7.0,11.6900,78.1750),
    "Periyakollapatti": (390,49,1650,7.2,11.6950,78.1800),
    "Reddiyur": (560,43,1700,6.8,11.6690,78.1240),
    "Narasothipatti": (600,42,1700,7.0,11.6630,78.1190),
    "Ammapet": (900,34,1750,7.5,11.6610,78.1700),
    "Ponnammapet": (780,37,1700,7.8,11.6540,78.1770),
    "Gugai": (920,33,1800,8.0,11.6480,78.1570),
    "Dadagapatti": (760,38,1700,7.4,11.6560,78.1500),
    "Annathanapatti": (700,40,1700,7.5,11.6500,78.1450),
    "Shevapet": (880,35,1800,7.0,11.6700,78.1450),
    "Kitchipalayam": (820,36,1750,7.2,11.6580,78.1530),
    "Fort": (900,34,1800,6.8,11.6645,78.1500),
    "Kottai": (920,33,1800,6.8,11.6630,78.1510),
    "Kumarasampatti": (520,45,1700,6.7,11.6750,78.1530),
    "Kondalampatti": (1050,29,1900,8.5,11.6420,78.1670),
    "Seelanaickenpatti": (950,32,1800,8.0,11.6380,78.1580),
    "Erumapalayam": (730,39,1700,7.8,11.6400,78.1450),
    "Karungalpatti": (780,37,1700,7.5,11.6500,78.1600),
    "Thiruvagoundanur": (650,41,1700,8.2,11.6820,78.1080),
    "Ayyamperumampatti": (500,44,1650,8.0,11.7000,78.1300),
    "Chettichavadi": (420,47,1650,8.5,11.7100,78.1150),
    "Dasanaickenpatti": (550,44,1700,8.0,11.7050,78.1450),
    "Omalur": (800,37,1800,8.2,11.6900,78.1100),
    "Karuppur": (620,42,1700,8.5,11.6500,78.0950),
    "Ayothiyapattinam": (700,40,1750,9.0,11.5870,78.1380),
    "Attayampatti": (560,43,1650,10.0,11.5830,78.0400),
    "Elampillai": (500,45,1650,10.5,11.6070,77.9940),
    "Edanganasalai": (480,46,1650,11.0,11.6500,77.9900),
    "Mallur": (600,42,1700,9.5,11.5480,78.1400),
    "Panamarathupatty": (450,46,1650,10.0,11.5650,78.1300),
    "Rasipuram": (650,41,1750,22.0,11.4600,78.1800),
    "Namakkal": (750,39,1800,35.0,11.2190,78.1670),
    "Attur": (700,40,1750,30.0,11.5950,78.6010),
    "Valapadi": (550,44,1650,25.0,11.6500,78.0250),
    "Belur": (420,46,1650,28.0,11.5500,78.9000),
    "Gangavalli": (450,45,1650,38.0,11.4800,78.6500),
    "Thammampatti": (430,46,1650,42.0,11.4300,78.4800),
    "Yethapur": (400,47,1600,45.0,11.5700,78.3300),
    "Kadayampatti": (460,45,1650,30.0,11.8600,78.1000),
    "Tharamangalam": (520,44,1650,20.0,11.6970,77.9600),
    "Poolampatti": (380,48,1600,35.0,11.5700,77.8300),
    "Vanavasi": (400,47,1600,32.0,11.5200,77.8700),
    "Nangavalli": (420,46,1650,40.0,11.7600,77.8900),
    "Arasiramani": (390,47,1600,38.0,11.5900,77.8700),
    "Veeraganur": (420,46,1650,38.0,11.4700,78.5300),
    "Mettur": (700,40,1700,35.0,11.7860,77.8000),
    "Mecheri": (500,45,1650,32.0,11.7920,77.6500),
    "Jalakandapuram": (480,46,1650,32.0,11.6970,77.8700),
    "Sankari": (700,40,1750,30.0,11.4800,77.8750),

    "Yercaud Road": (450,46,1650,7.0,11.6750,78.1650),
    "Mettur Road": (700,40,1700,7.8,11.6500,78.1750),
    "Trichy Main Road": (1000,30,1900,9.5,11.6300,78.1550),
    "Omalur Main Road": (800,37,1800,8.2,11.6900,78.1100),

    "Shri Sakthikailassh Women's College": (600,42,1700,7.8,11.6555,78.1780),
    "Sri Sarada College for Women": (580,43,1700,7.0,11.6750,78.1500),
    "Government Arts College Salem": (650,40,1750,7.2,11.6700,78.1550),
    "Sona College of Technology": (720,39,1750,8.0,11.6460,78.1180),
    "Government College of Engineering Salem": (680,41,1800,8.5,11.6900,78.1200),
    "Knowledge Institute of Technology": (550,44,1700,10.0,11.5750,78.0000),
    "Dhirajlal Gandhi College of Technology": (500,45,1700,10.5,11.6100,78.0000),
    "AVS College of Arts and Science": (480,46,1650,9.0,11.6250,78.1000),
    "AVS Engineering College": (520,44,1700,10.0,11.6200,78.0600),
    "Annapoorana Engineering College": (450,46,1650,11.0,11.6000,77.9900),
    "Mahendra Engineering College": (520,44,1700,12.0,11.5600,77.9700),
    "Mahendra Arts and Science College": (450,46,1650,12.0,11.5550,77.9600),
    "Bharathiyar Institute of Engineering for Women": (420,47,1650,11.0,11.5900,78.0200),
    "Ganesh College of Engineering": (430,46,1650,11.0,11.6100,78.0200),
    "Sri Shanmugha College of Engineering and Technology": (470,45,1700,12.0,11.5200,77.9700),
    "Tagore Institute of Engineering and Technology": (440,46,1650,11.5,11.5800,78.0000),
    "The Kavery Engineering College": (420,47,1650,12.0,11.4900,77.8500),
    "VSA Group of Institutions": (500,44,1700,10.0,11.6200,78.1100),
    "Sona College of Arts and Science": (520,44,1700,8.0,11.6450,78.1200),
    "Jairam Arts and Science College": (450,46,1650,9.0,11.6100,78.1000),
    "Padmavani Arts and Science College for Women": (430,46,1650,9.5,11.6500,78.0900)
}


# =========================================================
# ROUTE PROFILES
# =========================================================
route_profiles = {
    name: {
        "vehicles": v,
        "speed": s,
        "capacity": c,
        "distance": d,
        "lat": lat,
        "lon": lon
    }
    for name, (v, s, c, d, lat, lon) in raw_profiles.items()
}


# =========================================================
# SESSION STATE
# =========================================================
defaults = {
    "page": "🏠 Dashboard",
    "from_location": None,
    "to_location": None,
    "travel_time": None,
    "prediction": None,
    "confidence": None,
    "trip_active": False,
    "trip_alert": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# NAVIGATION
# =========================================================
def go_dashboard():
    st.session_state.page = "🏠 Dashboard"


def go_prediction():
    st.session_state.page = "🚦 Traffic Prediction"


def go_routes():
    st.session_state.page = "🛣️ Route Optimization"


def go_comparison():
    st.session_state.page = "🧭 Route Comparison"


def go_travel():
    st.session_state.page = "🚗 Travel Mode"


def go_map():
    st.session_state.page = "🗺️ Salem Traffic Map"


def go_about():
    st.session_state.page = "ℹ️ About System"


# =========================================================
# HELPER FUNCTIONS - CACHED
# =========================================================
@st.cache_data(show_spinner=False)
def predict_route(route_name, hour):

    route = route_profiles[route_name]

    input_data = pd.DataFrame({
        "vehicle_count": [route["vehicles"]],
        "average_speed": [route["speed"]],
        "road_capacity": [route["capacity"]],
        "hour": [hour]
    })

    prediction = model.predict(input_data)[0]

    probabilities = model.predict_proba(input_data)[0]

    confidence = max(probabilities) * 100

    return prediction, confidence


def traffic_score(prediction):

    return {
        "Low": 1,
        "Medium": 2,
        "High": 3
    }.get(prediction, 3)


@st.cache_data(show_spinner=False)
def build_alternatives(from_location, to_location, hour):

    rows = []

    for route_name, route in route_profiles.items():

        if route_name in [from_location, to_location]:
            continue

        prediction, confidence = predict_route(
            route_name,
            hour
        )

        estimated_time = (
            route["distance"] / route["speed"]
        ) * 60

        congestion_score = traffic_score(
            prediction
        )

        time_score = estimated_time / 10

        ai_score = (
            congestion_score * 10
            + time_score
        )

        rows.append({
            "Route": route_name,
            "Vehicles": route["vehicles"],
            "Speed": route["speed"],
            "Congestion": prediction,
            "Confidence": confidence,
            "Distance": route["distance"],
            "Travel Time": estimated_time,
            "AI Score": ai_score,
            "Latitude": route["lat"],
            "Longitude": route["lon"]
        })

    df = pd.DataFrame(rows)

    return (
        df.sort_values(
            ["AI Score", "Travel Time"]
        )
        .reset_index(drop=True)
    )


def traffic_box(prediction, confidence=None):

    if prediction == "High":

        st.error(
            f"🔴 HIGH TRAFFIC\n\n"
            f"Heavy congestion detected"
            + (
                f"\n\nAI Confidence: {confidence:.1f}%"
                if confidence is not None
                else ""
            )
        )

    elif prediction == "Medium":

        st.warning(
            f"🟡 MEDIUM TRAFFIC\n\n"
            f"Moderate congestion detected"
            + (
                f"\n\nAI Confidence: {confidence:.1f}%"
                if confidence is not None
                else ""
            )
        )

    else:

        st.success(
            f"🟢 LOW TRAFFIC\n\n"
            f"Traffic flow is relatively smooth"
            + (
                f"\n\nAI Confidence: {confidence:.1f}%"
                if confidence is not None
                else ""
            )
        )


def traffic_color(prediction):

    if prediction == "Low":
        return "green"

    elif prediction == "Medium":
        return "orange"

    return "red"


# =========================================================
# CACHED MAP SUMMARY
# =========================================================
@st.cache_data(show_spinner=False)
def get_map_summary(hour):

    low_count = 0
    medium_count = 0
    high_count = 0

    for name in route_profiles:

        prediction, _ = predict_route(
            name,
            hour
        )

        if prediction == "Low":
            low_count += 1

        elif prediction == "Medium":
            medium_count += 1

        else:
            high_count += 1

    return low_count, medium_count, high_count


# =========================================================
# CSS
# =========================================================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #f4f9ff 0%,
        #eef6ff 50%,
        #f8fbff 100%
    );
    color:#102a43;
}

.main .block-container {
    max-width:1450px;
    padding-top:2rem;
    padding-bottom:3rem;
}

h1 {
    color:#123d6b !important;
    font-weight:800 !important;
}

h2 {
    color:#174a7e !important;
    font-weight:750 !important;
}

h3 {
    color:#174a7e !important;
    font-weight:700 !important;
}

p {
    color:#243b53 !important;
}

[data-testid="stSidebar"] {
    background:linear-gradient(
        180deg,
        #123f6b 0%,
        #18598d 50%,
        #0f4775 100%
    ) !important;

    border-right:3px solid #0b3157;
}

[data-testid="stSidebar"] * {
    color:#ffffff !important;
}

[data-testid="stSidebar"] h1 {
    color:#ffffff !important;
    font-size:28px !important;
    font-weight:800 !important;
}

[data-testid="stSidebar"] .stButton {
    margin-bottom:9px;
}

[data-testid="stSidebar"] .stButton > button {

    width:100% !important;
    min-height:48px !important;

    background:rgba(255,255,255,.10) !important;

    color:#ffffff !important;

    border:1px solid rgba(255,255,255,.25) !important;

    border-radius:12px !important;

    font-size:14px !important;

    font-weight:700 !important;

    text-align:left !important;
}

[data-testid="stSidebar"] .stButton > button p {
    color:#ffffff !important;
    font-weight:700 !important;
}

[data-testid="stSidebar"] .stButton > button:hover {

    background:rgba(255,255,255,.22) !important;

    border-color:#ffffff !important;

    transform:translateX(4px);

    box-shadow:0 5px 15px rgba(0,0,0,.18);
}

hr {
    border-color:#c9d9ea !important;
}

.stApp .stButton > button {

    background:linear-gradient(
        90deg,
        #1976d2,
        #2f8bd8
    ) !important;

    color:#ffffff !important;

    border:1px solid #1976d2 !important;

    border-radius:12px !important;

    min-height:44px !important;

    font-size:15px !important;

    font-weight:700 !important;
}

.stApp .stButton > button p {
    color:#ffffff !important;
    font-weight:700 !important;
}

.stApp .stButton > button:hover {

    background:linear-gradient(
        90deg,
        #125ca8,
        #1976d2
    ) !important;

    transform:translateY(-2px);

    box-shadow:0 7px 18px rgba(25,118,210,.30);
}

[data-testid="stSelectbox"] label,
[data-testid="stTimeInput"] label {

    color:#173f68 !important;
    font-weight:700 !important;
}

[data-baseweb="select"] > div {

    background:#ffffff !important;

    border:1px solid #8da9c4 !important;

    border-radius:10px !important;

    color:#102a43 !important;
}

[data-baseweb="select"] span {

    color:#102a43 !important;

    font-weight:600 !important;
}

div[role="listbox"] {

    background:#ffffff !important;

    border:1px solid #7d9bb8 !important;

    box-shadow:0 10px 30px rgba(0,0,0,.20) !important;
}

div[role="option"] {

    background:#ffffff !important;

    color:#102a43 !important;

    font-weight:600 !important;
}

div[role="option"] * {
    color:#102a43 !important;
}

div[role="option"]:hover {
    background:#e4f0ff !important;
}

[data-testid="stTimeInput"] input {

    background:#ffffff !important;

    color:#102a43 !important;

    border:1px solid #8da9c4 !important;

    border-radius:10px !important;

    font-weight:600 !important;
}

input {
    color:#102a43 !important;
    background:#ffffff !important;
}

[data-testid="stMetric"] {

    background:#ffffff !important;

    border:1px solid #c6d7e8 !important;

    border-radius:16px !important;

    padding:18px !important;

    box-shadow:0 5px 18px rgba(31,78,121,.08);
}

[data-testid="stMetricLabel"] {
    color:#486581 !important;
}

[data-testid="stMetricValue"] {

    color:#123d6b !important;

    font-weight:800 !important;
}

.system-online {

    background:rgba(255,255,255,.12);

    border:1px solid rgba(255,255,255,.25);

    border-radius:10px;

    padding:11px;

    text-align:center;

    color:#b9ffd9 !important;

    font-weight:800;
}

.route-card {

    padding:18px;

    border-radius:16px;

    margin:10px 0;

    border:1px solid #d5e2ef;

    background:#ffffff;

    box-shadow:0 5px 18px rgba(31,78,121,.08);
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:

    st.title("🚦 TrafficAI")

    st.caption("Smart City Traffic Intelligence")

    st.divider()

    st.markdown("### 🧭 Navigation")

    st.button(
        "🏠   Dashboard",
        use_container_width=True,
        on_click=go_dashboard
    )

    st.button(
        "🚦   Traffic Prediction",
        use_container_width=True,
        on_click=go_prediction
    )

    st.button(
        "🛣️   Route Optimization",
        use_container_width=True,
        on_click=go_routes
    )

    st.button(
        "🧭   Route Comparison",
        use_container_width=True,
        on_click=go_comparison
    )

    st.button(
        "🚗   Travel Mode",
        use_container_width=True,
        on_click=go_travel
    )

    st.button(
        "🗺️   Salem Traffic Map",
        use_container_width=True,
        on_click=go_map
    )

    st.button(
        "ℹ️   About System",
        use_container_width=True,
        on_click=go_about
    )

    st.divider()

    st.markdown(
        '<div class="system-online">● SYSTEM ONLINE</div>',
        unsafe_allow_html=True
    )

    st.caption("Random Forest AI Model Ready")


page = st.session_state.page


# =========================================================
# DASHBOARD
# =========================================================
if page == "🏠 Dashboard":

    st.title("🚦 AI-BASED URBAN TRAFFIC INTELLIGENCE")

    st.subheader(
        "Smarter Routes  |  Less Traffic  |  A Better Tomorrow"
    )

    st.divider()

    st.header("📊 Smart City Traffic Overview")

    total_vehicles = int(
        data["vehicle_count"].sum()
    )

    avg_speed = round(
        data["average_speed"].mean(),
        1
    )

    high_count = int(
        (data["congestion"] == "High").sum()
    )

    records = len(data)

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.metric(
            "🚗 VEHICLES",
            f"{total_vehicles:,}"
        )

    with c2:
        st.metric(
            "⚡ AVG SPEED",
            f"{avg_speed} km/h"
        )

    with c3:
        st.metric(
            "🔴 HIGH TRAFFIC",
            high_count
        )

    with c4:
        st.metric(
            "📁 DATA RECORDS",
            records
        )

    st.divider()

    st.header("🧠 How TrafficAI Works")

    st.info(
        "1️⃣ User selects starting location, destination and travel time.\n\n"
        "2️⃣ Random Forest AI analyses traffic features.\n\n"
        "3️⃣ System predicts Low, Medium or High congestion.\n\n"
        "4️⃣ Medium or High traffic triggers route optimization.\n\n"
        "5️⃣ AI compares alternative routes using congestion and travel time.\n\n"
        "6️⃣ Travel Mode monitors the selected project route."
    )

    st.divider()

    st.header("📈 Traffic Level Distribution")

    traffic_counts = (
        data["congestion"]
        .value_counts()
        .reindex(
            ["Low","Medium","High"],
            fill_value=0
        )
    )

    st.bar_chart(
        traffic_counts,
        height=350
    )

    st.divider()

    st.header("🚦 Traffic Classification")

    a,b,c = st.columns(3)

    with a:
        st.success(
            "🟢 LOW\n\nSmooth traffic flow"
        )

    with b:
        st.warning(
            "🟡 MEDIUM\n\nModerate traffic"
        )

    with c:
        st.error(
            "🔴 HIGH\n\nHeavy congestion"
        )


# =========================================================
# TRAFFIC PREDICTION
# =========================================================
elif page == "🚦 Traffic Prediction":

    st.title("🚦 AI TRAFFIC PREDICTION")

    st.subheader(
        "Check the traffic condition before your journey"
    )

    st.divider()

    st.header("📍 Enter Journey Details")

    route_names = list(route_profiles.keys())

    col1,col2 = st.columns(2)

    with col1:

        from_location = st.selectbox(
            "📍 From",
            route_names,
            index=0,
            key="prediction_from"
        )

    with col2:

        to_location = st.selectbox(
            "📍 To",
            route_names,
            index=1,
            key="prediction_to"
        )

    selected_time = st.time_input(
        "🕐 Travel Time",
        value=pd.Timestamp("18:00").time(),
        key="prediction_time"
    )

    hour = selected_time.hour

    st.caption(
        f"Journey: {from_location} → {to_location} | "
        f"Time: {selected_time.strftime('%I:%M %p')}"
    )

    st.write("")

    if from_location == to_location:

        st.warning(
            "⚠️ From and To locations should be different."
        )

    if st.button(
        "🧠 PREDICT TRAFFIC",
        use_container_width=True,
        key="run_prediction"
    ):

        if from_location == to_location:

            st.warning(
                "Please select different From and To locations."
            )

        else:

            route = route_profiles[from_location]

            prediction, confidence = predict_route(
                from_location,
                hour
            )

            st.session_state.from_location = from_location
            st.session_state.to_location = to_location
            st.session_state.travel_time = selected_time
            st.session_state.prediction = prediction
            st.session_state.confidence = confidence

            st.divider()

            st.header(
                "🤖 Predicted Congestion Level"
            )

            traffic_box(
                prediction,
                confidence
            )

            st.divider()

            st.header(
                "📋 Prediction Summary"
            )

            r1,r2,r3,r4 = st.columns(4)

            with r1:
                st.metric(
                    "📍 From",
                    from_location
                )

            with r2:
                st.metric(
                    "📍 To",
                    to_location
                )

            with r3:
                st.metric(
                    "🚗 Vehicles",
                    route["vehicles"]
                )

            with r4:
                st.metric(
                    "⚡ Speed",
                    f"{route['speed']} km/h"
                )

            st.metric(
                "🕐 Travel Time",
                selected_time.strftime("%I:%M %p")
            )

            st.divider()

            if prediction in ["High","Medium"]:

                st.error(
                    f"🚨 TRAFFIC ALERT — "
                    f"{prediction.upper()} TRAFFIC\n\n"
                    f"Congestion detected on "
                    f"{from_location}.\n\n"
                    f"TrafficAI recommends checking "
                    f"alternative routes."
                )

                x,y = st.columns(2)

                with x:

                    st.button(
                        "🛣️ CHECK ALTERNATIVE ROUTES",
                        use_container_width=True,
                        key="check_alternative",
                        on_click=go_routes
                    )

                with y:

                    st.button(
                        "🚗 START TRAVEL MODE",
                        use_container_width=True,
                        key="start_from_prediction",
                        on_click=go_travel
                    )

            else:

                st.success(
                    "✅ Low traffic detected. "
                    "The current route is suitable for travel."
                )

                st.button(
                    "🚗 START TRAVEL MODE",
                    use_container_width=True,
                    key="start_low_trip",
                    on_click=go_travel
                )


# =========================================================
# ROUTE OPTIMIZATION
# =========================================================
elif page == "🛣️ Route Optimization":

    st.title("🛣️ AI ROUTE OPTIMIZATION")

    st.subheader(
        "Compare alternative Salem routes using AI traffic prediction"
    )

    st.divider()

    if any(
        st.session_state[k] is None
        for k in [
            "from_location",
            "to_location",
            "travel_time"
        ]
    ):

        st.info(
            "📍 Please run Traffic Prediction first."
        )

        st.button(
            "🚦 GO TO TRAFFIC PREDICTION",
            use_container_width=True,
            on_click=go_prediction
        )

    else:

        from_location = st.session_state.from_location
        to_location = st.session_state.to_location
        selected_time = st.session_state.travel_time

        hour = selected_time.hour

        st.header("🧭 Journey Summary")

        j1,j2,j3 = st.columns(3)

        with j1:
            st.metric(
                "📍 FROM",
                from_location
            )

        with j2:
            st.metric(
                "📍 TO",
                to_location
            )

        with j3:
            st.metric(
                "🕐 TIME",
                selected_time.strftime("%I:%M %p")
            )

        st.divider()

        current_route = route_profiles[from_location]

        current_prediction,current_confidence = predict_route(
            from_location,
            hour
        )

        st.header("🚦 Current Route Condition")

        c1,c2,c3,c4 = st.columns(4)

        with c1:
            st.metric(
                "📍 Current Route",
                from_location
            )

        with c2:
            st.metric(
                "🚗 Vehicles",
                current_route["vehicles"]
            )

        with c3:
            st.metric(
                "⚡ Speed",
                f"{current_route['speed']} km/h"
            )

        with c4:

            if current_prediction == "High":
                st.error("🔴 HIGH TRAFFIC")

            elif current_prediction == "Medium":
                st.warning("🟡 MEDIUM TRAFFIC")

            else:
                st.success("🟢 LOW TRAFFIC")

        st.caption(
            f"AI Confidence: {current_confidence:.1f}%"
        )

        alternatives = build_alternatives(
            from_location,
            to_location,
            hour
        ).head(5)

        if len(alternatives) > 0:

            st.divider()

            st.header(
                "🤖 AI Route Recommendation"
            )

            best_route = alternatives.iloc[0]

            if current_prediction in [
                "High",
                "Medium"
            ]:

                st.error(
                    f"⚠️ {current_prediction} traffic "
                    f"detected on {from_location}."
                )

                st.success(
                    f"🧠 AI Recommended Alternative\n\n"
                    f"📍 {from_location} → "
                    f"{best_route['Route']} → "
                    f"{to_location}"
                )

                r1,r2,r3,r4 = st.columns(4)

                with r1:

                    if best_route["Congestion"] == "Low":
                        st.success("🟢 LOW TRAFFIC")

                    elif best_route["Congestion"] == "Medium":
                        st.warning("🟡 MEDIUM TRAFFIC")

                    else:
                        st.error("🔴 HIGH TRAFFIC")

                with r2:

                    st.metric(
                        "📏 Distance",
                        f"{best_route['Distance']:.1f} km"
                    )

                with r3:

                    st.metric(
                        "⚡ Speed",
                        f"{int(best_route['Speed'])} km/h"
                    )

                with r4:

                    st.metric(
                        "⏱️ Travel Time",
                        f"{best_route['Travel Time']:.1f} min"
                    )

            else:

                st.success(
                    "🟢 Current route has Low Traffic."
                )

                st.info(
                    "AI found alternative profiles, "
                    "but changing route is not necessary "
                    "for the current Low Traffic condition."
                )

            st.divider()

            st.header(
                "🛣️ 5 Alternative Route Options"
            )

            for index, route in alternatives.iterrows():

                route_number = index + 1

                if route["Congestion"] == "Low":
                    icon = "🟢"
                    status_text = "LOW TRAFFIC"

                elif route["Congestion"] == "Medium":
                    icon = "🟡"
                    status_text = "MEDIUM TRAFFIC"

                else:
                    icon = "🔴"
                    status_text = "HIGH TRAFFIC"

                if route_number == 1:
                    st.success(
                        f"⭐ ROUTE {route_number} — "
                        f"AI RECOMMENDED"
                    )

                else:
                    st.markdown(
                        f"### 🛣️ ROUTE {route_number}"
                    )

                a,b,c,d,e = st.columns(5)

                with a:
                    st.write(
                        f"**📍 {route['Route']}**"
                    )

                with b:
                    st.write(
                        f"**{icon} {status_text}**"
                    )

                with c:
                    st.write(
                        f"🚗 **{int(route['Vehicles'])} vehicles**"
                    )

                with d:
                    st.write(
                        f"⚡ **{int(route['Speed'])} km/h**"
                    )

                with e:
                    st.write(
                        f"⏱️ **{route['Travel Time']:.1f} min**"
                    )

                st.caption(
                    f"Distance: {route['Distance']:.1f} km | "
                    f"AI Score: {route['AI Score']:.2f} | "
                    f"Confidence: {route['Confidence']:.1f}%"
                )

                st.divider()

        st.button(
            "🧭 VIEW ROUTE COMPARISON",
            use_container_width=True,
            on_click=go_comparison
        )


# =========================================================
# ROUTE COMPARISON
# =========================================================
elif page == "🧭 Route Comparison":

    st.title("🧭 ROUTE COMPARISON")

    st.subheader(
        "Compare 5 alternative routes using AI traffic predictions"
    )

    st.divider()

    if any(
        st.session_state[k] is None
        for k in [
            "from_location",
            "to_location",
            "travel_time"
        ]
    ):

        st.info(
            "📍 Please run Traffic Prediction first."
        )

        st.button(
            "🚦 GO TO TRAFFIC PREDICTION",
            use_container_width=True,
            on_click=go_prediction
        )

    else:

        from_location = st.session_state.from_location
        to_location = st.session_state.to_location
        selected_time = st.session_state.travel_time

        hour = selected_time.hour

        st.header("📋 Current Journey")

        a,b,c = st.columns(3)

        with a:
            st.metric(
                "📍 From",
                from_location
            )

        with b:
            st.metric(
                "📍 To",
                to_location
            )

        with c:
            st.metric(
                "🕐 Time",
                selected_time.strftime("%I:%M %p")
            )

        alternatives = build_alternatives(
            from_location,
            to_location,
            hour
        ).head(5)

        if len(alternatives):

            display = alternatives.copy()

            display["Vehicles"] = (
                display["Vehicles"]
                .astype(int)
            )

            display["Speed"] = (
                display["Speed"]
                .astype(int)
                .astype(str)
                + " km/h"
            )

            display["Distance"] = (
                display["Distance"]
                .round(1)
                .astype(str)
                + " km"
            )

            display["Travel Time"] = (
                display["Travel Time"]
                .round(1)
                .astype(str)
                + " min"
            )

            display["Confidence"] = (
                display["Confidence"]
                .round(1)
                .astype(str)
                + "%"
            )

            display["AI Score"] = (
                display["AI Score"]
                .round(2)
            )

            display = display[
                [
                    "Route",
                    "Congestion",
                    "Vehicles",
                    "Speed",
                    "Distance",
                    "Travel Time",
                    "Confidence",
                    "AI Score"
                ]
            ]

            st.header(
                "🛣️ 5 Route Options"
            )

            st.dataframe(
                display,
                use_container_width=True,
                hide_index=True
            )

            best = alternatives.iloc[0]

            st.divider()

            st.header(
                "🤖 AI Comparison Result"
            )

            if st.session_state.prediction in [
                "High",
                "Medium"
            ]:

                st.success(
                    f"🧠 AI Recommended Route\n\n"
                    f"{from_location} → "
                    f"{best['Route']} → "
                    f"{to_location}\n\n"
                    f"Traffic: {best['Congestion']} | "
                    f"Distance: {best['Distance']:.1f} km | "
                    f"Estimated Time: "
                    f"{best['Travel Time']:.1f} min"
                )

            else:

                st.info(
                    "🟢 Current route is Low Traffic, "
                    "so an alternative is not required."
                )

        st.divider()

        st.button(
            "🚗 GO TO TRAVEL MODE",
            use_container_width=True,
            on_click=go_travel
        )


# =========================================================
# TRAVEL MODE
# =========================================================
elif page == "🚗 Travel Mode":

    st.title("🚗 TRAVEL MODE")

    st.subheader(
        "Monitor your selected project route "
        "and receive traffic alerts"
    )

    st.divider()

    if any(
        st.session_state[k] is None
        for k in [
            "from_location",
            "to_location",
            "travel_time"
        ]
    ):

        st.info(
            "📍 First select From, To and Time "
            "in Traffic Prediction."
        )

        st.button(
            "🚦 GO TO TRAFFIC PREDICTION",
            use_container_width=True,
            on_click=go_prediction
        )

    else:

        from_location = st.session_state.from_location
        to_location = st.session_state.to_location
        selected_time = st.session_state.travel_time

        hour = selected_time.hour

        st.header("🧭 Trip Details")

        a,b,c = st.columns(3)

        with a:
            st.metric(
                "📍 FROM",
                from_location
            )

        with b:
            st.metric(
                "📍 TO",
                to_location
            )

        with c:
            st.metric(
                "🕐 TIME",
                selected_time.strftime("%I:%M %p")
            )

        st.divider()

        if not st.session_state.trip_active:

            st.info(
                "🚗 Trip is ready. "
                "Press Start Trip to begin monitoring."
            )

            if st.button(
                "▶️ START TRIP MONITORING",
                use_container_width=True
            ):

                st.session_state.trip_active = True

                st.rerun()

        else:

            st.success(
                "🟢 TRIP MONITORING ACTIVE"
            )

            current_prediction,confidence = predict_route(
                from_location,
                hour
            )

            st.session_state.trip_alert = current_prediction

            st.header(
                "🚦 Current Traffic Status"
            )

            traffic_box(
                current_prediction,
                confidence
            )

            route = route_profiles[from_location]

            x,y,z = st.columns(3)

            with x:
                st.metric(
                    "🚗 Vehicles",
                    route["vehicles"]
                )

            with y:
                st.metric(
                    "⚡ Speed",
                    f"{route['speed']} km/h"
                )

            with z:
                st.metric(
                    "🕐 Selected Time",
                    selected_time.strftime("%I:%M %p")
                )

            st.divider()

            if current_prediction == "High":

                st.error(
                    "🚨 AUTOMATIC TRAFFIC ALERT\n\n"
                    f"High traffic detected on "
                    f"{from_location}.\n\n"
                    "An alternative route should be considered."
                )

                st.button(
                    "🧭 COMPARE ALTERNATIVE ROUTES",
                    use_container_width=True,
                    on_click=go_comparison
                )

            elif current_prediction == "Medium":

                st.warning(
                    "⚠️ TRAFFIC WARNING\n\n"
                    f"Moderate traffic detected on "
                    f"{from_location}.\n\n"
                    "Check the route comparison before continuing."
                )

                st.button(
                    "🧭 COMPARE ALTERNATIVE ROUTES",
                    use_container_width=True,
                    on_click=go_comparison
                )

            else:

                st.success(
                    "🟢 TRAFFIC NORMAL\n\n"
                    "No significant congestion is predicted "
                    "for the selected project route."
                )

            st.caption(
                "Demo note: Travel Mode uses project-defined "
                "traffic profiles. It is not connected to "
                "live GPS or live traffic services."
            )

            st.divider()

            if st.button(
                "🔄 REFRESH TRAFFIC STATUS",
                use_container_width=True
            ):

                st.rerun()

            if st.button(
                "🛑 END TRIP",
                use_container_width=True
            ):

                st.session_state.trip_active = False
                st.session_state.trip_alert = None

                st.rerun()


# =========================================================
# SALEM TRAFFIC MAP
# =========================================================
elif page == "🗺️ Salem Traffic Map":

    st.title("🗺️ SALEM SMART TRAFFIC MAP")

    st.subheader(
        "Traffic monitoring zones across Salem"
    )

    st.divider()

    st.info(
        "This prototype uses project-defined Salem "
        "traffic profiles. Marker colors represent "
        "AI-predicted congestion levels."
    )

    st.header("🎨 Traffic Color Legend")

    l1,l2,l3 = st.columns(3)

    with l1:
        st.success("🟢 LOW TRAFFIC")

    with l2:
        st.warning("🟡 MEDIUM TRAFFIC")

    with l3:
        st.error("🔴 HIGH TRAFFIC")

    st.divider()

    # -----------------------------------------------------
    # USE SELECTED TIME IF AVAILABLE
    # -----------------------------------------------------
    if st.session_state.travel_time is not None:
        map_hour = st.session_state.travel_time.hour
    else:
        map_hour = 18

    # -----------------------------------------------------
    # CREATE MAP
    # -----------------------------------------------------
    salem_map = folium.Map(
        location=[
            11.6640,
            78.1460
        ],
        zoom_start=11,
        control_scale=True
    )

    # -----------------------------------------------------
    # ADD TRAFFIC ZONES
    # -----------------------------------------------------
    for name, route in route_profiles.items():

        prediction, confidence = predict_route(
            name,
            map_hour
        )

        marker_color = traffic_color(
            prediction
        )

        if prediction == "Low":
            emoji = "🟢"

        elif prediction == "Medium":
            emoji = "🟡"

        else:
            emoji = "🔴"

        popup_html = f"""
        <div style="width:240px">

        <h4>{emoji} {name}</h4>

        <b>Traffic:</b> {prediction}<br>
        <b>AI Confidence:</b> {confidence:.1f}%<br>
        <b>Vehicles:</b> {route['vehicles']}<br>
        <b>Speed:</b> {route['speed']} km/h<br>
        <b>Distance:</b> {route['distance']:.1f} km

        </div>
        """

        folium.Marker(
            location=[
                route["lat"],
                route["lon"]
            ],

            tooltip=(
                f"{emoji} {name} - "
                f"{prediction}"
            ),

            popup=folium.Popup(
                popup_html,
                max_width=300
            ),

            icon=folium.Icon(
                color=marker_color,
                icon="car",
                prefix="fa"
            )
        ).add_to(salem_map)

    # -----------------------------------------------------
    # SELECTED JOURNEY + TOP 3 ALTERNATIVES
    # -----------------------------------------------------
    if (
        st.session_state.from_location is not None
        and
        st.session_state.to_location is not None
        and
        st.session_state.travel_time is not None
    ):

        from_location = st.session_state.from_location
        to_location = st.session_state.to_location
        hour = st.session_state.travel_time.hour

        alternatives = build_alternatives(
            from_location,
            to_location,
            hour
        ).head(3)

        current = route_profiles[from_location]

        folium.Marker(
            location=[
                current["lat"],
                current["lon"]
            ],

            tooltip=(
                f"📍 CURRENT ROUTE: "
                f"{from_location}"
            ),

            popup=(
                f"Current Route<br>"
                f"{from_location}"
            ),

            icon=folium.Icon(
                color="blue",
                icon="location-arrow",
                prefix="fa"
            )
        ).add_to(salem_map)

        for number, (_, alt) in enumerate(
            alternatives.iterrows(),
            start=1
        ):

            prediction = alt["Congestion"]

            color = traffic_color(
                prediction
            )

            if number == 1:
                route_label = "⭐ AI RECOMMENDED"
            else:
                route_label = f"ALTERNATIVE {number}"

            folium.CircleMarker(

                location=[
                    alt["Latitude"],
                    alt["Longitude"]
                ],

                radius=11,

                color=color,

                fill=True,

                fill_color=color,

                fill_opacity=0.85,

                popup=folium.Popup(
                    f"""
                    <b>{route_label}</b><br><br>

                    <b>Route:</b> {alt['Route']}<br>
                    <b>Traffic:</b> {prediction}<br>
                    <b>Vehicles:</b> {int(alt['Vehicles'])}<br>
                    <b>Speed:</b> {int(alt['Speed'])} km/h<br>
                    <b>Distance:</b> {alt['Distance']:.1f} km<br>
                    <b>Estimated Time:</b> {alt['Travel Time']:.1f} min<br>
                    <b>AI Score:</b> {alt['AI Score']:.2f}
                    """,
                    max_width=300
                ),

                tooltip=(
                    f"{route_label} | "
                    f"{alt['Route']} | "
                    f"{prediction}"
                )

            ).add_to(salem_map)

    # -----------------------------------------------------
    # DISPLAY MAP
    # -----------------------------------------------------
    st.header("📍 Salem Traffic Zones")

    st_folium(
        salem_map,
        width=1400,
        height=650
    )

    st.divider()

    # -----------------------------------------------------
    # MAP SUMMARY - CACHED
    # -----------------------------------------------------
    st.header("🚦 Traffic Zone Summary")

    low_count, medium_count, high_count = get_map_summary(
        map_hour
    )

    s1,s2,s3 = st.columns(3)

    with s1:
        st.success(
            f"🟢 LOW ZONES\n\n{low_count}"
        )

    with s2:
        st.warning(
            f"🟡 MEDIUM ZONES\n\n{medium_count}"
        )

    with s3:
        st.error(
            f"🔴 HIGH ZONES\n\n{high_count}"
        )

    # -----------------------------------------------------
    # TOP 3 ALTERNATIVES
    # -----------------------------------------------------
    if (
        st.session_state.from_location is not None
        and
        st.session_state.to_location is not None
        and
        st.session_state.travel_time is not None
    ):

        st.divider()

        st.header(
            "🧭 Top 3 Alternative Routes on Map"
        )

        alternatives = build_alternatives(
            st.session_state.from_location,
            st.session_state.to_location,
            st.session_state.travel_time.hour
        ).head(3)

        for number, (_, route) in enumerate(
            alternatives.iterrows(),
            start=1
        ):

            if route["Congestion"] == "Low":

                st.success(
                    f"🟢 Alternative {number}: "
                    f"{route['Route']} | "
                    f"Low Traffic | "
                    f"{route['Travel Time']:.1f} min"
                )

            elif route["Congestion"] == "Medium":

                st.warning(
                    f"🟡 Alternative {number}: "
                    f"{route['Route']} | "
                    f"Medium Traffic | "
                    f"{route['Travel Time']:.1f} min"
                )

            else:

                st.error(
                    f"🔴 Alternative {number}: "
                    f"{route['Route']} | "
                    f"High Traffic | "
                    f"{route['Travel Time']:.1f} min"
                )


# =========================================================
# ABOUT SYSTEM
# =========================================================
elif page == "ℹ️ About System":

    st.title("ℹ️ ABOUT TRAFFICAI")

    st.subheader(
        "AI-Based Urban Traffic Congestion "
        "Prediction and Route Optimization"
    )

    st.divider()

    st.header("🎯 Project Objective")

    st.write(
        "TrafficAI is an AI-based Smart City application "
        "designed to predict urban traffic congestion and "
        "assist users in finding an alternative route when "
        "the current route has Medium or High traffic."
    )

    st.header("🧠 Machine Learning Algorithm")

    st.info(
        "Random Forest Classification"
    )

    st.header("📥 Input Features")

    st.write("🚗 Vehicle Count")
    st.write("⚡ Average Speed")
    st.write("🛣️ Road Capacity")
    st.write("🕐 Time of Day")

    st.header("📤 Prediction Output")

    p1,p2,p3 = st.columns(3)

    with p1:
        st.success("🟢 LOW TRAFFIC")

    with p2:
        st.warning("🟡 MEDIUM TRAFFIC")

    with p3:
        st.error("🔴 HIGH TRAFFIC")

    st.header("🛣️ Route Optimization")

    st.write(
        "When Medium or High traffic is predicted on "
        "the selected route, TrafficAI checks alternative "
        "project-defined Salem and surrounding area "
        "profiles and compares predicted congestion, "
        "distance and estimated travel time."
    )

    st.header("🧭 Route Comparison")

    st.write(
        "Route Comparison presents five alternative "
        "project profiles so users can compare congestion, "
        "vehicle count, speed, distance, confidence and "
        "estimated travel time."
    )

    st.header("🤖 AI Recommendation")

    st.write(
        "The AI route score combines predicted congestion "
        "and estimated travel time to identify the first "
        "route in the comparison list as the recommended "
        "alternative."
    )

    st.header("🚗 Travel Mode")

    st.write(
        "Travel Mode provides a trip-monitoring demo. "
        "It checks the selected project route and displays "
        "Low, Medium or High traffic alerts."
    )

    st.header("🗺️ Smart City Map")

    st.write(
        "The Salem Traffic Map displays project-defined "
        "monitoring zones. Green, yellow and red markers "
        "represent Low, Medium and High AI-predicted "
        "traffic respectively."
    )

    st.header("📌 Project Scope")

    st.info(
        "This is a Machine Learning prototype using "
        "project traffic data. It is not connected to "
        "live GPS traffic services. Real-time GPS, live "
        "traffic data and mobile push notifications can "
        "be added as future enhancements."
    )

    st.divider()

    st.success(
        "🚦 TrafficAI — Smart Traffic Intelligence System"
    )