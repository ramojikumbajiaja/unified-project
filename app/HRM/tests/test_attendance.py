def test_mark_attendance(client):
    client.post("/departments", json={"name": "HR"})
    client.post("/employees", json={
        "name": "Sachin",
        "email": "sachin@example.com",
        "department_id": 1
    })
    response = client.post("/attendance", json={
        "employee_id": 1,
        "date": "2025-08-12",
        "status": "Present"
    })
    assert response.status_code == 201
    assert response.json()["status"] == "Present"

def test_get_attendance(client):
    client.post("/departments", json={"name": "HR"})
    client.post("/employees", json={
        "name": "Akhil",
        "email": "akhil@example.com",
        "department_id": 1
    })
    client.post("/attendance", json={
        "employee_id": 1,
        "date": "2025-08-12",
        "status": "Absent"
    })
    response = client.get("/attendance?employee_id=1")
    assert response.status_code == 200
    assert len(response.json()) > 0
