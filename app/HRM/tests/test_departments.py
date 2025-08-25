def test_create_department(client):
    response = client.post("/departments", json={"name": "Finance"})
    assert response.status_code == 201
    assert response.json()["name"] == "Finance"

def test_get_departments(client):
    client.post("/departments", json={"name": "HR"})
    response = client.get("/departments")
    assert response.status_code == 200
    assert any(d["name"] == "HR" for d in response.json())

def test_get_single_department(client):
    client.post("/departments", json={"name": "IT"})
    response = client.get("/departments/1")
    assert response.status_code == 200
    assert response.json()["name"] == "IT"

def test_update_department(client):
    client.post("/departments", json={"name": "Temp"})
    response = client.put("/departments/1", json={"name": "Permanent"})
    assert response.status_code == 200
    assert response.json()["name"] == "Permanent"

def test_delete_department(client):
    client.post("/departments", json={"name": "DeleteMe"})
    response = client.delete("/departments/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Department deleted successfully"
