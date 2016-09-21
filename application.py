# -*- coding: utf-8 -*-
import cherrypy
import json
import os
import sys
import codecs
import re
import datetime
import xml.etree.cElementTree as ET
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import tostring
from shutil import copy2


import lxml.etree
import string
import random

scann = []
noscann = []
error = []
double = []
unique = set()
unique_scann = set()
try:
    copy2('./res/res.xml', './res/lastFile.xml')
except Exception as er:
    print er
try:
    approot = os.path.dirname(os.path.abspath(__file__))
except NameError:  # We are the main script, not a module
    approot = os.path.dirname(os.path.abspath(sys.argv[0]))

current_dir = approot

ht = lambda: [
        '%04d' % datetime.datetime.now().year,
        '%02d' % datetime.datetime.now().month,
        '%02d' % datetime.datetime.now().day,
        '%02d' % datetime.datetime.now().hour,
        '%02d' % datetime.datetime.now().minute,
        '%02d' % datetime.datetime.now().second
    ]


def logg(text):
    logname = './logs/%s-%s-%s.txt'%(ht()[0],ht()[1],ht()[2])
    if os.path.isfile(logname):

        logfile = codecs.open(logname, 'a', 'utf-8')
        logfile.write(text)
        logfile.close()
    else:

        logfile = codecs.open(logname, 'w+', 'utf-8')
        logfile.write(text)
        logfile.close()




top = Element('top')
child = SubElement(top, 'child')
child.text = 'This child contains text.'

W = open('./res/res.xml','w',)
W.write('<?xml version="1.0" encoding="utf-8"?>')
W.write(tostring(top))
W.close()


tree2 = ET.parse('./res/res.xml')
root2 = tree2.getroot()



class HelloWorld(object):
    @cherrypy.expose
    def check(self,stext =None):
        if (os.path.isfile('./res/res.xml')):
            logg(u'---%20s ;;;; ---%30s\r\n ' % ('-'.join(ht()),stext))
            page = ''.join(codecs.open('check.html','r','utf-8').readlines())

            we_are_search = None
            if stext :
                we_are_search = re.findall(u'[A-Z]{4}/?\d{6}/?\d{4}', stext)

                if len(we_are_search)>0:
                    we_are_search = we_are_search[0].replace('/', '')
                    we_are_search = '/'.join([we_are_search[0:4], we_are_search[4:10], we_are_search[10:]])
                    print we_are_search

            else:
                pass

            root = tree2.getroot()
            before = [len(scann),len(noscann)]

            if we_are_search:
                for child in root.iter():
                    if child.attrib.has_key('RefNo'):
                        pass
                    else:
                        continue
                    try:
                        if len(re.findall(u'%s/\d{2}'%we_are_search, child.attrib.get('RefNo','')))>0:
                            if child.attrib.get('status', '') == 'scann':
                                double.append(child.attrib.get('RefNo',''))
                            if  child.attrib.get('status','') == 'noscann' :
                                scann.append(child.attrib.get('RefNo',''))
                                noscann.count(child.attrib.get('RefNo','')) and noscann.remove(child.attrib.get('RefNo',''))
                                child.set('status', 'scann')
                                if we_are_search.replace('/', '') in unique:
                                    unique.remove(we_are_search.replace('/',''))
                                    unique_scann.add(we_are_search.replace('/',''))
                                try:
                                    tree2.write('./res/res.xml')
                                except Exception as err2:
                                    logg(u'---%20s ;;;; ---%30s\r\n ' % ('-'.join(ht()), err2))
                                    pass
                    except Exception as err:
                        logg(u'---%20s ;;;; ---%10s;;;; ---%10s\r\n ' % ('-'.join(ht()), stext,err))
                        pass
                    pass
                pass
            if stext and not we_are_search:
                error.append(stext)
            if before == [len(scann),len(noscann)] and stext:
                error.append(stext)


            page = page.replace('{{double}}'.decode("utf-8"),'%s'%', '.join(double))
            page = page.replace('{{error}}'.decode("utf-8"),'%s'%', '.join(error))
            page = page.replace('{{current}}'.decode("utf-8"),'%d/%d   %d/%d'%(len(scann),len(noscann),len(unique_scann),len(unique)))
            page = page.replace('{{res}}'.decode("utf-8"), '%s' % ', '.join(unique))

            return page
        return 'А вы загрузили файл ? '
    
    @cherrypy.expose
    def index(self):
        page_index = open('index.html','r')
        return page_index
    
    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def fileloader(self,upl):
        logg(u'Пошел процесс загрузки файла %s\r\n '%('-'.join(ht())))

        myFile = upl
        filename = ''.join([random.choice('asdfghjkl') for i in range(0, random.randint(20,30))])+'.xml'








        size = 0
        
        res = ''
        if myFile==None:
            logg(u'Загрузка прервалась %s\r\n '%('-'.join(ht())))
            return '-------------'
        while True:
            data = myFile.file.read()
            
            res += data
            if not data:
                logg(u'Потеря Дискриптора файла %s\r\n ' % ('-'.join(ht())))
                break
            size += len(data)
            if data:
                logg(u'Файл успешно загружен  %s\r\n ' % ('-'.join(ht())))
                f = open('./uploads/'+filename,'w',)
                f.write(res)
                f.close()



                tree = ET.parse('./uploads/'+filename)

                logg(u'Теперь файл преобразуется %s\r\n ' % ('-'.join(ht())))
                root = tree.getroot()
                for child in root.iter():
                    if child.attrib.has_key('RefNo'):

                        x = child.attrib['RefNo'].replace('/','')[:-2]
                        unique.add(x)
                        if child.attrib.get('status','')=='' or child.attrib.get('status','')=='noscann':
                            child.attrib['status'] = 'noscann'
                            if noscann.count(child.attrib.get('RefNo','')) < 1:
                                noscann.append(child.attrib.get('RefNo',''))
                                root2.append(child)
                        if child.attrib.get('status','')=='scann':
                            if scann.count(child.attrib.get('RefNo','')) < 1:
                                scann.append(child.attrib.get('RefNo',''))
                                root2.append(child)
                            if x in unique:
                               unique.remove(x)
                               unique_scann.add(x)
                        pass
                    pass
                tree.write('./uploads/'+filename)

                tree2.write('./res/res.xml')
                logg(u'Преобразованиее закончилось успехом! %s\r\n ' % ('-'.join(ht())))
            pass
            #
        return '200OK'
        
            
 
conf = {
        'global' :{
            'server.socket_host' : '0.0.0.0',
            'server.socket_port' : 137 },
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
    print 'bye'

    sys.exit()
