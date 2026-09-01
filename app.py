import random
import io
import streamlit as st
from fpdf import FPDF

st.set_page_config(
    page_title="Nauka dodawania i odejmowania",
    page_icon="➕➖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .main-header {
        font-size: 1.8rem;
        text-align: center;
        color: #FF6B6B;
        margin-bottom: 10px;
    }
    .score-box {
        background-color: #4ECDC4;
        padding: 8px;
        border-radius: 10px;
        text-align: center;
        margin: 10px 0;
        color: white;
        font-size: 1rem;
    }
    .question-box {
        background-color: #FFE66D;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 15px 0;
        font-size: 2rem;
        color: #2C3E50;
        border: 3px solid #FF6B6B;
    }
    .result-good {
        font-size: 1.2rem;
        color: #06D6A0;
        text-align: center;
        padding: 10px;
    }
    .result-bad {
        font-size: 1.2rem;
        color: #EF476F;
        text-align: center;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

OP_ADD = "➕ Dodawanie"
OP_SUB = "➖ Odejmowanie"
OP_MUL = "✖️ Mnożenie"
OP_DIV = "➗ Dzielenie"
ALL_OPS = [OP_ADD, OP_SUB, OP_MUL, OP_DIV]
OP_EMOJI = {"+": "➕", "-": "➖", "×": "✖️", "÷": "➗"}

for key, default in {
    "score": 0,
    "total": 0,
    "current_answer": None,
    "show_result": False,
    "is_correct": False,
    "pdf_bytes": None,
    "pdf_filename": None,
    "new_question": True,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


def remove_polish_chars(text):
    """Usuwa polskie znaki i zamienia na ASCII"""
    replacements = {
        "ą": "a", "ć": "c", "ę": "e", "ł": "l", "ń": "n",
        "ó": "o", "ś": "s", "ź": "z", "ż": "z",
        "Ą": "A", "Ć": "C", "Ę": "E", "Ł": "L", "Ń": "N",
        "Ó": "O", "Ś": "S", "Ź": "Z", "Ż": "Z"
    }
    for polish, ascii_char in replacements.items():
        text = text.replace(polish, ascii_char)
    return text


def generate_operation(op_type, max_num):
    """Losuje zadanie z liczbami od 0 do max_num."""
    n = max(0, int(max_num))

    if op_type == OP_ADD:
        a = random.randint(0, n)
        b = random.randint(0, n - a)
        return a, b, "+"

    if op_type == OP_SUB:
        a = random.randint(0, n)
        b = random.randint(0, a)
        return a, b, "-"

    if op_type == OP_MUL:
        hi = min(12, n)
        a = random.randint(0, hi)
        b = random.randint(0, hi)
        return a, b, "×"

    if n == 0:
        return 0, 1, "÷"
    b = random.randint(1, min(12, n))
    max_result = min(12, n // b)
    result = random.randint(0, max_result)
    a = b * result
    return a, b, "÷"


def answer_for(a, b, operation):
    if operation == "+":
        return a + b
    if operation == "-":
        return a - b
    if operation == "×":
        return a * b
    return a // b if b else 0


def make_question(max_num, operations):
    ops = operations or [OP_ADD]
    a, b, operation = generate_operation(random.choice(ops), max_num)
    st.session_state.a = a
    st.session_state.b = b
    st.session_state.operation = operation
    st.session_state.current_answer = answer_for(a, b, operation)
    st.session_state.show_result = False
    st.session_state.new_question = False


def generate_pdf(operations, max_num):
    """Generuje PDF z 40 zadaniami na jednej stronie"""
    pdf = FPDF(orientation="L")
    questions = []
    ops = operations or [OP_ADD]
    for _ in range(40):
        questions.append(generate_operation(random.choice(ops), max_num))

    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    title = remove_polish_chars("Zadania Matematyczne - 40 zadan")
    pdf.cell(0, 15, title, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)

    pdf.set_font("Helvetica", size=11)
    for i in range(40):
        a, b, op = questions[i]
        x = 8 + (i % 8) * 35
        y = 35 + (i // 8) * 28
        pdf.set_xy(x, y)
        pdf.cell(34, 10, f"{a} {op} {b} = _____")

    return pdf


def pdf_to_bytes(pdf):
    output = pdf.output()
    if isinstance(output, str):
        return output.encode("latin-1")
    return bytes(output)


def go_next():
    st.session_state.new_question = True
    st.session_state.show_result = False
    st.session_state.answer_text = ""


def go_new_game():
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.new_question = True
    st.session_state.show_result = False
    st.session_state.is_correct = False


st.markdown(
    '<h1 class="main-header">➕➖ Matematyka dla Pierwszaków ➖➕</h1>',
    unsafe_allow_html=True
)
score_placeholder = st.empty()

col1, col2 = st.columns(2)
with col1:
    max_number = st.slider(
        "Maksymalna liczba",
        min_value=0,
        max_value=100,
        value=50,
        step=1
    )
with col2:
    operations = st.multiselect(
        "Wybierz działania:",
        ALL_OPS,
        default=[OP_ADD, OP_SUB]
    )

if st.button("📄 Generuj PDF z zadaniami (40 zadań, 1 strona)", type="secondary"):
    if not operations:
        st.warning("Wybierz przynajmniej jedno działanie!")
    else:
        pdf_bytes = pdf_to_bytes(generate_pdf(operations, max_number))
        ops_str = "_".join([op.split()[1].lower() for op in operations])
        st.session_state.pdf_bytes = pdf_bytes
        st.session_state.pdf_filename = f"zadania_{ops_str}_{max_number}.pdf"
        st.success("✅ PDF wygenerowany! Kliknij przycisk 'Pobierz PDF' aby go pobrać.")

if st.session_state.pdf_bytes:
    st.download_button(
        label="📥 Pobierz PDF",
        data=st.session_state.pdf_bytes,
        file_name=st.session_state.pdf_filename,
        mime="application/pdf",
        key="download_pdf"
    )

st.markdown("---")

settings_key = (max_number, tuple(operations) if operations else (OP_ADD,))
if st.session_state.get("last_settings") != settings_key:
    st.session_state.last_settings = settings_key
    st.session_state.new_question = True

if st.session_state.new_question or "a" not in st.session_state:
    make_question(max_number, operations)

emoji = OP_EMOJI.get(st.session_state.operation, "➕")
st.markdown(f'''
    <div class="question-box">
        {st.session_state.a} {emoji} {st.session_state.b} = ?
    </div>
''', unsafe_allow_html=True)

with st.form("answer_form", clear_on_submit=True):
    raw_answer = st.text_input(
        "Twoja odpowiedź:",
        placeholder="Wpisz liczbę",
        key="answer_text"
    )
    check_button = st.form_submit_button(
        "✅ Sprawdź",
        use_container_width=True,
        type="primary"
    )

btn_col1, btn_col2 = st.columns(2)
with btn_col1:
    st.button("➡️ Następne", use_container_width=True, on_click=go_next)
with btn_col2:
    st.button("🔄 Nowa gra", use_container_width=True, on_click=go_new_game)

if check_button and not st.session_state.show_result:
    raw = (raw_answer or "").strip()
    if raw == "" or not raw.isdigit():
        st.warning("Wpisz liczbę całkowitą (0, 1, 2, …).")
    else:
        st.session_state.total += 1
        st.session_state.show_result = True
        if int(raw) == st.session_state.current_answer:
            st.session_state.score += 1
            st.session_state.is_correct = True
            st.balloons()
        else:
            st.session_state.is_correct = False

score_placeholder.markdown(f'''
    <div class="score-box">
        <strong>Wynik: {st.session_state.score} / {st.session_state.total}</strong>
    </div>
''', unsafe_allow_html=True)

if st.session_state.show_result:
    st.markdown("---")
    if st.session_state.is_correct:
        st.markdown(
            '<div class="result-good">🎉 Świetnie! Odpowiedź poprawna! 🎉</div>',
            unsafe_allow_html=True
        )
    else:
        correct_response = (
            f"{st.session_state.a} {st.session_state.operation} "
            f"{st.session_state.b} = {st.session_state.current_answer}"
        )
        st.markdown(f'''
            <div class="result-bad">
                Nie tym razem. Poprawna odpowiedź to: {correct_response}
            </div>
        ''', unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #7F8C8D; padding: 20px;">
        <p>💡 Świetna robota! Ćwicz codziennie, a będziesz mistrzem matematyki!</p>
    </div>
""", unsafe_allow_html=True)
