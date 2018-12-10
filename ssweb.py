import web
import sys
import ssr
from web.contrib.template import render_jinja
#sys.path.append('..')

urls=(
    '/', 'home',
    'add', 'add',
    'delete', 'delete',
    'edit','edit'
)

app=web.application(urls,globals())

render=render_jinja(
    'templates',
    encoding='utf-8'
)

ss=ssr.ssr()
class home():
    def GET(self):
        users=ss.Get_all_user()
        return render.home(users=users)

class add():
    def POST(self):
        return

class delete():
    def POST(self):
        return

class edit():
    def POST(self):
        return

if __name__ == '__main__':
    app.run()
