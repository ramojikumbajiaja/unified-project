import pytest
from fastapi.testclient import TestClient
from main import app
from models.transaction import Transaction

client = TestClient(app)

@pytest.fixture
def mock_session(mocker):
    """Fixture to mock the DB session dependency."""
    session = mocker.Mock()
    mocker.patch("routes.transaction_routes.get_session", return_value=session)
    return session


def test_get_transactions_no_filter(mock_session):
    """Test retrieving all transactions without filtering."""
    mock_session.exec.return_value.all.return_value = [
        Transaction(id=1, transaction_type="sale", amount=100),
        Transaction(id=2, transaction_type="purchase", amount=50),
    ]

    response = client.get("/transactions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["transaction_type"] == "sale"
    mock_session.exec.assert_called_once()


def test_get_transactions_with_filter(mock_session):
    """Test retrieving transactions with a specific type filter."""
    mock_session.exec.return_value.all.return_value = [
        Transaction(id=1, transaction_type="sale", amount=100)
    ]

    response = client.get("/transactions?type=sale")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["transaction_type"] == "sale"
    mock_session.exec.assert_called_once()


def test_get_transactions_with_filter_no_match(mock_session):
    """Test when filter is applied but no transactions match."""
    mock_session.exec.return_value.all.return_value = []

    response = client.get("/transactions?type=invalid_type")
    assert response.status_code == 200
    assert response.json() == []
    mock_session.exec.assert_called_once()


def test_get_transactions_empty(mock_session):
    """Test when there are no transactions in the DB."""
    mock_session.exec.return_value.all.return_value = []

    response = client.get("/transactions")
    assert response.status_code == 200
    assert response.json() == []
    mock_session.exec.assert_called_once()


def test_query_where_clause_called(mock_session, mocker):
    """Test that the where clause is applied when type is provided."""
    fake_stmt = mocker.Mock()
    mocker.patch("routes.transaction_routes.select", return_value=fake_stmt)

    fake_stmt.where.return_value = "WHERE_CLAUSE"
    mock_session.exec.return_value.all.return_value = []

    client.get("/transactions?type=sale")

    fake_stmt.where.assert_called_once()
