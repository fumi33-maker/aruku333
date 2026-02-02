import streamlit as st
import pandas as pd
from datetime import date

st.title("🐾 散歩ログ・アプリ")

# --- データの管理（セッション状態を使って一時保存） ---
if 'walking_data' not in st.session_state:
    # 初期データ（空のリスト）を作成
    st.session_state.walking_data = pd.DataFrame(columns=["日付", "歩数"])

# --- 入力エリア ---
with st.form("input_form"):
    selected_date = st.date_input("散歩した日を選んでください", date.today())
    steps = st.number_input("歩いた数（歩）", min_value=0, step=100)
    submitted = st.form_submit_button("記録を保存する")

    if submitted:
        # 新しいデータを追加
        new_data = pd.DataFrame({"日付": [selected_date], "歩数": [steps]})
        st.session_state.walking_data = pd.concat([st.session_state.walking_data, new_data], ignore_index=True)
        st.success(f"保存しました！")

# --- ランキング表示（ここが追加ポイント！） ---
st.write("---")
st.subheader("🏆 たくさん歩いた日 TOP 3")

if not st.session_state.walking_data.empty:
    # 歩数が多い順に並び替えて、上位3つを取得
    top_3 = st.session_state.walking_data.sort_values(by="歩数", ascending=False).head(3)
    
    # 順位をつけて表示
    for i, (index, row) in enumerate(top_3.iterrows(), 1):
        st.write(f"{i}位: {row['日付']} — **{row['歩数']} 歩**")
else:
    st.write("まだ記録がありません。")

# --- 全履歴の表示 ---
with st.expander("すべての履歴を見る"):
    st.dataframe(st.session_state.walking_data)

    