import unittest
import app.flask_todo as flask_todo
from app.flask_todo import app


class TestFlaskTodo(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        flask_todo.tasks.clear()
        flask_todo.task_id_counter = 1

    def test_add_task_success(self):
        response = self.client.post("/tasks", json={"title": "Einkaufen"})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["title"], "Einkaufen")
        self.assertFalse(data["done"])
        self.assertEqual(data["id"], 1)

    def test_add_task_missing_title_returns_400(self):
        response = self.client.post("/tasks", json={})
        self.assertEqual(response.status_code, 400)

    def test_add_task_empty_title_returns_400(self):
        response = self.client.post("/tasks", json={"title": ""})
        self.assertEqual(response.status_code, 400)

    def test_get_tasks_empty(self):
        response = self.client.get("/tasks")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_get_tasks_returns_all(self):
        self.client.post("/tasks", json={"title": "Task 1"})
        self.client.post("/tasks", json={"title": "Task 2"})
        response = self.client.get("/tasks")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 2)

    def test_get_task_by_id(self):
        self.client.post("/tasks", json={"title": "Meine Aufgabe"})
        response = self.client.get("/tasks/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["title"], "Meine Aufgabe")

    def test_get_task_not_found(self):
        response = self.client.get("/tasks/999")
        self.assertEqual(response.status_code, 404)

    def test_delete_task_success(self):
        self.client.post("/tasks", json={"title": "Löschen"})
        response = self.client.delete("/tasks/1")
        self.assertEqual(response.status_code, 204)

    def test_delete_task_removes_from_list(self):
        self.client.post("/tasks", json={"title": "Löschen"})
        self.client.delete("/tasks/1")
        response = self.client.get("/tasks")
        self.assertEqual(len(response.get_json()), 0)

    def test_delete_task_not_found(self):
        response = self.client.delete("/tasks/999")
        self.assertEqual(response.status_code, 404)

    def test_task_ids_increment(self):
        self.client.post("/tasks", json={"title": "Erste"})
        r2 = self.client.post("/tasks", json={"title": "Zweite"})
        self.assertEqual(r2.get_json()["id"], 2)


if __name__ == "__main__":
    unittest.main()
