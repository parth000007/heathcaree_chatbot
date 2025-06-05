import streamlit as st
# Import pdfminer.six for PDF processing
from pdfminer.high_level import extract_text
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFSyntaxError

# Ensure 'symptom_assessor.py' is in the same directory or accessible in your Python path
from symptom_assessor import assess_symptoms

# --- Streamlit App Configuration ---
st.set_page_config(
    page_title="Healthcare Chatbot Assistant",
    layout="wide",
    initial_sidebar_state="expanded" # Keep sidebar expanded by default
)

# --- Custom CSS for Styling ---
st.markdown("""
    <style>
    /* Main container font and background */
    .main {
        font-family: 'Segoe UI', sans-serif;
        background-color: #000000; /* Dark background as per original */
        color: #FFFFFF; /* White text for better contrast */
    }
    /* Specific styling for the Streamlit app container */
    .stApp {
        background-color: #000000; /* Ensure the very base is black */
    }
    /* Response box styling */
    .response-box {
        background-color: #333333; /* Darker grey for response boxes */
        color: #E0E0E0; /* Light text for response boxes */
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 0 15px rgba(0,0,0,0.5); /* Stronger shadow for depth */
        margin-bottom: 20px;
        border: 1px solid #555555; /* Subtle border */
    }
    /* Style for Streamlit buttons */
    .stButton>button {
        background-color: #4CAF50; /* Green submit buttons */
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    /* Input fields and text areas */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #222222;
        color: #FFFFFF;
        border: 1px solid #555555;
        border-radius: 5px;
        padding: 10px;
    }
    /* Selectbox styling */
    .stSelectbox>div>div>div>div {
        background-color: #222222;
        color: #FFFFFF;
        border: 1px solid #555555;
        border-radius: 5px;
    }
    /* Sidebar styling */
    .stSidebar {
        background-color: #1a1a1a; /* Darker sidebar */
        color: #FFFFFF;
    }
    .stSidebar .stSelectbox {
        background-color: #222222;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🩺 AI-Powered Healthcare Chatbot Assistant")
st.markdown("---") # Horizontal line for visual separation

# --- Sidebar Navigation ---
st.sidebar.header("Choose a Service")
service = st.sidebar.selectbox(
    "Services Offered",
    [
        "Symptom Assessment",
        "Appointment Scheduling",
        "Medication Reminders",
        "Health Information",
        "Patient Support"
    ],
    index=0 # Default to Symptom Assessment
)

# --- Service Implementations ---

if service == "Symptom Assessment":
    st.header("Symptom Assessment")
    st.info("Provide your symptoms and how long they’ve lasted. "
            "The AI will return a **preliminary** insight (not a diagnosis).")

    with st.form("symptom_form", clear_on_submit=False):
        symptoms = st.text_area("✍️ Describe your symptoms thoroughly (e.g., 'fever, headache, body aches').", height=150)
        duration = st.text_input("⏱ Duration (e.g., '3 days', '1 week', 'since yesterday')")
        submitted = st.form_submit_button("🩺 Assess My Symptoms")

    if submitted:
        if not symptoms:
            st.warning("⚠️ Please describe your symptoms to proceed.")
        elif not duration:
            st.warning("⚠️ Please provide the duration of your symptoms.")
        else:
            with st.spinner("🧠 Gemini is thinking and analyzing your symptoms..."):
                # Call your symptom assessment function without file content
                assessment_result = assess_symptoms(symptoms, duration)

            st.markdown("### ✨ AI Assessment Result")
            st.markdown(f"<div class='response-box'>{assessment_result}</div>", unsafe_allow_html=True)
            st.info("⚠️ **Disclaimer:** This assessment is for informational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of a qualified healthcare provider for any medical concerns.")git status
elif service == "Appointment Scheduling":
    st.header("🗓️ Appointment Scheduling")
    with st.form("appointment_form", clear_on_submit=True):
        name = st.text_input("👤 Full Name")
        department = st.selectbox("🏥 Desired Department", ["General Practice", "Cardiology", "Orthopedics", "Gynecology", "Dermatology", "Pediatrics"])
        date = st.date_input("📅 Preferred Date")
        time = st.time_input("⏰ Preferred Time")
        notes = st.text_area("📝 Additional Notes (e.g., reason for visit)", height=80)
        submit = st.form_submit_button("✅ Book Appointment")

        if submit:
            if not all([name, department, date, time]):
                st.warning("⚠️ Please fill in all required fields to book an appointment.")
            else:
                st.success(f"🎉 Appointment booked for **{name}** with the **{department}** department on **{date.strftime('%B %d, %Y')} at {time.strftime('%I:%M %p')}**.")
                st.info("You will receive a confirmation email shortly.")

elif service == "Medication Reminders":
    st.header("⏰ Medication Reminders")
    with st.form("med_form", clear_on_submit=True):
        med_name = st.text_input("💊 Medication Name (e.g., 'Aspirin')")
        dosage = st.text_input("🧪 Dosage (e.g., '100mg', '2 pills')")
        times = st.text_area("🔔 Reminder Times (e.g., '9:00 AM, 6:00 PM, 10:00 PM' or 'Every 8 hours')", height=100)
        start_date = st.date_input("🗓️ Start Date for Reminders")
        submit = st.form_submit_button("➕ Set Reminder")

        if submit:
            if not all([med_name, dosage, times, start_date]):
                st.warning("⚠️ Please fill in all fields to set a medication reminder.")
            else:
                st.success(f"✅ Reminder set for **{med_name} ({dosage})** starting **{start_date.strftime('%B %d, %Y')}** at: **{times}**.")
                st.info("You will receive notifications at the specified times.")

elif service == "Health Information":
    st.header("📚 Health Information")
    st.subheader("Choose a Health Topic to learn more:")
    topic = st.selectbox(
        "Select a Topic",
        [
            "Nutrition",
            "Cardiology",
            "Diabetes",
            "Mental Health",
            "Fitness",
            "Women's Health",
            "General Wellness"
        ],
        index=0 # Default to Nutrition
    )

    health_topics_info = {
        "Nutrition": {
            "title": "🥗 Healthy Eating Essentials",
            "points": [
                "**Balanced Diet:** Focus on fruits, vegetables, whole grains, lean proteins, and healthy fats.",
                "**Vitamins & Minerals:** Understand essential nutrients and their sources.",
                "**Hydration:** Drink adequate water throughout the day.",
                "**Macronutrients:** Balance your intake of carbohydrates, proteins, and fats.",
                "**Fiber:** Incorporate fiber-rich foods for digestive health."
            ],
            "description": "Learn the fundamentals of good nutrition for a healthy lifestyle. Small changes in diet can lead to significant health improvements."
        },
        "Cardiology": {
            "title": "❤️ Heart Health Tips",
            "points": [
                "**Blood Pressure Control:** Regular monitoring and management are crucial.",
                "**Cholesterol Management:** Understand LDL, HDL, and triglycerides.",
                "**ECG (EKG):** What it is and why it's used.",
                "**Heart Attack Signs:** Recognize symptoms for prompt action (e.g., chest pain, shortness of breath).",
                "**Stress Management:** Techniques to reduce stress and its impact on heart health."
            ],
            "description": "Information on maintaining a healthy heart and recognizing cardiovascular concerns."
        },
        "Diabetes": {
            "title": "🩸 Managing Diabetes",
            "points": [
                "**Blood Sugar Monitoring:** Importance of regular glucose checks.",
                "**Insulin Therapy:** Understanding different types and administration.",
                "**Low-carb Diet:** Benefits and considerations for diabetes management.",
                "**Glycemic Index:** How foods affect blood sugar levels."
            ],
            "description": "Comprehensive guide to understanding and managing diabetes effectively."
        },
        "Mental Health": {
            "title": "🧠 Mental Wellness & Support",
            "points": [
                "**Meditation & Mindfulness:** Practices for stress reduction and focus.",
                "**Therapy & Counseling:** When and how to seek professional help.",
                "**Sleep Hygiene:** Tips for improving sleep quality.",
                "**Stress Relief Techniques:** Breathing exercises, hobbies, and relaxation.",
                "**CBT (Cognitive Behavioral Therapy):** An overview of this therapeutic approach."
            ],
            "description": "Resources and advice for fostering positive mental health and well-being."
        },
        "Fitness": {
            "title": "💪 Fitness and Active Lifestyle",
            "points": [
                "**Cardio Exercises:** Benefits and different types (running, swimming, cycling).",
                "**Strength Training:** Building muscle and improving bone density.",
                "**Yoga & Flexibility:** Enhancing balance, flexibility, and relaxation.",
                "**Routine Building:** How to create an effective workout plan.",
                "**Recovery:** Importance of rest and recovery in fitness."
            ],
            "description": "Guidance on incorporating physical activity into your daily life for improved health."
        },
        "Women's Health": {
            "title": "🌸 Women's Wellness",
            "points": [
                "**Menstrual Health:** Understanding cycles and common issues.",
                "**PCOS (Polycystic Ovary Syndrome):** Symptoms and management.",
                "**Breast Health:** Self-exams and screening guidelines.",
                "**Pregnancy & Postpartum Care:** Essential information for expectant and new mothers.",
                "**Menopause:** Navigating changes and symptoms."
            ],
            "description": "Specific health topics and concerns relevant to women's well-being."
        },
        "General Wellness": {
            "title": "✨ Holistic Health & General Well-being",
            "points": [
                "**Preventive Care:** Importance of regular check-ups and screenings.",
                "**Stress Management:** Techniques to cope with daily stressors.",
                "**Work-Life Balance:** Achieving harmony between personal and professional life.",
                "**Healthy Habits:** Building routines for sustained well-being.",
                "**Community & Social Health:** The role of connections in overall health."
            ],
            "description": "Broad topics covering overall health and a balanced lifestyle."
        }
    }

    if topic:
        info = health_topics_info.get(topic, health_topics_info["General Wellness"]) # Fallback to general wellness
        st.subheader(info["title"])
        st.markdown(f"*{info['description']}*")
        st.markdown("**Key Points:**")
        for point in info["points"]:
            st.markdown(f"- {point}")

elif service == "Patient Support":
    st.header("🤝 Patient Support")
    st.info("Share your concerns or questions, and our wellness coach team will provide support and guidance.")
    with st.form("support_form", clear_on_submit=True):
        full_name = st.text_input("👤 Your Full Name")
        contact_email = st.text_input("📧 Your Email Address")
        concern = st.text_area("💬 Describe your concern or question here", height=150)
        privacy_agree = st.checkbox("✅ I agree to share this information for support purposes.")
        submit = st.form_submit_button("📩 Request Support")

        if submit:
            if not all([full_name, contact_email, concern, privacy_agree]):
                st.warning("⚠️ Please fill in all fields and agree to the terms to request support.")
            else:
                st.success("🙏 Thank you for sharing your concern. Our wellness coach will get back to you via email shortly.")
                st.markdown(f"**Concern submitted by:** {full_name} ({contact_email})")
                st.markdown(f"**Your Message:** _{concern}_")

# --- Footer ---
st.markdown("---")
st.markdown("<center>Built with ❤️ using Streamlit | Still under active development</center>", unsafe_allow_html=True)
st.markdown("<center>_For emergencies, always contact professional medical services directly._</center>", unsafe_allow_html=True)