import streamlit as st
from google import genai
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+JP&family=Noto+Sans+JP:wght@100..900&display=swap" rel="stylesheet">
<style>
    body, p, div, selectbox, input, textarea, button {
      font-family: "IBM Plex Sans JP", sans-serif;
      font-weight: 400;
      font-style: normal;
    }
    div.stTextArea, div.stTextInput, div.stSelectbox, div.stHeading, div.stButton {
      width: 800px;
    }
    div.stButton {
        text-align: right;
    }
    </style>""",
    unsafe_allow_html=True,
)
      # font-family: "Noto Sans JP", sans-serif;
      # font-optical-sizing: auto;
      # font-weight: <weight>;
      # font-style: normal;

def generate_summary(option: str, api_key: str, prompt: str) -> str:
    try:
        st.session_state.processing = True
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=option,
            contents=[(
                "あなたはMBAを持っているBさん(40歳男性)と、Bさんの後輩でMBAを持っていないAさん(35歳男性)の役割です。"
                "AさんはMBAを保有していないけど、浅い質問だけでなく本質的な鋭い質問もできるタイプです。"
                "BさんはMBAを保有しているのでMBA的な観点を持っています。IQは140程度。"
                "以下の議題を、AさんとBさんの漫才形式で、"
                "重要なポイントが分かるように1000トークン程度で議論して下さい。"
                "最初に「はい、承知いたしました。」のような文は不要で、シンプルに【議題】と議題の内容を表示して下さい。"
                "会話はAさんから始めて下さい。Aさんは「A」、Bさんは「B」と表示して下さい。"
                "口調は命令口調ではなく、やさしい口調で会話して下さい。"
                "また、議論の内容を議論の背景、今回の議論のポイント、今後期待できること、今後の課題という過去から未来に向けたストーリーを意識して要約して下さい。"
                "議論の内容を表示した後に、要約した内容を表示して下さい。"
                "要約を表示する際は、【要約】というタイトルと要約した内容を200トークン程度に要約して、箇条書きで表示して下さい。"
                "文頭は「・」で始め、余計な箇条書きのタイトルなどは表示せず、要約の観点は直接表示せず、見る人が「この要約は背景、この要約は課題について書いているのだな」ということを想像できるようにして下さい。"
                f"{prompt}")]
        )
        st.session_state.processing = False
        return response.text
    except Exception as e:
        return f"エラーが発生しました： {e}"


st.subheader("事前課題②「生成AIによって教育や業務がどう変わるのか」", divider="gray")
option = st.selectbox("モデル",["gemini-2.0-flash-001", "gemini-2.0-flash-thinking-exp-01-21", "gemini-2.5-pro-exp-03-25"],label_visibility="hidden")

# テキストインプット
api_key = st.text_input('APIキー', label_visibility="hidden", placeholder='APIキーを入力', type="password")
prompt = st.text_input('プロンプト', label_visibility="hidden", placeholder='プロンプトを入力')
disable_button = not api_key.strip() or not prompt.strip()

if st.button('送信', disabled=disable_button):
    processed_text = generate_summary(option, api_key, prompt)
    text_area = st.text_area('出力結果',label_visibility="hidden", value=processed_text, height=1400)
else:
    # 初期状態または送信前
    text_area = st.text_area('出力結果',label_visibility="hidden", placeholder='ここに結果が表示されます。')
