from flask import Flask, request, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Identity Monitor</title>
    <style>
        body {
            background-color: black;
            color: #00ff00;
            font-family: monospace;
            text-align: center;
            padding-top: 50px;
        }

        input, button {
            padding: 10px;
            font-size: 16px;
            background: black;
            color: #00ff00;
            border: 1px solid #00ff00;
        }

        button:hover {
            background: #00ff00;
            color: black;
        }

        h2 {
            text-shadow: 0 0 10px #00ff00;
        }

        .result {
            margin-top: 20px;
            font-size: 18px;
        }
    </style>
</head>
<body>

    <h2>🕵️ IDENTITY MONITOR</h2>

    <form method="POST">
        <input type="text" name="username" placeholder="Enter username..." required>
        <button type="submit">SCAN</button>
    </form>

    {% if result %}
        <div class="result">
            <p>{{ result }}</p>
        </div>
    {% endif %}

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        username = request.form["username"]

        url = f"https://duckduckgo.com/html/?q={username}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            results = soup.find_all('a', class_='result__a')

            score = 0

            for r in results:
                text = r.text.lower()

                # 🔥 simple logic (barqaror)
                if "password" in text or "leak" in text or "hack" in text:
                    score += 50
                elif "login" in text or "admin" in text:
                    score += 20

            score = min(score, 100)

            if score >= 70:
                level = "High"
            elif score >= 30:
                level = "Medium"
            else:
                level = "Low"

            result = f"Username: {username} | Score: {score}/100 | Level: {level}"
        else:
            result = "Error"

    return render_template_string(HTML, result=result)


if __name__ == "__main__":
    app.run(debug=True)