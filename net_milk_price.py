from sanic.response import json
from aiopg.sa import create_engine
from config import Config
from model import connection, milk_price
from sanic import Blueprint
from sanic.exceptions import NotFound, ServerError
from sqlalchemy.sql import select, func
from sqlalchemy import and_


bp_milk_price = Blueprint('milk_price')

@bp_milk_price.route('/milkprice/<rmp_farm_id:string>', methods=['GET'])
async def bp_get_milk_price(request, rmp_farm_id):
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            results = {}
            date_value = request.json['rmp_date']
            select_query = milk_price.select().where(and_(milk_price.c.rmp_farm_id==rmp_farm_id, milk_price.c.rmp_date == date_value))
            async for row in conn.execute(select_query):
                results.update(row)
                results.__setitem__('rmp_id', str(results['rmp_id']))
                results.__setitem__('rmp_farm_id', str(results['rmp_farm_id']))
                results.__setitem__('rmp_product_id', str(results['rmp_product_id']))
                results.__setitem__('rmp_date', str(results['rmp_date']))
        return json(results, status=200)


@bp_milk_price.exception(NotFound)
async def ignore_404(request, exception):
    return json({"Not Found": "Page Not Found"}, status=404)


@bp_milk_price.exception(ServerError)
async def ignore_503(request, exception):
    return json({"Server Error": "503 internal server error"}, status=503)

