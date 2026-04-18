from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    if request.method == "POST":
        user_input = request.form.get("text", "")
        result = user_input[::-1]  # simple processing: reverse text

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simple Functional App</title>
        <style>
            body {
                font-family: Arial;
                text-align: center;
                margin-top: 50px;
                background: #f2f2f2;
            }
            input, button {
                padding: 10px;
                font-size: 16px;
                margin: 5px;
            }
            .result {
                margin-top: 20px;
                font-weight: bold;
                color: #333;
            }
        </style>
    </head>
    <body>
        <h2>Text Reverser</h2>
        <form method="POST">
            <input type="text" name="text" placeholder="Enter text" required>
            <button type="submit">Submit</button>
        </form>

        {% if result %}
        <div class="result">
            Result: {{ result }}
        </div>
        {% endif %}
    </body>
    </html>
    """, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)