from webpage import webpage
import automator
import re
import random
from time import sleep
from datetime import date, timedelta
import pycurl
from StringIO import StringIO
import os

class RealtorListingPage(webpage):
    def __init__(self,url=""):
        webpage.__init__(self,url)
        self.status=''
        self.listdate=''
        self.mls=''
        self.address=''
        self.price=''
        self.beds=''
        self.baths=''
        self.homesize=''
        self.lotsize=''
        self.description=''
        self.imageurls=[]
        self.comments=''

        self.photoCount=-1

    def processRealtor(self):
        #***************Get listing status
        try:
            self.status = self.doc.xpath("//div[@id='PropertyAddress']/p//i")[0].tail.strip()
        except:
            pass

        #***************Get listing date
        try:
            self.listdate = self.doc.xpath(".//*[@id='OnSite']//th[contains(text(),'Added to Site')]/following-sibling::td/text()")[0]
        except:
            pass

        #***************Get address
        try:
            street = self.doc.xpath("//*[@id='PropertyAddress']/h1/span[contains(@itemprop,'streetAddress')]/text()")[0]
            city = self.doc.xpath("//*[@id='PropertyAddress']/h1/span[contains(@itemprop,'addressLocality')]/text()")[0]
            state = self.doc.xpath("//*[@id='PropertyAddress']/h1/span[contains(@itemprop,'addressRegion')]/text()")[0]
            zipcode = self.doc.xpath("//*[@id='PropertyAddress']/h1/span[contains(@itemprop,'postalCode')]/text()")[0]
            self.address = street+', '+city+', '+state+' '+zipcode
        except:
            pass
        #***************Get price
        try:
            self.price = self.doc.xpath(".//*[@id='MetaData']//span[contains(@itemprop,'price')]/text()")[0].strip()
        except:
            pass

        #***************Get beds
        try:
            self.beds = self.doc.xpath("//*[@id='GeneralInfo']/ul//span[contains(text(),'Beds')]/following-sibling::span/text()")[0]
        except:
            pass
        #***************Get baths
        try:
            self.baths = self.doc.xpath("//*[@id='GeneralInfo']/ul//span[contains(text(),'Baths')]/following-sibling::span/text()")[0]
        except:
            pass
        #***************Get homesize
        try:
            self.homesize = self.doc.xpath("//*[@id='GeneralInfo']/ul//span[contains(text(),'House Size')]/following-sibling::span/text()")[0]
        except:
            pass
        #***************Get lotsize
        try:
            self.lotsize = self.doc.xpath("//*[@id='GeneralInfo']/ul//span[contains(text(),'Lot Size')]/following-sibling::span/text()")[0]
        except:
            pass
        #***************Get description
        try:
            self.description = self.doc.xpath("//*[@id='tab-overview']//p[@class='property-description']/text()")[0].strip()
        except:
            pass
        #***************Get image urls

        if self.status == 'Property Records' or self.status == 'Recently Sold' :
            self.photoCount=1
            photoUrl = self.doc.xpath("//*[@id='EmbeddedPhotoGallery']/figure/div/ul/li/img/@src")
            self.imageurls.append(photoUrl[0])
        else:
            photoPageHtml = automator.getPhotoPage(self.url)
            if photoPageHtml != '':
                photoPage = webpage().fromstring(photoPageHtml,self.url)
                photoPage.save('trouble1.html')
                self.photoCount = photoPage.doc.xpath("//*[@id='TabDetails']/ul/li[2]/a/text()")[0]
                self.photoCount = re.findall('Photos \((.*?)\)',self.photoCount)[0]
                for i in range(0,int(self.photoCount)):
                    try:
                        #print 'finding url'
                        #print i
                        #print photoPage.doc.xpath("//img[@id='"+str(i)+"']/@src")
                        thumbUrl = photoPage.doc.xpath("//img[@id='"+str(i)+"']/@src")[0]
                        #print thumbUrl
                        photoUrl = thumbUrl.replace('t.jpg','r.jpg').replace('l.jpg','r.jpg')
                        self.imageurls.append(photoUrl)
                    except:
                        #print self.photoCount
                        #print photoPage.doc.xpath("//img[@id='"+str(i)+"']/@src")
                        self.save('trouble2.html')
                        #print 'trouble'
                        exit()
        return self

    def load(self,path):
        webpage.load(self,path)
        self.processRealtor()
        return self

    def process(self):
        webpage.process(self)
        self.processRealtor()
        return self


    def getdict(self):
        return {"url":self.url,"status":self.status,"listdate":self.listdate,"mls":self.mls,"address":self.address,"price":self.price,\
                "beds":self.beds,"baths":self.baths,"homesize":self.homesize,"lotsize":self.lotsize,"description":self.description,\
                "images":self.imageurls,"comments":self.comments}

    def saveimages(self):
        imageCount = len(self.imageurls)
        counter = 0
        for i in self.imageurls:
            counter = counter + 1
            print 'saving image',counter,'of',imageCount
            self.saveimage(i,self.url,ref=self.url)
            sleep(random.uniform(2.2,8.7))


    def __str__(self):
        return \
         self.url+'\n'+\
         self.status+'\n'+\
         self.listdate+'\n'+\
         self.mls+'\n'+\
         self.address+'\n'+\
         self.price+'\n'+\
         self.beds+'\n'+\
         self.baths+'\n'+\
         self.homesize+'\n'+\
         self.lotsize+'\n'+\
         self.description+'\n'+\
         self.comments+'\n'+\
         str(self.imageurls)