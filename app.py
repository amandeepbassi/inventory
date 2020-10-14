from sanic import Sanic
from milk_produced import milk_produce
from processed_goods import bp_pgoods
from net_milk_price import bp_milk_price
from processed_goods_price import bp_pg_price
#from inventory_api import apibp
from milk_produced import bp_milk_produced
from net_stock import bp_net_stock
from sanic_jwt import Initialize


app = Sanic(name='inventory_microservice')
Initialize(bp_pgoods, app=app, auth_mode=False)
Initialize(bp_pg_price, app=app, auth_mode=False)
Initialize(bp_milk_produced, app=app, auth_mode=False)
Initialize(bp_milk_price, app=app, auth_mode=False)
Initialize(bp_net_stock, app=app, auth_mode=False)
app.config.from_object('config.Config')
app.blueprint(bp_pgoods)
app.blueprint(bp_pg_price)
app.blueprint(bp_milk_produced)
app.blueprint(bp_milk_price)
app.blueprint(bp_net_stock)

if __name__ == '__main__':
    app.run(host=app.config.HOST_URL, port=app.config.HOST_PORT)