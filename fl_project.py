from flask import Flask, make_response, redirect, abort, render_template
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap


# 初始化app，接收所有客户端的请求
app = Flask(__name__)
bootstrap = Bootstrap(app)
# manager = Manager(app)


# 普通的交互设计
@app.route('/page1')
def page1():
    return '<h1>Hello World!</h1>'


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
    return render_template('index.html')


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


# 自定义错误类型
@app.errorhandler(404)
def page10(name):
    name = name if name != '' else ''
    return render_template('bootstrap.html', name=name)

# 主函数
if __name__ == '__main__':
    app.run()
    # manager.run()
