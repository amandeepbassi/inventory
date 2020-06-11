from sanic.response import json
from aiopg.sa import create_engine
from inventory_service import connection
from inventory_service.models import milk_produced, app
from sanic import Blueprint

milkp = Blueprint('milkp')

@milkp.route("/milk_produced", methods=['GET', 'POST'])
async def post_raw_milk_data(request):
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            if request.method=='POST':
                last_row = await (await conn.execute(milk_produced.
                            select().order_by(milk_produced.select().columns['id'].desc()))).fetchone()
                data = abs(request.json["milk"])
                add_stock = data+last_row.stock
                await conn.execute(milk_produced.insert().values(raw_milk=data, stock=add_stock))
                return json({"data added": data})
            else:
                data1 = []
                async for row in conn.execute(milk_produced.select()):
                    date = str(row.date)
                    time = str(row.time)
                    milk = abs(row.raw_milk)
                    result = {"date": date, "time": time, "milk": milk}
                    data1.append(result)
                return json({"200": data1})



