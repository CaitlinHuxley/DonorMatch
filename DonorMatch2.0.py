# import psycopg2
from urllib.request import Request, urlopen
import time
import csv
import re
import bs4 as BS

#conn = psycopg2.connect("dbname='campaign_finance' user='postgres' host='localhost' password='victory2018'")
#cur = conn.cursor()

## Open the file full of prospects
PotentialDonorsFile = open('PotentialDonors.csv', encoding="utf8")
PotentialDonors = csv.reader(PotentialDonorsFile)

## Create a file to put all the successful donation
ConfirmedDonorsFile = open('ConfirmedDonors.csv', 'w', newline='', )
ConfirmedDonors = csv.writer(ConfirmedDonorsFile)
ConfirmedDonors.writerow(['id', 'full name', 'first', 'last', 'zip', 'date', 'amount', 'given to'])

for row in PotentialDonors:
    time.sleep(0)
    potentiallist = row
    print(potentiallist[0], ", ", potentiallist[1], ", ", potentiallist[2], ", ", potentiallist[3])
    id = re.sub('[A-Z]* ', ' ', potentiallist[0])
    id = re.sub('[^a-zA-Z0-9-_*.]', '', id)
    name = re.sub('[A-Z]* ', ' ', potentiallist[1])
    name = re.sub('[^a-zA-Z0-9-_*.]', '', name)
    lastname = re.sub('[A-Z]* ', ' ', potentiallist[2])
    lastname = re.sub('[^a-zA-Z0-9-_*.]', '', lastname)
    zipcode = potentiallist[3]
    url = 'https://www.opensecrets.org/donor-lookup/results?cand=&cycle=&employ=&name=' + str(name) + '+' + str(lastname) + '&order=desc&sort=D&state=&zip=' + str(zipcode)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

#Try to open the page, keep trying till it works
    while True:
        try:
            page = urlopen(req).read()
        except Exception as ex:
            print(ex)
            time.sleep(1)
            continue
        break

#Look at the page
    soup = BS.BeautifulSoup(page, "lxml")
    for entry in soup.find_all('tr'):
        donation = []
        for line in entry.find_all('td'):
            donation.append(str(line.text))
        try:
            donation_date = str(donation[3])
            donation_amnt = str(donation[4])
            donation_cand = str(donation[5])
            print(donation_date, '-', donation_amnt, '-', donation_cand)
        except:
            print('No Data')
            pass
        try:
            ConfirmedDonors.writerow([id, name + ' ' + lastname, name, lastname, zipcode, donation_date, donation_amnt, donation_cand])
        except:
            pass

ConfirmedDonorsFile.close()