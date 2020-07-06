from sanic import Sanic
app = Sanic('__name__')

from processed_goods import pgoods
from inventory_api import apibp
from milk_produced import milkp
app.blueprint(pgoods)
app.blueprint(apibp)
app.blueprint(milkp)

app.run(host='0.0.0.0', port=8000)