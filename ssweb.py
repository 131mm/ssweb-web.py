import web
import ssr
from web.contrib.template import render_jinja

## 路由
urls=(
    '/', 'home',
    '/add', 'add',
    '/delete', 'delete',
    '/edit','edit'
)

app=web.application(urls,globals())

## 使用jinja渲染
render=render_jinja(
    'templates',
    encoding='utf-8'
)

ss=ssr.ssr()

## 主页
class home():
    def GET(self):
        users = ss.Get_all_user()
        return render.home(users=users)

## 添加用户
class add():
    def POST(self):
        data=web.input()
        user={
        'user'    :data.get('name',''),
        'port'    :data.get('port'),
        'method'  :data.get('method'),
        'protocol':data.get('protocol'),
        'obfs'    :data.get('obfs')
        }
        passwd = data.get('passwd','')
        if passwd:
            user.update({'passwd':passwd})
        elif passwd == '':
            passwd = self.rand_pass()
            user.update({'passwd': passwd})
        if not user.get('user') or user.get('user')=='':
            user_name=ss.next_user()
            user.update({'user':user_name})
        if not user.get('port') or user.get('port')==0:
            port=ss.next_port()
            user.update({'port':port})
        flag, code = 'no',1
        port = user.get('port')
        if user.get('user') and port:
            if ss.add(user):
                ss.del_rule(port)
                ss.add_rule(port)
                ss.save_table()
                flag, code = 'ok', 0
        return {'msg': flag, 'code': code}

    def rand_pass(self):
        import random
        return ''.join([random.choice('''ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789~-_=+(){}[]^&%$@''') for i in range(8)])

## 删除用户
class delete():
    def POST(self):
        data = web.input()
        port = data.get("port")
        flag, code = 'no',1
        if port:
            port = int(port)
            user = {'port': port, }
            ss.delete(user)
            ss.del_rule(port)
            ss.save_table()
            flag, code = 'ok', 0
        return {'msg': flag, 'code': code}

## 修改用户配置
class edit():
    def POST(self):
        data = web.input()
        name = data.get('name', '')
        port=data.get('port','')
        passwd=data.get('passwd','')
        method=data.get('method','')
        protocol=data.get('protocol','')
        obfs=data.get('obfs','')
        flag, code = 'no',1
        if port:
            port=int(port)
            if port<65534:
                user={'port':port,}
            else:return {'code':1,'msg':'error'}
            if name:
                user.update({'user':name})
            if passwd:
                user.update({'passwd':passwd})
            if method:
                user.update({'method':method})
            if protocol:
                user.update({'protocol':protocol})
            if obfs:
                user.update({'obfs':obfs})
            ss.edit(user)
            flag, code = 'ok', 0
        return {'msg': flag, 'code': code}

application=app.wsgifunc()
if __name__ == '__main__':
    app.run()
