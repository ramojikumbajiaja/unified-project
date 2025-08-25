def test_create_payroll(client):
    client.post("/departments", json={"name": "HR"})
    client.post("/employees", json={
        "name": "Dhanu",
        "email": "dhanu@example.com",
        "department_id": 1
    })
    response = client.post("/payroll", json={
        "employee_id": 1,
        "month": "2025-08",
        "amount": 50000
    })
    assert response.status_code == 201
    assert response.json()["amount"] == 50000

def test_get_payroll(client):
    client.post("/departments", json={"name": "HR"})
    client.post("/employees", json={
        "name": "Dhanu",
        "email": "dhanu@example.com",
        "department_id": 1
    })
    client.post("/payroll", json={
        "employee_id": 1,
        "month": "2025-08",
        "amount": 50000
    })
    response = client.get("/payroll?employee_id=1")
    assert response.status_code == 200
    assert len(response.json()) > 0
