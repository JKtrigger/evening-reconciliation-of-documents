# -*- coding: utf-8 -*-
import cherrypy
import json
import os
import sys
import codecs
import re
import datetime
import xml.etree.cElementTree as ET
import lxml.etree
parser = lxml.etree.XMLParser(recover=True)

import re

global scann , noscann ,error , double
scann   = []
noscann = []
error = []
double = []
d = datetime.datetime.now()
ht = lambda :['%02d'%datetime.datetime.now().hour ,'%02d'%datetime.datetime.now().minute,'%02d'%datetime.datetime.now().second]
try:
    tree = lxml.etree.parse('./uploads/rep.xml', parser)
    logFile = codecs.open('./uploads/%04d-%02d-%02d-%02d-%02d-%02d.txt'%(d.year,d.month,d.day,d.hour,d.minute,d.second),'w+','utf-8')
    approot = os.path.dirname(os.path.abspath(__file__))
except NameError:  # We are the main script, not a module
    approot = os.path.dirname(os.path.abspath(sys.argv[0]))
current_dir = approot
class HelloWorld(object):
    global scann , noscann ,error , double
    scann = []
    noscann = []
    error = []
    double = []
    @cherrypy.expose
    def check(self,stext =None):
        if (os.path.isfile('./uploads/rep.xml')):
            logFile.write(u'---%20s ;;;; ---%30s\r\n ' % ('-'.join(ht()),stext))
            page = ''.join(codecs.open('check.html','r','utf-8').readlines())

            WeAreSearch = None
            if stext :
                WeAreSearch = re.findall(u'/?\d{6}/?\d{4}', stext) and re.findall(u'/?\d{6}/?\d{4}', stext)[0].replace('/','')
                print WeAreSearch
                if len(WeAreSearch)>0:
                    WeAreSearch =WeAreSearch[0:6] + '/' +WeAreSearch[6:]


            else:
                pass



            root = tree.getroot()
            before = [len(scann),len(noscann)]

            if WeAreSearch:
                for child in root.iter():
                    if child.attrib.has_key('RefNo'):
                        pass
                    else:
                        continue
                    try:
                        if len(re.findall(u'[A-Z]{4}/%s/\d{2}'%WeAreSearch, child.attrib.get('RefNo','')))>0:
                            if child.attrib.get('status', '') == 'scann':
                                double.append(child.attrib.get('RefNo',''))
                            if  child.attrib.get('status','') == 'noscann' :
                                scann.append(child.attrib.get('RefNo',''))
                                noscann.count(child.attrib.get('RefNo','')) and noscann.remove(child.attrib.get('RefNo',''))
                                child.set('status', 'scann')
                                try:
                                    tree.write('./uploads/rep.xml')
                                except Exception as err2:
                                    logFile.write(u'---%20s ;;;; ---%30s\r\n ' % ('-'.join(ht()), err2))
                                    pass
                    except Exception as err:
                        logFile.write(u'---%20s ;;;; ---%10s;;;; ---%10s\r\n ' % ('-'.join(ht()), stext,err))
                        pass
                    pass
                pass
            if stext and not WeAreSearch:
                error.append(stext)

            #page = page.replace('{{scan}}'.decode("utf-8"),'%s'%,''.join(scann))
            page = page.replace('{{double}}'.decode("utf-8"),'%s'%','.join(double))
            page = page.replace('{{error}}'.decode("utf-8"),'%s'%','.join(error))
            page = page.replace('{{current}}'.decode("utf-8"),'%d/%d'%(len(scann),len(noscann)))
            page = page.replace('{{res}}'.decode("utf-8"), '%s' % ','.join(noscann))

            return page
        return 'А вы загрузили файл ? '
    
    @cherrypy.expose
    def index(self):
        page_index = open('index.html','r')
        return page_index
    
    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def fileloader(self,upl):
        print '-'.join((ht())) ,type('-'.join((ht())))
        global scann, noscann, error, double
        logFile.write(u'Пошел процесс загрузки файла %s\r\n '%('-'.join(ht())))
        scann   = []
        noscann = []
        error = []
        double = []
        myFile = upl
        size = 0
        
        res = ''
        if myFile==None:
            logFile.write(u'Загрузка прервалась %s\r\n '%('-'.join(ht())))
            return '-------------'
        while True:
            data = myFile.file.read()
            
            res +=data
            if not data:
                logFile.write(u'Потеря Дискриптора файла %s\r\n ' % ('-'.join(ht())))
                break
            size += len(data)
            if data :
                logFile.write(u'Файл успешно загружен  %s\r\n ' % ('-'.join(ht())))
                f = open('./uploads/rep.xml','w',)
                f.write(res)
                f.close()
                tree = ET.parse('./uploads/rep.xml')

                logFile.write(u'Теперь файл преобразуется %s\r\n ' % ('-'.join(ht())))
                root = tree.getroot()
                for child in root.iter():
                    if len(child.attrib)>0:
                        if child.attrib.get('status','')=='' or child.attrib.get('status','')=='noscann':
                            child.attrib['status'] = 'noscann'
                            noscann.append(child.attrib.get('RefNo',''))
                        if child.attrib.get('status','')=='scann':
                            scann.append(child.attrib.get('RefNo',''))

                        pass
                    pass
                tree.write('./uploads/rep.xml')
                logFile.write(u'Преобразованиее закончилось успехом! %s\r\n ' % ('-'.join(ht())))
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
    logFile.close()
    sys.exit()
