import web
import ssr
from web.contrib.template import render_jinja

urls=(
    '/', 'home',
    '/add', 'add',
    '/delete', 'delete',
    '/edit','edit'
)

app=web.application(urls,globals())

render=render_jinja(
    'templates',
    encoding='utf-8'
)

class users():
    name = ''
    port = ''
    passwd = ''
    method = ''
    protocol = ''
    obfs = ''

ss=ssr.ssr()
class home():
    def GET(self):
        users = ss.Get_all_user()
        return render.home(users=users)

class add():
    def POST(self):
        data=web.input()
        user={
        'user'    :data.get('name'),
        'port'    :int(data.get('port'),
        'passwd'  :data.get('passwd'),
        'method'  :data.get('method'),
        'protocol':data.get('protocol'),
        'obfs'    :data.get('obfs')
        }
        flag = 'no'
        code = 1
        port = user.get('port')
        if user.get('user') and port:
            if ss.add(user):
                ss.del_rule(port)
                ss.add_rule(port)
                ss.save_table()
                flag = 'ok'
                code = 0
        return {'msg': flag, 'code': code}

class delete():
    def POST(self):
        data = web.input()
        port = data.get("port")
        flag = 'no'
        code = 1
        if port:
            port = int(port)
            user = {'port': port, }
            ss.delete(user)
            ss.del_rule(port)
            ss.save_table()
            flag = 'ok'
            code = 0
        return {'msg': flag, 'code': code}

class edit():
    def POST(self):
        data = web.input()
        name = data.get('name', '')
        port=data.get('port','')
        passwd=data.get('passwd','')
        method=data.get('method','')
        protocol=data.get('protocol','')
        obfs=data.get('obfs','')
        flag = 'no'
        code = 1
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
            flag = 'ok'
            code = 0
        return {'msg': flag, 'code': code}
application=app.wsgifunc()
if __name__ == '__main__':
    app.run()
