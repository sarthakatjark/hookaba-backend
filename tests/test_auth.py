import pytest
from app import create_app
from flask import json
import mongomock
from app.extensions import mongo

@pytest.fixture
def client(monkeypatch):
    app = create_app()
    app.config['TESTING'] = True
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/hookaba-test'
    # Patch PyMongo to use mongomock
    client = mongomock.MongoClient()
    monkeypatch.setattr(mongo, 'cx', client)
    with app.test_client() as client:
        yield client

def test_request_otp(client):
    res = client.post('/auth/request-otp', json={'phone': '1234567890'})
    assert res.status_code == 200
    data = res.get_json()
    assert 'message' in data

def test_verify_otp(client):
    # First, request OTP
    client.post('/auth/request-otp', json={'phone': '1234567890'})
    # Retrieve OTP from mongomock
    otp_record = mongo.cx['hookaba-test']['otps'].find_one({'phone': '1234567890'})
    otp = otp_record['otp']
    res = client.post('/auth/verify-otp', json={'phone': '1234567890', 'otp': otp})
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True 