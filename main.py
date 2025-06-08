import streamlit as st
import PyPDF2  # Make sure you have this installed: pip install PyPDF2
import io

# --- IMPORTANT: Ensure symptom_assessor.py is in the same directory ---
# This file contains the 'assess_symptoms' function which uses the Gemini API.
# Make sure you also have 'secret_key.py' in the same directory with your Gemini API key.
try:
    from symptom_assessor import assess_symptoms
except ImportError:
    st.error("Error: 'symptom_assessor.py' not found or 'assess_symptoms' not defined.")
    st.warning("Please ensure symptom_assessor.py is in the same directory and contains the assess_symptoms function.")
    st.info("The application will run, but symptom assessment will not function correctly.")
    # Define a dummy function to prevent errors if import fails, but indicate the issue
    def assess_symptoms(symptoms, duration, file_content=None):
        return "Error: Symptom assessment service is unavailable. Check your 'symptom_assessor.py' setup."


# ───────────── Streamlit App Configuration ──────────────
st.set_page_config(page_title="Healthcare Chatbot", layout="wide")

st.markdown("""
    <style>
    /* General body styling for dark background and font */
    body {
        font-family: 'Segoe UI', sans-serif;
        background-color: #000000; /* Dark background */
        color: #FFFFFF; /* White text for better contrast */
    }
    /* Streamlit's main content area */
    .main {
        background-color: #000000; /* Ensure main content area is also dark */
        color: #FFFFFF;
    }
    /* Streamlit's sidebar */
    .stSidebar {
        background-color: #1a1a1a; /* Slightly lighter dark for sidebar */
        color: #FFFFFF;
    }
    /* Custom styling for the AI assessment result box */
    .response-box {
        background-color: #1a1a1a; /* Darker grey for response box */
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        color: #FFFFFF;
    }
    /* Adjusting input field colors for dark theme in Streamlit */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stDateInput > div > div > input,
    .stTimeInput > div > div > input {
        background-color: #333333 !important;
        color: #FFFFFF !important;
        border: 1px solid #555555 !important;
    }
    /* Placeholder text color */
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: #AAAAAA !important;
    }
    /* Selectbox styling */
    .stSelectbox > div > div > div {
        background-color: #333333 !important;
        color: #FFFFFF !important;
        border: 1px solid #555555 !important;
    }
    .stSelectbox > div > div > div > div {
        color: #FFFFFF !important; /* Text inside selectbox */
    }
    /* Button styling */
    .stButton > button {
        background-color: #007bff !important; /* Blue button */
        color: white !important;
        border-radius: 5px !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
        border: none !important;
    }
    .stButton > button:hover {
        background-color: #0056b3 !important;
    }
    /* Info/Warning/Success boxes */
    .stAlert {
        background-color: #004d40; /* Darker teal/green for info */
        color: #e0f2f1;
        border-radius: 5px;
        margin-bottom: 15px;
        font-weight: bold;
    }
    .stAlert > div > div > div > div {
        color: #e0f2f1 !important; /* Ensure text color is light */
    }
    .stAlert.warning {
        background-color: #8B4513; /* Darker orange/brown for warning */
        color: #FFD700;
    }
    .stAlert.success {
        background-color: #228B22; /* Darker green for success */
        color: #90EE90;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🩺 AI-Powered Healthcare Chatbot Assistant")

# ───────────── Sidebar Navigation ──────────────
st.sidebar.header("Choose a Service")
service = st.sidebar.selectbox("Services Offered", [
    "Symptom Assessment",
    "Appointment Scheduling",
    "Medication Reminders",
    "Health Information",
    "Patient Support"
])

# ───────────── Service Implementations ──────────────

if service == "Symptom Assessment":
    st.info("Provide your symptoms and how long they’ve lasted. "
            "The AI will return a **preliminary** insight (not a diagnosis).")

    with st.form("symptom_form"):
        symptoms = st.text_area(" Describe your symptoms", key="symptoms_input")
        duration = st.text_input("⏱ Duration (e.g., 3 days, 1 week)", key="duration_input")
        upload = st.file_uploader("📎 Optional: upload extra info (TXT or PDF)", type=["txt", "pdf"], key="upload_file")
        submitted = st.form_submit_button("🩺 Assess")

    if submitted:
        if not symptoms or not duration:
            st.warning("⚠ Please fill in both symptoms and duration.")
            # st.stop() # Removed st.stop() as it can be abrupt in some contexts

        else:
            file_text = None
            if upload:
                try:
                    if upload.type == "text/plain":
                        file_text = upload.read().decode("utf-8")
                    elif upload.type == "application/pdf":
                        # PyPDF2.PdfReader expects a file-like object, which upload provides
                        reader = PyPDF2.PdfReader(io.BytesIO(upload.read()))
                        file_text = " ".join(page.extract_text() or "" for page in reader.pages)
                    st.success(f"📄 Processed upload: {upload.name}")
                except Exception as e:
                    st.warning(f"❌ Could not read the uploaded file: {e}")

            with st.spinner("Gemini is thinking…"):
                result = assess_symptoms(symptoms, duration, file_text)

            st.markdown("### AI Assessment Result")
            st.markdown(f"<div class='response-box'>{result}</div>", unsafe_allow_html=True)

elif service == "Appointment Scheduling":
    with st.form("appointment_form"):
        name = st.text_input("👤 Full Name", key="appointment_name")
        department = st.selectbox("Department", ["General", "Cardiology", "Orthopedics", "Gynecology", "Dermatology"], key="appointment_department")
        date = st.date_input("Date", key="appointment_date")
        time = st.time_input("Time", key="appointment_time")
        submit = st.form_submit_button("Book Appointment")
        if submit:
            if not name or not department or not date or not time:
                st.warning("⚠ Please fill in all appointment details.")
            else:
                st.success(f"✅ Appointment booked for **{name}** with **{department}** on **{date} at {time}**.")

elif service == "Medication Reminders":
    with st.form("med_form"):
        med_name = st.text_input("Medication Name", key="med_name")
        dosage = st.text_input("Dosage", key="dosage")
        times = st.text_area("Reminder Times (e.g., 9:00 AM, 6:00 PM)", key="times")
        submit = st.form_submit_button("Set Reminder")
        if submit:
            if not med_name or not dosage or not times:
                st.warning("⚠ Please fill in all medication reminder details.")
            else:
                st.success(f"⏰ Reminder set for **{med_name}** at: {times}")

elif service == "Patient Support":
    with st.form("support_form"):
        concern = st.text_area(" Share your concern", key="concern")
        submit = st.form_submit_button("Request Support")
        if submit:
            if not concern:
                st.warning("⚠ Please describe your concern.")
            else:
                st.success("✅ Thank you for sharing. A wellness coach will get back to you soon.")

elif service == "Health Information":
    st.subheader(" Choose a Health Topic")
    topic = st.selectbox("Select Topic", [
        "Nutrition", "Cardiology", "Diabetes", "Mental Health", "Fitness", "Women's Health"
    ], key="health_topic_selector")

    health_topics = {
        "Nutrition": ("Healthy Eating Essentials", ["Balanced Diet", "Vitamins", "Hydration", "Macronutrients", "Fiber"]),
        "Cardiology": ("Heart Health Tips", ["Blood Pressure", "Cholesterol", "ECG", "Heart Attack Signs", "Stress Management"]),
        "Diabetes": ("Managing Diabetes", ["Blood Sugar Monitoring", "Insulin", "Low-carb Diet", "Glycemic Index"]),
        "Mental Health": ("Mental Wellness", ["Meditation", "Therapy", "Sleep Hygiene", "Stress Relief", "CBT"]),
        "Fitness": ("Fitness and Lifestyle", ["Cardio", "Strength Training", "Yoga", "Routine Building", "Recovery"]),
        "Women's Health": ("Women's Wellness", ["Menstrual Health", "PCOS", "Breast Health", "Pregnancy", "Menopause"]),
    }

    if topic: # This check ensures content only displays if a topic is selected (which it always is by default)
        title, points = health_topics.get(topic, ("General Info", []))
        st.subheader(title)
        st.markdown("**Key Points:**")
        for point in points:
            st.markdown(f"- {point}")

# ───────────── Footer ──────────────
st.markdown("---")
st.markdown("<center>Built with using Streamlit (DIVYANSHU KAUSHIK -ANURAG DAS)| Still under development</center>", unsafe_allow_html=True)
