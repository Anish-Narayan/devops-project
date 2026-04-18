from flask import Flask, request, jsonify

app = Flask(__name__)

# in-memory storage
habits = {}


# ---------------------------
# FRONTEND (HTML UI)
# ---------------------------
@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Habit Tracker</title>
    <style>
        body { font-family: Arial; margin: 40px; }
        input, button { padding: 8px; margin: 5px; }
        .card { padding: 10px; border: 1px solid #ccc; margin-top: 10px; width: 300px; }
    </style>
</head>
<body>

<h2>🔥 Habit Tracker</h2>

<input id="habit" placeholder="Enter habit">
<button onclick="addHabit()">Add</button>

<h3>My Habits</h3>
<div id="list"></div>

<script>
async function load() {
    let res = await fetch('/habits');
    let data = await res.json();

    let list = document.getElementById('list');
    list.innerHTML = "";

    data.forEach(h => {
        list.innerHTML += `
            <div class="card">
                <b>${h.name}</b><br>
                Done: ${h.count}
                <br>
                <button onclick="done('${h.name}')">Mark Done</button>
            </div>
        `;
    });
}

async function addHabit() {
    let name = document.getElementById('habit').value;

    await fetch('/habit', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name})
    });

    document.getElementById('habit').value = "";
    load();
}

async function done(name) {
    await fetch(`/habit/${name}/done`, {method: 'POST'});
    load();
}

load();
</script>

</body>
</html>
"""


# ---------------------------
# API: add habit
# ---------------------------
@app.route("/habit", methods=["POST"])
def add_habit():
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "name required"}), 400

    name = data["name"]

    if name in habits:
        return jsonify({"error": "already exists"}), 409

    habits[name] = {"name": name, "count": 0}
    return jsonify({"message": "habit added"}), 201


# ---------------------------
# API: list habits
# ---------------------------
@app.route("/habits", methods=["GET"])
def list_habits():
    return jsonify(list(habits.values()))


# ---------------------------
# API: mark done
# ---------------------------
@app.route("/habit/<name>/done", methods=["POST"])
def mark_done(name):
    if name not in habits:
        return jsonify({"error": "not found"}), 404

    habits[name]["count"] += 1
    return jsonify(habits[name])


# ---------------------------
# RUN APP
# ---------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)