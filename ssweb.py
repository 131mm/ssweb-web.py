import web
import ssr
from web.contrib.template import render_jinja
import json

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
        name= data.get('name','')
        port=data.get('port','')
        method=data.get('method','aes-256-cfb')
        protocol=data.get('protocol','origin')
        obfs=data.get('obfs','plain')
        passwd = data.get('passwd','')
        transfer_e = data.get('transfer_e','')
        name = ss.next_user() if name=='' else name
        port = ss.next_port() if port=='' else port
        passwd = self.rand_pass() if passwd=='' else passwd
        transfer_e = 100*1073741824 if transfer_e=='' else int(transfer_e)*1073741824
        user={
        'user':name,
        'port':int(port),
        'method':method,
        'protocol':protocol,
        'obfs':obfs,
        'passwd':passwd,
        'transfer_enable':transfer_e,
        }
        if ss.add(user):
            # ss.del_rule(port)
            # ss.add_rule(port)
            # ss.save_table()
            msg='添加成功'
        else: msg='添加失败'
        return json.dumps(msg)

    def rand_pass(self):
        import random
        return ''.join([random.choice('''ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789~-_=+(){}[]^&%$@''') for i in range(8)])

## 删除用户
class delete():
    def POST(self):
        data = web.input()
        port = data.get("port")
        print(port)
        msg = '删除失败'
        if port:
            port = int(port)
            user = {'port': port, }
            print(user)
            if ss.delete(user):
                print('ok')
            else:print('err')
            # ss.del_rule(port)
            # ss.save_table()
            msg = '删除成功'
        return json.dumps(msg)

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
        transfer_e = data.get('transfer_e','')
        msg = '修改失败'
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
            if transfer_e:
                transfer_e = int(transfer_e)*1073741824
                user.update({'transfer_enable':transfer_e})
            ss.edit(user)
            msg = '修改成功'
        return json.dumps(msg)

application=app.wsgifunc()
if __name__ == '__main__':
    app.run()
