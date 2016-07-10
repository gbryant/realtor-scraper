from webpage import webpage
from realtor import RealtorListingPage
import automator
import os
from pymongo import MongoClient
from time import sleep
import random

client = MongoClient()
db = client.RealEstate
collection = db.Realtor

def getlistingurls(wpage):
    pages=[]
    for i in wpage.doc.xpath("//a[contains(@class,'viewDetails')]"):
        pages.append(i.get('href'))
    return pages

try:
    os.remove('cookie.txt')
except:
    pass

realtor = webpage()

if os.path.exists("favorites.html") != True:
    print 'fetching favorites file'
    data = automator.getRealtorFavorites()
    realtor.fromstring(data[0],data[1])
    realtor.save('favorites.html')
else:
    print 'using saved file'
    realtor.load('favorites.html')


#***************Get saved comments from the favorites page
comments=[]
rawComments = realtor.doc.xpath("//*[contains(@id,'editNotesSection')]")
for i in rawComments:
   comments.append(list(i)[0].text.strip())

#***************Get urls not already in the database and pair up the comments
newUrls=[]
theUrls=getlistingurls(realtor)
for i in range(0,len(theUrls)):
    cursor = collection.find({"url": theUrls[i]})
    if cursor.count() == 0:
        newUrls.append((theUrls[i],comments[i]))

print 'adding',len(newUrls),'new urls to the database'

total = len(newUrls)
counter=0
for i in newUrls:
    print i[0]
    counter = counter + 1
    listing = RealtorListingPage(i[0])
    print listing.get()
    listing.comments=i[1]
    print 'inserting into database'
    collection.insert_one(listing.getdict())
    listing.saveimages()
    print 'next',(counter+1),'of',total
    sleep(random.uniform(5.32,45.7))


