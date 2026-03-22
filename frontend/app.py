"""
app.py — مساعد الطالب الذكي  |  Pro UI
"""

import os
import requests
import streamlit as st

API_BASE = os.getenv("API_BASE", "http://localhost:8000")

# ── Page config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="مساعد الطالب الذكي",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ───────────────────────────────────────────────────────────────

st.markdown("""
<style>
/* ---------- base ---------- */
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Cairo', 'Segoe UI', sans-serif;
    direction: rtl;
}

.stApp {
    background: #0f1117;
    color: #e8eaf0;
}

/* ---------- hide default streamlit chrome ---------- */
#MainMenu, footer, header { visibility: hidden; }

/* ---------- sidebar ---------- */
section[data-testid="stSidebar"] {
    background: #161b27;
    border-left: 1px solid #2a2f3e;
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 1.5rem;
}

/* ---------- hero header ---------- */
.hero {
    background: linear-gradient(135deg, #1a237e 0%, #283593 50%, #0d47a1 100%);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1.2rem;
    box-shadow: 0 4px 24px rgba(26,35,126,0.4);
}

.hero-icon { font-size: 3rem; }

.hero-title {
    font-size: 2rem;
    font-weight: 700;
    color: #fff;
    margin: 0;
    line-height: 1.2;
}

.hero-sub {
    font-size: 0.95rem;
    color: #90caf9;
    margin: 0;
}

/* ---------- doc badge ---------- */
.doc-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: #1e3a5f;
    border: 1px solid #2979ff;
    border-radius: 20px;
    padding: 0.35rem 1rem;
    font-size: 0.9rem;
    color: #90caf9;
    margin-bottom: 1rem;
}

/* ---------- tabs ---------- */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
    background: #161b27;
    border-radius: 12px;
    padding: 0.4rem;
    border: 1px solid #2a2f3e;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 0.5rem 1.2rem;
    font-size: 0.95rem;
    font-weight: 600;
    color: #8892b0;
    background: transparent;
    border: none;
    transition: all 0.2s;
}

.stTabs [aria-selected="true"] {
    background: #1a237e !important;
    color: #fff !important;
}

/* ---------- buttons ---------- */
.stButton > button {
    background: linear-gradient(135deg, #1565c0, #1976d2);
    color: #fff;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1.8rem;
    font-size: 1rem;
    font-weight: 600;
    font-family: 'Cairo', sans-serif;
    cursor: pointer;
    transition: all 0.2s;
    width: 100%;
    box-shadow: 0 2px 8px rgba(21,101,192,0.4);
}

.stButton > button:hover {
    background: linear-gradient(135deg, #1976d2, #1e88e5);
    box-shadow: 0 4px 16px rgba(21,101,192,0.6);
    transform: translateY(-1px);
}

/* ---------- text inputs ---------- */
.stTextArea textarea, .stTextInput input {
    background: #1a1f2e !important;
    border: 1px solid #2a2f3e !important;
    border-radius: 10px !important;
    color: #e8eaf0 !important;
    font-family: 'Cairo', sans-serif !important;
    direction: rtl;
}

.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #1976d2 !important;
    box-shadow: 0 0 0 2px rgba(25,118,210,0.2) !important;
}

/* ---------- answer box ---------- */
.answer-box {
    background: #131929;
    border: 1px solid #1a237e;
    border-right: 4px solid #2979ff;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-top: 1rem;
    font-size: 1.05rem;
    line-height: 1.9;
    color: #e8eaf0;
}

.answer-label {
    font-size: 0.8rem;
    font-weight: 700;
    color: #2979ff;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
}

/* ---------- source chips ---------- */
.source-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    background: #1e3a5f;
    border-radius: 20px;
    padding: 0.25rem 0.8rem;
    font-size: 0.82rem;
    color: #90caf9;
    margin: 0.2rem;
    border: 1px solid #2979ff44;
}

/* ---------- flashcard ---------- */
.flashcard {
    background: linear-gradient(145deg, #1a1f2e, #161b27);
    border: 1px solid #2a2f3e;
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.8rem;
    transition: all 0.2s;
    border-right: 3px solid #1565c0;
}

.flashcard:hover {
    border-color: #1976d2;
    box-shadow: 0 4px 20px rgba(25,118,210,0.15);
    transform: translateY(-2px);
}

.flashcard-q {
    font-weight: 700;
    color: #90caf9;
    font-size: 1rem;
    margin-bottom: 0.6rem;
}

.flashcard-a {
    color: #cdd6f4;
    font-size: 0.95rem;
    line-height: 1.7;
    border-top: 1px solid #2a2f3e;
    padding-top: 0.6rem;
    margin-top: 0.4rem;
}

/* ---------- MCQ card ---------- */
.mcq-card {
    background: #1a1f2e;
    border: 1px solid #2a2f3e;
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
}

.mcq-question {
    font-weight: 700;
    color: #e8eaf0;
    margin-bottom: 0.8rem;
    font-size: 1rem;
}

.mcq-option {
    padding: 0.45rem 0.9rem;
    border-radius: 8px;
    margin-bottom: 0.4rem;
    font-size: 0.93rem;
    color: #8892b0;
    background: #161b27;
    border: 1px solid #2a2f3e;
}

.mcq-option.correct {
    background: #0d2e1a;
    border-color: #2e7d32;
    color: #a5d6a7;
    font-weight: 600;
}

/* ---------- TF card ---------- */
.tf-card {
    background: #1a1f2e;
    border: 1px solid #2a2f3e;
    border-radius: 14px;
    padding: 1rem 1.5rem;
    margin-bottom: 0.8rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
}

.tf-question { color: #cdd6f4; font-size: 0.97rem; flex: 1; }

.tf-badge {
    border-radius: 20px;
    padding: 0.3rem 0.9rem;
    font-size: 0.85rem;
    font-weight: 700;
    white-space: nowrap;
}

.tf-true  { background: #0d2e1a; color: #81c784; border: 1px solid #388e3c; }
.tf-false { background: #2e0d0d; color: #ef9a9a; border: 1px solid #c62828; }

/* ---------- summary ---------- */
.summary-box {
    background: #131929;
    border: 1px solid #2a2f3e;
    border-radius: 14px;
    padding: 1.5rem;
    font-size: 1rem;
    line-height: 2;
    color: #cdd6f4;
}

/* ---------- upload zone ---------- */
.stFileUploader {
    background: #1a1f2e !important;
    border: 2px dashed #2a2f3e !important;
    border-radius: 12px !important;
}

/* ---------- selectbox ---------- */
.stSelectbox > div > div {
    background: #1a1f2e !important;
    border: 1px solid #2a2f3e !important;
    border-radius: 10px !important;
    color: #e8eaf0 !important;
}

/* ---------- radio ---------- */
.stRadio label { color: #8892b0 !important; }

/* ---------- expander ---------- */
.streamlit-expanderHeader {
    background: #1a1f2e !important;
    border-radius: 10px !important;
    color: #cdd6f4 !important;
}

/* ---------- metric cards ---------- */
.metric-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.metric-card {
    flex: 1;
    background: #161b27;
    border: 1px solid #2a2f3e;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    text-align: center;
}

.metric-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: #2979ff;
}

.metric-label {
    font-size: 0.82rem;
    color: #8892b0;
    margin-top: 0.2rem;
}

/* ---------- divider ---------- */
hr { border-color: #2a2f3e !important; }

/* ---------- spinner ---------- */
.stSpinner > div { border-top-color: #1976d2 !important; }

/* scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0f1117; }
::-webkit-scrollbar-thumb { background: #2a2f3e; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────

if "doc_id"   not in st.session_state: st.session_state.doc_id   = None
if "filename" not in st.session_state: st.session_state.filename = None
if "qa_history" not in st.session_state: st.session_state.qa_history = []

# ── Helpers ───────────────────────────────────────────────────────────────────

def fetch_documents():
    try:
        r = requests.get(f"{API_BASE}/documents", timeout=10)
        return r.json().get("documents", []) if r.status_code == 200 else []
    except Exception:
        return []

# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 0.5rem 0 1rem;">
        <div style="font-size:2.5rem;">🎓</div>
        <div style="font-size:1.2rem; font-weight:700; color:#e8eaf0;">مساعد الطالب الذكي</div>
        <div style="font-size:0.8rem; color:#8892b0; margin-top:0.2rem;">AI Study Assistant</div>
    </div>
    <hr style="border-color:#2a2f3e; margin-bottom:1.2rem;">
    """, unsafe_allow_html=True)

    # Upload section
    st.markdown('<div style="font-size:0.85rem; font-weight:700; color:#8892b0; margin-bottom:0.5rem;">📁 رفع ملف دراسي</div>', unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "اختر ملف PDF أو PPTX أو DOCX",
        type=["pdf", "pptx", "docx"],
        label_visibility="collapsed",
    )

    if uploaded:
        st.markdown(f'<div style="font-size:0.85rem; color:#90caf9; margin:0.4rem 0;">📄 {uploaded.name}</div>', unsafe_allow_html=True)
        if st.button("⬆️  رفع وتحليل"):
            with st.spinner("جاري المعالجة..."):
                try:
                    resp = requests.post(
                        f"{API_BASE}/upload",
                        files={"file": (uploaded.name, uploaded.getvalue(), uploaded.type)},
                        timeout=120,
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        if data["status"] == "skipped":
                            st.info(data["message"])
                        else:
                            st.success(f"✅ تم الرفع — {data['chunks_added']} جزء")
                            st.session_state.doc_id   = data["doc_id"]
                            st.session_state.filename = data["filename"]
                        for w in data.get("warnings", []):
                            st.warning(w)
                    else:
                        st.error(f"خطأ: {resp.text}")
                except Exception as e:
                    st.error(f"تعذّر الاتصال بالخادم: {e}")

    st.markdown("<hr style='border-color:#2a2f3e; margin:1rem 0;'>", unsafe_allow_html=True)

    # Document selector
    st.markdown('<div style="font-size:0.85rem; font-weight:700; color:#8892b0; margin-bottom:0.5rem;">📚 الملفات المتاحة</div>', unsafe_allow_html=True)
    docs = fetch_documents()
    if docs:
        names = [d["filename"] for d in docs]
        selected_name = st.selectbox("اختر ملفًا", options=names, label_visibility="collapsed")
        selected_doc  = next(d for d in docs if d["filename"] == selected_name)
        if selected_doc["doc_id"] != st.session_state.doc_id:
            st.session_state.doc_id   = selected_doc["doc_id"]
            st.session_state.filename = selected_doc["filename"]
            st.session_state.qa_history = []
    else:
        st.markdown('<div style="font-size:0.85rem; color:#8892b0; text-align:center; padding:0.5rem;">لا توجد ملفات بعد</div>', unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#2a2f3e; margin:1rem 0;'>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.75rem; color:#4a5568; text-align:center;">Powered by GPT-4o mini + ChromaDB</div>', unsafe_allow_html=True)

# ── Main area ─────────────────────────────────────────────────────────────────

# Hero header
st.markdown(f"""
<div class="hero">
    <div class="hero-icon">🎓</div>
    <div>
        <p class="hero-title">مساعد الطالب الذكي</p>
        <p class="hero-sub">افهم مادتك أسرع — اسأل، لخّص، احفظ، واختبر نفسك</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Active document badge
if st.session_state.filename:
    st.markdown(f'<div class="doc-badge">📄 <strong>{st.session_state.filename}</strong></div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="doc-badge" style="border-color:#2a2f3e; color:#4a5568;">← اختر ملفًا من الشريط الجانبي</div>', unsafe_allow_html=True)

# ── Tabs ───────────────────────────────────────────────────────────────────────

tab_qa, tab_summary, tab_flash, tab_exam = st.tabs([
    "💬  سؤال وجواب",
    "📝  ملخص",
    "🃏  بطاقات تعليمية",
    "📋  أسئلة اختبار",
])

# ════════════════════════════════════════════
#  Q&A
# ════════════════════════════════════════════

with tab_qa:
    # Chat history
    for item in st.session_state.qa_history:
        st.markdown(f"""
        <div style="background:#1a1f2e; border-radius:12px; padding:0.8rem 1.2rem; margin-bottom:0.5rem; border:1px solid #2a2f3e;">
            <div style="font-size:0.8rem; color:#8892b0; margin-bottom:0.3rem;">🧑‍🎓 السؤال</div>
            <div style="color:#cdd6f4;">{item['q']}</div>
        </div>
        <div class="answer-box">
            <div class="answer-label">🤖 الإجابة</div>
            {item['a']}
        </div>
        """, unsafe_allow_html=True)

        if item.get("sources"):
            chips = "".join(
                f'<span class="source-chip">📄 {s["filename"]} — ص {s["page_num"]} ({s["score"]:.0%})</span>'
                for s in item["sources"]
            )
            st.markdown(f'<div style="margin: 0.5rem 0 1.2rem;">{chips}</div>', unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)

    # Input
    question = st.text_area(
        "سؤالك",
        height=100,
        placeholder="مثال: ما هي الفكرة الرئيسية في الفصل الثالث؟",
        label_visibility="collapsed",
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        ask_btn = st.button("💬  أجب على السؤال", key="btn_qa", use_container_width=True)
    with col2:
        if st.button("🗑️  مسح", key="btn_clear", use_container_width=True):
            st.session_state.qa_history = []
            st.rerun()

    if ask_btn:
        if not question.strip():
            st.warning("اكتب سؤالًا أولًا.")
        elif not st.session_state.doc_id:
            st.warning("اختر ملفًا من الشريط الجانبي أولًا.")
        else:
            with st.spinner("جاري البحث عن الإجابة..."):
                try:
                    resp = requests.post(
                        f"{API_BASE}/ask",
                        json={"question": question, "doc_id": st.session_state.doc_id},
                        timeout=60,
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        st.session_state.qa_history.append({
                            "q": question,
                            "a": data["answer"],
                            "sources": data.get("sources", []),
                        })
                        st.rerun()
                    else:
                        st.error(f"خطأ: {resp.text}")
                except requests.exceptions.Timeout:
                    st.error("انتهت مهلة الاتصال — الخادم بطيء الاستجابة. حاول مجددًا.")
                except Exception as e:
                    st.error(f"خطأ في الاتصال: {e}")

# ════════════════════════════════════════════
#  Summary
# ════════════════════════════════════════════

with tab_summary:
    col_l, col_r = st.columns([2, 1])
    with col_r:
        lang = st.radio(
            "اللغة",
            options=["ar", "en"],
            format_func=lambda x: "🇸🇦 عربي" if x == "ar" else "🇺🇸 English",
            horizontal=True,
        )
    with col_l:
        gen_sum = st.button("📝  توليد الملخص", key="btn_summary", use_container_width=True)

    if gen_sum:
        if not st.session_state.doc_id:
            st.warning("اختر ملفًا أولًا.")
        else:
            with st.spinner("جاري تلخيص المحتوى..."):
                try:
                    resp = requests.post(
                        f"{API_BASE}/summarize",
                        json={"doc_id": st.session_state.doc_id, "language": lang},
                        timeout=90,
                    )
                    if resp.status_code == 200:
                        summary = resp.json()["summary"]
                        st.markdown(f'<div class="summary-box">{summary}</div>', unsafe_allow_html=True)
                    else:
                        st.error(f"خطأ: {resp.text}")
                except requests.exceptions.Timeout:
                    st.error("انتهت مهلة الاتصال. حاول مجددًا.")
                except Exception as e:
                    st.error(f"خطأ: {e}")

# ════════════════════════════════════════════
#  Flashcards
# ════════════════════════════════════════════

with tab_flash:
    gen_flash = st.button("🃏  توليد البطاقات التعليمية", key="btn_flash", use_container_width=True)

    if gen_flash:
        if not st.session_state.doc_id:
            st.warning("اختر ملفًا أولًا.")
        else:
            with st.spinner("جاري إنشاء البطاقات..."):
                try:
                    resp = requests.post(
                        f"{API_BASE}/flashcards",
                        json={"doc_id": st.session_state.doc_id},
                        timeout=90,
                    )
                    if resp.status_code == 200:
                        cards = resp.json()["cards"]
                        st.markdown(f"""
                        <div class="metric-row">
                            <div class="metric-card">
                                <div class="metric-value">{len(cards)}</div>
                                <div class="metric-label">بطاقة تعليمية</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        for i, card in enumerate(cards, start=1):
                            st.markdown(f"""
                            <div class="flashcard">
                                <div class="flashcard-q">❓ {i}. {card.get('q', '')}</div>
                                <div class="flashcard-a">✅ {card.get('a', '')}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.error(f"خطأ: {resp.text}")
                except requests.exceptions.Timeout:
                    st.error("انتهت مهلة الاتصال. حاول مجددًا.")
                except Exception as e:
                    st.error(f"خطأ: {e}")

# ════════════════════════════════════════════
#  Exam Questions
# ════════════════════════════════════════════

with tab_exam:
    gen_exam = st.button("📋  توليد أسئلة الاختبار", key="btn_exam", use_container_width=True)

    if gen_exam:
        if not st.session_state.doc_id:
            st.warning("اختر ملفًا أولًا.")
        else:
            with st.spinner("جاري إنشاء أسئلة الاختبار..."):
                try:
                    resp = requests.post(
                        f"{API_BASE}/exam-questions",
                        json={"doc_id": st.session_state.doc_id},
                        timeout=90,
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        mcqs = data.get("mcq", [])
                        tfs  = data.get("true_false", [])

                        # metrics
                        st.markdown(f"""
                        <div class="metric-row">
                            <div class="metric-card">
                                <div class="metric-value">{len(mcqs)}</div>
                                <div class="metric-label">اختيار متعدد</div>
                            </div>
                            <div class="metric-card">
                                <div class="metric-value">{len(tfs)}</div>
                                <div class="metric-label">صح / خطأ</div>
                            </div>
                            <div class="metric-card">
                                <div class="metric-value">{len(mcqs) + len(tfs)}</div>
                                <div class="metric-label">إجمالي الأسئلة</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        # MCQ
                        if mcqs:
                            st.markdown('<div style="font-size:1rem; font-weight:700; color:#e8eaf0; margin:1rem 0 0.8rem;">📌 أسئلة الاختيار من متعدد</div>', unsafe_allow_html=True)
                            for i, q in enumerate(mcqs, start=1):
                                opts_html = ""
                                for j, opt in enumerate(q.get("options", [])):
                                    cls = "mcq-option correct" if j == q.get("correct_index", -1) else "mcq-option"
                                    mark = "✅ " if j == q.get("correct_index", -1) else f"{['أ','ب','ج','د'][j] if j < 4 else str(j+1)}. "
                                    opts_html += f'<div class="{cls}">{mark}{opt}</div>'
                                st.markdown(f"""
                                <div class="mcq-card">
                                    <div class="mcq-question">{i}. {q.get('question','')}</div>
                                    {opts_html}
                                </div>
                                """, unsafe_allow_html=True)

                        # True/False
                        if tfs:
                            st.markdown('<div style="font-size:1rem; font-weight:700; color:#e8eaf0; margin:1.5rem 0 0.8rem;">✔️ أسئلة صح / خطأ</div>', unsafe_allow_html=True)
                            for i, q in enumerate(tfs, start=1):
                                ans     = q.get("answer", False)
                                badge_cls = "tf-badge tf-true" if ans else "tf-badge tf-false"
                                label   = "✅ صح" if ans else "❌ خطأ"
                                st.markdown(f"""
                                <div class="tf-card">
                                    <div class="tf-question">{i}. {q.get('question','')}</div>
                                    <div class="{badge_cls}">{label}</div>
                                </div>
                                """, unsafe_allow_html=True)
                    else:
                        st.error(f"خطأ: {resp.text}")
                except requests.exceptions.Timeout:
                    st.error("انتهت مهلة الاتصال. حاول مجددًا.")
                except Exception as e:
                    st.error(f"خطأ: {e}")
