from uuid import uuid4

CUSTOMERS={
 'cust-1001': {'name':'Alex Morgan','tier':'Gold','email':'alex@example.com'},
 'cust-1002': {'name':'Priya Sharma','tier':'Standard','email':'priya@example.com'}
}
ORDERS={
 'ORD-501': {'customer_id':'cust-1001','status':'shipped','amount':79.99,'tracking':'TRK-9001'},
 'ORD-502': {'customer_id':'cust-1001','status':'delivered','amount':35.50,'tracking':'TRK-9002'},
 'ORD-601': {'customer_id':'cust-1002','status':'processing','amount':120.00,'tracking':None}
}
TICKETS=[]

def customer_profile(customer_id):
    c=CUSTOMERS.get(customer_id)
    return {'ok': bool(c), 'output': c or {'error':'customer not found'}}

def order_status(customer_id, order_id):
    o=ORDERS.get(order_id)
    if not o or o['customer_id'] != customer_id:
        return {'ok':False,'output':{'error':'order not found for customer'}}
    return {'ok':True,'output':{'order_id':order_id, **o}}

def create_ticket(customer_id, subject, details):
    ticket={'ticket_id':f'TKT-{uuid4().hex[:8].upper()}','customer_id':customer_id,'subject':subject,'details':details,'status':'open'}
    TICKETS.append(ticket)
    return {'ok':True,'output':ticket}

def request_refund(customer_id, order_id):
    o=ORDERS.get(order_id)
    if not o or o['customer_id'] != customer_id:
        return {'ok':False,'output':{'error':'order not found for customer'}}
    # Demo: execution is deliberately approval-gated by the agent.
    return {'ok':True,'output':{'order_id':order_id,'amount':o['amount'],'status':'refund_requested'}}
