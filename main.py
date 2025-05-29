import streamlit as st
import PyPDF2
from symptom_assessor import assess_symptoms  # Import your helper function

# ───────────── Streamlit App Configuration ──────────────
st.set_page_config(page_title="Healthcare Chatbot", layout="wide")

st.markdown("""
    <style>
    .main { font-family: 'Segoe UI', sans-serif; }
    .stApp { background-color: #000000; }
    .response-box {
        background-color: #f0f0f0;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
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
        symptoms = st.text_area(" Describe your symptoms")
        duration = st.text_input("⏱ Duration (e.g., 3 days, 1 week)")
        upload = st.file_uploader("📎 Optional: upload extra info (TXT or PDF)", type=["txt", "pdf"])
        submitted = st.form_submit_button("🩺 Assess")

    if submitted:
        if not symptoms or not duration:
            st.warning("⚠ Please fill in both symptoms and duration.")
            st.stop()

        file_text = None
        if upload:
            try:
                if upload.type == "text/plain":
                    file_text = upload.read().decode("utf-8")
                elif upload.type == "application/pdf":
                    reader = PyPDF2.PdfReader(upload)
                    file_text = " ".join(page.extract_text() or "" for page in reader.pages)
                st.success(f"📄 Processed upload: {upload.name}")
            except Exception as e:
                st.warning(f"❌ Could not read the uploaded file: {e}")

        with st.spinner("Gemini is thinking…"):
            result = assess_symptoms(symptoms, duration, file_text)

        st.markdown("###  AI Assessment Result")
        st.markdown(f"<div class='response-box'>{result}</div>", unsafe_allow_html=True)

elif service == "Appointment Scheduling":
    with st.form("appointment_form"):
        name = st.text_input("👤 Full Name")
        department = st.selectbox("Department", ["General", "Cardiology", "Orthopedics", "Gynecology", "Dermatology"])
        date = st.date_input("Date")
        time = st.time_input("Time")
        submit = st.form_submit_button("Book Appointment")
        if submit:
            st.success(f" Appointment booked for **{name}** with **{department}** on **{date} at {time}**.")

elif service == "Medication Reminders":
    with st.form("med_form"):
        med_name = st.text_input("Medication Name")
        dosage = st.text_input("Dosage")
        times = st.text_area("Reminder Times (e.g., 9:00 AM, 6:00 PM)")
        submit = st.form_submit_button("Set Reminder")
        if submit:
            st.success(f"⏰ Reminder set for **{med_name}** at: {times}")

elif service == "Patient Support":
    with st.form("support_form"):
        concern = st.text_area(" Share your concern")
        submit = st.form_submit_button("Request Support")
        if submit:
            st.success(" Thank you for sharing. A wellness coach will get back to you soon.")

elif service == "Health Information":
    st.subheader(" Choose a Health Topic")
    topic = st.selectbox("Select Topic", [
        "Nutrition", "Cardiology", "Diabetes", "Mental Health", "Fitness", "Women's Health"
    ])

    health_topics = {
        "Nutrition": ("Healthy Eating Essentials", ["Balanced Diet", "Vitamins", "Hydration", "Macronutrients", "Fiber"]),
        "Cardiology": ("Heart Health Tips", ["Blood Pressure", "Cholesterol", "ECG", "Heart Attack Signs", "Stress Management"]),
        "Diabetes": ("Managing Diabetes", ["Blood Sugar Monitoring", "Insulin", "Low-carb Diet", "Glycemic Index"]),
        "Mental Health": ("Mental Wellness", ["Meditation", "Therapy", "Sleep Hygiene", "Stress Relief", "CBT"]),
        "Fitness": ("Fitness and Lifestyle", ["Cardio", "Strength Training", "Yoga", "Routine Building", "Recovery"]),
        "Women's Health": ("Women's Wellness", ["Menstrual Health", "PCOS", "Breast Health", "Pregnancy", "Menopause"]),
    }

    if topic:
        title, points = health_topics.get(topic, ("General Info", []))
        st.subheader(title)
        st.markdown("**Key Points:**")
        for point in points:
            st.markdown(f"- {point}")

# ───────────── Footer ──────────────
st.markdown("---")
st.markdown("<center>Built with using Streamlit | Still under development</center>", unsafe_allow_html=True)