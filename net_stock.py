from sanic.response import json
from model import net_stock
from config import Config
from sanic import Blueprint

bp_net_stock = Blueprint('net_stock_blueprint')


@bp_net_stock.route(uri='/checkquantity', methods=['GET'])
