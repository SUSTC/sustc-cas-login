#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import urllib
import urllib2
import cookielib
import socket
import re

__TIMEOUT__ = 2
# 10 min
__PERIOD__ = 10 * 60

class NoRedirectHandler(urllib2.HTTPErrorProcessor):
    def http_response(self, request, response):
        return response

    https_response = http_response

def init_env():
    # cookie processor
    cookie = cookielib.CookieJar()

    #httpHandler = urllib2.HTTPHandler(debuglevel = 1)
    #httpsHandler = urllib2.HTTPSHandler(debuglevel = 1)

    cookieprocessor = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(cookieprocessor)
    #opener = urllib2.build_opener(cookieprocessor, httpHandler, httpsHandler)
    urllib2.install_opener(opener)

def dologin(username, password):
    login(username, password)

def login(username, password):
    opener = urllib2.build_opener(NoRedirectHandler)
    try:
        req = urllib2.Request('http://baidu.com')
        response = opener.open(req, timeout = __TIMEOUT__)
        location = response.info().getheader('Location')
    except:
        return

    if location and "http://enet.10000.gd.cn" in location:
        date = time.strftime('%Y-%m-%d %H:%M:%S')
        print '[%s] Logging...' % date,
        sys.stdout.flush()

        success = False
        content = None
        try:
            response = urllib2.urlopen(location, timeout = __TIMEOUT__)
            content = response.read()
        #except socket.timeout, e:
        #    print "There was an error: %r" % e
        #except urllib2.URLError, e:
        #    print "There was an error: %r" % e
        except:
            pass

        if content:
            patt_action = re.compile(r'<form .*?action="(.*?)"', re.M)
            patt_lt = re.compile(r'<input type="hidden" name="lt" .*?value="(.*?)"', re.M)
            patt_exec = re.compile(r'<input type="hidden" name="execution" .*?value="(.*?)"', re.M)

            mat_action = patt_action.findall(content)
            mat_lt = patt_lt.findall(content)
            mat_exec = patt_exec.findall(content)

            if mat_action and mat_lt and mat_exec:
                action = mat_action[0]
                lt = mat_lt[0]
                execution = mat_exec[0]

                data = {
                    'username': username,
                    'password': password,
                    'lt': lt,
                    'execution': execution,
                    '_eventId': 'submit',
                    'submit': 'LOGIN'
                }

                # login
                url = 'http://weblogin.sustc.edu.cn' + action
                data = urllib.urlencode(data)
                content = None
                timeout = False
                try:
                    response = urllib2.urlopen(url, data = data, timeout = __TIMEOUT__)
                    content = response.read()
                except socket.timeout, e:
                    timeout = True
                except urllib2.URLError, e:
                    timeout = True
                except:
                    pass

                if timeout:
                    print 'Timeout...',
                    try:
                        response = urllib2.urlopen(url, data = data, timeout = __TIMEOUT__)
                        content = response.read()
                    except:
                        pass

                if content and '<h2>success' in content:
                    success = True

        if success:
            print "Success"
        else:
            print "Failed"
        sys.stdout.flush()

def usage():
    print """Usage:
             ./sustc-cas-login.py [--loop] [username] [password]
          """

def main(argv):
    if len(argv) < 2:
        usage()
        return

    loop = False
    i = 0
    if argv[0] == '--loop':
        loop = True
        i += 1

    # check args again
    if loop and len(argv) < 3:
        usage()
        return

    username = argv[i]
    password = argv[i + 1]

    init_env()

    dologin(username, password)

    while loop:
        time.sleep(__PERIOD__)
        dologin(username, password)

if __name__ == '__main__':
    main(sys.argv[1:])
