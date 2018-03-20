from flask import Flask, make_response, redirect, abort, render_template, url_for, session, flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask.ext.sqlalchemy import SQLAlchemy


# 初始化app，接收所有客户端的请求
app = Flask(__name__)
# 设置跨站请求防护（csrf）
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

# manager = Manager(app)


# 定义一个简单的表单
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


# 定义角色表类
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)

    def __repr__(self):
        return '<Role %r>' % self.name


# 定义用户表类
class User(db.Model):
    __teblename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)

    def __repr__(self):
        return '<User %r>' % self.username


# 普通的交互设计（url_for打印出当前url的绝对路径和相对路径）
@app.route('/')
@app.route('/page1')
def page1():
    return '<h1>Hello World!</h1>' + '————' + url_for('page1', _external=True) + '————' + url_for('page1')


# 自己创造response的交互，还可以设置cookie
@app.route('/page2')
def page2():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response


# 页面重定向
@app.route('/page3')
def page3():
    return redirect('http://www.baidu.com')


# abort错误处理，直接返回404页面，遇到abort函数强制返回，后续不再执行
@app.route('/page4')
def page4():
    a = 2
    if a == 1:
        abort(404)
    return '<h1>Hello, %s</h1>' % a


# 空模板
@app.route('/page5')
def page5():
    try:
        return render_template('index.html')
    except Exception as e:
        return render_template('500.html')


# 模板传入变量
@app.route('/page6/<name>')
def page6(name):
    user = {'name': name}
    return render_template('index.html', name=user)


# 模板中的循环及if判断句式，均在模板中体现
@app.route('/page7')
def page7():
    tem_list = list(range(5))
    tem_dic = dict(zip(range(5), range(15, 20)))
    return render_template('index2.html', tem_list=tem_list, tem_dic=tem_dic)


# 模板继承
@app.route('/page8')
def page8():
    return render_template('extend.html')


# 基于bootstrap的模板继承
@app.route('/page9/<name>')
def page9(name):
    name = name if name != '' else ''
    return render_template('bootstrap.html', name=name)


# 自定义404错误类型（访问一个不存在的页面就会自动跳转到404页面）
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# 自定义500错误类型
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# 跨站请求
@app.route('/page11', methods=['GET', 'POST'])
def page11():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('form.html', form=form, name=name)


# post-->重定向-->get
@app.route('/page12', methods=['GET', 'POST'])
def page12():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        print(form.name.data)
        return redirect(url_for('page12'))
    return render_template('form.html', form=form, name=session.get('name'))


# 登录失败后的响应
@app.route('/page13', methods=['GET', 'POST'])
def page13():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('page13'))
    return render_template('form.html', form=form, name=session.get('name'))




# 主函数
if __name__ == '__main__':
    app.run()
    # manager.run()
