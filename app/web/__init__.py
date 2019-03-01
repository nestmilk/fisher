
# 这里有循环引用，但是也可以
# from flask import Blueprint
#
# # web = Blueprint('web',__name__)
#
# print('Blueprint id()=' + str(id(web)))
from flask import render_template

from app.web.blueprint import web


@web.app_errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


from . import book
from . import auth
from . import drift
from . import gift
from . import main
from . import wish