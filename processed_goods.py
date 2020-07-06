from sanic.response import json
from aiopg.sa import create_engine
from config import connection
from models import p_goods, milk_produced
from sanic import Blueprint

pgoods = Blueprint('pgoods')

@pgoods.route('/processed_goods', methods=["GET", 'POST'])
async def processed_goods(request):
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            if request.method == 'POST':
                data = request.json
                last_row = await (await conn.execute(milk_produced.select().order_by(milk_produced.select().columns['id'].desc()))).fetchone()
                quantity_produced = data['quantity_produced']
                quantity_used = data['quantity_used']
                product_id = data['product_id']
                add_stock = last_row.stock - quantity_used
                if last_row.stock < quantity_used:
                    return json({"Error": "Not enough raw milk is present"})
                else:
                    await conn.execute(milk_produced.insert().values(raw_milk=0, stock=add_stock))
                    await conn.execute(p_goods.insert().values(product_id=product_id,
                                                                    quantity_produced = quantity_produced,
                                                                    quantity_used = quantity_used))
                    return json({"message": "200ok"})
            else:
                data1 = []
                s_query = p_goods.select()
                async for row in conn.execute(s_query):
                # row = await (await conn.execute(s_query.order_by(p_goods.columns['pg_id'].desc()))).fetchone()
                    id = row.pg_id
                    date = str(row.date)
                    time = str(row.time)
                    product_id = row.product_id
                    quantity_produced = row.quantity_produced
                    quantity_used = row.quantity_used
                    result = {"date": date, "time": time, "product_id": product_id, "quantity_produced": quantity_produced,
                                   "quantity_used": quantity_used}
                    data1.append(result)
                print(data1)
                return json({"data": data1})




# app.run(host='0.0.0.0', port=8000)