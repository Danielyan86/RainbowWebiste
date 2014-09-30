
# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db.models import Q
from SearchDiamond.models import *

import requests
import json
import operator

# -*- coding: unicode-escape -*-
Shape_add_slash_unicode = {u"\u5706\u5f62":"\\\u5706\\\u5f62", u'\u57ab\u5f62':'\\\u57ab\\\u5f62', u'\u516c\u4e3b\u65b9':'\\\u516c\\\u4e3b\\\u65b9',\
                            u'\u7956\u6bcd\u7eff':'\\\u7956\\\u6bcd\\\u7eff', u'\u692d\u5706\u5f62':'\\\u692d\\\u5706\\\u5f62', u'\u5fc3\u5f62':'\\\u5fc3\\\u5f62',\
                            u'\u57ab\u5f62':'\\\u57ab\\\u5f62', u'\u68a8\u5f62':'\\\u68a8\\\u5f62',u'\u9a6c\u773c\u5f62':'\\\u9a6c\\\u773c\\\u5f62',
                            }
current_page = 0

class search_diamonds(object):
    requst_data={}
    return_data = {}
    total_number = 0 # the total number of diamonds
    page = 0   #toatl pages
    page_list = []
    empty_result = False
    
    def __init__(self, where={}):
        self.get_diamonds_data(where)

    def get_diamonds_data(self,where):
        amount_of_search = len(Diamonds.objects.all())
        print "enter", amount_of_search
        self.total_number = amount_of_search
        self.get_page_number()
        self._deal_page()
        
        if where:
            print "-----------------------------enter get_diamonds_data-----------------------"
            DB_query_parameters = []
            print where.values()
            #catagorized the paramters
            color_para = []
            purity_para = []
            cut_para = []
            polish_para = []
            shape_para = []
            fol_para = []
            cert_para = []
            symmetry_para = []

            for para in where.keys():
                if para.find("color") != -1:
                    color_para.append(where[para])
                elif para.find("purity") != -1:
                    purity_para.append(where[para])
                elif para.find("cut") != -1:
                    cut_para.append(where[para])
                elif para.find("polish") != -1:
                    polish_para.append(where[para])
                elif para.find("shape") != -1:
                    shape_para.append(Shape_add_slash_unicode[where[para]])
                elif para.find("fol") != -1:
                    fol_para.append(where[para])
                elif para.find("cert") != -1:
                    cert_para.append(where[para])
                elif para.find("symmetry") != -1:
                    symmetry_para.append(where[para])

            if color_para:
                print color_para
                DB_query_parameters.append(Q(color__in = color_para))
            if purity_para:
                DB_query_parameters.append(Q(purity__in = purity_para))
            if cut_para:
                DB_query_parameters.append(Q(cut__in = cut_para))
            if polish_para:
                DB_query_parameters.append(Q(polish__in = polish_para))
            if shape_para:
                DB_query_parameters.append(Q(shape__in = shape_para))
            if fol_para:
                DB_query_parameters.append(Q(flo__in = fol_para))
            if cert_para:
                DB_query_parameters.append(Q(cert__in = cert_para))
            if symmetry_para:
                DB_query_parameters.append(Q(symmetry__in = symmetry_para))

                    # Diamonds.objects.filter(color__in =[u'D',u'E'] ).all().values() 
            # if "purity" in where.keys():
            #     if where["purity"] != "":
            #         # purity1= where["purity"][0]
            #         # where['purity'] = str(purity1)
            #         print type(where['purity'])
            #         print where
            #         print "purity is :", where['purity']
            #         for i in where['purity']:
            #             print i
            #         DB_query_parameters.append(Q(purity__in = where["purity"]))
            #         # print "purity results is:,", Diamonds.objects.filter(purity__in = "I2").all().values() 
            #         # print "cut results is:,", Diamonds.objects.filter(cut__in = "V").all().values()
            #         # print "fol results is:,", Diamonds.objects.filter(flo__in = "N").all().values()
            #         # print "purity results is:,", Diamonds.objects.filter(purity__in = "I2").all().values()
            # if "cut" in where.keys():
            #     if where["cut"] != '':
            #         DB_query_parameters.append(Q(cut__in = where["cut"]))
            # if "polish" in where.keys():
            #     if where["polish"] != u'':
            #         DB_query_parameters.append(Q(polish__in = where["polish"]))
            # if "fol" in where.keys():
            #     if where["fol"] != u'':
            #         DB_query_parameters.append(Q(fol__in = where["fol"]))
            # if "shape" in where.keys():
            #     if where["shape"] != u'':
            #         DB_query_parameters.append(Q(shape__in = Shape_add_slash_unicode[where["shape"]]))
            # if "symmetry" in where.keys():
            #     if where["symmetry"] != u'':
            #         DB_query_parameters.append(Q(symmetry__in = Shape_add_slash_unicode[where["symmetry"]]))
            # if "cert" in where.keys():
            #     if where["cert"] != u'':
            #         DB_query_parameters.append(Q(cert__in = where["cert"]))
            if "page" in where.keys():
                current_page = where["page"]
            if "weight-little" in where.keys():
                print "weight caculation"
                if where["weight-little"] != "" or where["weight-big"] != "":
                    DB_query_parameters.append(Q(weight__range = (where["weight-little"] ,where["weight-big"])))
            if DB_query_parameters:
                #deal with the results based on the number of results
                print DB_query_parameters
                amount_of_search = len(Diamonds.objects.filter(reduce(operator.and_, DB_query_parameters)).all())
                self.total_number = amount_of_search
                print self.total_number
                self.get_page_number()

                print "the page is:",self.page
                self._deal_page()
                if amount_of_search >= 20:
                    start_number = (int(current_page)-1) * 20 +1
                    end_number = start_number + 20
                    self.return_data = Diamonds.objects.order_by('price').filter(reduce(operator.and_, DB_query_parameters)).all()[start_number:end_number].values()
                else:
                    self.return_data = Diamonds.objects.order_by('price').filter(reduce(operator.and_, DB_query_parameters)).all()[1:].values()
    #                 print self.return_data
                
                #decode the value from DB so that it couls be shown in browser normally
                self._unicode_decode()

            # only the page is changed in submit condition 
            elif current_page:
                start_number = (int(current_page)-1) * 20 +1
                end_number = start_number + 20
                self.return_data = Diamonds.objects.order_by('price').all()[start_number:end_number].values()
                self._unicode_decode()

    #caculate the total pages shown in web page    
    def get_page_number(self):
        if self.total_number%20 == 0:
            self.page = self.total_number/20
        else:
            self.page = self.total_number/20 + 1
            
    def _deal_page(self):
        if self.page > 10:
            self.page_list = [i for i in range(1,10)]
        else:
            self.page_list = [i for i in range(1,self.page)]
    
    def _unicode_decode(self):
        for item in self.return_data:
            item["shape"] = str(item["shape"]).decode("unicode-escape")
            item["shape"] = str(item["shape"]).decode("unicode-escape")
    
#create the code dynamic        
class Create_html_codes(object):
    #create the continuous pages which are showed in search page
    def create_pages_codes(self, pages, last_number):
        first_num = int(pages)/10 * 10
        if first_num == 0:
            first_num = 1
        nineth_num = int(pages)/10 * 10 + 9
        if nineth_num > last_number:
            nineth_num = last_number
        page_codes=""
        for i in range(first_num, nineth_num+1):
            if pages == str(i):
                page_codes = page_codes + '<li class="active"><a href="javascript:sumbmit_page(%s);"> %s </a></li>\n' % (str(i),str(i))
            else:
                page_codes = page_codes + '<li><a href="javascript:sumbmit_page(%s);"> %s </a></li>\n' % (str(i),str(i))
        return page_codes

def search_diamond(request):
    
    #if there is a conditional search
    if request.POST:
        request_table  = request.POST
        print "------------------------this request------------------"
        print request_table
        search_obj = search_diamonds(request_table)
        if search_obj.empty_result:
            payload = {
                       "results":"empty",
                       }
        else:
            print "search_obj.page", search_obj.page
            page_js_html = Create_html_codes().create_pages_codes(request_table['page'], search_obj.page)
#             print page_js_html
            payload = {
                        "results":list(search_obj.return_data),
                        "page":search_obj.page,
                        "total_num":search_obj.total_number,
                        "split_page_number":search_obj.page_list,
                        "page_js_html":page_js_html,
                        "current_page":request_table['page'],
                        'success': True
                        }
#         print search_obj.return_data
        #return the data to webste with json format
        for item in search_obj.return_data:
            print item
            item['price'] = int(item['price'] * 6.2 * 1.4)

        return HttpResponse(json.dumps(payload), mimetype="application/json")
    
    #load the whole search page firstly or refresh again
    else:
        print "---------------------enter search Dianmond page firstly:-------------------------"

        search_obj = search_diamonds()
        current_page = 1
        split_page_number = search_obj.page
        return_data = Diamonds.objects.order_by('price').all()[0:20].values()

        # change the price from dollar into RMB and add the profit
        for item in return_data:
            print item
            item['price'] = int(item['price'] * 6.2 * 1.4)

        for item in return_data:
            item["shape"] = str(item["shape"]).decode("unicode-escape")
            item["shape"] = str(item["shape"]).decode("unicode-escape")
        
        return render_to_response("search_diamond.html", {
            "results":return_data, "page":split_page_number, "total_num":search_obj.total_number,
            "split_page_number":range(1, 10), 'current_page':current_page, 'search_active':"active",
        })