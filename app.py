from flask import Flask, render_template, request, jsonify, session
from groq import Groq

application = Flask(__name__)
app = application
app.secret_key = 'your_secret_key_here'
client = Groq(api_key='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')

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/api/get-response", methods=["POST"])
def api_get_response():
    messages = session.get('messages', [])
    user_input = request.json.get("input")

    # Ensure user_input is not None or empty
    if not user_input:
        return jsonify({"error": "Input cannot be empty"}), 400

    messages.append({"role": "user", "content": user_input})
    
    try:
        assistant_response = generate_response(messages)
        messages.append({"role": "assistant", "content": assistant_response})
        session['messages'] = messages[-100:]  # Store only the last 100 messages in the session
        return jsonify({"response": assistant_response})
    except Exception as e:
        # Log the error
        print(f"Error generating response: {e}")
        return jsonify({"error": "Failed to generate response"}), 500

def generate_response(messages_list):
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages_list,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )

        # Extract the response content from the choices
        response_content = ""
        for choice in completion.choices:
            response_content += choice.message.content

        return response_content
    except Exception as e:
        # Log the error
        print(f"Error in generate_response: {e}")
        raise e

if __name__ == "__main__":
    app.run(debug=True)
