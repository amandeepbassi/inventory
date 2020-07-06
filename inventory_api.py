from sanic.response import json
from aiopg.sa import create_engine
from config import connection
from models import p_goods
from alert_class import StockAvailable
from sanic import Blueprint

apibp = Blueprint('api')

@apibp.route('/quantity_available/')
async def check_quantity(request):
    p_id = request.json['product_id']
    stock = StockAvailable(p_id)
    avl = await stock.stock()
    # print(stock.stock())
    return json({"product": p_id, "quantity": avl})

@apibp.route('/update_inventory', methods=["GET", 'POST'])
async def update_inventory(request):
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            data = request.json
            p_id = data['product_id']
            order_qty = data['quantity']
            stock_left = data['stock_left']
            # last_row = await (await conn.execute(p_goods.select().where(p_goods.c.product_id == p_id)
            #                                      .order_by(p_goods.c.pg_id.desc()))).fetchone()
            # stock_avl = last_row.stock_left
            await conn.execute(p_goods.insert().values(product_id=p_id,
                                                       quantity_produced=-1*order_qty,
                                                       quantity_used = 0,
                                                       stock_left=stock_left))
            return json({"message": "inventory updated"})