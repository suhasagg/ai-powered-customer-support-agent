import re
from .tools import customer_profile, order_status, create_ticket, request_refund

ORDER_RE=re.compile(r'ORD-\d+', re.I)

class SupportAgent:
    def __init__(self, kb):
        self.kb=kb
        self.memory={}

    def run(self, req):
        msg=req.message.strip(); low=msg.lower(); tools=[]; approval=False
        key=f'{req.customer_id}:{req.conversation_id}'
        history=self.memory.setdefault(key,[]); history.append({'role':'user','content':msg})
        sources=self.kb.search(msg)
        order_match=ORDER_RE.search(msg); order_id=order_match.group(0).upper() if order_match else None

        if any(w in low for w in ['refund','money back']):
            intent='refund'
            if not order_id:
                answer='Please provide the order ID (for example ORD-501) so I can validate the refund request.'
            elif not req.allow_actions:
                r=order_status(req.customer_id,order_id); tools.append(('order_status',r))
                approval=True
                answer=f'I found {order_id}. A refund is a state-changing action, so explicit action approval is required before I submit it.' if r['ok'] else r['output']['error']
            else:
                r=request_refund(req.customer_id,order_id); tools.append(('request_refund',r))
                answer=f"Refund request submitted for {order_id}. Status: {r['output'].get('status')}." if r['ok'] else r['output']['error']
        elif order_id or any(w in low for w in ['order','tracking','shipment','delivery']):
            intent='order_status'
            if not order_id: answer='Please provide your order ID so I can check its status.'
            else:
                r=order_status(req.customer_id,order_id); tools.append(('order_status',r))
                if r['ok']:
                    o=r['output']; answer=f"{order_id} is {o['status']}. Tracking: {o['tracking'] or 'not assigned yet'}."
                else: answer=o['error'] if (o:=r['output']) else 'Order not found.'
        elif any(w in low for w in ['agent','human','ticket','complaint','escalate']):
            intent='escalation'
            if req.allow_actions:
                r=create_ticket(req.customer_id,'Customer support escalation',msg); tools.append(('create_ticket',r))
                answer=f"I created support ticket {r['output']['ticket_id']}."
            else:
                approval=True; answer='I can create a support ticket for a human agent. Enable action approval to proceed.'
        elif any(w in low for w in ['profile','account','tier']):
            intent='customer_profile'; r=customer_profile(req.customer_id); tools.append(('customer_profile',r))
            answer=f"Account: {r['output'].get('name')}, tier: {r['output'].get('tier')}." if r['ok'] else r['output']['error']
        else:
            intent='knowledge'
            if sources:
                context=' '.join(s['text'].replace('\n',' ')[:450] for s in sources[:2])
                answer='Based on the support knowledge base: '+context
            else: answer="I couldn't find a grounded answer in the knowledge base. I can escalate this to a human support ticket."
        history.append({'role':'assistant','content':answer})
        return {'answer':answer,'intent':intent,'sources':[{'title':s['title'],'score':round(s['score'],4),'excerpt':s['text'][:220]} for s in sources],
                'tools':[{'tool':name,'ok':r['ok'],'output':r['output']} for name,r in tools], 'requires_approval':approval}
