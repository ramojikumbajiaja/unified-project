def test_create_employee(client):
    client.post("/departments", json={"name": "HR"})
    response = client.post("/employees", json={
        "name": "Ramoji",
        "email": "ramoji@example.com",
        "department_id": 1
    })
    assert response.status_code == 201
    assert response.json()["name"] == "Ramoji"

def test_get_employees(client):
    client.post("/departments", json={"name": "HR"})
    client.post("/employees", json={
        "name": "Mahi",
        "email": "mahi@example.com",
        "department_id": 1
    })
    response = client.get("/employees")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_single_employee(client):
    client.post("/departments", json={"name": "HR"})
    client.post("/employees", json={
        "name": "Dhanu",
        "email": "dhanu@example.com",
        "department_id": 1
    })
    response = client.get("/employees/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Dhanu"

def test_update_employee(client):
    client.post("/departments", json={"name": "HR"})
    client.post("/employees", json={
        "name": "Old Name",
        "email": "old@example.com",
        "department_id": 1
    })
    response = client.put("/employees/1", json={
        "name": "New Name",
        "email": "new@example.com",
        "department_id": 1
    })
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"

def test_delete_employee(client):
    client.post("/departments", json={"name": "HR"})
    client.post("/employees", json={
        "name": "DeleteMe",
        "email": "delete@example.com",
        "department_id": 1
    })
    response = client.delete("/employees/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Employee deleted successfully"
