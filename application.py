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
colors = []
colorpair = {}
double  = set()
unique = set()
unique_scann = set()
pagecolorserrors = {}
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
    def colorlogic(self, **kwarg):
        for i in kwarg:
            k = kwarg.get(i, "-?-")
            i = i.replace('color-','')
            code_pattern = re.findall(u'[A-Z]{4}/?\d{6}/?\d{4}', k)
            if len(code_pattern):
                pass
            else:
                error.append(k)
                return 'No one items found'
            word = code_pattern[0].replace('/', '')
            print i , colorpair.get(word,"+?+"),word
            if colorpair.get(word,"+?+")==i:
                logg(u'---%20s ;;;; ---%20s ;;;; ---%20s\r\n ' % (k,i,u'НАЙДЕН'))
                self.findMe(code = k)
                return  '{%s:%s}'%(i, colorpair.get(word,''))
            else:
                self.findMe(code=k)
                logg(u'---%20s ;;;; ---%20s ;;;; ---%20s\r\n ' % (k, i, u'НЕ ТОТ ЦВЕТ'))
                try:
                    pagecolorserrors[i].update({k: colorpair.get(word, 'NO COLOR')})
                except:
                    logg(u'---%20s ;;;; ---%20s ;;;; ---%20s\r\n ' % (k,u'Либо файл не загружен',u'Либо нет такого номера'))

                return '{%s:%s}'%(k, colorpair.get(word,'---'))


        
    @cherrypy.expose
    def findMe(self,code = None):
        host = cherrypy.request.headers.get('Remote-Addr','unknow')
        logg(u'---%20s ;;;; ---%20s ;;;; ---%20s\r\n ' % ('-'.join(ht()),host,code or '*Empty'))
        if (os.path.isfile('./res/res.xml')):
            pass
        else:
            return u'<h1>Так нельзя!</h1><p>И за чем мне проверять файл по адресу ? ./res/res.xml</p><br><p>Когда я вижу, что это провакация</p>'
        if code:
            pass
        else:
            raise cherrypy.HTTPError("404 Not found",'we are sorry')
        code_pattern = re.findall(u'[A-Z]{4}/?\d{6}/?\d{4}', code)
        if len(code_pattern):
            pass
        else:
            error.append(code)
            return 'error :%s'%code
        word = code_pattern[0].replace('/','')
        phrase = '/'.join([word[0:4],word[4:10],word[10:]])
        root = tree2.getroot()
        res = ''
        before = [len(scann),len(noscann)]
        for child in root.iter():
            if child.attrib.has_key('RefNo'):
                pass
            else:
                continue
            
           
            if len(re.findall(u'%s/\d{2}'%phrase, child.attrib.get('RefNo','')))>0:
                if child.attrib.get('status', '') == 'scann':
                    double.add(code)
                    return "double :%s ;"%code

                if  child.attrib.get('status','') == 'noscann' :
                    scann.append(child.attrib.get('RefNo',''))
                    noscann.count(child.attrib.get('RefNo','')) and noscann.remove(child.attrib.get('RefNo',''))
                    child.set('status', 'scann')
                    res += "scann :%s ;"%code
                    if phrase.replace('/', '') in unique:
                        unique.remove(phrase.replace('/',''))
                        unique_scann.add(phrase.replace('/',''))
        if before == [len(scann),len(noscann)]:
            logg(u'---%20s ;;;; ---%20s ;;;; ---%20s ---НЕ НАЙДЕННО\r\n' % ('-'.join(ht()),host,code))
            error.append(code)
            return 'error :%s'%code
            
            
            
        try:
            tree2.write('./res/res.xml')
        except Exception as err2:
            logg(u'---%20s ;;;; ---%30s\r\n ' % ('-'.join(ht()), err2))

        res +='lenScann :%s ;lenNocann :%s; lenUniqueScann :%s ; lenSUniqueNocann :%s ;'%(len(scann),len(noscann),len(unique_scann),len(unique))
        
        return res
    @cherrypy.expose
    def check(self):
        page = ''.join(codecs.open('check.html','r','utf-8').readlines())
        page = page.replace('{{double}}'.decode("utf-8"),'%s'%', '.join(double))
        page = page.replace('{{error}}'.decode("utf-8"),'%s'%', '.join(error))
        page = page.replace('{{current}}'.decode("utf-8"),'%d/%d   %d/%d'%(len(scann),len(noscann),len(unique_scann),len(unique)))
        page = page.replace('{{res}}'.decode("utf-8"), '%s' % ', '.join(unique))
        return page
        
        
    @cherrypy.expose
    def color(self):
        page = ''.join(codecs.open('color.html','r','utf-8').readlines())
        tabs = '''<div id="{}" class="tab-pane fade">
          <h3 class='h3'>{}</h3>
          <p>{}</p>
        </div>'''
        litab = '<li><a data-toggle="tab" href="{}">{}</a></li>'

        inpuut = '''<div class="form-group">
        <input type="search" value="" class="form-control" name="color-{}" id="id{}" autofocus>
        </div>
            <table class="table">
            <thead>
            <tr>
                <th>RefNo</th>
                <th>colorcode</th>
            </tr>
            </thead>
            <tbody id='tbody-{}'>
            <h4 class='h4'>{}</h4>
             </tbody>
        </table>
        '''
        soursesubmit  = '''
        $('#id%s').keypress(function(event){
            if (event.keyCode == 13) {

                $.ajax({
                    url: "./colorlogic",
			        type:'POST',
			        data: {'color-%s': $('#id%s').val()},
	                datatype:'html',
	                success: function(ans){
					    var response = ans.replace(/{/g,'').replace(/}/g,'').split(':')
					    console.log(response,response[0],response[1])
					    if (response[0] == response[1]) {}
					    else {

					    $('#tbody-%s').append("<tr><td>" + response[0] + "</td><td>" + response [1] + "</td></tr>")
					    }
					}

                })
                $('#id%s').val('')
            return true

            }

        })
        '''
        
        tabmenu = ''
        tabstext = ''
        submit = ''
        relload = json.dumps(pagecolorserrors)
        for i in colors:
            submit += soursesubmit%(i,i,i,i,i)
            htmlinput = inpuut.format(i,i,i,i)
            tabmenu += litab.format('#{}'.format(i),'{}'.format(i))
            tabstext += tabs.format('{}'.format(i),'{}'.format(i),'{}'.format(htmlinput))
            
        page = page.replace('{{litab}}'.decode("utf-8"),tabmenu)
        page = page.replace('{{color}}'.decode("utf-8"),tabstext)
        page = page.replace('{{submit}}'.decode("utf-8"),submit)
        page = page.replace('{{onload}}'.decode("utf-8"), relload)
        return page
                       
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
                    if child.attrib.has_key('colourcode'):
                        color = child.attrib['colourcode']
                        colorpair[x]=color
                        pagecolorserrors[color]={}
                        if color in colors:
                            pass
                        else:
                            print color
                            colors.append(color)
                            
                
                tree.write('./uploads/'+filename)
                tree2.write('./res/res.xml')
                logg(u'Преобразованиее закончилось успехом! %s\r\n ' % ('-'.join(ht())))
            
            
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
        '/findMe': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd()),
         },

        '/color': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd()),
         },

        '/colorlogic': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd()),
         },

         '/static': {
             'tools.staticdir.on': True,
             'tools.staticdir.dir': os.path.join(current_dir,'stc'), 
         },
        
        '/img': {
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
