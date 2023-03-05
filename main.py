
from fastapi import Depends, FastAPI,HTTPException,Request
from models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_cockroachdb import run_transaction
from fpdf import FPDF
from twilio.rest import Client

app = FastAPI()

def order(session,l):
    obj = Order(
        user = l['user'],
        Total_items = l['Total_items'],
        Total_cost = l['Total_cost']
    )
    session.add(obj)
    print("Added")
    client = Client('AC650ee5c9f0a1d51c072cd9c6ad024d75', 'f503be39f9c13638fdc0d29ae7fba7ba')
    no = l['user'].user.number
    # Restaurant number
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body="New Order Recieved",
        to='whatsapp:' + no
    )

def Users(session,l):
    #create_user_item
    obj = User(
        id=l[0],
        name=l[1],
        phone=l[2])
    session.add(obj)

    return {
        "status": "SUCCESS",
        "data": obj
    }
    # # Use a breakpoint in the code line below to debug your script.

def Updates(session,data):
    # update data remains
    # req_info = await info.json()
    Stats = data['status']
    if Stats=='Processing':
        client = Client('AC650ee5c9f0a1d51c072cd9c6ad024d75', 'f503be39f9c13638fdc0d29ae7fba7ba')
        no = data['order'].user.number
        # customer number
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body="Your Order Under Processing",
            to='whatsapp:' + no
        )
    if Stats=='Completed':
        client = Client('AC650ee5c9f0a1d51c072cd9c6ad024d75', 'f503be39f9c13638fdc0d29ae7fba7ba')
        # msg = req_info['first_name'] + '\n' + req_info['last_name'] + '\n' + req_info['lat'] + '\n' + req_info['long']
        no = data['order'].user.number
        # customer number
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body="Your order has been cooked",
            to='whatsapp:' + no
        )
    obj = Order(
        status=str
    )
    session.add(obj)
    return {
        "status": "SUCCESS",
        "data": str
    }
@app.post('/bill/<int>')
async def bill_download(info:Request):
    info_bill = await info.json()
    # Create a PDF object
    pdf = FPDF()

    # Add a page
    pdf.add_page()

    # Set font and size
    pdf.set_font('Arial', 'B', 16)

    # Write the title
    pdf.cell(0, 10, 'Bill', 0, 1, 'C')

    # Set font and size for the customer name
    pdf.set_font('Arial', '', 12)

    # Write the customer name
    customer_name = info_bill['name']
    pdf.cell(0, 10, f"Customer name: {customer_name}",1,0,1)

    # Add a table for items purchased
    pdf.cell(40, 10, 'Item', 1)
    pdf.cell(40, 10, 'Quantity', 1)
    pdf.cell(40, 10, 'Price', 1)
    pdf.cell(40, 10, 'Total', 1)
    pdf.ln()
    # Sample items
    items = []
    # for item in len(info_bill):
    items.append({'item': info_bill['items'], 'quantity': info_bill['quantity'], 'price': info_bill['price']})
    # Set font and size for items
    pdf.set_font('Arial', '', 10)

    # Add items to the table
    total = 0
    for item in items:
        pdf.cell(40, 10, item[0]['item'], 1)
        pdf.cell(40, 10, str(item[0]['quantity']), 1)
        pdf.cell(40, 10, f"${item[0]['price']}", 1)
        item_total = item[0]['quantity'] * item[0]['price']
        total += item_total
        pdf.cell(40, 10, f"${item_total}", 1)
        pdf.ln()

    # Add the total amount
    pdf.cell(0, 10, f'Total amount: ${total}', 0, 1, 'R')

    # Save the PDF
    # pdf.output('bill.pdf', 'F')
    print("File "," downloaded")

SQL_ALCHEMY_URL = ("postgresql://akash:QA7rCKUzX0PrPpmM4QRJpw@dour-snorter-2446.7s5.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full")

engine = create_engine(
    SQL_ALCHEMY_URL.replace("postgresql://", "cockroachdb://")
)
@app.post('/user')
async def user(info:Request):
    info_r = await info.json()
    id = info_r['id']
    name = info_r['name']
    phone = info_r['phone']
    l = [id,name,phone]
    run_transaction(sessionmaker(bind=engine),lambda s: Users(s,l))




@app.post('/Updates')
async def Updates(info:Request):
    info_r = await info.json()
    user = Request.user
    order = info_r['order']
    status = info_r['status']
    data = [user,order,status]
    run_transaction(sessionmaker(bind=engine),
                lambda s: Updates(s,data))

@app.post('/order')
async def order(info:Request):
    data = info.json()
    run_transaction(sessionmaker(bind=engine),lambda s: order(s,data))


@app.get('/orderdetails/<id:int>')
async def read_item(item_id: int):
    async with Order.acquire() as conn:
        query = f"SELECT * FROM order WHERE id = {item_id}"
        result = await conn.fetchrow(query, item_id)
        if result is None:
            return {"error": "Item not found"}
        return result