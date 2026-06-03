from flask import Flask, jsonify, request, abort

app = Flask(__name__)

tasks = []
task_id_counter = 1


@app.route("/tasks", methods=["POST"])
def add_task():
    global task_id_counter
    data = request.json
    if "title" not in data or not data["title"]:
        abort(400, description="Titel darf nicht leer sein")

    task = {"id": task_id_counter, "title": data["title"], "done": False}
    tasks.append(task)
    task_id_counter += 1
    return jsonify(task), 201


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks), 200


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        abort(404, description="Aufgabe nicht gefunden")
    return jsonify(task), 200


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        abort(404, description="Aufgabe nicht gefunden")
    tasks = [t for t in tasks if t["id"] != task_id]
    return "", 204


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
