from collections import namedtuple

from flask import current_app
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, desc, func
from sqlalchemy.orm import relationship

from app.models.base import Base

from app.spider.yushu_book import YuShuBook
from app.models.base import db

# EachGiftWishCount = namedtuple('EachGiftWishCount',['count','isbn'])

class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))
    launched = Column(Boolean, default=False)

    def is_yourself_gift(self,uid):
        return True if self.uid == uid else False

    @classmethod
    def get_user_gifts(cls,uid):
        gifts =cls.query.filter_by(uid=uid, launched=False).order_by(
            desc(cls.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls,isbn_list):
        from app.models.wish import Wish
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False,
            Wish.isbn.in_(isbn_list),
            Wish.status == 1).group_by(
            Wish.isbn).all()
        count_list = [{'count': w[0],'isbn': w[1]} for w in count_list]
        return  count_list

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first()

    @classmethod
    def recent(cls):
        recent_gifts = Gift.query.group_by(
            cls.isbn).order_by(
            desc(cls.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).all()
        return recent_gifts