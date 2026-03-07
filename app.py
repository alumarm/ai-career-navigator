import json
import time
import streamlit as st

# =========================
# Page Config
# =========================
st.set_page_config(page_title="AI Career Navigator", page_icon="🎯", layout="centered")


# =========================
# Style
# =========================
def apply_custom_style():
    st.markdown(
        """
        <style>
        .main-title {
            font-size: 42px;
            font-weight: 800;
            color: #1f2937;
            margin-bottom: 10px;
        }

        .sub-text {
            font-size: 18px;
            color: #4b5563;
            margin-bottom: 25px;
        }

        .section-box {
            background-color: #f8fafc;
            padding: 20px;
            border-radius: 14px;
            border: 1px solid #e5e7eb;
            margin-bottom: 20px;
        }

        .scenario-card {
            background-color: #ffffff;
            padding: 18px;
            border-radius: 14px;
            border: 1px solid #e5e7eb;
            margin-bottom: 16px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        }

        .scenario-title {
            font-size: 22px;
            font-weight: 700;
            color: #111827;
            margin-bottom: 8px;
        }

        .scenario-text {
            font-size: 16px;
            color: #374151;
            margin-bottom: 10px;
            line-height: 1.7;
        }

        .scenario-question {
            font-size: 15px;
            color: #1f2937;
            font-weight: 600;
            margin-top: 8px;
            margin-bottom: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


apply_custom_style()

# =========================
# Load Data
# =========================
with open("majors.json", "r", encoding="utf-8") as f:
    majors_data = json.load(f)

with open("skill_questions.json", "r", encoding="utf-8") as f:
    skill_questions = json.load(f)

with open("simulation_scenarios.json", "r", encoding="utf-8") as f:
    simulation_scenarios = json.load(f)

# =========================
# Session State
# =========================
if "page" not in st.session_state:
    st.session_state.page = "assessment"

if "results" not in st.session_state:
    st.session_state.results = None

if "selected_major" not in st.session_state:
    st.session_state.selected_major = None

if "user_profile" not in st.session_state:
    st.session_state.user_profile = None

# =========================
# Helpers
# =========================
majors_lookup = {item["name"]: item for item in majors_data}
labels = ["Best Match", "Strong Alternative", "Exploration Option"]

profile_labels = {
    "math": "القدرة الرياضية",
    "analysis": "التحليل",
    "technology": "الميول التقنية",
    "creativity": "الإبداع",
    "human": "الجانب الإنساني",
    "management": "الإدارة واتخاذ القرار"
}


def calculate_user_profile(q1, q2, q3, q4, q5, q6, sim1, sim2, sim3):
    profile = {
        "math": 0,
        "analysis": 0,
        "technology": 0,
        "creativity": 0,
        "human": 0,
        "management": 0
    }

    # Skill questions
    profile["math"] += q1
    profile["analysis"] += q2
    profile["technology"] += q3
    profile["creativity"] += q4
    profile["human"] += q5
    profile["management"] += q6

    # Simulation 1
    if sim1 == "أراجع البيانات المدخلة أولًا":
        profile["analysis"] += 2
        profile["technology"] += 2
    elif sim1 == "أعيد تصميم الواجهة مباشرة":
        profile["creativity"] += 2
    elif sim1 == "أسأل المستخدمين عن المشكلة":
        profile["human"] += 2
    elif sim1 == "أجرب أداة أخرى فورًا":
        profile["management"] += 1

    # Simulation 2
    if sim2 == "أجمع المعلومات أولًا قبل الحكم":
        profile["analysis"] += 2
    elif sim2 == "أبدأ بطمأنته والاستماع له":
        profile["human"] += 2
    elif sim2 == "أتخذ قرارًا سريعًا من أول انطباع":
        profile["management"] += 1
    elif sim2 == "أرتب الخيارات وأحدد الأولويات":
        profile["management"] += 2

    # Simulation 3
    if sim3 == "أحلل بيانات السوق والعملاء":
        profile["analysis"] += 2
        profile["management"] += 1
    elif sim3 == "أغير الحملة التسويقية":
        profile["creativity"] += 2
    elif sim3 == "أتحدث مع العملاء لفهم السبب":
        profile["human"] += 2
    elif sim3 == "أعيد تنظيم خطة الإطلاق":
        profile["management"] += 2

    return profile


def calculate_fit_score(user_profile, major_profile):
    score = 0
    max_score = 0

    for key in user_profile:
        score += min(user_profile[key], major_profile[key])
        max_score += 5

    fit = int((score / max_score) * 100)
    return fit


def recommend_top_majors(user_profile):
    results = []

    for major in majors_data:
        fit_score = calculate_fit_score(user_profile, major["profile"])
        results.append((major["name"], fit_score))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:3]


def generate_final_message(best_major, domain):
    return f"بناءً على نتائجك، يظهر أن لديك ميولًا قوية نحو مجال {domain}، ويُعد تخصص {best_major} من أكثر الخيارات المناسبة لك في هذه المرحلة."


# =========================
# Page 1: Assessment
# =========================
if st.session_state.page == "assessment":
    st.markdown('<div class="main-title">AI Career Navigator</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-text">اختبار ذكي يساعدك على اكتشاف التخصص الجامعي المناسب لك باستخدام تحليل المهارات والمحاكاة المهنية.</div>',
        unsafe_allow_html=True
    )

    name = st.text_input("اكتب اسمك")

    st.markdown(
        '<div class="section-box"><h3>1) اختبار المهارات</h3><p>قيّم ميولك ومهاراتك من خلال الأسئلة التالية.</p></div>',
        unsafe_allow_html=True
    )

    answers = {}
    for question in skill_questions:
        answers[question["id"]] = st.slider(question["label"], 1, 5)

    st.markdown(
        '<div class="section-box"><h3>2) المحاكاة المهنية التفاعلية</h3><p>اقرأ الموقف التالي، ثم اختر القرار الذي ترى أنه الأنسب في بداية التعامل مع الحالة.</p></div>',
        unsafe_allow_html=True
    )

    sim_answers = {}
    for scenario in simulation_scenarios:
        st.markdown(
            f"""
            <div class="scenario-card">
                <div class="scenario-title">{scenario["title"]}</div>
                <div class="scenario-text">{scenario["scenario"]}</div>
                <div class="scenario-question">{scenario["question"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        sim_answers[scenario["id"]] = st.radio(
            label="اختر قرارك:",
            options=scenario["options"],
            key=scenario["id"]
        )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("تحليل النتائج"):
            st.session_state.user_name = name
            st.session_state.user_profile = calculate_user_profile(
                answers["q1"], answers["q2"], answers["q3"],
                answers["q4"], answers["q5"], answers["q6"],
                sim_answers["sim1"], sim_answers["sim2"], sim_answers["sim3"]
            )
            st.session_state.results = recommend_top_majors(st.session_state.user_profile)
            st.session_state.page = "analysis"
            st.rerun()

    with col2:
        if st.button("إعادة ضبط"):
            st.session_state.page = "assessment"
            st.session_state.results = None
            st.session_state.selected_major = None
            st.session_state.user_profile = None
            st.rerun()

# =========================
# Page 2: AI Analysis
# =========================
elif st.session_state.page == "analysis":
    st.title("AI Analysis in Progress")
    st.write("يقوم النظام الآن بتحليل ملفك المهاري والسلوكي...")

    progress_bar = st.progress(0)
    status = st.empty()

    steps = [
        "تحليل نتائج اختبار المهارات...",
        "تحليل قراراتك داخل المحاكاة المهنية...",
        "بناء الملف المهاري الشخصي...",
        "مقارنة الملف مع التخصصات المرجعية...",
        "احتساب Career Fit Score...",
        "إنتاج أفضل 3 تخصصات مناسبة..."
    ]

    for i, step in enumerate(steps):
        status.info(step)
        progress_bar.progress(int((i + 1) / len(steps) * 100))
        time.sleep(0.7)

    st.session_state.page = "results"
    st.rerun()

# =========================
# Page 3: Results
# =========================
elif st.session_state.page == "results":
    st.title("🎯 نتائجك النهائية")
    st.write("فيما يلي أفضل 3 تخصصات مناسبة لك بناءً على تحليل المهارات والمحاكاة المهنية.")

    user_name = st.session_state.get("user_name", "")
    results = st.session_state.results
    user_profile = st.session_state.user_profile

    st.success(f"مرحبًا {user_name if user_name else 'بك'}، هذه أفضل 3 تخصصات مناسبة لك:")

    st.subheader("📊 ملفك المهاري")
    st.write("هذا الملخص يوضح الجوانب التي ظهرت بشكل أقوى في نتائجك:")

    max_profile_score = 7

    for key, value in user_profile.items():
        label = profile_labels[key]
        ratio = min(value / max_profile_score, 1.0)
        st.write(f"{label}: {value}")
        st.progress(ratio)

    st.divider()

    for i, (major, fit_score) in enumerate(results):
        major_info = majors_lookup[major]

        st.subheader(f"{labels[i]} — {major}")
        st.write(f"المجال العام: {major_info['domain']}")
        st.write(f"Career Fit Score: {fit_score} / 100")
        st.progress(fit_score / 100)

        risk = major_info["saturation_risk"]
        if risk == "منخفض":
            st.success(f"Saturation Risk: {risk}")
        elif risk == "متوسط":
            st.warning(f"Saturation Risk: {risk}")
        else:
            st.error(f"Saturation Risk: {risk}")

        st.write(f"سبب التوصية: {major_info['explanation']}")

        if st.button(f"عرض المسار المهني لـ {major}", key=major):
            st.session_state.selected_major = major
            st.session_state.page = "details"
            st.rerun()

        st.divider()

    best_major = results[0][0]
    best_domain = majors_lookup[best_major]["domain"]
    st.info(generate_final_message(best_major, best_domain))

    if st.button("🔄 إعادة التجربة من البداية"):
        st.session_state.page = "assessment"
        st.session_state.results = None
        st.session_state.selected_major = None
        st.session_state.user_profile = None
        st.rerun()

# =========================
# Page 4: Career Path
# =========================
elif st.session_state.page == "details":
    major = st.session_state.selected_major
    data = majors_lookup[major]

    st.title(f"🧭 Career Path Map — {major}")
    st.write("هذه الخريطة تساعدك على فهم المهارات المطلوبة، الوظائف المستقبلية، وكيف تبدأ مبكرًا في استكشاف المجال.")

    st.write(f"**المجال العام:** {data['domain']}")

    st.subheader("المهارات المطلوبة")
    for skill in data["skills"]:
        st.write(f"- {skill}")

    st.subheader("الوظائف المستقبلية")
    for job in data["jobs"]:
        st.write(f"- {job}")

    st.subheader("Career Discovery Kit")
    for item in data["discovery"]:
        st.write(f"- {item}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("العودة إلى النتائج"):
            st.session_state.page = "results"
            st.rerun()

    with col2:
        if st.button("🔄 إعادة التجربة"):
            st.session_state.page = "assessment"
            st.session_state.results = None
            st.session_state.selected_major = None
            st.session_state.user_profile = None
            st.rerun()
