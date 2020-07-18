from sanic.response import json
from aiopg.sa import create_engine
from config import Config
from model import p_goods, connection
from sanic import Blueprint
from sanic.exceptions import NotFound, ServerError

bp_pgoods = Blueprint('processed_goods_blueprint')

@bp_pgoods.route('/processedgoods', methods=["GET", 'POST'])
async def bp_processed_goods(request):
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            results = {}
            if request.method == 'POST':
                insert_query = p_goods.insert(inline=True,returning=[p_goods.c.pg_id]).values(request.json)
                try:
                    result_id = await(await conn.execute(insert_query)).fetchone()
                    url_prefix = str(Config.HOST_URL) + ":" + str(Config.HOST_PORT) + "/processedgoods/" + str(result_id[0])
                except Exception as e_x:
                    print(e_x)
                    results = {"Inserted Values": "Values have been not successfully inserted",
                                "Error": str(e_x)}
                else:
                    results = {"Inserted Values": "Values have been successfully inserted",
                                "location": url_prefix}
                    return json(results, status=201)
            elif request.method == 'GET':
                select_query = p_goods.select()
                async for row in conn.execute(select_query):
                    result = []
                    result.append({"pg_timestamp": str(row.pg_timestamp), "pg_product_id": str(row.pg_product_id), "pg_quantity_produced": row.pg_quantity_produced, "pg_quantity_used": row.pg_quantity_used})
                    results.__setitem__(row['pg_id'], result)
                    return json(results, status=200)


@bp_pgoods.exception(NotFound)
async def ignore_404(request, exception):
    return json({"Not Found": "Page Not Found"}, status=404)


@bp_pgoods.exception(ServerError)
async def ignore_503(request, exception):
    return json({"Server Error": "503 internal server error"}, status=503)