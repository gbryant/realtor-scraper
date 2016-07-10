from time import sleep
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def savedata(path,data):
    file = open(path, 'w')
    #file.write(self.data.encode('ascii','ignore'))
    file.write(data.encode('utf-8','ignore'))
    file.close()

def getRealtorFavorites():
    display = Display(visible=0, size=(800, 600))
    display.start()
    driver = webdriver.Firefox()
    driver.implicitly_wait(10)
    driver.get("http://www.realtor.com")
    element = driver.find_element_by_xpath("//*[@id='menuLogIn']")
    sleep(3)
    element.click()
    element = driver.find_element_by_xpath("//*[@id='siEml']")
    sleep(1)
    element.send_keys("username@domain.com")
    element = driver.find_element_by_xpath("//*[@id='siPwd']")
    sleep(1)
    element.send_keys("password")
    element = driver.find_element_by_xpath("//*[@id='signInSubmit']")
    sleep(2)
    element.click()
    element = driver.find_element_by_xpath("//*[@id='thank-you-login-form']/div[1]/a")
    sleep(2)
    element.click()
    sleep(1)
    driver.get("http://myaccount.realtor.com/properties")
    sleep(5)
    data = driver.page_source
    driver.quit()
    display.stop()
    return (data,"http://myaccount.realtor.com/properties")

def getPhotoPage(url):
    display = Display(visible=0, size=(800, 600))
    display.start()
    driver = webdriver.Firefox()
    driver.implicitly_wait(13)
    driver.get(url)
    try:
        dismiss = driver.find_element_by_xpath("//*[@id='modalClose']")
        print dismiss
        dismiss.click()
    except:
        pass
    try:
        dismiss = driver.find_element_by_xpath("//div[@class='Stage_close_id']")
        print dismiss
        dismiss.click()
    except:
        pass
    sleep(3)
    try:
        scrollto = driver.find_element_by_xpath("//*[@id='OpenHouse1']/h2/span")
        element = driver.find_element_by_xpath("//a[@href='#tab-photos']")
        driver.execute_script("return arguments[0].scrollIntoView();", scrollto)
        sleep(3.5)
        element.click()
        sleep(4.7)
        scrollto = driver.find_element_by_xpath("//*[@id='TabLeadForms']/h2")
        driver.execute_script("return arguments[0].scrollIntoView();", scrollto)
        sleep(5)
        data = driver.page_source
        #savedata("popup.html",data)
        driver.quit()
        display.stop()
        return data
    except:
        print "not found"
        driver.quit()
        return ''
        #id="fullScreenBtn"
