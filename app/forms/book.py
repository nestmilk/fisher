from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired, Regexp


class SearchForm(Form):
    q = StringField(validators=[DataRequired(),Length(min=1,max=30,message='长度必须介于1-30')])
    page = IntegerField(validators=[NumberRange(min=1,max=99,message='范围必须介于1-99')], default=1)

class DriftForm(Form):
    recipient_name = StringField('收件人姓名', validators=[DataRequired(message='收件人姓名不可以为空'),
                                                      Length(min=2,max=20,message='收件人姓名长度必须在2到20个字符之间')])
    mobile = StringField('手机号', validators=[DataRequired(message='手机号不可以为空'),
                                                Regexp('^1[0-9]{10}$',0,'请输入正确的手机号')])
    message = StringField('留言')
    address=StringField('邮寄地址',validators=[DataRequired(message='邮寄地址不可以为空'),
                                           Length(min=10,max=70,message='邮寄地址长度为10到70个字符')])