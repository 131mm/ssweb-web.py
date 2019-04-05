'''
作者：github.com/131mm
声明：模块MuJsonLoader 和MuMgr 非作者本人编写

'''
import random,os,json,base64,socket,struct
class Address():
    website='ssweb.diao.ml'
    ssr_folder='../shadowsocksr'
    config_file=ssr_folder+'/config.json'
    config_user_file=ssr_folder+'/user-config.json'
    config_user_api_file=ssr_folder+'/userapiconfig.py'
    config_user_mudb_file=ssr_folder+'/mudb.json'
    ssr_log_file=ssr_folder+'/ssserver.log'

class MuJsonLoader(object):
    def __init__(self):
        self.json = None

    def load(self, path):
        l = "[]"
        try:
            with open(path, 'rb+') as f:
                l = f.read().decode('utf8')
        except:
            pass
        self.json = json.loads(l)

    def save(self, path):
        if self.json is not None:
            output = json.dumps(self.json, sort_keys=True, indent=4, separators=(',', ': '))
            with open(path, 'a'):
                pass
            with open(path, 'rb+') as f:
                f.write(output.encode('utf8'))
                f.truncate()


class MuMgr(object):
    def __init__(self):
        self.adr=Address()
        self.config_path = self.adr.config_user_mudb_file
        self.data = MuJsonLoader()
        self.server_addr = self.getipaddr()

    def getipaddr(self, ifname='eth0'):
        ret = '127.0.0.1'
        try:
            ret = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
        except:pass
        if ret == '127.0.0.1':
            try:
                import fcntl
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                ret = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])
            except:
                pass
        return ret

    def rand_pass(self):
        return ''.join([random.choice('''ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789~-_=+(){}[]^&%$@''') for i in range(8)])

    def add(self, user):
        '''添加用户'''
        up = {
            'enable': 1,
            'u': 0,
            'd': 0,
            'method': "aes-256-cfb",
            'protocol': "origin",
            'obfs': "plain",
            'transfer_enable': 107374182400
        }
        up['passwd'] = self.rand_pass()
        up.update(user)
        self.data.load(self.config_path)
        for row in self.data.json:
            match = False
            if 'user' in user and row['user'] == user['user']:
                match = True
            if 'port' in user and row['port'] == user['port']:
                match = True
            if match:
                return
        self.data.json.append(up)
        self.data.save(self.config_path)
        return True

    def edit(self, user):
        '''编辑用户配置'''
        self.data.load(self.config_path)
        for row in self.data.json:
            match = True
            #if 'user' in user and row['user'] != user['user']:
            #    match = False
            if 'port' in user and row['port'] != user['port']:
                match = False
            if match:
                row.update(user)
                break
        self.data.save(self.config_path)
        return True

    def delete(self, user):
        '''删除用户'''
        self.data.load(self.config_path)
        index = 0
        for row in self.data.json:
            match = True
            if 'user' in user and row['user'] != user['user']:
                match = False
            if 'port' in user and row['port'] != user['port']:
                match = False
            if match:
                del self.data.json[index]
                break
            index += 1
        self.data.save(self.config_path)
        return True

    def clear_ud(self, user):
        '''清除用户已用流量'''
        up = {'u': 0, 'd': 0}
        self.data.load(self.config_path)
        for row in self.data.json:
            match = True
            if 'user' in user and row['user'] != user['user']:
                match = False
            if 'port' in user and row['port'] != user['port']:
                match = False
            if match:
                row.update(up)
                print("clear user [%s]" % row['user'])
        self.data.save(self.config_path)

    def list_user(self, user):
        self.data.load(self.config_path)
        if not user:
            for row in self.data.json:
                print("user [%s] port %s" % (row['user'], row['port']))
            return
        for row in self.data.json:
            match = True
            if 'user' in user and row['user'] != user['user']:
                match = False
            if 'port' in user and row['port'] != user['port']:
                match = False
            if match:
                muid = None
                if 'muid' in user:
                    muid = user['muid']
                print("### user [%s] info %s" % (row['user'], self.userinfo(row, muid)))


class Iptables():
    def add_rule(self,port):
        '''新建一条iptables规则，仅适用于debian'''
        commands=[]
        commands.append('iptables -I INPUT -m state --state NEW -m udp -p udp --dport {} -j ACCEPT'.format(port))
        commands.append('iptables -I INPUT -m state --state NEW -m tcp -p tcp --dport {} -j ACCEPT'.format(port))
        for c in commands:
            try:
                os.popen(c)
            except: pass

    def del_rule(self,port):
        '''删除一条iptables规则，仅适用于debian'''
        commands=[]
        commands.append('iptables -D INPUT -m state --state NEW -m udp -p udp --dport {} -j ACCEPT'.format(port))
        commands.append('iptables -D INPUT -m state --state NEW -m tcp -p tcp --dport {} -j ACCEPT'.format(port))
        for c in commands:
            try:
                os.popen(c)
            except: pass

    def save_table(self):
        '''保存iptables规则，仅适用于debian'''
        try:
            os.popen('iptables-save > /etc/iptables.up.rules')
        except: pass

class Ssr(Address,MuMgr,Iptables):
    def triffic(self,big):
        '''计算流量单位'''
        flag = 0
        units = {0: 'B', 1: 'K', 2: 'M', 3: 'G'}
        little = int(big / 1024)
        for i in range(4):
            if little:
                little = int(little / 1024)
                flag += 1
            else:
                return str(round(big/(1024 ** flag),2)) + units[flag]

    def ss_link(self,i):
        '''获取ss链接'''
        ss = i['method'] + ':' + i['passwd'] + '@' + self.website + ':' + str(i['port'])
        sslink = base64.b64encode(ss.encode('utf-8'))
        return 'ss://' + str(sslink, 'utf-8')

    def ssr_link(self, user):
        '''获取ssr链接'''
        protocol = user.get('protocol', '')
        obfs = user.get('obfs', '')
        protocol = protocol.replace("_compatible", "")
        obfs = obfs.replace("_compatible", "")
        passwd64=base64.b64encode(user['passwd'].encode('utf-8'))
        passwd64=str(passwd64, 'utf-8')
        #passwd64=user['passwd']
        link = ("%s:%s:%s:%s:%s:%s" % (self.website, user['port'], protocol, user['method'], obfs, passwd64.replace('=','')))
        return "ssr://"+str(base64.b64encode(link.encode('utf-8')),'utf-8')

    def Get_all_user(self):
        '''获取所有用户信息'''
        with open(self.config_user_mudb_file, 'r') as user_file:
            mudb = json.load(user_file)
            users=[]
            for i in mudb:
                user={
                    'ip':self.website,
                    'traffic':self.triffic(i['transfer_enable']),
                    'used':self.triffic(i['d'] + i['u']),
                    'sslink':self.ss_link(i),
                    'ssrlink':self.ssr_link(i),
                }
                user.update(i)
                users.append(user)
            return users

    def next_user(self):
        '''返回下一个可使用的username'''
        users=self.Get_all_user()
        user_name = 'user_{}'.format(str(len(users)+1))
        return user_name

    def next_port(self):
        '''返回下一个可使用的端口'''
        users=self.Get_all_user()
        port = 1024
        for user in users:
            user_port = user.get('port')
            if port < user_port:
                port = user_port
        port += 1
        return port

class User():
    methods = ['aes-256-cfb','aes-192-cfb','aes-128-cfb','rc4-md5','rc4-md5-6',
    'chacha20','chacha20-ietf','salsa20','aes-128-ctr','aes-192-ctr','aes-256-ctr']
    protocols = ['origin','auth_sha1_v4','auth_sha1_v4_compatible','auth_aes128_md5',
    'auth_aes128_sha1','auth_chain_a']
    obfses = ['plain','http_simple_compatible','http_simple',
    'tls1.2_ticket_auth_compatible',    'tls1.2_ticket_auth']
    def __init__(self,data):
        name= data.get('name','')
        port=data.get('port','')
        method=data.get('method','aes-256-cfb')
        protocol=data.get('protocol','origin')
        obfs=data.get('obfs','plain')
        passwd = data.get('passwd','')
        transfer_e = data.get('transfer_e','')

        ssr = Ssr()
        name = ssr.next_user() if name=='' else name
        port = ssr.next_port() if port=='' else port
        method = 'aes-256-cfb' if method not in self.methods else method
        protocol = 'origin' if protocol not in self.protocols else protocol
        obfs = 'plain' if obfs not in self.obfses else obfs
        passwd = ssr.rand_pass() if passwd=='' else passwd
        transfer_e = 100*1073741824 if transfer_e=='' else int(transfer_e.split('.')[0])*1073741824
        self.user ={
        'user':name,
        'port':int(port),
        'method':method,
        'protocol':protocol,
        'obfs':obfs,
        'passwd':passwd,
        'transfer_enable':transfer_e,
        }

