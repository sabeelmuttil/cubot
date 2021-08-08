# -*- coding: utf-8 -*-
#!/usr/bin/python
from __future__ import unicode_literals
import time
from datetime import datetime
import mysql.connector as mysql
import bs4
from bs4 import BeautifulSoup
from unidecode import unidecode
import urllib2
import requests
from urllib2 import urlopen as ureq
import nltk  # noun splitter
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
# database connection
db = mysql.connect(user="root", password="", database="cubot")
cur = db.cursor()
while(1):
    notificationdocs = []
    notifications = []
    print('Trying to load notifications...')
    uocnot = 'http://www.universityofcalicut.info/index2.php?option=com_content&task=view&id=744'
    r = requests.get(uocnot)
    print('Trying to load timetable')
    uoctimetable = 'http://www.universityofcalicut.info/index2.php?option=com_content&task=view&id=745'
    print('[Done]')
    page_text = unidecode(r.text)
    page_text = r.text.encode('ascii', 'ignore')
    page_soupy = BeautifulSoup(page_text, 'html.parser')
    print('Page title says : ' + page_soupy.title.string)
    page_soupy.find_all('a')
    for link in page_soupy.findAll('a'):
        # got links to pdfs
        print('found link ' + link.get('href'))
        notificationdocs.append(link.get('href'))
        temp = u'null'
        notifications.append(link.string)
        try:
            temp = link.string
            print temp
        except:
            print 'fixing unicode error'
            temp = temp.encode('latin_1')
            print temp
    # add links and text to database from those arrays
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    i = 0
    for items in notifications:
        doclink = notificationdocs[i]
        i = i + 1
        try:
            text = items

            cur.execute("INSERT IGNORE INTO cubot.updates (date,text,type,link,tags) VALUES (%s,%s,%s,%s,%s)", (str(
                timestamp), text, 'Notification', str(doclink), text))
            db.commit()
        except:
            if items is not None:
                text = u'sample'
                text = items.encode('latin_1')
                text.strip()
                # noun splitter [tags]
                tokens = nltk.word_tokenize(text)
                tagged = nltk.pos_tag(tokens)
                nouns = [word for word, pos in tagged
                         if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
                tags = [x.lower() for x in nouns]
                tags = str(tags)

                cur.execute("INSERT IGNORE INTO cubot.updates (date,text,type,link,tags) VALUES (%s,%s,%s,%s,%s)", (str(
                    timestamp), text, 'Notification', str(doclink), tags))
                db.commit()

    # timetable
    timetable = []
    timedocs = []
    print('Trying to load timetable')
    uoctimetable = 'http://www.universityofcalicut.info/index2.php?option=com_content&task=view&id=745'
    r = requests.get(uoctimetable)
    print('[Done]')
    page_text = unidecode(r.text)
    page_text = r.text.encode('ascii', 'ignore')
    page_soupy = BeautifulSoup(page_text, 'html.parser')
    print('Page title says : ' + page_soupy.title.string)
    page_soupy.find_all('a')
    for link in page_soupy.findAll('a'):
        # got links to pdfs
        print('found link ' + link.get('href'))
        timedocs.append(link.get('href'))
        temp = u'null'
        timetable.append(link.string)
        try:
            temp = link.string
            print temp
        except:
            print 'fixing unicode error'
            temp = temp.encode('latin_1')
            print temp
    # add links and text to database from those arrays
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    i = 0
    for items in timetable:
        doclink = timedocs[i]
        i = i + 1
        try:
            text = items
            cur.execute("INSERT IGNORE INTO cubot.updates (date,text,type,link,tags) VALUES (%s,%s,%s,%s,%s)", (str(
                timestamp), text, 'Timetable', str(doclink), text))
            db.commit()
        except:
            if items is not None:
                text = u'sample'
                text = items.encode('latin_1')
                text.strip()
                # noun splitter [tags]
                tokens = nltk.word_tokenize(text)
                tagged = nltk.pos_tag(tokens)
                nouns = [word for word, pos in tagged
                         if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
                tags = [x.lower() for x in nouns]
                tags = str(tags)

                cur.execute("INSERT IGNORE INTO cubot.updates (date,text,type,link,tags) VALUES (%s,%s,%s,%s,%s)", (str(
                    timestamp), text, 'Timetable', str(doclink), tags))
                db.commit()

    # Results
    result = []
    pid = []
    print('Trying to load Results')
    resultpage = 'http://www.cupbresults.uoc.ac.in/CuPbhavan/getlist.php'
    urlhead = 'http://www.cupbresults.uoc.ac.in/CuPbhavan/common_result.php?resulttxt='
    r = requests.get(resultpage)
    print('[Done]')
    page_text = unidecode(r.text)
    page_text = r.text.encode('ascii', 'ignore')
    page_soupy = BeautifulSoup(page_text, 'html.parser')
    page_soupy.find_all('a')
    for link in page_soupy.findAll('a'):
        # got links to pdfs
        temp = u'null'
        pid.append(link['id'])
        result.append(link.string)
        try:
            temp = link.string
            print temp
        except:
            print 'fixing unicode error'
            temp = temp.encode('latin_1')
            print temp
    # add links and text to database from those arrays
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    i = 0
    for items in result:
        url = urlhead + pid[i]
        print url
        i = i + 1
        try:
            text = items
            cur.execute("INSERT IGNORE INTO cubot.updates (date,text,type,link,tags) VALUES (%s,%s,%s,%s,%s)", (str(
                timestamp), text, 'Result', str(url), text))
            db.commit()
        except:
            if items is not None:
                text = u'sample'
                text = items.encode('latin_1')
                text.strip()
                # noun splitter [tags]
                tokens = nltk.word_tokenize(text)
                tagged = nltk.pos_tag(tokens)
                nouns = [word for word, pos in tagged
                         if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
                tags = [x.lower() for x in nouns]
                tags = str(tags)

                cur.execute("INSERT IGNORE INTO cubot.updates (date,text,type,link,tags) VALUES (%s,%s,%s,%s,%s)", (str(
                    timestamp), text, 'Result', str(url), tags))
                db.commit()

    cur.execute("DELETE FROM cubot.updates WHERE text IS NULL;")
    db.commit()
    cur.execute("DELETE FROM cubot.updates WHERE text='>>Next'")
    db.commit()
    print 'Fetching compleated'
    # close the cursor
    cur.close()
    # close the connection
    db.close()
    time.sleep(300)  # 5 minutes
