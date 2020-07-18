from sanic import Sanic
from milk_produced import milk_produce
from processed_goods import bp_pgoods
#from inventory_api import apibp
from milk_produced import bp_milk_produced

app = Sanic(name='inventory_microservice')
app.config.from_object('config.Config')
app.blueprint(bp_pgoods)
#app.blueprint(apibp)
app.blueprint(bp_milk_produced)

if __name__ == '__main__':
    app.run(host=app.config.HOST_URL, port=app.config.HOST_PORT)