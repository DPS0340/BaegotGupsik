from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from models import menu as makemenu
import requests
import bs4
import datetime
import json
import datetime
import sqlite3


def keyboard(request):

    return JsonResponse({
        'type': 'buttons',
        'buttons': ['오늘 급식 보여줘', '내일 급식 보여줘', '이번달 남은 급식 보여줘']
    })


@csrf_exempt
def message(request):
    global menu
    head = ''
    todaysmenu = makemenu.objects.get(id=1).body
    tomorrowsmenu = makemenu.objects.get(id=2).body
    thismonthsmenu = ''
    menu = ''
    for i in makemenu.objects.all():
        thismonthsmenu += i.body
    json_str = (request.body).decode('utf-8')
    received_json = json.loads(json_str)
    question_name = received_json['content']
    if question_name == '오늘 급식 보여줘':
        head = '오늘'
        menu = todaysmenu
    elif question_name == '내일 급식 보여줘':
        head = '내일'
        menu = tomorrowsmenu
    elif question_name == '이번달 남은 급식 보여줘':
        head = '이번달의 남은'
        menu = thismonthsmenu
    return JsonResponse({
        'message': {
                        'text': '%s 급식입니다. \n\n %s' % (head, menu)
                        },
        'keyboard': {
            'type': 'buttons',
            'buttons': ['오늘 급식 보여줘', '내일 급식 보여줘', '이번달 남은 급식 보여줘']
        }

    })


def crawl(crawl):
    global menu, menu1
    makemenu.objects.all().delete()
    sqlite3.connect('/home/jiho/venv/db.sqlite3').cursor().execute(
        "DELETE FROM sqlite_sequence WHERE name = 'menu'").close()
    month = datetime.datetime.now().strftime("%m")
    day = datetime.datetime.now().strftime("%d")
    time = ("%s월 %s일 [중식]" % (month, day)).replace("0", '')
    raw = requests.get(
        "http://www.iamschool.net/organization/122238/group/3224954")
    soup = bs4.BeautifulSoup
    html = soup(raw.text, "html.parser")
    menus = []
    finalmenus = []
    rawmenus = html.find_all("a", {"class": "_3bkZ"})
    count = 0
    menu1 = ''
    returnchar = ''
    for tag in reversed(rawmenus):
        print(tag)
        if tag.find("[중식]") != -1:
            menu = tag.get_text()
            menus.append(menu)
    print(menus)
    for i in range(len(menus)):
        element = menus.pop(0)
        if (i + 1) % 2 == 1:
            menu1 = element
        if (i + 1) % 2 == 0:
            date = element
            print(time)
            print(date)
            if time == date:
                dateplusmenu = '\n' + date + '\n' + menu1
                finalmenus.append(dateplusmenu)
                count = 1
            else:
                if count == 1:
                    dateplusmenu = '\n' + date + '\n' + menu1
                    finalmenus.append(dateplusmenu)
        i = 0
    for menu in finalmenus:
        i += 1
        savemenu = makemenu(id=i, body=menu)
        savemenu.save()
        returnchar += menu + '<br>'
    returnchar += '<br>' + '크롤링이 완료되었습니다.'
    return HttpResponse(returnchar)
