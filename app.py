import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
import hashlib
import pandas as pd

from main import run_drowsiness_detection
from SQL import DrowsinessDatabase
from utils import resource_path

userDB = resource_path("db/users.db")

#----------------------- DATABASE SETUP --------------------- 
conn = sqlite3.connect(userDB, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT,
    family1_name TEXT,
    family1_phone TEXT,
    family1_email TEXT,
    family2_name TEXT,
    family2_phone TEXT,
    family2_email TEXT
)
""")
conn.commit()

#------------------------Hashing functions------------------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored, provided):
    return stored == hash_password(provided)

def register_user(name, email, password, fam1, fam2):
    try:
        cursor.execute("""
        INSERT INTO users (name, email, password, 
            family1_name, family1_phone, family1_email,
            family2_name, family2_phone, family2_email)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name, email, hash_password(password),
            fam1["name"], fam1["phone"], fam1["email"],
            fam2["name"], fam2["phone"], fam2["email"]
        ))
        conn.commit()
        return True, "✅ Registered successfully!"
    except sqlite3.IntegrityError:
        return False, "❌ Email already exists."

def login_user(email, password):
    cursor.execute("SELECT name, password FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    if result and verify_password(result[1], password):
        return True, f"✅ Welcome back, {result[0]}!", result[0]
    return False, "❌ Invalid email or password.", None

#---------------------------------- streamlit UI ----------------------------------
st.set_page_config(page_title="Driver Monitoring System", layout="wide")

st.markdown("""
    <style>
    div[data-testid="stAlert"] {
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
        text-align: center;
        padding: 10px;
        border-radius: 12px;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

custom_style = """   
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        /* General Button Styling */
        .stButton>button {
            background-color: #0e7c86;
            color: white;
            font-weight: bold;
            padding: 8px 20px;
            border: none;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-top: 10px;
            transition: 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #095f66;
            color:white;
            font-size: 15px;
            transform: scale(1.03);
        }
        input {
            border-radius: 10px !important;
        }
    </style>
    """
st.markdown(custom_style, unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        [data-testid="collapsedControl"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

#----------------------------Option Menu---------------------------------------
if not st.session_state.logged_in:
    with st.sidebar:
        st.markdown(
            """
            <h1 style='color: #0e7c86; text-align: center; font-size: 40px;'> 
                DriCare360
            </h1>
            """,
            unsafe_allow_html=True
        )

        selected = option_menu(
            menu_title=None,
            options=["Welcome", "Login / Register"],
            icons=["house", "person"],
            menu_icon="car-front-fill",
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "color": "#0e7c86",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {
                    "background-color": "#0e7c86",
                    "color": "white",
                },
            },
        )
else:
    selected = None

#---------------------------------------Welcome Page----------------------------------
if not st.session_state.get("logged_in"):
    if selected == "Welcome":
        st.markdown("<h1 style='color:#0e7c86; text-align:center;'>🚗 Welcome to <br> Driver Monitoring System</h1>", unsafe_allow_html=True)
        st.markdown("<h6 style='margin-top:20px; text-align:right;'>~It's better to stop driving when drowsy than to sink one foot in the grave.</h6>", unsafe_allow_html=True)
        st.markdown("<p style='margin-top:20px; font-size:20px;'> Your safety on the road is our priority...</p>",unsafe_allow_html=True)
        st.markdown("<p style='font-size:18px;'> This intelligent system uses your webcam to monitor real-time signs of drowsiness—like eye closure, yawning, and head movement—to help prevent fatigue-related accidents.</p>",unsafe_allow_html=True)
        st.markdown("<p style='margin-top:20px; font-size:20px; text-align:center'>---<br> Drive safe. Stay awake. Stay alive..</p>",unsafe_allow_html=True)

    elif selected == "Login / Register":
        st.markdown("<h1 style='color:#0e7c86; text-align:center;'>🔐 Login or Register</h1>", unsafe_allow_html=True)

        if "form_type" not in st.session_state:
            st.session_state.form_type = "initial"

        def switch_to_signup():
            st.session_state.form_type = "signup"

        def switch_to_login():
            st.session_state.form_type = "initial"

        col_left, col_mid, col_right = st.columns([1, 4, 1])
        with col_mid:
            if st.session_state.form_type == "initial":
                st.markdown("<h3 style='text-align:center;'>🧑‍💻 New user?</h3>", unsafe_allow_html=True)
                st.button("Sign Up", on_click=switch_to_signup, use_container_width=True)
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align:center;'>🔐 Returning user? Login below</h3>", unsafe_allow_html=True)

                with st.form("login_form"):
                    email = st.text_input("Email")
                    password = st.text_input("Password", type="password")
                    submitted = st.form_submit_button("Login", use_container_width=True)
                    if submitted:
                        if not email or not password:
                            st.warning("⚠️ Please enter both email and password.")
                        else:
                            success, msg, name = login_user(email, password)
                            if success:
                                st.success(msg)
                                st.session_state.logged_in = True
                                st.session_state.username = name  # or use the actual name if fetched
                                st.session_state.user_email = email  # <- Add this
                                st.rerun()
                            else:
                                st.error(msg)


            elif st.session_state.form_type == "signup":
                st.subheader("👋 New user? Sign up below")
                with st.form("signup_form"):
                    name = st.text_input("Full Name")
                    email = st.text_input("Email")
                    password = st.text_input("Password", type="password")
                    confirm_password = st.text_input("Confirm Password", type="password")
                    st.markdown("### 👨‍👩‍👧‍👦 Family Member 1 Details")
                    family1_name = st.text_input("Family Member 1 - Name")
                    family1_phone = st.text_input("Family Member 1 - Phone")
                    family1_email = st.text_input("Family Member 1 - Email")
                    st.markdown("### 👨‍👩‍👧‍👦 Family Member 2 Details")
                    family2_name = st.text_input("Family Member 2 - Name")
                    family2_phone = st.text_input("Family Member 2 - Phone")
                    family2_email = st.text_input("Family Member 2 - Email")

                    submitted = st.form_submit_button("Register", use_container_width=True)
                    if submitted:
                        if password != confirm_password:
                            st.error("❌ Passwords do not match!")
                        elif not all([name, email, password, family1_name, family1_phone, family1_email, family2_name, family2_phone, family2_email]):
                            st.warning("⚠️ All fields are required.")
                        else:
                            fam1 = {"name": family1_name, "phone": family1_phone, "email": family1_email}
                            fam2 = {"name": family2_name, "phone": family2_phone, "email": family2_email}
                            success, msg = register_user(name, email, password, fam1, fam2)
                            if success:
                                st.success(msg + " Please log in to continue.")
                                st.session_state.form_type = "initial"
                                st.rerun()
                            else:
                                st.error(msg)
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("<h4 style='color:#0e7c86; text-align:center;'>Already have an account?</h4>", unsafe_allow_html=True)
                st.button("Back to Login", on_click=switch_to_login, use_container_width=True)

#-------------------------------Main Menu Options-------------------------------
if st.session_state.get("logged_in"):
    st.markdown(f"<h2 style='color:#0e7c86; text-align:center;'>👋 Welcome, {st.session_state.username}!</h2>", unsafe_allow_html=True)
    menu_option = option_menu(
    menu_title=None,
    options=["Start Detection System", "Show Event Database", "About", "Log out"],
    icons=["camera-video", "bar-chart-line", "info-circle", "door-closed"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
            "container": {
                "max-width": "900px",  
                "margin": "0 auto",   
                "padding": "0px",
                "background-color": "#fafafa",
                "display": "flex",
                "justify-content": "space-between",
                "width": "100%",
                "border-radius": "12px",  
                "overflow": "hidden", 
            },
            "icon": {
                "color": "orange",
                "font-size": "22px",
            },
            "nav-link": {
                "font-size": "16px",
                "color": "#0e7c86",
                "margin": "0px",
                "padding": "10px",
                "height": "120px",
                "width": "100%",
                "text-align": "center",
                "border": "1px solid #ccc",
                "border-radius": "0px",
                "display": "flex",
                "flex-direction": "column",
                "justify-content": "center",
                "align-items": "center",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {
                "background-color": "#0e7c86",
                "color": "white",
            },
        }
    )

    if menu_option == "Start Detection System":    
        st.markdown("<h3 style='margin-left:100px'>🕵️ Driver Drowsiness Detection System</h3>", unsafe_allow_html=True)
        st.info("➡️ Press Start Detection to run full detection.")

        col1, col2, col3 = st.columns([3, 2, 2])
        with col2:
            start_clicked = st.button("▶ Start Detection")

        if start_clicked:
            st.warning("⏳ Running detection... An OpenCV window will open. Press 'q' to quit.")
            try:
                run_drowsiness_detection(st.session_state.user_email)
            except Exception as e:
                st.error(f"⚠️ Detection failed: {e}")
       
    elif menu_option == "Show Event Database":
        user_email = st.session_state.get("user_email", "")
        if not user_email:
            st.warning("Login required to view logs.")
        else:
            st.markdown("<h1 style='text-align:center; color:#0e7c86;'>📊 Drowsiness Log Viewer</h1>", unsafe_allow_html=True)
            db = DrowsinessDatabase()

            def get_table_names():
                db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                return [row[0] for row in db.cursor.fetchall() if row[0].startswith("drowsiness_")]

            def fetch_user_table(table_name, user_email):
                try:
                    df = pd.read_sql_query(
                        f"SELECT timestamp, ear, mar, yaw_angle, status FROM {table_name} WHERE user_email = ?",
                        db.conn, params=(user_email,)
                    )
                    df.insert(0, 'id', range(1, len(df) + 1))
                    return df
                except Exception as e:
                    st.error(f"Failed to load table: {e}")
                    return pd.DataFrame()

            st.markdown("<h3>📅 Today’s Log</h3>", unsafe_allow_html=True)
            today_table = db.get_today_table_name()
            df_today = fetch_user_table(today_table, user_email)
            st.dataframe(df_today, use_container_width=True)

            st.markdown("<h3 style='margin-top:40px;'>📁 View Logs by Date</h3>", unsafe_allow_html=True)
            all_tables = sorted(get_table_names(), reverse=True)
            index_today = all_tables.index(today_table) if today_table in all_tables else 0
            selected_table = st.selectbox("Choose a table", options=all_tables, index=index_today)

            if st.button("🔍 Show Selected Table"):
                df_selected = fetch_user_table(selected_table, user_email)
                st.markdown(f"<h4>Showing: {selected_table}</h4>", unsafe_allow_html=True)
                st.dataframe(df_selected, use_container_width=True)

            st.markdown("<h3 style='margin-top:40px;'>📂 Full History</h3>", unsafe_allow_html=True)
            if st.button("✅ Show my full event history"):
                try:
                    df_all = pd.read_sql_query(
                        "SELECT timestamp, ear, mar, yaw_angle, status FROM drowsiness_events WHERE user_email = ?",
                        db.conn, params=(user_email,)
                    )
                    df_all.insert(0, 'id', range(1, len(df_all) + 1))
                    st.dataframe(df_all, use_container_width=True)
                except Exception as e:
                    st.error(f"Could not load full history: {e}")
            db.close_connection()

    elif menu_option == "About":
        st.markdown("<h3 style='margin-left:100px'>ℹ️ About DriCare360</h3>",unsafe_allow_html=True)
        st.markdown(""" <p style='margin:0px 100px'>
        DriCare360 is a real-time driver drowsiness detection system that keeps you and your loved ones safe.
        When prolonged drowsiness is detected, alerts are sent to registered family contacts.</p>
        """, unsafe_allow_html=True)

    elif menu_option == "Log out":
        if "confirm_logout" not in st.session_state:
            st.session_state.confirm_logout = False
        if not st.session_state.confirm_logout:
            col1, col2 = st.columns([5, 1])
            with col2:
                if st.button("Log out?", type="primary"):
                    st.session_state.confirm_logout = True
                    st.rerun()
        else:
            st.warning("⚠️ Are you sure you want to log out?")
            col1, col2, col3 = st.columns([1, 3, 2])
            with col2:
                if st.button("Yes✅ Yes, log me out"):
                    st.session_state.logged_in = False
                    st.session_state.username = ""
                    st.session_state.confirm_logout = False
                    st.rerun()
            with col3:
                if st.button("❌ No, stay logged in"):
                    st.session_state.confirm_logout = False
                    st.rerun()
