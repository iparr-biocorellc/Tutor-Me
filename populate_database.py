# import os
#
# import requests
#
# from tutor_me.models import Course
#
# def get_url_page(page):
#     url = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1228&page=" + str(page)
#     return requests.get(url).json()
#
# def set_classes():
#     counter = 1
#     url_list = get_url_page(counter)
#     while len(url_list) > 0:
#         for c in url_list:
#             course = Course(number=c['class_nbr'], mnemonic=c['subject']+c['catalog_nbr'], name=c['descr'])
#             course.save()
#         counter += 1
#         url_list = get_url_page(counter)
