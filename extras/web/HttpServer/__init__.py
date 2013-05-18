"""
cherrypy torberry app
alex.a.bravo@gmail.com
"""

import os
import sys
import cherrypy
import PAM
from jinja2 import Environment, FileSystemLoader
from torcon import TorCon
from cherrypy.lib.static import serve_file
from subprocess import *

env = Environment(loader=FileSystemLoader('/root/HttpServer/templates'))

def authenticate():
	user = cherrypy.session.get('user',None)
	if not user:
		raise cherrypy.HTTPRedirect('/?errMsg=You%20are%20not%20logged%20in')

cherrypy.tools.authenticate = cherrypy.Tool('before_handler', authenticate)

class HttpServer:
	@cherrypy.expose
	def index(self, errMsg=''):
		user = cherrypy.session.get('user',None)
		if not user:
			tmpl = env.get_template('login.tpl')
			if not errMsg:
				errMsg = ''
			return tmpl.render(errMsg=errMsg)
		else:	
			tmpl = env.get_template('frame.tpl')
			return tmpl.render()

	@cherrypy.expose
	def login(self,user,passwd,ok):
		def pam_conv(aut, query_list, user_data):
		        resp = []
		        for item in query_list:
		        	query, qtype = item
		                                
		                # If PAM asks for an input, give the password
		                if qtype == PAM.PAM_PROMPT_ECHO_ON or qtype == PAM.PAM_PROMPT_ECHO_OFF:
		         	       resp.append((str(passwd), 0))
		                                                                               
		                elif qtype == PAM.PAM_PROMPT_ERROR_MSG or qtype == PAM.PAM_PROMPT_TEXT_INFO:
		                       resp.append(('', 0))
		                                                                                                                            
		        return resp

		auth = PAM.pam()
		auth.start('login')
		auth.set_item(PAM.PAM_USER, user)
		auth.set_item(PAM.PAM_CONV, pam_conv)
		#if user == 'root' and passwd == 'raspberry':
		try:
			auth.authenticate()
			auth.acct_mgmt()
		except PAM.error,resp:	
			raise cherrypy.HTTPRedirect('/?errMsg=Invalid%20credentials')
		except:
			raise cherrypy.HTTPRedirect('/?errMsg=Invalid%20credentials')
				
		cherrypy.session['user'] = user
		return self.index() 

	@cherrypy.expose
	@cherrypy.tools.authenticate()	
	def logout(self):
		cherrypy.session.clear()
		tmpl = env.get_template('frame.tpl')
		return tmpl.render(msg="Session terminated")
		
				
	@cherrypy.expose
	@cherrypy.tools.authenticate()	
	def torStat(self):
		torcon = TorCon()
		logListener = torcon.LogsListener()
		conn = torcon.myconnect(logListener)
		if conn:
		        version = conn.get_info("version")["version"]
		        config = conn.get_info("config-file")["config-file"] 
		        extip = conn.get_info("address")["address"]
		        live = conn.is_live()
		        circuit = conn.get_info("circuit-status")["circuit-status"]
		        flog = open("/var/log/tor/notices.log","r")
		        logs = flog.read()
		        tmpl = env.get_template('status.tpl')
		        return tmpl.render(version=version, config=config,extip=extip,live=live,circuit=circuit,logs=logs)
		else:
			tmpl = env.get_template('frame.tpl')
			return tmpl.render(msg="TOR doesn't seem to be running")

	@cherrypy.expose
	@cherrypy.tools.authenticate()	
        def renewip(self):
                torcon = TorCon()
                logListener = torcon.LogsListener()
                conn = torcon.myconnect(logListener)
                if conn:
                        conn.sendAndRecv('signal newnym\r\n')
                        tmpl = env.get_template('frame.tpl')
                        return tmpl.render(msg="IP Renew requested")

        @cherrypy.expose
	@cherrypy.tools.authenticate()	
        def halt(self):
        	torcon = TorCon()
        	logListener = torcon.LogsListener()
        	conn = torcon.myconnect(logListener)
        	if torcon:
        		conn.sendAndRecv('signal halt\r\n')
        		tmpl = env.get_template('frame.tpl')
        		return tmpl.render(msg="TOR halted")

        @cherrypy.expose
	@cherrypy.tools.authenticate()	
        def sysStat(self):
        	uptime = Popen("uptime", stdout=PIPE, shell=True).stdout.read()
        	uname = Popen("uname -a", stdout=PIPE, shell=True).stdout.read()
        	free = Popen("free -m | grep Mem | cut -d: -f2", stdout=PIPE, shell=True).stdout.read()
        	disk = Popen("df -h", stdout=PIPE, shell=True).stdout.read()
        	net = Popen("ip a", stdout=PIPE, shell=True).stdout.read()
        	modules = Popen("lsmod", stdout=PIPE, shell=True).stdout.read()
        	dmesg = Popen("dmesg", stdout=PIPE, shell=True).stdout.read()
        	iptables = Popen("iptables -L && iptables -t nat -L", stdout=PIPE, shell=True).stdout.read()
        	sysctl = Popen("sysctl -a", stdout=PIPE, shell=True).stdout.read()
      		tmpl = env.get_template('sysstatus.tpl')
       		return tmpl.render(uptime=uptime,uname=uname,free=free,disk=disk,net=net,modules=modules,dmesg=dmesg,iptables=iptables,sysctl=sysctl)
        	
	@cherrypy.expose
	@cherrypy.tools.authenticate()	
	def torCtl(self):
		tmpl = env.get_template('control.tpl')
		return tmpl.render()

	@cherrypy.expose
	@cherrypy.tools.authenticate()	
	def restoreConfig(self):
		tmpl = env.get_template('uconfig.tpl')
		return tmpl.render()	

	@cherrypy.expose	
	@cherrypy.tools.authenticate()	
	def upload(self,conffile):
		size = 0
		while True:
			data = conffile.file.read(8192)
		        if not data:
		        	break
		        size += len(data)
		        cfig = ""
		        cfig = cfig + data
		if conffile.filename != "torberry.conf":
			tmpl = env.get_template('frame.tpl')
			return tmpl.render(msg="You aren't uploading a torberry conf file. Ensure that filename is torberry.conf")
		f = open("/etc/torberry.conf","w")
		f.write(cfig)
		f.close()
		tmpl = env.get_template('ufile.tpl')	
		return tmpl.render(length=size,filename=conffile.filename,filetype=conffile.content_type)

		
	@cherrypy.expose
	@cherrypy.tools.authenticate()	
	def downloadConfig(self):
		return serve_file("/etc/torberry.conf", "application/x-download", "attachment")
		
	@cherrypy.expose
	@cherrypy.tools.authenticate()	
	def reset(self):
		os.system("reboot")
		tmpl = env.get_template('reset.tpl')
		return tmpl.render()
		
settings={
            '/': {
            	    'tools.sessions.on': True,
            	    'tools.sessions.timeout': 60,
            	    'tools.sessions.storage_type': "file",
            	    'tools.sessions.storage_path': "/var/log/tor/",
                 }
}
cherrypy.config.update(settings)

httpserver = HttpServer()

if __name__ == '__main__':
	cherrypy.config.update({'server.socket_host': '0.0.0.0','server.socket_port': 8080})
	root = Root()
	cherrypy.quickstart(root)

