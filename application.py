# -*- coding: utf-8 -*-
import cherrypy
import json
import os
import sys
import codecs
import re
import xml.etree.cElementTree as ET
import re        
import time 
global errors , doubles , scann , noscann
scann   = []
errors  = []
doubles = []
noscann = []

def wrm():
    
    pass
        
try:
    approot = os.path.dirname(os.path.abspath(__file__))
except NameError:  # We are the main script, not a module
    approot = os.path.dirname(os.path.abspath(sys.argv[0]))
current_dir = approot
class HelloWorld(object):
    global errors , doubles , scann , noscann
    @cherrypy.expose
    def check(self,stext =None):
        if (os.path.isfile('./uploads/rep.xml')):
            page = ''.join(codecs.open('check.html','r','utf-8').readlines())
            page = page.replace('{{res}}'.decode("utf-8"),'%d'%len(noscann))
            XML_FILE = open('./uploads/rep.xml','r')
            tree = ET.ElementTree(file = XML_FILE)
            root = tree.getroot()

            if stext:
                for child in root.iter():
                    if len(re.findall(u'[A-Z]{4}/\d{6}/%04d/\d{2}'%int(stext), child.attrib.get('RefNo','')))>0:
                        scann.count(child.attrib) == 0 and scann.append(child.attrib)
                        scann.count(child.attrib) == 1 and doubles.append(child.attrib.get('RefNo',''))
                        scann.count(child.attrib) ==-1 and errors.append(stext)
                        
                        child.attrib['status'] ='scann'
                        
            tree.write('./uploads/rep.xml')
            XML_FILE.close()
                        
            page = page.replace('{{scan}}'.decode("utf-8"),'%d'%len(scann))
            page = page.replace('{{double}}'.decode("utf-8"),'%s'%('<br>'.join((doubles))))
            page = page.replace('{{error}}'.decode("utf-8"),'%d'%len(errors))
            return page
        return 'А вы загрузили файл ? '
    
    @cherrypy.expose
    def index(self):
        page_index = open('index.html','r')
        return page_index
    
    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def fileloader(self,upl):
        global errors , doubles , scann , noscann
        scann   = []
        errors  = []
        doubles = []
        noscann = []
        myFile = upl
        size = 0
        
        res = ''
        if myFile==None:
            return '-------------'
        while True:
            data = myFile.file.read()
            
            res +=data
            if not data:
                break
            size += len(data)
            if data :
                f = open('./uploads/rep.xml','w',)
                f.write(res)
                f.close()
                XML_FILE = open('./uploads/rep.xml','r')
                tree = ET.ElementTree(file = XML_FILE)
                
                root = tree.getroot()
                for child in root.iter():
                    if len(child.attrib)>0:
                        if child.attrib.get('status','')=='' or child.attrib.get('status','')=='noscann':
                            child.attrib['status'] = 'noscann'
                            noscann.append(child.attrib)
                        if child.attrib.get('status','')=='scan':
                            scann.append(child.attrib)
                        pass
                    pass
                tree.write('./uploads/rep.xml')
            pass
        return '200OK'
        
            
 
conf = {
        'global' :{
            'server.socket_host' : '0.0.0.0',
            'server.socket_port' : 8080 },
        '/': {
             'tools.sessions.on': True,
             'tools.staticdir.root': os.path.abspath(os.getcwd())
         },

        '/fileloader': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd()),
         },
         

         '/static': {
             'tools.staticdir.on': True,
             'tools.staticdir.dir': os.path.join(current_dir,'stc'),
            
             
         }

        }
try:
    webapp = HelloWorld()
    cherrypy.quickstart(webapp, '/', conf)
except KeyboardInterrupt:
    sys.exit()
