import html
import json
from datetime import datetime

import streamlit as st


st.set_page_config(page_title="십삼지신 | 수학 탐구 활동지", page_icon="🐭", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Gowun+Dodum&display=swap');
    :root {
      --ink: #20383a; --muted: #617476; --teal: #285c62; --teal-dark: #20474c;
      --coral: #d8755e; --yellow: #e3b94f; --paper: #f4f7f4; --line: #dce5df;
    }
    html, body, [class*="css"] { font-family: 'DM Sans', 'Gowun Dodum', sans-serif; color: var(--ink); }
    .stApp { background: #f4f7f4; }
    [data-testid="stHeader"] { background: rgba(244,247,244,.92); }
    [data-testid="stMainBlockContainer"] { max-width: 1120px; padding-top: 1rem; }
    .brandline { display:flex; align-items:center; gap:12px; color:var(--teal-dark); font-weight:700; padding:4px 0 20px; }
    .brandmark { display:grid; place-items:center; width:38px; height:38px; background:var(--teal); color:#fff; border-radius:12px; font-size:17px; }
    .brandline small { display:block; font-size:11px; font-weight:500; color:var(--muted); }
    .hero { display:grid; grid-template-columns:1.35fr .65fr; gap:24px; align-items:center; background:#e5efeb; border-top:4px solid var(--teal); padding:34px 38px; margin-bottom:20px; }
    .eyebrow { color:var(--coral); font:700 11px 'DM Sans',sans-serif; letter-spacing:1.6px; margin:0 0 10px; }
    .hero h1 { font:400 42px 'Gowun Dodum',sans-serif; line-height:1.3; margin:0; color:#20383a; }
    .hero h1 span { color:var(--teal); font-weight:700; }
    .hero p { color:#52696a; line-height:1.8; margin:12px 0 0; }
    .hero-art { display:flex; justify-content:center; align-items:center; gap:8px; min-height:150px; }
    .hero-art img { width:78px; max-height:118px; object-fit:contain; filter:drop-shadow(0 8px 8px #31555022); }
    .hero-art img:nth-child(2) { transform:translateY(-12px) rotate(7deg); }
    .hero-art img:nth-child(3) { transform:translateY(8px) rotate(-7deg); }
    .student-box { background:#fff; border:1px solid var(--line); padding:16px 20px; margin-bottom:20px; }
    .student-title { color:var(--muted); font-size:12px; font-weight:600; padding:0 0 6px; }
    .progress-label { display:flex; justify-content:space-between; font-size:12px; color:var(--muted); }
    .progress-label strong { color:var(--teal-dark); }
    .status-note { font-size:11px; color:var(--muted); margin-top:4px; }
    .section-kicker { color:var(--coral); font-size:11px; font-weight:700; letter-spacing:1.3px; margin:5px 0 4px; }
    .section-intro { color:var(--muted); margin:0 0 22px; }
    .question-box { border-top:1px solid var(--line); padding:20px 0 14px; }
    .question-title { font-weight:700; margin-bottom:8px; }
    .q-number { display:inline-grid; place-items:center; width:26px; height:26px; border-radius:50%; background:#e5efeb; color:var(--teal); margin-right:8px; font-size:12px; }
    .hint { background:#edf3ee; border-left:3px solid var(--yellow); padding:12px 15px; color:#506565; font-size:13px; margin:16px 0; }
    .card-back { width:108px; aspect-ratio:2/3; border-radius:8px; display:flex; flex-direction:column; justify-content:center; align-items:center; color:white; box-shadow:0 4px 12px #20383a22; margin:0 auto 8px; }
    .card-back strong { font-size:19px; }
    .card-back small { margin-top:5px; opacity:.8; font-size:10px; }
    .card-red { background:#c86859; } .card-yellow { background:#d5a936; } .card-blue { background:#56889a; }
    .subsection { border-top:2px solid var(--teal); margin-top:26px; padding-top:16px; }
    .notice { background:#fff8df; border:1px solid #f0dfab; padding:14px 16px; color:#62552e; font-size:13px; }
    .footer { text-align:center; color:var(--muted); font-family:'Gowun Dodum',sans-serif; padding:30px 0 12px; }
    .footer span { color:var(--coral); }
    div[data-testid="stTabs"] button[role="tab"] { font-weight:600; }
    div[data-testid="stTabs"] button[aria-selected="true"] { color:var(--teal); }
    .stButton button[kind="primary"] { background:var(--teal); border-color:var(--teal); }
    .stButton button { border-radius:5px; }
    @media (max-width:700px) {
      .hero { grid-template-columns:1fr; padding:24px 20px; gap:8px; }
            .hero h1 { font-size:32px; }
      .hero-art { min-height:100px; justify-content:flex-start; }
      .hero-art img { width:58px; max-height:88px; }
      [data-testid="stMainBlockContainer"] { padding-left:1rem; padding-right:1rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


BASE_URL = "https://sipsamjisin-jinam-worksheet.fairy-pine-2708.chatgpt.site"
ANIMALS = ["쥐", "소", "호랑이", "토끼", "용", "뱀", "말", "양", "원숭이", "닭", "개", "돼지"]
NUMBERS = [str(number) for number in range(1, 13)]
CARDS = NUMBERS + ["odd", "even"]
COLORS = {
    "빨간색": [1, 4, 7, 10],
    "노란색": [2, 5, 8, 11],
    "파란색": [3, 6, 9, 12],
}
COLOR_CLASS = {"빨간색": "card-red", "노란색": "card-yellow", "파란색": "card-blue"}
SCHEMA = "sipsamjisin-worksheet-v1"

TEXT_FIELDS = {
    "a1_info_1": "카드 앞면 정보 1",
    "a1_info_2": "카드 앞면 정보 2",
    "a1_info_3": "카드 앞면 정보 3",
    "a1_info_4": "카드 앞면 정보 4",
    "a1_same": "같은 의미를 나타내는 두 가지 정보",
    "a1_back": "카드 뒷면에 담긴 정보",
    "a1_color": "수와 색깔 사이의 관계",
    "a2_rule_1": "카드의 어느 면이 보이도록 내려놓나요?",
    "a2_rule_2": "누가 나머지 플레이어와 대결하나요?",
    "a2_rule_3": "어떤 수 카드가 승리하나요?",
    "a2_rule_4": "두 수의 합이 얼마이면 큰 수가 승리하나요?",
    "a2_rule_5": "무승부인 경우 말을 몇 칸 전진하나요?",
    "a3_good": "카드를 유리하게 냈던 상황과 이유",
    "a3_bad": "카드를 불리하게 냈던 상황과 다시 선택한다면",
    "a3_blue_reason": "파란색 카드를 반드시 이길 카드와 이유",
    "a3_cat": "고양이 카드를 사용하면 유리한 상황",
    "a3_red_reason": "남은 카드로 빨간색 카드를 이길 방법과 이유",
    "a3_deduction": "합이 13이 되는 색깔 관계를 연역적으로 설명하기",
    "a3_finish": "십삼지신 게임의 결승점이 13인 이유",
}
WIN_KEYS = [f"wins_{card}" for card in CARDS]
SUM_KEYS = [f"a3_sum_{color}" for color in COLORS]
ANSWER_KEYS = list(TEXT_FIELDS) + WIN_KEYS + SUM_KEYS
RULE_KEYS = [f"a2_rule_{number}" for number in range(1, 6)]
WIN_EXAMPLES = {
    "wins_1": ["2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "even"],
    "wins_8": ["5", "9", "10", "11", "12", "odd"],
}


def card_label(card):
    if card == "odd":
        return "홀수 고양이"
    if card == "even":
        return "짝수 고양이"
    number = int(card)
    return f"{number} / {ANIMALS[number - 1]}"


def color_of(card):
    number = int(card)
    return next(color for color, values in COLORS.items() if number in values)


def compare_cards(first, second):
    first_cat = first in ("odd", "even")
    second_cat = second in ("odd", "even")
    if first == second or (first_cat and second_cat):
        return 0
    if first_cat:
        matches = int(second) % 2 == (1 if first == "odd" else 0)
        return 1 if matches else -1
    if second_cat:
        return -compare_cards(second, first)
    first_number, second_number = int(first), int(second)
    if first_number + second_number == 13:
        return 1 if first_number > second_number else -1
    return 1 if first_number < second_number else -1


def winners_for(card):
    return [other for other in CARDS if compare_cards(card, other) == 1]


def toggle_flip(card):
    key = f"flipped_{card}"
    st.session_state[key] = not st.session_state.get(key, False)


def record_trial():
    first = st.session_state.get("battle_my", "1")
    second = st.session_state.get("battle_opponent", "1")
    st.session_state.setdefault("trials", []).append(
        {
            "my": first,
            "opponent": second,
            "result": compare_cards(first, second),
            "note": st.session_state.get("battle_note", ""),
        }
    )


def reset_answers():
    for key in ANSWER_KEYS:
        st.session_state[key] = list(WIN_EXAMPLES[key]) if key in WIN_EXAMPLES else ([] if key in WIN_KEYS else "")
    st.session_state["trials"] = []
    st.session_state["student_id"] = ""
    st.session_state["student_name"] = ""


def restore_answers():
    uploaded = st.session_state.get("restore_file")
    if uploaded is None:
        st.session_state["restore_status"] = ("error", "먼저 답안 JSON 파일을 선택하세요.")
        return
    try:
        payload = json.loads(uploaded.getvalue().decode("utf-8"))
        if payload.get("schema") != SCHEMA:
            raise ValueError("이 활동지에서 저장한 JSON 파일을 선택해주세요.")
        student = payload.get("student", {})
        answers = payload.get("answers", {})
        if not isinstance(student, dict) or not isinstance(answers, dict):
            raise ValueError("파일의 답안 형식이 올바르지 않습니다.")
        for key, label in (("id", "student_id"), ("name", "student_name")):
            value = student.get(key, "")
            if not isinstance(value, str) or len(value) > 100:
                raise ValueError("학번과 이름 항목을 확인해주세요.")
            st.session_state[label] = value
        for key in ANSWER_KEYS:
            if key not in answers:
                continue
            value = answers[key]
            if key in WIN_KEYS:
                if not isinstance(value, list) or any(card not in CARDS for card in value):
                    raise ValueError("카드 선택 정보가 올바르지 않습니다.")
                st.session_state[key] = [card for card in CARDS if card in value]
            elif key in SUM_KEYS:
                if value not in ("", *COLORS.keys()):
                    raise ValueError("색깔 선택 정보가 올바르지 않습니다.")
                st.session_state[key] = value
            elif isinstance(value, str) and len(value) <= 20000:
                st.session_state[key] = value
            else:
                raise ValueError("답안 항목을 확인해주세요.")
        trials = payload.get("trials", [])
        if not isinstance(trials, list) or len(trials) > 300:
            raise ValueError("실험 기록은 최대 300개까지 불러올 수 있습니다.")
        restored = []
        for trial in trials:
            first, second = trial.get("my"), trial.get("opponent")
            note = trial.get("note", "")
            if first not in CARDS or second not in CARDS or not isinstance(note, str):
                raise ValueError("실험 기록을 확인해주세요.")
            restored.append({"my": first, "opponent": second, "result": compare_cards(first, second), "note": note})
        st.session_state["trials"] = restored
        st.session_state["restore_status"] = ("success", "답안을 불러왔습니다.")
    except (UnicodeDecodeError, json.JSONDecodeError, AttributeError, ValueError) as error:
        st.session_state["restore_status"] = ("error", str(error))


for answer_key in ANSWER_KEYS:
    default = WIN_EXAMPLES.get(answer_key, [] if answer_key in WIN_KEYS else "")
    st.session_state.setdefault(answer_key, list(default) if isinstance(default, list) else default)
st.session_state.setdefault("student_id", "")
st.session_state.setdefault("student_name", "")
st.session_state.setdefault("trials", [])

answered = sum(
    bool(st.session_state.get(key))
    for key in ANSWER_KEYS
)
total_answers = len(ANSWER_KEYS)

st.markdown(
    '<div class="brandline"><span class="brandmark">13</span><span>십삼지신<small>수학 탐구 활동지</small></span></div>',
    unsafe_allow_html=True,
)
st.markdown(
    f"""
    <section class="hero">
      <div><p class="eyebrow">PLAY, DISCOVER, EXPLAIN</p>
      <h1>놀이와 수학을 동시에!<br><span>십삼지신</span></h1>
      <p>카드를 관찰하고, 전략을 탐구하고,<br>나의 생각을 수학으로 설명해보세요.</p></div>
      <div class="hero-art" aria-hidden="true">
        <img src="{BASE_URL}/assets/card_1.png" alt="">
        <img src="{BASE_URL}/assets/card_8.png" alt="">
        <img src="{BASE_URL}/assets/card_3.png" alt="">
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

with st.container(border=True):
    st.markdown('<div class="student-title">학습자 정보와 활동 진행</div>', unsafe_allow_html=True)
    student_cols = st.columns([1, 1, 1.4])
    with student_cols[0]:
        st.text_input("학번", placeholder="학번을 입력하세요", key="student_id", max_chars=100)
    with student_cols[1]:
        st.text_input("이름", placeholder="이름을 입력하세요", key="student_name", max_chars=100)
    with student_cols[2]:
        st.markdown(f'<div class="progress-label"><span>나의 활동 진행</span><strong>{answered} / {total_answers}</strong></div>', unsafe_allow_html=True)
        st.progress(answered / total_answers)
        st.markdown('<div class="status-note">입력 내용은 현재 앱 세션에 보관됩니다. 파일로 내려받아 이어서 작성할 수 있습니다.</div>', unsafe_allow_html=True)

observe_tab, rules_tab, strategy_tab, save_tab = st.tabs(
    ["01  카드 관찰", "02  게임과 규칙", "03  전략 탐구", "↓  답안 저장"]
)

with observe_tab:
    st.markdown('<div class="section-kicker">ACTIVITY 01</div>', unsafe_allow_html=True)
    st.title("십이지신 카드의 특징은?")
    st.markdown('<p class="section-intro">카드를 살펴보고 그림, 수, 색깔 사이에서 발견한 점을 기록해보세요.</p>', unsafe_allow_html=True)
    st.markdown('<div class="hint">카드를 누르면 뒷면이 나타납니다. 그림과 수의 관계도 함께 살펴보세요.</div>', unsafe_allow_html=True)
    card_columns = st.columns(4)
    for index, card in enumerate(NUMBERS):
        color = color_of(card)
        with card_columns[index % 4]:
            if st.session_state.get(f"flipped_{card}", False):
                st.markdown(
                    f'<div class="card-back {COLOR_CLASS[color]}"><strong>{color}</strong><small>뒷면</small></div>',
                    unsafe_allow_html=True,
                )
            else:
                st.image(f"{BASE_URL}/assets/card_{card}.png", width=108)
            st.caption(card_label(card))
            st.button(
                "앞면 보기" if st.session_state.get(f"flipped_{card}", False) else "뒷면 보기",
                key=f"flip_button_{card}",
                on_click=toggle_flip,
                args=(card,),
                use_container_width=True,
            )

    st.markdown('<div class="question-box"><div class="question-title"><span class="q-number">1</span>카드 앞면에 담긴 네 가지 정보를 써보세요.</div></div>', unsafe_allow_html=True)
    info_columns = st.columns(2)
    for index in range(1, 5):
        with info_columns[(index - 1) % 2]:
            st.text_input(f"정보 {index}", placeholder="관찰한 정보를 입력하세요", key=f"a1_info_{index}")
    with st.expander("예시 답안 확인"):
        st.markdown("**동물, 문양, 색깔, 수**\n\n카드 앞면에는 동물 그림, 문양, 배경 색깔, 수가 담겨 있습니다.")

    st.markdown('<div class="question-box"><div class="question-title"><span class="q-number">2</span>네 가지 정보 중 같은 의미를 나타내는 두 가지를 써보세요.</div></div>', unsafe_allow_html=True)
    st.text_area("두 정보와 그 이유", placeholder="두 정보를 적고, 같은 의미라고 생각한 이유를 설명해보세요.", key="a1_same", height=100)
    with st.expander("예시 답안 확인"):
        st.markdown("**동물과 수**\n\n동물과 수는 각각 12가지이며, 정해진 순서에 따라 하나의 동물이 하나의 수와 대응됩니다.")

    st.markdown('<div class="question-box"><div class="question-title"><span class="q-number">3</span>카드 뒷면에 담긴 한 가지 정보를 써보세요.</div></div>', unsafe_allow_html=True)
    st.text_input("카드 뒷면 정보", placeholder="위의 카드를 뒤집어 확인해보세요.", key="a1_back")
    with st.expander("예시 답안 확인"):
        st.markdown("**색깔**\n\n카드 뒷면에서 색깔을 확인할 수 있습니다.")

    st.markdown('<div class="question-box"><div class="question-title"><span class="q-number">4</span>수와 색깔 사이의 관계를 설명해보세요.</div></div>', unsafe_allow_html=True)
    st.text_area("수와 색깔 사이의 관계", placeholder="같은 색의 수들을 모아 비교하면 어떤 규칙이 보이나요?", key="a1_color", height=140)
    with st.expander("예시 답안 확인"):
        st.markdown("**같은 색의 수는 3씩 커집니다.**\n\n- 빨간색: 1, 4, 7, 10\n- 노란색: 2, 5, 8, 11\n- 파란색: 3, 6, 9, 12")

with rules_tab:
    st.markdown('<div class="section-kicker">ACTIVITY 02</div>', unsafe_allow_html=True)
    st.title("십삼지신 게임하기")
    st.markdown('<p class="section-intro">규칙을 이해하고, 어떤 카드가 다른 카드를 이길 수 있는지 알아보세요.</p>', unsafe_allow_html=True)
    st.subheader("1. 게임 규칙 정리")
    rule_questions = [
        "카드의 어느 면이 보이도록 내려놓나요?",
        "누가 나머지 플레이어와 대결하나요?",
        "어떤 수 카드가 승리하나요?",
        "두 수의 합이 얼마이면 큰 수가 승리하나요?",
        "무승부인 경우 말을 몇 칸 전진하나요?",
    ]
    for index, question in enumerate(rule_questions, 1):
        st.text_input(question, key=f"a2_rule_{index}", placeholder="빈칸에 들어갈 말을 써보세요")
    with st.expander("규칙 확인"):
        st.markdown("- 카드는 뒷면이 보이도록 내려놓습니다.\n- 선 플레이어와 나머지 플레이어들이 대결합니다.\n- 숫자 카드끼리 대결하면 합이 13인 경우 큰 수가, 그 외에는 작은 수가 이깁니다.\n- 고양이 카드는 같은 홀짝의 숫자 카드에 이깁니다.\n- 같은 카드 또는 고양이 카드끼리는 무승부입니다.")

    st.markdown('<div class="subsection"><h3>2. 카드별 승리 목록</h3><p>각 카드로 이길 수 있는 상대 카드를 골라보세요. 1과 8은 예시 답안입니다.</p></div>', unsafe_allow_html=True)
    win_columns = st.columns(2)
    for index, card in enumerate(CARDS):
        with win_columns[index % 2]:
            with st.container(border=True):
                st.markdown(f"**{card_label(card)} 카드**" + ("　`예시`" if f"wins_{card}" in WIN_EXAMPLES else ""))
                st.multiselect(
                    "이길 수 있는 상대 카드",
                    CARDS,
                    key=f"wins_{card}",
                    format_func=card_label,
                    label_visibility="collapsed",
                )
    if st.button("선택한 승리 목록 확인", key="check_wins"):
        st.session_state["show_wins_check"] = True
    if st.session_state.get("show_wins_check"):
        incorrect = [
            card
            for card in CARDS
            if set(st.session_state[f"wins_{card}"]) != set(winners_for(card))
        ]
        if incorrect:
            st.warning("아직 확인이 필요한 카드가 있습니다. 각 목록에는 이길 수 있는 카드를 모두 골라야 합니다.")
            st.write("확인할 카드: " + ", ".join(card_label(card) for card in incorrect))
        else:
            st.success("모든 카드의 승리 목록이 맞습니다.")

    st.markdown('<div class="subsection"><h3>3. 두 카드 대결 실험</h3><p>카드 두 장의 승패를 확인하고 결과를 기록해보세요.</p></div>', unsafe_allow_html=True)
    battle_cols = st.columns(2)
    with battle_cols[0]:
        st.selectbox("내 카드", CARDS, key="battle_my", format_func=card_label)
    with battle_cols[1]:
        st.selectbox("상대 카드", CARDS, key="battle_opponent", format_func=card_label)
    st.text_input("실험 메모", key="battle_note", placeholder="어떤 결과를 예상했나요?")
    st.button("대결하고 기록하기", type="primary", on_click=record_trial, key="record_trial")
    if st.session_state["trials"]:
        result_labels = {1: "승리", 0: "무승부", -1: "패배"}
        for index, trial in enumerate(st.session_state["trials"], 1):
            st.write(f"{index}. {card_label(trial['my'])} 대 {card_label(trial['opponent'])}: **{result_labels[trial['result']]}** · {trial['note'] or '메모 없음'}")

with strategy_tab:
    st.markdown('<div class="section-kicker">ACTIVITY 03</div>', unsafe_allow_html=True)
    st.title("게임 전략 탐구하기")
    st.markdown('<p class="section-intro">나의 선택을 돌아보고, 항상 성립하는 전략인지 설명해보세요.</p>', unsafe_allow_html=True)
    st.subheader("1. 게임 중 나의 선택 돌아보기")
    st.markdown("게임을 하면서 카드를 유리하게 냈던 순간과 불리하게 냈던 순간을 떠올려보세요.")
    st.text_area("카드를 유리하게 냈던 상황", placeholder="상대의 정보, 내가 낸 카드, 결과와 이유를 적어보세요.", key="a3_good", height=100)
    st.text_area("카드를 불리하게 냈던 상황", placeholder="어떤 정보를 놓쳤나요? 다시 선택한다면 어떻게 할까요?", key="a3_bad", height=100)

    st.markdown('<div class="subsection"><h3>2. 파란색 카드를 반드시 이기려면?</h3><p>상대방의 파란색 카드는 고양이 카드가 아닙니다. 선택한 카드와 이유를 설명해보세요.</p></div>', unsafe_allow_html=True)
    st.text_area("선택한 카드와 이유", key="a3_blue_reason", height=110)
    blue_choice = st.selectbox("검증할 내 카드", CARDS, key="blue_candidate", format_func=card_label)
    if st.button("가능한 상대와 비교", key="check_blue"):
        st.session_state["blue_result"] = [card for card in NUMBERS if color_of(card) == "파란색" and compare_cards(blue_choice, card) == 1]
    if "blue_result" in st.session_state:
        st.info("이 카드로 이길 수 있는 파란색 카드: " + (", ".join(card_label(card) for card in st.session_state["blue_result"]) or "없음"))

    st.markdown('<div class="subsection"><h3>3. 고양이 카드의 활용</h3><p>고양이 카드는 어떤 상황에서 사용하면 유리합니까?</p></div>', unsafe_allow_html=True)
    st.text_area("고양이 카드 전략", placeholder="상대의 남은 카드와 알 수 있는 정보를 연결하여 설명해보세요.", key="a3_cat", height=110)

    st.markdown('<div class="subsection"><h3>4. 남은 카드로 전략 세우기</h3><p><b>나:</b> 3, 6, 7, 8, 9, 11　 <b>상대:</b> 2, 4, 5, 6, 10, 12</p><p>상대방이 빨간색 카드를 냈을 때, 반드시 승리할 수 있는 카드는 무엇인가요?</p></div>', unsafe_allow_html=True)
    st.text_area("반드시 승리하는 카드와 이유", key="a3_red_reason", height=110)
    red_candidates = ["3", "6", "7", "8", "9", "11"]
    red_choice = st.selectbox("검증할 남은 카드", red_candidates, key="red_candidate", format_func=card_label)
    if st.button("상대의 빨간색 카드와 비교", key="check_red"):
        st.session_state["red_result"] = [card for card in ["4", "10"] if compare_cards(red_choice, card) == 1]
    if "red_result" in st.session_state:
        st.info("이 카드로 이길 수 있는 상대의 빨간색 카드: " + (", ".join(card_label(card) for card in st.session_state["red_result"]) or "없음"))

    st.markdown('<div class="subsection"><h3>5. 합이 13인 카드와 색깔의 관계</h3><p>각 색깔은 어떤 색 카드와 대결할 때 합이 13이 가능한가요?</p></div>', unsafe_allow_html=True)
    color_cols = st.columns(3)
    for index, color in enumerate(COLORS):
        with color_cols[index]:
            st.selectbox(
                f"{color} 카드와 합이 13이 가능한 색",
                ["", *COLORS.keys()],
                key=f"a3_sum_{color}",
                format_func=lambda value: value or "선택하세요",
            )
    st.text_area("색깔별 수를 이용해 연역적으로 설명하기", key="a3_deduction", height=110)
    slider_number = st.slider("한 카드의 수", min_value=1, max_value=12, value=1, key="sum_number")
    partner = 13 - slider_number
    st.markdown(f'<div class="hint"><b>{slider_number} + {partner} = 13</b><br>{color_of(str(slider_number))} 카드와 {color_of(str(partner))} 카드</div>', unsafe_allow_html=True)
    st.caption("몇 가지 사례를 확인한 것과 모든 경우에 성립함을 설명한 것은 어떻게 다를까요?")

    st.markdown('<div class="subsection"><h3>6. 결승점은 왜 13일까요?</h3><p>각자 가진 카드 수와 한 번의 대결에서 두 사람이 전진하는 칸 수를 생각해보세요.</p></div>', unsafe_allow_html=True)
    st.text_area("결승점이 13인 이유", key="a3_finish", height=110)
    st.markdown('<div class="notice">서술형 답안은 자동 채점하지 않습니다. 서로의 설명을 비교하며 근거가 충분한지 토의해보세요.</div>', unsafe_allow_html=True)

with save_tab:
    st.markdown('<div class="section-kicker">MY WORKSHEET</div>', unsafe_allow_html=True)
    st.title("생각을 기록으로 남기기")
    st.markdown('<p class="section-intro">작성한 답안을 내려받고, 나중에 파일을 불러와 이어서 작성할 수 있습니다.</p>', unsafe_allow_html=True)
    student = {"id": st.session_state.get("student_id", ""), "name": st.session_state.get("student_name", "")}
    answers = {key: st.session_state.get(key, "") for key in ANSWER_KEYS}
    payload = {"schema": SCHEMA, "saved_at": datetime.now().astimezone().isoformat(), "student": student, "answers": answers, "trials": st.session_state["trials"]}
    safe_name = "_".join(part for part in (student["id"], student["name"]) if part.strip()) or "미기입"
    safe_name = "".join(char if char.isalnum() or char in "-_" else "_" for char in safe_name)

    with st.container(border=True):
        st.markdown("**제출용 답안**")
        st.write("브라우저에서 열어 인쇄하거나 PDF로 저장할 수 있습니다.")
        sections = {
            "활동 1. 십이지신 카드의 특징은?": [key for key in TEXT_FIELDS if key.startswith("a1_")],
            "활동 2. 십삼지신 게임하기": RULE_KEYS + WIN_KEYS,
            "활동 3. 게임 전략 탐구하기": [key for key in TEXT_FIELDS if key.startswith("a3_")] + SUM_KEYS,
        }
        report_parts = []
        for section, keys in sections.items():
            report_parts.append(f"<h2>{html.escape(section)}</h2>")
            for key in keys:
                value = answers.get(key, "")
                if isinstance(value, list):
                    value = ", ".join(card_label(card) for card in value)
                report_parts.append(f"<section><h3>{html.escape(TEXT_FIELDS.get(key, key))}</h3><p>{html.escape(str(value)) or '미작성'}</p></section>")
        report_html = """<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>십삼지신 활동지 답안</title><style>body{max-width:820px;margin:36px auto;padding:0 22px;font:16px/1.75 sans-serif;color:#20383a}h1{color:#285c62}h2{margin-top:36px;border-bottom:2px solid #285c62;padding-bottom:8px}section{break-inside:avoid}p{white-space:pre-wrap;background:#f2f6f3;padding:12px;min-height:24px}@media print{button{display:none}body{margin:0}}</style><body><button onclick="window.print()">인쇄 / PDF로 저장</button><h1>놀이와 수학을 동시에! 십삼지신</h1><p>학번: """ + html.escape(student["id"] or "미기입") + "　이름: " + html.escape(student["name"] or "미기입") + "</p>" + "".join(report_parts) + "</body></html>"
        st.download_button("답안 HTML 다운로드", report_html, file_name=f"십삼지신_답안_{safe_name}.html", mime="text/html", type="primary")

    with st.container(border=True):
        st.markdown("**이어서 작성하기**")
        st.write("답안과 대결 실험 기록을 JSON 파일로 저장하거나 불러옵니다.")
        st.download_button("이어쓰기 JSON 다운로드", json.dumps(payload, ensure_ascii=False, indent=2), file_name=f"십삼지신_이어쓰기_{safe_name}.json", mime="application/json")
        st.file_uploader("저장한 답안 JSON 파일", type=["json"], key="restore_file")
        st.button("답안 불러오기", on_click=restore_answers, key="restore_button")
        if "restore_status" in st.session_state:
            kind, message = st.session_state["restore_status"]
            (st.success if kind == "success" else st.error)(message)

    with st.expander("전체 답안 확인"):
        for section, keys in sections.items():
            st.markdown(f"**{section}**")
            for key in keys:
                value = answers.get(key, "")
                if isinstance(value, list):
                    value = ", ".join(card_label(card) for card in value)
                st.write(f"{TEXT_FIELDS.get(key, key)}: {value or '미작성'}")

    st.markdown('<div class="notice">답안은 현재 앱 세션에 보관되며 교사에게 자동 전송되지 않습니다. 다른 기기에서 이어서 작성하려면 JSON 파일을 내려받아 보관하세요.</div>', unsafe_allow_html=True)
    st.button("전체 초기화", on_click=reset_answers, key="reset_button")

st.markdown('<div class="footer"><span>●</span>　관찰에서 발견으로, 발견에서 설명으로.</div>', unsafe_allow_html=True)