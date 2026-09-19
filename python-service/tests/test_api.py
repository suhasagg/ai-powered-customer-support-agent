from fastapi.testclient import TestClient
from app.main import app
c=TestClient(app)
def test_health(): assert c.get('/health').status_code==200
def test_order():
 r=c.post('/v1/support/chat',json={'customer_id':'cust-1001','message':'Where is ORD-501?'})
 assert r.status_code==200 and 'shipped' in r.json()['answer']
def test_refund_approval():
 r=c.post('/v1/support/chat',json={'customer_id':'cust-1001','message':'refund ORD-502'})
 assert r.json()['requires_approval'] is True
