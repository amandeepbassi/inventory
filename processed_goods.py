from sanic.response import json
from aiopg.sa import create_engine
from config import Config
from model import p_goods, connection
from sanic import Blueprint
from sanic.exceptions import NotFound, ServerError
from sqlalchemy import and_
from sqlalchemy.sql import select, func
from datetime import date

bp_pgoods = Blueprint('processed_goods_blueprint')


@bp_pgoods.route('/processedgoods/<pg_id:string>', methods=['GET', 'PATCH', 'PUT', 'DELETE'])
async def bp_goods(request, pg_id):
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            results = {}
            if request.method == 'GET':
                select_query = p_goods.select().where(p_goods.c.pg_id == pg_id)
                async for row in conn.execute(select_query):
                    results.update(row)
                    results.__setitem__('pg_id', str(results['pg_id']))
                    results.__setitem__('pg_timestamp', str(results['pg_timestamp']))
                    results.__setitem__('pg_product_id', str(results['pg_product_id']))
                    results.__setitem__('pg_farm_id', str(results['pg_farm_id']))
                    results.__setitem__('pg_milk_id', str(results['pg_milk_id']))
                return json(results, status=200)
            elif request.method == 'PUT' or request.method == 'PATCH':
                goods_json = request.json
                result_value = await(await conn.execute(select([func.count(p_goods.c.pg_id)]).where(p_goods.c.pg_id == pg_id))).fetchone()
                if str(result_value[0]) == "1":
                    update_query = p_goods.update().where(p_goods.c.pg_id == pg_id).values(goods_json)
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
                return json(results, status=200)
            elif request.method == 'DELETE':
                result_value = await(await conn.execute(select([func.count(p_goods.c.pg_id)]).where(p_goods.c.pg_id == pg_id))).fetchone()
                if str(result_value[0]) == "1":
                    delete_query = p_goods.delete().where(p_goods.c.pg_id == pg_id)
                    isDeleted = await conn.execute(delete_query)
                    #result_value = await(await conn.execute(select([func.count(milk_produce.c.raw_milk_id)]).where(milk_produce.c.raw_milk_id == raw_milk_id))).fetchone()
                    if str(isDeleted.rowcount) == '1':
                        results = {"Deleted Data": "Data has been deleted successfully"}
                    else:
                        results = {"Deleted Data": "Data has not been deleted successfully"}
                else:
                    results = {"Deleted Data": "Deleted data not present"}
                return json(results, status=200)
                    



@bp_pgoods.route('/processedgoods', methods=['POST', 'GET'])
async def bp_processed_goods(request):
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            results = {}    
            if request.method == 'POST':
                insert_query = p_goods.insert(inline=True,returning=[p_goods.c.pg_id]).values(request.json)
                try:
                    result_id = await(await conn.execute(insert_query)).fetchone()
                    url_prefix = str(Config.HOST_URL) + ":" + str(Config.HOST_PORT) + "/milkproduced/" + str(result_id[0])
                except Exception as e_x:
                    print(e_x)
                    results = {"Inserted Values": "Values have been not successfully inserted",
                                "Error": str(e_x)}
                else:
                    results = {"Inserted Values": "Values have been successfully inserted"}
                return json(results, headers={'URL': url_prefix}, status=201)
            elif request.method == 'GET':
                pass


@bp_pgoods.route('/processedgoodsbydate/<pg_farm_id:string>', methods=['GET'])
async def bp_processed_goodsbydate(request, pg_farm_id):
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            results = {}
            if request.method == 'GET':
                results = {}
                select_query = p_goods.select().where(and_(p_goods.c.pg_farm_id == pg_farm_id, func.date(p_goods.c.pg_timestamp) == date.today()))
                async for row in conn.execute(select_query):
                    result = []
                    result.append({"pg_product_id": str(row.pg_product_id), "pg_quantity_produced": str(row.pg_quantity_produced), "pg_quantity_used": str(row.pg_quantity_used), "pg_farm_id": str(row.pg_farm_id), "pg_units": str(row.pg_units), "pg_milk_id": str(row.pg_milk_id), "pg_price": str(row.pg_price)})
                    results.__setitem__(str(row.pg_id), result)
                    #results.__setitem__('raw_milk_farm_id', str(results['raw_milk_farm_id']))
                    #results.__setitem__('raw_milk_product_id', str(results['raw_milk_product_id']))
                    #results.__setitem__('raw_milk_timestamp', str(results['raw_milk_timestamp']))
        return json(results, status=200)


@bp_pgoods.exception(NotFound)
async def ignore_404(request, exception):
    return json({"Not Found": "Page Not Found"}, status=404)


@bp_pgoods.exception(ServerError)
async def ignore_503(request, exception):
    return json({"Server Error": "503 internal server error"}, status=503)
