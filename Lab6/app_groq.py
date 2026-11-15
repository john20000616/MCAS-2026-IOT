import os
from uuid import uuid4

from flask import jsonify, request, session, redirect, url_for
from groq import Groq
import app as original

app = original.app
MODEL = "openai/gpt-oss-20b"

client = Groq(
    api_key=os.environ["GROQ_API_KEY"],
    timeout=30.0,
    max_retries=0,
)

# 對話存在伺服器記憶體，Cookie 只保存識別碼。
histories = {}


def clear_history():
    chat_id = session.pop("groq_chat_id", None)
    if chat_id:
        histories.pop(chat_id, None)


@original.login_required
def groq_chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()

    if not message:
        return jsonify(error="訊息不可為空"), 400
    if len(message) > 2000:
        return jsonify(error="訊息過長"), 400

    chat_id = session.get("groq_chat_id")
    history = histories.get(chat_id, [])
    messages = [
        {"role": "system", "content": "請使用繁體中文回答。"},
        *history,
        {"role": "user", "content": message},
    ]

    try:
        result = client.chat.completions.create(
            model=MODEL,
            messages=messages,
        )
        reply = (result.choices[0].message.content or "").strip()
        if not reply:
            return jsonify(error="模型沒有回傳文字，請重試。"), 502

        if not chat_id:
            chat_id = uuid4().hex
            session["groq_chat_id"] = chat_id

        histories[chat_id] = (
            history
            + [{"role": "user", "content": message},
               {"role": "assistant", "content": reply}]
        )[-20:]

        print(f"[Groq] model={result.model}", flush=True)
        return jsonify(reply=reply, model=result.model, provider="Groq")

    except Exception as error:
        status = getattr(error, "status_code", None)
        print(
            f"[Groq Error] {type(error).__name__}, status={status}",
            flush=True,
        )
        return jsonify(error="Groq 呼叫失敗，請查看終端機錯誤類型。"), 502


@original.login_required
def groq_reset():
    clear_history()
    return jsonify(ok=True)


@original.login_required
def groq_logout():
    clear_history()
    session.clear()
    return redirect(url_for("login"))


app.view_functions["api_chat"] = groq_chat
app.view_functions["reset_chat"] = groq_reset
app.view_functions["logout"] = groq_logout

if __name__ == "__main__":
    print(f"平台：Groq；模型：{MODEL}", flush=True)
    app.run(host="0.0.0.0", port=3000, debug=False)
