import web
import sys
import ssr
from web.contrib.template import render_jinja
#sys.path.append('..')

urls=(
    '/', 'home',
    '/add', 'add',
    'delete', 'delete',
    'edit','edit'
)

app=web.application(urls,globals())

render=render_jinja(
    'templates',
    encoding='utf-8'
)

class users():
    name = ''
    port = ''
    passwd =''
    method =''
    protocol=''
    obfs = ''

ss=ssr.ssr()
class home():
    def GET(self):
        users=ss.Get_all_user()
        return render.home(users=users)

class add():
    def POST(self):
        data=web.data().decode('utf-8')
        data=data.split('&')
        user={
        'user'    :data[0][5:],
        'port'    :data[1][5:],
        'passwd'  :data[2][7:],
        'method'  :data[3][7:],
        'protocol':data[4][9:],
        'obfs'    :data[5][5:]
        }
        msg='no'
        print(user)
        if user.get('user') and user.get('port'):
            if ss.add(user):
                msg='ok'
        return {'msg':msg}

class delete():
    def POST(self):
        return

class edit():
    def POST(self):
        return

if __name__ == '__main__':
    app.run()
