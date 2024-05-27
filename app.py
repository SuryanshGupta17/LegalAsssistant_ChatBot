from flask import Flask, render_template, request, session
from groq import Groq

application = Flask(__name__)
app = application
app.secret_key = 'your_secret_key_here'
client = Groq(api_key='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')

@app.route("/", methods=["GET", "POST"])
def index():
    messages = session.get('messages', [])
    if request.method == "POST":
        user_input = request.form["input"]
        messages.append({"role": "user", "content": user_input})
        assistant_response = get_response(messages)
        messages.append({"role": "assistant", "content": assistant_response})
        session['messages'] = messages[-100:]  # Store only the last 100 messages in the session
    return render_template("index.html", messages=messages)

def get_response(messages_list):
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages_list,
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )

    response_content = ""
    for chunk in completion:
        response_content += chunk.choices[0].delta.content or ""

    return response_content

if __name__ == "__main__":
    app.run(debug=True)
