#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2012 - Caio Begotti <caio1982@gmail.com>
# Distributed under the GPLv2, see the LICENSE file.

#import sys
#sys.path.append('/home/caio/py_libs/')

import web

from amazonwish.config import *

from amazonwish.amazonwish import Search
from amazonwish.amazonwish import Profile
from amazonwish.amazonwish import Wishlist

render = web.template.render( 'templates/', base='index')

urls = (
    '/(.*)', 'index'
)

app = web.application(urls, globals(), True)

class index:        
    def GET(self, term):
        res = web.input()
        if len(res) == 0:
            return render.search()

        site = 'us'
        if 'site' in res:
            site = res['site']

        if 'search' in res:
            wl = []
            p = []
            term = res['search']
            s = Search(term, country=site)

            if s.list() is None:
                return render.error('null')

            if len(s.list()) > 1:
                names = []
                for l in s.list():
                    entry = l[0].lower().title(), l[1]
                    names.append(entry)
                return render.multiples(site, names)
            elif len(s.list()) == 1:
                list = s.list()[0]
                wishlist = list[1]
                wl = Wishlist(wishlist, country=site)
                p = Profile(wishlist, country=site)
            else:
                return render.error(term)
        elif 'list' in res:
            id = res['list']
            wl = Wishlist(id, country=site)
            p = Profile(id, country=site)
        else:
            return render.search()

        info = p.basicInfo()          
        total = wl.total_expenses()
        covers = wl.covers()
        urls = wl.urls()
        titles = wl.titles()
        authors = wl.authors()
        prices = wl.prices()
        items = zip(covers, urls, titles, authors, prices)

        listnames = p.wishlists()
        listcodes = p.wishlistsDetails()[0]
        listsizes = p.wishlistsDetails()[1]
        lists = zip(listnames, listsizes, listcodes)
        
        configs = [wl.currency, wl.symbol, wl.domain]
        return render.result(info, configs, lists, items, total)

#web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)

if __name__ == "__main__":
    #web.runwsgi = web.runfcgi
    app.run()
