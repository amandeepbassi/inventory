from sanic.response import json
from model import net_stock
from config import Config
from sanic import Blueprint

bp_pgoods = Blueprint('net_stock_blueprint')