#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2012 - Caio Begotti <caio1982@gmail.com>
# Distributed under the GPLv2, see the LICENSE file.

#import sys
#sys.path.append('/home/caio/py_libs/')

import web

from amazonwishlist import search
from amazonwishlist import profile
from amazonwishlist import wishlist

render = web.template.render( 'templates/', base='index')

urls = (
    '/(.*)', 'index'
)

def internalerror():
    return web.debugerror()

app = web.application(urls, globals(), True)
app.internalerror = internalerror

class index:        
    def GET(self, term):
        res = web.input()
        if len(res) == 0:
            return render.search()

        site = 'us'
        if 'site' in res:
            site = res['site']

        if 'search' in res:
            wishlists = []
            profiles = []
            term = res['search']
            searched = search.Query(term, country=site)

            if searched.list() is None:
                return render.error('null')

            if len(searched.list()) > 1:
                names = []
                for item in searched.list():
                    entry = item[0].lower().title(), item[1]
                    names.append(entry)
                return render.multiples(site, names)
            elif len(searched.list()) == 1:
                item = searched.list()[0]
                wishlistid = item[1]
                wishlistid = wishlist.Query(wishlistid, country=site)
                profiles = profile.Query(wishlistid, country=site)
            else:
                return render.error(term)
        elif 'list' in res:
            username = res['list']
            wishlists = wishlist.Query(username, country=site)
            profiles = profile.Query(username, country=site)
        else:
            return render.search()

        info = profiles.basic_info()          
        total = wishlists.total_expenses()
        covers = wishlists.covers()
        urls = wishlists.urls()
        titles = wishlists.titles()
        authors = wishlists.authors()
        prices = wishlists.prices()
        items = zip(covers, urls, titles, authors, prices)

        listnames = profiles.wishlists()
        listcodes = profiles.wishlists_details()[0]
        listsizes = profiles.wishlists_details()[1]
        lists = zip(listnames, listsizes, listcodes)
        
        configs = [wishlists.currency, wishlists.symbol, wishlists.domain]
        return render.result(info, configs, lists, items, total)

#web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)

if __name__ == "__main__":
    #web.runwsgi = web.runfcgi
    app.run()
