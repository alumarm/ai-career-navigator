import streamlit as st
import json
import random

# --------------------------------
# تحميل البيانات
# --------------------------------

with open("majors.json", "r", encoding="utf-8") as f:
    majors = json.load(f)

with open("skill_questions.json", "r", encoding="utf-8") as f:
    skill_questions = json.load(f)

with open("simulation_scenarios.json", "r", encoding="utf-8") as f:
    simulation_scenarios = json.load(f)


# --------------------------------
# إعداد الصفحة
# --------------------------------

st.set_page_config(
    page_title="AI Career Navigator",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Career Navigator")
st.write("اكتشف التخصص التقني الأنسب لك بناءً على مهاراتك واهتماماتك.")


# --------------------------------
# إدخال اسم المستخدم
# --------------------------------

name = st.text_input("اكتب اسمك")

if name:
    st.success(f"مرحبًا {name} 👋")

# --------------------------------
# اختبار المهارات
# --------------------------------

st.header("اختبار المهارات")

answers = {}

for q in skill_questions:
    answers[q["question"]] = st.slider(
        q["question"],
        1,
        5,
        3
    )

# --------------------------------
# تحليل النتائج
# --------------------------------

if st.button("تحليل النتائج"):

    scores = {}

    for major in majors:

        score = 0

        for skill in major["skills"]:

            for q in skill_questions:

                if q["skill"] == skill:
                    score += answers[q["question"]]

        scores[major["name"]] = score

    sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    st.header("نتائجك النهائية")

    best_major = sorted_results[0]

    st.subheader(f"Best Match — {best_major[0]}")
    st.progress(1.0)

    st.write("Saturation Risk: منخفض")

    st.write("سبب التوصية: هذا التخصص مناسب لك لأن لديك ميول تحليلية وتقنية قوية.")

    st.button(f"عرض المسار المهني لـ {best_major[0]}")

    st.divider()

    if len(sorted_results) > 1:
        second_major = sorted_results[1]

        st.subheader(f"Strong Alternative — {second_major[0]}")
        st.progress(0.7)

    st.divider()

    st.header("المهارات المطلوبة")

    for skill in majors[0]["skills"]:
        st.write(f"- {skill}")

    st.header("الوظائف المستقبلية")

    for job in majors[0]["careers"]:
        st.write(f"- {job}")

    st.header("Career Discovery Kit")

    st.write("- تعلم Python")
    st.write("- جرّب مشروع ML بسيط")
    st.write("- تعرّف على مفاهيم الذكاء الاصطناعي")

# --------------------------------
# المحاكاة المهنية
# --------------------------------

st.divider()
st.header("المحاكاة المهنية")

scenario = random.choice(simulation_scenarios)

st.write(scenario["scenario"])

choice = st.radio("ما القرار الذي ستتخذه؟", scenario["choices"])

if st.button("عرض النتيجة"):

    if choice == scenario["correct"]:
        st.success("قرار ممتاز! هذا يعكس تفكير مهني صحيح.")
    else:
        st.warning("ليس الخيار الأفضل، لكن التعلم من التجربة مهم.")


# --------------------------------
# ملاحظة المشروع
# --------------------------------

st.divider()

st.caption(
"تم تطوير هذا النموذج الأولي كجزء من مشروع تدريبي في معسكر بناء القدرات في الذكاء الاصطناعي."
)
