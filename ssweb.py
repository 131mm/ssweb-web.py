import web
import ssr
from web.contrib.template import render_jinja
import json

## 路由
urls=(
    '/', 'home',
    '/add', 'add',
    '/delete', 'delete',
    '/edit','edit',
    '/visitor','visitor'
)

app=web.application(urls,globals())

## 使用jinja渲染
render=render_jinja(
    'templates',
    encoding='utf-8'
)

ss=ssr.Ssr()

## 主页
class home():
    def GET(self):
        users = ss.Get_all_user()
        return render.home(users=users)

## 主页
class visitor():
    def GET(self):
        users = ss.Get_all_user()
        return render.user(users=users)


## 添加用户
class add():
    def POST(self):
        data=web.input()
        user = ssr.User(data).user
        port = user.get('port')
        if ss.add(user):
            ss.del_rule(port)
            ss.add_rule(port)
            ss.save_table()
            msg='添加成功'
        else: msg='添加失败'
        return json.dumps(msg)


## 删除用户
class delete():
    def POST(self):
        data = web.input()
        port = data.get("port")
        msg = '删除失败'
        if port:
            port = int(port)
            user = {'port': port, }
            if ss.delete(user):
                ss.del_rule(port)
                ss.save_table()
                msg = '删除成功'
        return json.dumps(msg)

## 修改用户配置
class edit():
    def POST(self):
        data = web.input()
        port=data.get('port','')
        user = ssr.User(data).user
        msg = '修改失败'
        if port:
            port=int(port)
            if port<65534 and port >0:
                user.update({'port':port})
            else:return {'code':1,'msg':'error'}
            ss.edit(user)
            msg = '修改成功'
        return json.dumps(msg)

application=app.wsgifunc()
if __name__ == '__main__':
    app.run()
