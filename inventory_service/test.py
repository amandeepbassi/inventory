# import datetime
# from datetime import timedelta
# current = datetime.date.today()
# d = datetime.date.today() - timedelta(days=10)
# print(current)
# print(d)
# from inventory_service.alert_class import Alert_Messages
#
#
# from sanic.response import json
# from aiopg.sa import create_engine
# from inventory_service import connection
# from inventory_service.models import milk_produced, app
#
#
# @app.route("/milk_produced", methods=['GET', 'POST'])
# async def post_raw_milk_data(request):
#     async with create_engine(connection) as engine:
#         async with engine.acquire() as conn:
#             last_row = await (await conn.execute(milk_produced.
#                 select().order_by(
#                 milk_produced.select().columns['id'].desc()))).fetchone()
#             if request.method == 'POST':
#                 data = abs(request.json["milk"])
#                 add_stock = data + last_row.stock
#                 await conn.execute(milk_produced.insert().values(raw_milk=data, stock=add_stock))
#                 return json({"data added": data})
#             else:
#                 query = Alert_Messages(milk_produced)
#                 s_query = milk_produced.select()
#                 res = await query.alert_ten()
#                 if res is not None:
#                     return res
#                 else:
#                     return json({"error": "Try Again"})
#                 # data1 = []
#                 # count = 0
#                 # total_milk = 0
#                 # async for row in conn.execute(milk_produced.select().where(milk_produced.c.date > d)):
#                 #     date = str(row.date)
#                 #     time = str(row.time)
#                 #     milk = abs(row.raw_milk)
#                 #     total_milk += milk
#                 #     result = {"date": date, "time": time, "milk": milk}
#                 #     data1.append(result)
#                 #     count += 1
#                 # calc = (total_milk/count)*.1
#                 # if calc > last_row.stock:
#                 #     return json({"alert": "Raw milk stock is less than 10%", "total milk": total_milk, "count": count})
#                 # return json({"total milk": total_milk, "count": count})
#
#
#
#
#
#
# app.run(host='0.0.0.0', port=8000)