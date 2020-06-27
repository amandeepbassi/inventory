from sanic import Sanic
app = Sanic('__name__')

database_name = 'inventory'
database_host = 'localhost'
database_user = 'postgres'
database_password = '1234'
connection = 'postgres://{0}:{1}@{2}/{3}'.format(database_user,
                                                 database_password,
                                                 database_host,
                                                 database_name)

from inventory_service.processed_goods import pgoods
from inventory_service.inventory_api import apibp
from inventory_service.milk_produced import milkp
app.blueprint(pgoods)
app.blueprint(apibp)
app.blueprint(milkp)


