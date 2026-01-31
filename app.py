import streamlit as st
import datetime

# --- アプリの基本設定 ---
st.set_page_config(page_title="大津港アジング予測", page_icon="🎣")
st.title("🌊 大津港アジング予測")
st.caption("自分専用・釣果期待度算出ツール")

# --- サイドバー：入力項目 ---
st.sidebar.header("現在の状況を入力")
target_date = st.sidebar.date_input("遠征日", datetime.date.today())
target_time = st.sidebar.slider("時間帯 (時)", 0, 23, 19)
water_temp = st.sidebar.number_input("海水温 (℃)", value=18.0, step=0.1)
tide_moving = st.sidebar.checkbox("潮が動いている（上げ三分・下げ七分など）", value=True)

# --- 予測ロジック ---
def calculate_score():
    score = 0
    month = target_date.month
    if 9 <= month <= 11: score += 40
    elif 4 <= month <= 8: score += 30
    else: score += 10
    if (4 <= target_time <= 6) or (17 <= target_time <= 19): score += 40
    elif (19 < target_time <= 23): score += 30
    else: score += 5
    if tide_moving: score += 20
    if 18 <= water_temp <= 23: multiplier = 1.2
    elif water_temp < 13: multiplier = 0.5
    else: multiplier = 1.0
    final_score = min(100, int(score * multiplier))
    return final_score

# --- 結果表示 ---
score = calculate_score()
st.metric(label="本日の釣果期待度", value=f"{score} %")
if score >= 80:
    st.error("🔥 【爆釣警報】今すぐ大津港へ向かってください！")
elif score >= 60:
    st.success("✨ 【チャンス】かなり期待できます。準備しましょう。")
else:
    st.warning("☁️ 【忍耐】厳しい状況かもしれません。深場を狙いましょう。")

st.subheader("📍 大津港ピンポイント攻略")
tab1, tab2 = st.tabs(["市場前", "新港堤防"])
with tab1:
    st.write("**夜間の鉄板ポイント**\n常夜灯の明暗にアジが溜まります。")
with tab2:
    st.write("**回遊待ちの聖地**\n潮通し抜群。尺アジを狙うならここ。")
