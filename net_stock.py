from sanic.response import json
from aiopg.sa import create_engine
from config import Config
from model import connection, net_stock
from sanic import Blueprint
from sanic.exceptions import NotFound, ServerError
from sqlalchemy.sql import select, func
from sqlalchemy import and_

bp_net_stock = Blueprint('net_stock_blueprint')


@bp_net_stock.route('/netstock/<product_id:string>', methods=['GET'])
async def net_stock(request, product_id):
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            results = {}
            select_query = select([func.sum(net_stock.c.net_stock_product_quantity)]).where(net_stock.c.net_stock_product_id == product_id).group_by(net_stock.c.net_stock_product_id)
            t1 = await conn.begin(isolation_level='REPEATABLE READ')
            total_products_count = await(await conn.execute(select_query)).fetchone()

            await t1.commit()

            results ={"product_count": str(total_products_count[0])}
        return json(results, status=200)
