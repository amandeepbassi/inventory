from sanic.response import json
from aiopg.sa import create_engine
from config import Config
from model import milk_produce, connection
from sanic import Blueprint
from sanic.exceptions import NotFound, ServerError
from sqlalchemy.sql import select, func
from datetime import date
from sqlalchemy import and_

bp_milk_produced = Blueprint('milk_produced_blueprint')


@bp_milk_produced.route("/milkproduced", methods=['POST'])
async def bp_post_milk_produced(request):
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            results = {}
            if request.method == 'POST':
                insert_query = milk_produce.insert(inline=True,returning=[milk_produce.c.raw_milk_id]).values(request.json)
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
                return json(results, headers={'URL': url_prefix}, status=201)
            



@bp_milk_produced.route('/milkproduced/<raw_milk_id:string>', methods=['PUT', 'PATCH', 'DELETE'])
async def bp_raw_milk_produced(request, raw_milk_id):
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            results = {}
            milk_json = request.json
            result_value = await(await conn.execute(select([func.count(milk_produce.c.raw_milk_id)]).where(milk_produce.c.raw_milk_id == raw_milk_id))).fetchone()
            if request.method == 'PUT' or request.method == 'PATCH':
                if str(result_value[0]) == "1":
                    update_query = milk_produce.update().where(milk_produce.c.raw_milk_id == raw_milk_id).values(milk_json)
                    try:
                        await conn.execute(update_query)
                    except Exception as e_x:
                        print(e_x)
                        results = {"Updated Values": "Values have not been successfully updated",
                        "exception": str(e_x)}
                    else:
                        results = {"Updated Values": "values have been successfully updated"}
                else:
                    results = {"Updated Values": "Values not found"}
            elif request.method == 'DELETE':
                if str(result_value[0]) == "1":
                    delete_query = milk_produce.delete().where(milk_produce.c.raw_milk_id == raw_milk_id)
                    isDeleted = await conn.execute(delete_query)
                    #result_value = await(await conn.execute(select([func.count(milk_produce.c.raw_milk_id)]).where(milk_produce.c.raw_milk_id == raw_milk_id))).fetchone()
                    if str(isDeleted.rowcount) == '1':
                        results = {"Deleted Data": "Data has been deleted successfully"}
                    else:
                        results = {"Deleted Data": "Data has not been deleted successfully"}
                else:
                    results = {"Deleted Data": "Deleted data not present"}

        return json(results, status=200)

@bp_milk_produced.route('/milkproduced/<raw_milk_farm_id:string>', methods=['GET'])
async def get_current_milk(request, raw_milk_farm_id):
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            results = {}
            select_query = milk_produce.select().where(and_(milk_produce.c.raw_milk_farm_id == raw_milk_farm_id, func.date(milk_produce.c.raw_milk_timestamp) == date.today()))
            async for row in conn.execute(select_query):
                result = []
                result.append({"raw_milk_farm_id": str(row.raw_milk_farm_id), "raw_milk_product_id": str(row.raw_milk_product_id), "raw_milk_product_quantity": str(row.raw_milk_product_quantity), "raw_milk_product_price": str(row.raw_milk_product_price), "raw_milk_product_units": str(row.raw_milk_product_units), "raw_milk_timestamp": str(row.raw_milk_timestamp)})
                results.__setitem__(str(row.raw_milk_id), result)
                #results.__setitem__('raw_milk_farm_id', str(results['raw_milk_farm_id']))
                #results.__setitem__('raw_milk_product_id', str(results['raw_milk_product_id']))
                #results.__setitem__('raw_milk_timestamp', str(results['raw_milk_timestamp']))
        return json(results, status=200)


@bp_milk_produced.exception(NotFound)
async def ignore_404(request, exception):
    return json({"Not Found": "Page Not Found"}, status=404)


@bp_milk_produced.exception(ServerError)
async def ignore_503(request, exception):
    return json({"Server Error": "503 internal server error"}, status=503)