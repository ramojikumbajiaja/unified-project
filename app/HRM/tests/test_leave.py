def test_apply_leave(client):
    client.post("/departments", json={"name": "HR"})
    client.post("/employees", json={
        "name": "Ramoji",
        "email": "ramoji@example.com",
        "department_id": 1
    })
    response = client.post("/leaves", json={
        "employee_id": 1,
        "start_date": "2025-08-15",
        "end_date": "2025-08-20",
        "reason": "Vacation"
    })
    assert response.status_code == 201
    assert response.json()["reason"] == "Vacation"

def test_approve_leave(client):
    client.post("/departments", json={"name": "HR"})
    client.post("/employees", json={
        "name": "Mahi",
        "email": "mahi@example.com",
        "department_id": 1
    })
    client.post("/leaves", json={
        "employee_id": 1,
        "start_date": "2025-08-15",
        "end_date": "2025-08-20",
        "reason": "Vacation"
    })
    response = client.put("/leaves/1/approve")
    assert response.status_code == 200
    assert response.json()["status"] == "Approved"
