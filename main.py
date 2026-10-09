import operator
from datetime import datetime

import streamlit as st


st.set_page_config(
    page_title="Calcular",
    page_icon="+",
    layout="centered",
    initial_sidebar_state="collapsed",
)


OPERATIONS = {
    "+": operator.add,
    "-": operator.sub,
    "x": operator.mul,
    "/": operator.truediv,
}


def reset_calculator() -> None:
    st.session_state.display = "0"
    st.session_state.stored_value = None
    st.session_state.pending_operator = None
    st.session_state.waiting_for_operand = False


def calculate_pending() -> None:
    stored_value = st.session_state.stored_value
    pending_operator = st.session_state.pending_operator
    if stored_value is None or pending_operator is None:
        return

    current_value = float(st.session_state.display)
    if pending_operator == "/" and current_value == 0:
        st.session_state.display = "Error"
    else:
        result = OPERATIONS[pending_operator](stored_value, current_value)
        st.session_state.display = format_number(result)
    st.session_state.stored_value = None
    st.session_state.pending_operator = None
    st.session_state.waiting_for_operand = True


def format_number(value: float) -> str:
    if value.is_integer():
        return str(int(value))
    return f"{value:.10g}"


def enter_digit(digit: str) -> None:
    if st.session_state.display == "Error" or st.session_state.waiting_for_operand:
        st.session_state.display = digit
        st.session_state.waiting_for_operand = False
    elif st.session_state.display == "0":
        st.session_state.display = digit
    else:
        st.session_state.display += digit


def enter_decimal() -> None:
    if st.session_state.display == "Error" or st.session_state.waiting_for_operand:
        st.session_state.display = "0."
        st.session_state.waiting_for_operand = False
    elif "." not in st.session_state.display:
        st.session_state.display += "."


def choose_operator(symbol: str) -> None:
    if st.session_state.display == "Error":
        reset_calculator()
        return

    if st.session_state.stored_value is not None and not st.session_state.waiting_for_operand:
        calculate_pending()

    st.session_state.stored_value = float(st.session_state.display)
    st.session_state.pending_operator = symbol
    st.session_state.waiting_for_operand = True


def handle_equals() -> None:
    expression = build_expression()
    calculate_pending()
    if st.session_state.display != "Error":
        st.session_state.history.insert(
            0,
            {
                "expression": expression,
                "result": st.session_state.display,
                "time": datetime.now().strftime("%H:%M"),
            },
        )
        st.session_state.history = st.session_state.history[:6]


def build_expression() -> str:
    stored_value = st.session_state.stored_value
    pending_operator = st.session_state.pending_operator
    if stored_value is None or pending_operator is None:
        return st.session_state.display
    return f"{format_number(stored_value)} {pending_operator} {st.session_state.display}"


if "display" not in st.session_state:
    reset_calculator()
if "history" not in st.session_state:
    st.session_state.history = []


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@500;600;700;800&display=swap');

    :root {
        --ink: #18211f;
        --muted: #697773;
        --paper: #f4f1e9;
        --panel: #fffdf8;
        --line: #dfe3d9;
        --accent: #df5a3d;
        --accent-dark: #b84028;
        --teal: #1e7771;
    }

    .stApp {
        background: radial-gradient(circle at 15% 0%, #e8eee1 0, transparent 34%),
                    radial-gradient(circle at 100% 100%, #f2d9ca 0, transparent 30%), var(--paper);
        color: var(--ink);
        font-family: 'Manrope', sans-serif;
    }

    .block-container { max-width: 760px; padding: 5rem 1.2rem 3rem; }
    h1, h2, h3, p { font-family: 'Manrope', sans-serif; }
    h1 { font-size: clamp(2.7rem, 8vw, 5.2rem); letter-spacing: 0; line-height: .95; margin-bottom: .6rem; }
    .intro { color: var(--muted); font-size: 1rem; margin-bottom: 2rem; }
    .display-label { color: var(--teal); font-size: .72rem; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; }
    .display-value {
        background: var(--panel); border: 1px solid var(--line); border-radius: 10px;
        box-shadow: 0 14px 30px rgba(41, 51, 42, .08); color: var(--ink);
        font-family: 'DM Mono', monospace; font-size: clamp(2.3rem, 8vw, 4.5rem); font-weight: 500;
        margin: .5rem 0 1.5rem; min-height: 7.2rem; overflow: hidden; padding: 1rem 1.2rem;
        text-align: right; text-overflow: ellipsis; white-space: nowrap;
    }
    .stButton > button { border: 1px solid var(--line); border-radius: 8px; color: var(--ink); font-size: 1.1rem; font-weight: 700; min-height: 3.8rem; }
    .stButton > button:hover { border-color: var(--teal); color: var(--teal); }
    div[data-testid='column']:last-child .stButton > button,
    div[data-testid='column']:nth-child(4) .stButton > button { background: var(--accent); border-color: var(--accent); color: white; }
    div[data-testid='column']:last-child .stButton > button:hover,
    div[data-testid='column']:nth-child(4) .stButton > button:hover { background: var(--accent-dark); color: white; }
    .history-title { border-bottom: 1px solid var(--line); color: var(--muted); font-size: .75rem; font-weight: 800; letter-spacing: .12em; margin-top: 2rem; padding-bottom: .7rem; text-transform: uppercase; }
    .history-row { align-items: center; border-bottom: 1px solid var(--line); display: flex; justify-content: space-between; padding: .75rem 0; }
    .history-expression { color: var(--muted); font-family: 'DM Mono', monospace; font-size: .85rem; }
    .history-result { color: var(--ink); font-family: 'DM Mono', monospace; font-weight: 500; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Calcular")
st.markdown('<p class="intro">A small, calm space for getting the numbers right.</p>', unsafe_allow_html=True)
st.markdown('<div class="display-label">Current value</div>', unsafe_allow_html=True)
st.markdown(f'<div class="display-value">{st.session_state.display}</div>', unsafe_allow_html=True)

rows = [
    [("AC", "clear"), ("+/-", "sign"), ("%", "percent"), ("/", "operator")],
    [("7", "digit"), ("8", "digit"), ("9", "digit"), ("x", "operator")],
    [("4", "digit"), ("5", "digit"), ("6", "digit"), ("-", "operator")],
    [("1", "digit"), ("2", "digit"), ("3", "digit"), ("+", "operator")],
    [("0", "digit"), (".", "decimal"), ("=", "equals")],
]

for row_index, row in enumerate(rows):
    columns = st.columns(len(row))
    for column, (label, action) in zip(columns, row):
        with column:
            if st.button(label, key=f"key_{row_index}_{label}", use_container_width=True):
                if action == "clear":
                    reset_calculator()
                elif action == "digit":
                    enter_digit(label)
                elif action == "decimal":
                    enter_decimal()
                elif action == "operator":
                    choose_operator(label)
                elif action == "equals":
                    handle_equals()
                elif action == "sign" and st.session_state.display != "0":
                    st.session_state.display = str(-float(st.session_state.display))
                elif action == "percent":
                    st.session_state.display = format_number(float(st.session_state.display) / 100)
                st.rerun()

if st.session_state.history:
    st.markdown('<div class="history-title">Recent calculations</div>', unsafe_allow_html=True)
    for item in st.session_state.history:
        st.markdown(
            f'<div class="history-row"><span class="history-expression">{item["expression"]}</span>'
            f'<span class="history-result">= {item["result"]} <small>{item["time"]}</small></span></div>',
            unsafe_allow_html=True,
        )
