from sanic.response import json
from aiopg.sa import create_engine
from config import Config
from model import connection, net_stock_value
from sanic import Blueprint
from sanic.exceptions import NotFound, ServerError
from sqlalchemy.sql import select, func
from sqlalchemy import and_
import json as regularjson
from sanic_jwt.decorators import protected


bp_net_stock = Blueprint('net_stock_blueprint')


@bp_net_stock.route(uri='/netstock/<product_id:string>', methods=['GET'])
@protected(initialized_on=bp_net_stock)
async def net_stock(request, product_id):
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            results = {}
            select_query = select([func.sum(net_stock_value.c.net_stock_product_quantity)]).where(net_stock_value.c.net_stock_product_id == product_id).group_by(net_stock_value.c.net_stock_product_id)
            t1 = await conn.begin(isolation_level='REPEATABLE READ')
            total_products_count = await(await conn.execute(select_query)).fetchone()

            await t1.commit()

            results = {"product_count": str(total_products_count[0])}
        return json(results, status=200)


@bp_net_stock.route('/updatenetstock', methods=['POST'])
@protected(initialized_on=bp_net_stock)
async def update_net_stock(request):
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            results = {}
            t1 = await conn.begin(isolation_level='SERIALIZABLE')
            select_query = select([net_stock_value.c.net_stock_product_quantity]).where(and_(net_stock_value.c.net_stock_product_id == request.json['net_stock_product_id'], net_stock_value.c.net_stock_vendor_id == request.json['net_stock_vendor_id']))          
            try:
                #select_query = net_stock_value.select().where(net_stock.c.net_stock_product_id == request.json['net_stock_product_id'])
                total_products_count = await(await conn.execute(select_query)).fetchone()
                products_count = total_products_count[0]

                if request.json['transaction_type'] == 'ADD':
                    products_count = products_count + int(request.json['product_update'])
                elif request.json['transaction_type'] == 'SUB':
                    products_count = products_count - int(request.json['product_update'])          
                update_query = net_stock_value.update().where(and_(net_stock_value.c.net_stock_product_id == request.json['net_stock_product_id'], net_stock_value.c.net_stock_vendor_id == request.json['net_stock_vendor_id'])).values(net_stock_product_quantity=products_count)
                query_result = await conn.execute(update_query)
                results = {"Updated Values": "values have been successfully updated"}
            except Exception as e:
                print(e)
                results = {"Updated Values": "Values have not been successfully updated"}
            await t1.commit()
        return json(results, status=200)


@bp_net_stock.exception(NotFound)
@protected(initialized_on=bp_net_stock)
async def ignore_404(request, exception):
    return json({"Not Found": "Page Not Found"}, status=404)


@bp_net_stock.exception(ServerError)
@protected(initialized_on=bp_net_stock)
async def ignore_503(request, exception):
    return json({"Server Error": "503 internal server error"}, status=503)

