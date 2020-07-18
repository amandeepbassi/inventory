from sanic.response import json
from aiopg.sa import create_engine
from config import Config
from model import milk_produce, connection
from sanic import Blueprint
from sanic.exceptions import NotFound, ServerError

bp_milk_produced = Blueprint('milk_produced_blueprint')


@bp_milk_produced.route("/milkproduced", methods=['GET', 'POST'])
async def bp_post_milk_produced(request):
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            results = {}
            if request.method == 'POST':
                insert_query = milk_produce.insert(inline=True,returning=[milk_produce.c.raw_milk_id]).values(request.json)

                """last_row = await (await conn.execute(milk_produced.
                            select().order_by(milk_produced.select().columns['id'].desc()))).fetchone()
                data = abs(request.json["milk"])"""
                try:
                    result_id = await(await conn.execute(insert_query)).fetchone()
                    url_prefix = str(Config.HOST_URL) + ":" + str(Config.HOST_PORT) + "/milkproduced/" + str(result_id[0])
                except Exception as e_x:
                    print(e_x)
                    results = {"Inserted Values": "Values have been not successfully inserted",
                                "Error": str(e_x)}
                else:
                    results = {"Inserted Values": "Values have been successfully inserted",
                                "location": url_prefix}
                    return json(results, status=201)
            elif request.method == 'GET':
                select_query = milk_produce.select()
                async for row in conn.execute(select_query):
                    result = []
                    result.append({"raw_milk_timestamp": str(row.raw_milk_timestamp), "raw_milk_stock": str(row.raw_milk_stock)})
                    results.__setitem__(row['raw_milk_id'], result)
                return json(results, status=200)


@bp_milk_produced.exception(NotFound)
async def ignore_404(request, exception):
    return json({"Not Found": "Page Not Found"}, status=404)


@bp_milk_produced.exception(ServerError)
async def ignore_503(request, exception):
    return json({"Server Error": "503 internal server error"}, status=503)