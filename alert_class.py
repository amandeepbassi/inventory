from datetime import timedelta
import datetime
from sanic.response import json
from aiopg.sa import create_engine
from config import connection
from models import p_goods


class Alert_Messages:
    def __init__(self, tb_name):
        # self.s_query = s_query
        self.tb_name = tb_name

    async def alert_ten(self):
        day_10 = datetime.date.today() - timedelta(days=10)
        data = []
        count = 0
        total = 0
        async with create_engine(connection) as engine:
            async with engine.acquire() as conn:
                last_row = await (await conn.execute(self.tb_name.
                    select().order_by(
                    self.tb_name.select().columns['id'].desc()))).fetchone()
                async for row in conn.execute(self.tb_name.select().where(self.tb_name.c.date > day_10)):
                    date = str(row.date)
                    time = str(row.time)
                    product_stock = abs(row.raw_milk)
                    total += product_stock
                    result = {"date": date, "time": time, "Quantity": total}
                    data.append(result)
                    count += 1
                    calc = (total / count) * .1
                    if calc > last_row.stock:

                        return json({"alert": "product stock is less than 10%"})
                    return json({"total milk": "amazing"})

class StockAvailable():
    def __init__(self, p_id):
        self.p_id = p_id
    async def stock(self):
        async with create_engine(connection) as engine:
            async with engine.acquire() as conn:
                last_row = await (await conn.execute(p_goods.select().where(p_goods.c.product_id == self.p_id)
                                                     .order_by(p_goods.c.pg_id.desc()))).fetchone()
                details = last_row.stock_left
                # print(details)
                print(last_row)
                return details