# -*- coding: utf-8 -*-
# TODO : SORT THIS
# TODO : Comment lang is English
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
import random

# TODO : Separate settings into different files
# FIXME: Add space in variable names
# FIXME: re-name variable name


scann = []
noscann = []
error = []
colors = []
colorpair = {}
double = set()
unique = set()
unique_scann = set()
pagecolorserrors = {}
top = Element('top')
child = SubElement(top, 'child')
child.text = 'This child contains text.'
CATEGORIES = "categories"
COLORS = "colors"
NAME = "name"
VALUES = "values"

ERROR = "error"
DOUBLE = "double"

SCAN = "SCAN"

LEN_SCAN = "lenScann"
LEN_NO_SCAN = "lenNoScann"
LEN_UNIQUE_SCAN = "lenUniqueScann"
LEN_UNIQUE_NO_SCAN = "lenSUniqueNoScann"
LEN_DOUBLE = "LEN_DOUBLE"
LEN_ERRORS = "LEN_ERRORS"

COLOR = "color"

YES = u"ДА"
NO = u"НЕТ"
img_folder = './stc/chess/'
# TODO: issue upper case variables ,
# TODO: folder get from os.path or from os name space
STATIC_CHESS = '/static/chess/'

SOUND_FOLDER = './stc/colors/'
SOUND_FOLDER_WEB = '/static/colors/'
MP3 = '.mp3'


W = open('./res/res.xml', 'w',)
W.write('<?xml version="1.0" encoding="utf-8"?>')
W.write(tostring(top))
W.close()


tree2 = ET.parse('./res/res.xml')
root2 = tree2.getroot()
FILE = './stc/color_loader/category.json'
allRequest = json.load(file(FILE, 'r'))
try:
    copy2('./res/res.xml', './res/lastFile.xml')
except Exception as er:
    print er
try:
    approot = os.path.dirname(os.path.abspath(__file__))
except NameError:  # We are the main script, not a module
    approot = os.path.dirname(os.path.abspath(sys.argv[0]))

current_dir = approot

# FIXME: functions
ht = lambda: [
        '%04d' % datetime.datetime.now().year,
        '%02d' % datetime.datetime.now().month,
        '%02d' % datetime.datetime.now().day,
        '%02d' % datetime.datetime.now().hour,
        '%02d' % datetime.datetime.now().minute,
        '%02d' % datetime.datetime.now().second
    ]


class MetaCache(type):
    def __new__(mcs, name, bases, dct):
        return super(MetaCache, mcs).__new__(mcs, name, bases, dct)

    def __init__(cls, name, bases, dct):
        super(MetaCache, cls).__init__(name, bases, dct)


# TODO: make BASE Cache variable
class Cache(object):
    __metaclass__ = MetaCache


def inCache(obj, param):
    if hasattr(obj, '{}'.format(param)):
        return True
    return False


def logg(text):
    log_name = './logs/%s-%s-%s.txt' % (ht()[0], ht()[1], ht()[2])
    if os.path.isfile(log_name):
        pass
    else:
        logfile = codecs.open(log_name, 'w+', 'utf-8')
        logfile.close()
    logfile = codecs.open(log_name, 'a', 'utf-8')
    logfile.write(text)
    logfile.close()


# Special list mean list of journals (Info class)
# [journal1,journal2,...]
monitor = []
common_cache = Cache()


class MTypes(object):
    """
    msg_types
    """
    ERROR_CATEGORIES = "ERROR_CATEGORIES"
    ERROR_ORDER = "ERROR_ORDER"
    INFO = "INFO"
    COMMON = "COMMON"


class Message(object):
    """
    Message is a unit for Info
    """
    def __init__(self, host, msg_type, cat, msg):
        self.host = host
        self.msg_type = msg_type
        self.cat = cat
        self.msg = msg

    def __call__(self):
        return {"host": self.host, "data": [self.msg, self.msg_type]}

    def __str__(self):
        return '{}'.format(self.msg)

    def __repr__(self):
        return 'Message("host": {} , "data": [{},{}])'.format(
            self.host, self.msg, self.msg_type)


class Info(object):
    """
    Base Info class
    (journal message class)
    """

    def __init__(self, host):
        self.__host = host
        self.__log = {self.__host: []}
        self.__msg = []
        self.__num = -1
        self.__order = Cache()
        self.__right = -1
        self.__delta = 0
        self.__two_digit = []
        # TODO: check differ in monitor

    def __repr__(self):
        return "Info({})".format(self.__host)

    def __eq__(self, x):
        return self.__host == x.__host

    def __hash__(self):
        return hash(self.__repr__())

    def __len__(self):
        return self.__num

    def log(self, msg):
        """
        case for keeping msg
        """
        self.__msg.append(msg)
        self.__num += 1

    def order_check(self, digit, cat):
        """
        check order
        """
        cat_list = "".join([cat, '__list__'])
        if inCache(self.__order, cat_list):
            pass
        else:
            setattr(
                self.__order,
                cat_list,
                []
            )
        order = getattr(self.__order, cat_list, None)

        if isinstance(digit, list):
            digit = int(''.join(digit))
            # TODO: without try , catch (Exception) ?
            # TODO: just belief

        res = False

        if digit in order:
            return res

        order.append(digit)
        before_index = order.index(digit)
        order.sort()
        after_index = order.index(digit)

        delta_n_plus_one = after_index - before_index

        if delta_n_plus_one < self.__delta:
            res = True

        self.__delta = delta_n_plus_one

        self.__two_digit.insert(0, digit)
        self.__two_digit = self.__two_digit[:2]

        digit_list = "".join([cat, '__digit__'])

        setattr(
            self.__order,
            digit_list,
            self.__two_digit
            )

        return res

    def two_last_digits(self, cat):
        """
        2 Last digit from one category and historical input
        """
        digit_list = "".join([cat, '__digit__'])
        if inCache(self.__order, digit_list):
            pass
        else:
            setattr(
                self.__order,
                digit_list,
                self.__two_digit
            )
        return getattr(self.__order, digit_list, None)

    def actual(self):
        """
        actual log is 2 last msg and num of last msg
        """
        # order
        return self.__msg[-1:-3:-1]
    
    def journal(self):
        return self.__msg


# TODO: rename class
class HelloWorld(object):
    """
    Manager application
    """

    @cherrypy.expose
    def ajax_check_order(self, code, cat):
        host = cherrypy.request.headers.get('Remote-Addr', 'unknow')

        if Info(host) in monitor:
            pass
        else:
            monitor.append(Info(host))
        user_monitor = monitor[monitor.index(Info(host))]

        type_msg = MTypes.COMMON
        msg = {}
        colors_cat = allRequest.get(CATEGORIES, '')

        older_protocol = self.findMe(code)

        msg[LEN_SCAN] = len(scann)
        msg[LEN_NO_SCAN] = len(noscann)
        msg[LEN_UNIQUE_SCAN] = len(unique_scann)
        msg[LEN_UNIQUE_NO_SCAN] = len(unique)
        msg[LEN_DOUBLE] = len(double)
        msg[LEN_ERRORS] = len(error)

        if ERROR in older_protocol:
            msg[ERROR] = u"{} possible error".format(code)

        elif DOUBLE in older_protocol:
            msg[ERROR] = u"{} double".format(code)

        elif LEN_SCAN in older_protocol:
            type_msg = MTypes.COMMON

        user_monitor.log(Message(host, type_msg, '', msg))
        logg(u'---%20s ;;;; ---%20s ;;;; ---%20s\r\n ' % (
            '-'.join(ht()), host, msg))

        # new logic
        msg = {}
        code = re.findall(u'[A-Z]{4}/?\d{6}/?\d{4}', code)
        code = ''.join(code).replace('/', '')

        if code:
            search_color = colorpair.get(code, None)
            msg[COLOR] = search_color

            # Cache mb put it in function ?
            # -----------------------------------------------------------------
            if inCache(Cache, cat):
                list_cat_colors = getattr(common_cache, cat, None)
            else:
                for c in colors_cat:
                    setattr(
                        common_cache,
                        '{}'.format(c.get("name", "")),
                        c.get("values", "")
                    )
                list_cat_colors = getattr(common_cache, cat, None)
            # -----------------------------------------------------------------

            if search_color not in list_cat_colors and search_color:
                logg(u'---%20s ;;;; ---%20s ;;;; ---%20s\r\n ' % (
                    code, host, u'Ошибка категории '))

                #  means category error
                type_msg = MTypes.ERROR_CATEGORIES
                msg[type_msg] = "code {} not in  category {}".format(
                    code,
                    cat
                )

            elif search_color is None:
                #  means category error
                type_msg = MTypes.ERROR_CATEGORIES
                logg(u'---%20s ;;;; ---%20s ;;;; ---%20s\r\n ' % (
                    code, host, u'Ошибка категории или не загружен отчет'))
                msg[type_msg] = "code {} return None".format(code)

            else:
                # TODO: Check order
                bad_order = user_monitor.order_check(re.findall(
                    '\d+', code), cat)

                if bad_order:
                    history = user_monitor.two_last_digits(cat)

                    logg(u'---%20s ;;;; ---%20s ;;;; ---%20s\r\n ' % (
                        u'{}-->{}'.format(history[1],
                                      history[0]), unicode(host),
                        u' Порядок нарушен '))

                    #  means order error
                    type_msg = MTypes.ERROR_ORDER
                    msg[MTypes.ERROR_ORDER] = user_monitor.two_last_digits(cat)

                elif not bad_order:

                    logg(u'---%20s ;;;; ---%20s ;;;; ---%20s\r\n ' % (
                        '-'.join(ht()), host, msg))
                    type_msg = MTypes.INFO
                    msg[type_msg] = "Correct!"
            user_monitor.log(Message(host, type_msg, cat, msg))
            logg(u'---%20s ;;;; ---%20s ;;;; ---%20s\r\n ' % (
                '-'.join(ht()), host, msg))
        ans = []
        for message in user_monitor.actual():
            ans.append(message())
        print json.dumps(ans[::-1])
        return json.dumps(ans[::-1])

    @staticmethod
    def check_colors(color):
        """
        check file exists and return status and link with audio
        """
        # TODO : bring out features
        # TODO : check_colors and check_img from this class
        WARNING = "class=warning"
        sound_path = ''.join([SOUND_FOLDER, color, MP3])

        if os.path.isfile(sound_path):
            sound_path = ''.join([SOUND_FOLDER_WEB, color, MP3])
            return """
            <span>{color}</span>
            <audio src ={sound_path} id="{color}-in_voice">
            </audio>
            """.format(
                color=color,
                sound_path=sound_path), "", YES, sound_path
        return """
            <span "class=warning" >{color}</span>
            <audio src ={sound_path} id="{color}-in_voice">
            </audio>
            """.format(
                color=color,
                sound_path=sound_path), WARNING, NO, sound_path

    @staticmethod
    def check_img(name):
        """
        return row for HTML, with img link or text (text = name)
        :param name:
        :return:
        """
        PNG = '.png'
        img_src = ''.join([img_folder, name, PNG])
        if os.path.isfile(img_src):
            img_src_web = ''.join([STATIC_CHESS, name, PNG])

            img = """<img src='{}' height="128" width="128"/>
            """.format(img_src_web)
            return img

        return name

    @cherrypy.expose
    def order(self):
        """
        order page - page with "monitor - journal"
        page init Info class for host
        -----------------------------------------------------------------------
        Main page for reconciliation on stage "DO"
        -----------------------------------------------------------------------
        """
        host = cherrypy.request.headers.get('Remote-Addr', 'unknow')

        if Info(host) in monitor:
            pass
        else:
            monitor.append(Info(host))

        user_monitor = monitor[monitor.index(Info(host))]

        all_messages = user_monitor.journal()
        
        logg(u'---%20s ;;;; ---%20s ;;;; ---%20s\r\n ' % (
            '-'.join(ht()), host, u'Подключился к журналу'))

        page = ''.join(codecs.open('order_scel.html', 'r', 'utf-8').readlines()
                       )
        # define option
        summary_tab_li = []
        summary_tab_div = []
        colors_ = allRequest[COLORS]
        for option in allRequest[CATEGORIES]:
            name_option = option.get(NAME)

            TAB_LI = """
                    <li>
                        <a data-toggle="tab" href="#{menu_tag}">{menu_img}</a>
                    </li>
                    """.format(menu_tag=name_option,
                               menu_img=self.check_img(name_option))
            summary_tab_li.append(TAB_LI)
            list_enabled_colors = ', '.join(option.get(VALUES))
            TAB_DIV = """
                           <div id="{menu_tag}" class="tab-pane fade">
                               <h3 data-val="{content}">{menu_tag}</h3>
                               <p>{content}</p>


                            <div class="form-group">
                            <label for="{menu_tag}">{menu_tag} :</label>
                            <input type="text" class="form-control codeInput"
                            id="{menu_tag}">
                            </div>
                           </div>""".format(menu_tag=name_option,
                                            content=list_enabled_colors)
            summary_tab_div.append(TAB_DIV)

        result_summary_tab_li = ''.join(summary_tab_li)
        result_summary_tab_div = ''.join(summary_tab_div)

        #######################################################################
        # make tabs
        #######################################################################


        TAB = """
        <ul class="nav nav-tabs">
            {TAB_LI}
        </ul>
        <div class="tab-content">
            {TAB_DIV}
        </div>
        """.format(TAB_LI=result_summary_tab_li,
                   TAB_DIV=result_summary_tab_div)

        page = page.replace('{{TABS}}'.decode("utf-8"),
                            '{}'.format(TAB))

        #######################################################################
        # Make table
        #######################################################################
        TABLE_HEAD = u"""
            <thead>
                <tr>
                    <th>Цвет</th>
                    <th>Существует</th>
                    <th>Включен</th>
                    <th style="text-align: center;">Послушать</th>
                </tr>
            </thead>
        """
        summary_table_body_tr = []
        for color in colors_:

            # TODO: refactor check colors and check images
            tag, class_, status, sound_path = self.check_colors(color)
            table_body_tr = u"""
            <tr {class_} >
                <td>{color}</td>
                <td>{status}</td>
                <td>
                    <div class="btn-group btn-toggle" width ="105%">
                        <button class="btn btn-lg btn-default {color_name}" >
                        ON</button>
                        <button
                        class="btn btn-lg btn-primary active {color_name}" >
                        OFF</button>
                    </div>
                </td>
                <td class="TEST" style="text-align: center;" >
                <audio controls src={src}></audio></td>
            </tr>
            """.format(color=tag,
                       class_=class_,
                       status=status,
                       src=sound_path,
                       color_name=color
                       )

            summary_table_body_tr.append(table_body_tr)
        result_summary_table_body_tr = ''.join(summary_table_body_tr)
        TABLE = u"""
        <table class="table">
            {head}
            <tbody>
                {tr_body}
            </tbody>
        </table>
        """.format(head=TABLE_HEAD, tr_body=result_summary_table_body_tr)

        page = page.replace(u'{{TABLE}}'.decode("utf-8"),
                            u'{}'.format(TABLE))

        #######################################################################
        # make messages INFO
        #######################################################################
        MSG_FISH = """<div class="alert alert-info">
                    <strong> {info} </strong> {message}
                </div>"""

        INFO_LOG = ""
        INFO_ERROR_CATEGORY = ""
        INFO_ERROR_ORDER = ""

        for ms in all_messages:
            row = ms().get("data", None)

            if row[1] == MTypes.COMMON:

                message = row[0].get(ERROR, None)
                if message:
                    INFO_LOG += MSG_FISH.format(
                        info=u"Common!",
                        message=message
                    )

            if row[1] == MTypes.INFO:
                INFO_LOG += MSG_FISH.format(
                    message=row[0].get(COLOR, None),
                    info=row[0].get(MTypes.INFO, None)
                )

            elif row[1] == MTypes.ERROR_CATEGORIES:
                message = row[0].get(MTypes.ERROR_CATEGORIES, None)
                if message:
                    INFO_ERROR_CATEGORY += MSG_FISH.format(
                        info=row[0].get(COLOR, None),
                        message=row[0].get(MTypes.ERROR_CATEGORIES, None)
                    )

            elif row[1] == MTypes.ERROR_ORDER:
                INFO_ERROR_ORDER += MSG_FISH.format(
                    info=row[0].get(COLOR, None),
                    message=u'{}--->{}'.format(row[0].get(
                        MTypes.ERROR_ORDER, [])[-2], row[0].get(
                        MTypes.ERROR_ORDER, [])[-1])
                )
        page = page.replace(u'{{INFO_LOG}}'.decode("utf-8"),
                            u'{}'.format(INFO_LOG))
        page = page.replace(u'{{INFO_ORDER}}'.decode("utf-8"),
                            u'{}'.format(INFO_ERROR_ORDER))
        page = page.replace(u'{{INFO_CATEGORY}}'.decode("utf-8"),
                            u'{}'.format(INFO_ERROR_CATEGORY))

        return page

    @cherrypy.expose
    def colors_set(self, colors=None, categories=None):
        """
            Function for save with validate json file
        """

        host = cherrypy.request.headers.get('Remote-Addr', 'unknow')
        logg(u'---%20s ;;;; ---%20s ;;;; ---%20s\r\n ' % (
            '-'.join(ht()), host, u'Передача параметров(настройка)'))

        if colors or categories:
            if colors:
                allRequest[u'colors'] = filter(lambda x: x, colors.split(','))
            if categories:
                all_cat = []
                sending_cat = json.loads(categories)
                for obj in sending_cat:
                    all_cat += obj[u'values']
                val_set = set(all_cat) ^ set(allRequest[u'colors'])
                if len(all_cat) != len(set(all_cat)):
                    logg(u'---%20s ;;;; ---%20s ;;;; ---%20s\r\n ' % (
                        '-'.join(ht()), host,
                        u'Не успешный результат'))
                    return (
                        u"Выбирайте Один цвет для одной категории!")

                if len(val_set):
                    logg(u'---%20s ;;;; ---%20s ;;;; ---%20s\r\n ' % (
                        '-'.join(ht()), host,
                        u'Не успешный результат'))
                    return (
                        u"Слудующие значения :{} выдали ошибку".format(val_set)
                    )
                allRequest[u'categories'] = sending_cat

            json.dump(allRequest, file(FILE, 'w'))
            logg(u'---%20s ;;;; ---%20s ;;;; ---%20s\r\n ' % (
                '-'.join(ht()), host,
                u'Успешно загружено'))
            return "Успешно"

        return "NOT Found 404"

    @cherrypy.expose
    def pre_settings(self):
        """
        'Pre_setting' - page with setting for 'ordering input"
        Before start ordering scanning, application must
        get params from json file
        """
        page = codecs.open('order_input.html', 'r', 'utf-8')
        return page

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
                return '{%s:%s}'%(i, colorpair.get(word,''))
            else:
                self.findMe(code=k)
                logg(u'---%20s ;;;; ---%20s ;;;; ---%20s\r\n ' % (k, i, u'НЕ ТОТ ЦВЕТ'))
                try:
                    pagecolorserrors[i].update({k: colorpair.get(word, 'NO COLOR')})
                except:
                    logg(u'---%20s ;;;; ---%20s ;;;; ---%20s\r\n ' % (k,u'Либо файл не загружен',u'Либо нет такого номера'))

                return '{%s:%s}'%(k, colorpair.get(word,'---'))


        
    @cherrypy.expose
    def findMe(self, code=None):
        host = cherrypy.request.headers.get('Remote-Addr','unknow')
        logg(u'---%20s ;;;; ---%20s ;;;; ---%20s\r\n ' % ('-'.join(ht()),host,code or '*Empty'))
        if (os.path.isfile('./res/res.xml')):
            pass
        else:
            return u'<h1>Так нельзя!</h1><p>И за чем мне проверять файл по адресу ? ./res/res.xml</p><br><p>Когда я вижу, что это провакация</p>'
        if code:
            pass
        else:
            raise cherrypy.HTTPError("404 Not found", 'we are sorry')
        code_pattern = re.findall(u'[A-Z]{4}/?\d{6}/?\d{4}', code)
        if len(code_pattern):
            pass
        else:
            error.append(code)
            return 'error :%s' % code
        word = code_pattern[0].replace('/','')
        phrase = '/'.join([word[0:4], word[4:10], word[10:]])
        root = tree2.getroot()
        res = ''
        before = [len(scann), len(noscann)]
        for child in root.iter():
            if child.attrib.has_key('RefNo'):
                pass
            else:
                continue

            if len(re.findall(u'%s/\d{2}'%phrase, child.attrib.get('RefNo','')))>0:
                if child.attrib.get('status', '') == 'scann':
                    double.add(code)
                    return "double :%s ;"%code

                if child.attrib.get('status','') == 'noscann' :
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
            return 'error :%s' % code

        try:
            tree2.write('./res/res.xml')
        except Exception as err2:
            logg(u'---%20s ;;;; ---%30s\r\n ' % ('-'.join(ht()), err2))

        res +='lenScann :%s ;lenNoScann :%s; lenUniqueScann :%s ; lenSUniqueNoScann :%s ;'%(len(scann),len(noscann),len(unique_scann),len(unique))
        
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
        page_index = open('index.html', 'r')
        return page_index
    
    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def fileloader(self, upl):
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
                            colors.append(color)
                            
                
                tree.write('./uploads/'+filename)
                tree2.write('./res/res.xml')
                logg(u'Преобразованиее закончилось успехом! %s\r\n ' % ('-'.join(ht())))
        return '200OK'
        
            
 
conf = {
        'global' :{
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 137},
        '/': {
             'tools.sessions.on': True,
             'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/ajax_check_order': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd()),
        },

        '/ colors_set': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd()),
        },

        '/pre_settings': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd()),
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
             'tools.staticdir.dir': os.path.join(current_dir, 'stc'),
        },
        
        '/img': {
             'tools.staticdir.on': True,
             'tools.staticdir.dir': os.path.join(current_dir, 'stc'),
             
        },

        
        

        }
try:
    webapp = HelloWorld()
    cherrypy.quickstart(webapp, '/', conf)
except KeyboardInterrupt:
    print 'bye'

    sys.exit()
