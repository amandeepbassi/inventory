from sanic.response import json
from aiopg.sa import create_engine
from config import Config
from model import connection, p_goods_price
from sanic import Blueprint
from sanic.exceptions import NotFound, ServerError
from sqlalchemy.sql import select, func
from sqlalchemy import and_
from sanic_jwt.decorators import protected


bp_pg_price = Blueprint('pg_price')


@bp_pg_price.route(uri='/pgprice/<pgp_farm_id:string>', methods=['GET'])
@protected(initialized_on=bp_pg_price)
async def bp_get_milk_price(request, pgp_farm_id):
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            results = {}
            date_value = request.json['pgp_date']
            select_query = p_goods_price.select().where(and_(p_goods_price.c.pgp_farm_id==pgp_farm_id, p_goods_price.c.pgp_date == date_value))
            async for row in conn.execute(select_query):
                results.update(row)
                results.__setitem__('pgp_id', str(results['pgp_id']))
                results.__setitem__('pgp_farm_id', str(results['pgp_farm_id']))
                results.__setitem__('pgp_product_id', str(results['pgp_product_id']))
                results.__setitem__('pgp_date', str(results['pgp_date']))
                results.__setitem__('pgp_milk_id', str(results['pgp_milk_id']))
        return json(results, status=200)


@bp_pg_price.exception(NotFound)
@protected(initialized_on=bp_pg_price)
async def ignore_404(request, exception):
    return json({"Not Found": "Page Not Found"}, status=404)


@bp_pg_price.exception(ServerError)
@protected(initialized_on=bp_pg_price)
async def ignore_503(request, exception):
    return json({"Server Error": "503 internal server error"}, status=503)
