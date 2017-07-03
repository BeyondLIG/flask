#数据模型

from nowstagram import db,login_manager
from datetime import datetime
import random

class User(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(80),unique=True)
    password=db.Column(db.String(32))
    salt=db.Column(db.String(32))
    head_url=db.Column(db.String(256))
    images=db.relationship('Image',backref='user',lazy='dynamic')


    def __init__(self,username,password,salt=''):
        self.username=username
        self.password=password
        self.salt=salt
        self.head_url='http://images.nowcoder.com/head'+str(random.randint(0,1000))+'t.png'

    def __repr__(self):
        return '<User %d %s>'% (self.id,self.username)

    #Flask Login 接口
    def is_authenticated(self):
        print('is_authenticated')
        return True

    def is_active(self):
        print('is_active')
        return True

    def is_anonymous(self):
        print('is_anonymous')
        return True

    def get_id(self):
        print('get_id')
        return self.id




class Image(db.Model):
        id=db.Column(db.Integer,primary_key=True,autoincrement=True)
        url=db.Column(db.String(512))
        user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
        created_date=db.Column(db.DateTime)
        comments=db.relationship('Comment')

        def __init__(self,url,user_id):
            self.url=url
            self.user_id=user_id
            self.created_date=datetime.now()

        def __repr__(self):
            return '<Image %d %s>' % (self.id,self.url)


class Comment(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    content=db.Column(db.String(1024))
    image_id=db.Column(db.Integer,db.ForeignKey('image.id'))
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    status=db.Column(db.Integer,default=0)
    user=db.relationship('User')

    def __init__(self,content,image_id,user_id):
        self.content=content
        self.image_id=image_id
        self.user_id=user_id

    def __repr__(self):
        return '<Comment %d %s>' % (self.id,self.content)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)