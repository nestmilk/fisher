from flask import jsonify, request, render_template, flash

#导入当前包下__init__中的web蓝图
# from .blueprint import web
from flask_login import current_user

from app.forms.book import SearchForm
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.book import BookViewModel, BookCollection
from app.view_models.trade import TradeInfo
from .blueprint import web
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
import json



@web.route("/book/search")
def search():
    '''
    :param q: 普通关键字 isbn
    :param page:
    :return:
    '''
    # q = request.args['q']
    # page = request.args['page']
    form = SearchForm(request.args)
    books = BookCollection()

#form当中有errors的dict类型，form.errors.q
    if form.validate():
        #strip去除前后空格
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q,page)

        books.fill(yushu_book, q)
    else:
        # return jsonify(form.errors)
        flash('搜索的关键字不符合要求，请重新输入关键字')
    return render_template('search_result.html', books=books)

@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gifts = False
    has_in_wishes = False

    # 取书籍详情数据
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first())

    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id,
                             isbn=isbn,
                             launched=False).first():
            has_in_gifts=True
        if Wish.query.filter_by(uid=current_user.id,
                             isbn=isbn,
                             launched=False).first():
            has_in_wishes=True


    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes= Wish.query.filter_by(isbn=isbn, launched=False).all()

    trade_gifts_model = TradeInfo(trade_gifts)
    trade_wishes_model = TradeInfo(trade_wishes)

    return render_template('book_detail.html',
                           book=book,
                           wishes=trade_wishes_model,
                           gifts=trade_gifts_model,
                           has_in_gifts=has_in_gifts,
                           has_in_wishes=has_in_wishes)


@web.route('/test')
def test():
    r = {
        'name': '',
        'age': 20
    }

    return render_template('test.html',data=r)