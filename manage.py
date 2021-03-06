# 脚本数据文件
import random

from nowstagram import app,db
from flask_script import Manager
from nowstagram.models import User,Image,Comment
import unittest

manager=Manager(app)

@manager.command
def run_test():
    db.drop_all()
    db.create_all()
    tests = unittest.TestLoader().discover('./')
    unittest.TextTestRunner().run(tests)

def get_image_url():
    return 'http://images.nowcoder.com/head/'+str(random.randint(0,1000))+'m.png'

@manager.command
def init_database():
    db.drop_all()
    db.create_all()
    #添加数据 db.session.add(对象实例化)
    for i in range(0, 100):
        db.session.add(User('牛客' +str(i), 'a'+str(i)))

        for j in range(0, 3): #每人发三张图
            db.session.add(Image(get_image_url(), i + 1))
            for k in range(0, 3):
                db.session.add(Comment('这是一条评论'+str(k), 1+3*i+j, i+1))
    db.session.commit()

    #更新
    for i in range(0,100,10):
        #方法1：通过update函数
        User.query.filter_by(id=i+1).update({'username':'牛新'+str(i)})

    for i in range(1,100,2):
        #方法2：通过设置属性
        u=User.query.get(i+1)
        u.username='n'+str(i*i)
    db.session.commit()

    #删除
    for i in range(50,100,2):
        #方法1：
        Comment.query.filter_by(id=i+1).delete()
    for i in range(51,100,2):
        #方法2：
        comment=Comment.query.get(i+1)
        db.session.delete(comment)
    db.session.commit()

    #查询
    print(1,User.query.all())
    print(2,User.query.get(3))
    print(3,User.query.filter_by(id=2).first())
    print(4,User.query.order_by(User.id.desc()).offset(1).limit(2).all())
    #分页查询
    print(5,User.query.paginate(page=1,per_page=10).items)
    u=User.query.get(1)
    print(6,u.images)
    print(7,Image.query.get(1).user)

if __name__=='__main__':
    manager.run()