#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import sys
import time
import chardet  #中文编码判断
import urllib2
import hashlib
import datetime
import json

reload(sys)
sys.setdefaultencoding( "utf-8" )

class CryptoCoinTool(object):
    """docstring for ClassName"""
    def __init__(self, isCmdMode = True):
        
        self.isCmdMode = isCmdMode
        self.wdriver = None

        self.AllCoinURL = 'https://cn.investing.com/crypto/currencies'

        self.oneCoinURLBase = 'https://cn.investing.com/crypto/'

        self.lastDownDay = ''                                           #上次更新数据时间,计划每小时更新一次，每天读取一次最新日数据
        self.coinList = []                                              #上次更新数据市值排名

        #货币图标数据下载地址
        self.coinIconUrl = 'https://i-invdn-com.akamaized.net/crypto_icons/v_6896_cryptoIconAll.css'

        self.todayCoinsNumber = 0                                       #今天虚拟货数种类
        self.todayMarketCap = 0                                         #今日虚拟货币总市值,单位:美元
        self.lastDayVol = 0                                             #24小时成交金额,单位:美元

        #node investing.js get -i 1037047 -s 10/01/2017 -e 01/14/2018


    #下载所有货币的图标图片半切割为单张图片
    def downloadIconImage(self):
        pass

    #获取当日所有货币价格,涨幅，成交量
    def getTodayAllPrice(self):

        pass


    # def getManager(wdriver,tid):
    def conventStrTOUtf8(self,oldstr):
        try:
            nstr = oldstr.encode("utf-8")
            return nstr
        except Exception as e:
            print 'nstr do not encode utf-8'
        cnstrtype = chardet.detect(oldstr)['encoding']
        utf8str =  oldstr.decode(cnstrtype).encode('utf-8')
        return utf8str

    def getYearMathDay(self,pstr):
        tmptime = time.strptime(pstr,'%a %d %b %Y')
        stemtime = int(time.mktime(tmptime)) + (22 * 60 * 60) #转为中国时间
        outdate = time.strftime("%Y-%m-%d", time.gmtime(stemtime))
        wday = time.strftime("%w", time.gmtime(stemtime))
        return outdate,wday

    def getAllCoinFromWeb(self,browser):


        isReload = False

        oldcoins = {}

        if os.path.exists('coins.csv'):
            f = open('coins.csv','r')
            csvtmp = f.readlines()
            f.close()
            for l in csvtmp:
                linestr = l.replace('\r','').replace('\n','')
                ltmps = linestr.split(',')
                oldcoins[ltmps[1]]= ltmps
            isReload = True
        browser.implicitly_wait(10)
        isReload = False
        if isReload:

            diftab = browser.find_element_by_xpath('//*[@id="top_crypto_tbl"]/tbody')                       


            tmpn = 0

            

            tmpstr = diftab.text
            coins = tmpstr.split('\n')

    # 1 Bitcoin BTC 13,369.0 $228.68B $10.94B 32.74% 1 -5.30% -16.98%
    # 2 Ethereum ETH 1,309.70 $129.00B $4.81B 14.38% 0.0977734 -7.25% +15.61%
    # 3 Ripple XRP 1.7934 $71.20B $1.87B 5.60% 0.0001351 -8.73% -45.10%
    # 4 Bitcoin Cash BCH 2,492.9 $42.98B $984.90M 2.95% 0.186817 -6.07% -9.97%
    # 5 Cardano ADA 0.76255 $20.04B $152.18M 0.46% 0.00005682 -11.55% -23.36%
    # 6 Litecoin LTC 239.81 $13.13B $974.97M 2.92% 0.0176286 -3.18% -16.66%
    # 7 NEM XEM 1.26705 $12.19B $37.70M 0.11% 0.00009959 -11.57% -23.99%
    # 8 Stellar XLM 0.61184 $11.16B $114.50M 0.34% 0.00004584 -5.29% -10.10%
    # 9 NEO NEO 156.88 $10.33B $515.51M 1.54% 0.0116839 +8.95% +55.23%
    # 10 IOTA MIOTA 3.7000 $10.24B $132.20M 0.40% 0.0002708 -6.36% -11.91%
    # 11 EOS EOS 13.4510 $8.27B $1.22B 3.66% 0.00100837 -17.74% +10.29%
    # 12 Dash DASH 995.00 $7.88B $173.50M 0.52% 0.0740698 -8.39% -22.44%
            outs = []

            for s in coins:
                tmp = ' '.join(s.split())
                tmps = tmp.split(' ')
                print len(tmps),tmps[0],tmps[-8]
            return outs
        else:
            diftab = browser.find_elements_by_xpath('//*[@id="top_crypto_tbl"]/tbody/tr')   
            count = 0
            coins = []
            for d in diftab:
                # print d.text
                count += 1
                print count
                tmps = []
                #//*[@id="top_crypto_tbl"]/tbody/tr[1]/td[1]
                # for n in range(len(tds)):
                #     if n == 0:
                #         tmpx = tds[n]
                #         tmps.append(int(tmpx.text))

                #市值排行
                # nstr = d.find_element_by_xpath('//td[1]')
                tmpx = d.find_element_by_css_selector("td:nth-child(1)")
                tmpn = int(tmpx.text)    
                tmps.append(tmpn)

                #货币全名称
                # tmpx = d.find_element_by_xpath('//td[3]')
                tmpx = d.find_element_by_css_selector("td:nth-child(3)")  
                tmps.append(tmpx.text)

                #货币缩写
                # tmpx = d.find_element_by_xpath('//td[4]')  
                tmpx = d.find_element_by_css_selector("td:nth-child(4)")
                tmps.append(tmpx.text)

                #当前价格
                # tmpx = d.find_element_by_xpath('//td[5]')  
                tmpx = d.find_element_by_css_selector("td:nth-child(5)")
                tmpprice = tmpx.text.replace(',','')
                tmps.append(tmpprice)

                #当前市值
                # tmpx = d.find_element_by_xpath('//td[6]')  
                tmpx = d.find_element_by_css_selector("td:nth-child(6)")
                datavalue = tmpx.get_attribute('data-value')
                tmps.append(datavalue)
                tmps.append(tmpx.text)

                #24小时成交量
                # tmp7 = d.find_element_by_xpath('//td[7]') 
                tmp7 = d.find_element_by_css_selector("td:nth-child(7)")
                datavalue = tmp7.get_attribute('data-value')
                tmps.append(datavalue)
                tmps.append(tmp7.text) 

                #8:交易份额
                # tmpx = d.find_element_by_xpath('//td[8]') 
                tmpx = d.find_element_by_css_selector("td:nth-child(8)")
                tmps.append(tmpx.text)

                #9:对应的BTC价格
                # tmpx = d.find_element_by_xpath('//td[9]') 
                tmpx = d.find_element_by_css_selector("td:nth-child(9)")
                tmps.append(tmpx.text)

                #10:1天涨跌幅
                # tmpx = d.find_element_by_xpath('//td[10]') 
                tmpx = d.find_element_by_css_selector("td:nth-child(10)")
                tmps.append(tmpx.text)

                #11:7天涨跌幅
                # tmpx = d.find_element_by_xpath('//td[11]') 
                tmpx = d.find_element_by_css_selector("td:nth-child(11)")
                tmps.append(tmpx.text)
                
                coins.append(tmps)
                
            return coins


    def getDateDayWithTime(self,ptime = None):
        loctim = time.localtime(ptime)
        #time.struct_time(tm_year=2015, tm_mon=8, tm_mday=2, tm_hour=12, tm_min=16, tm_sec=47, tm_wday=6, tm_yday=214, tm_isdst=0)
        m = str(loctim.tm_mon)
        if len(m) == 1:
            m = '0' + m

        d = str(loctim.tm_mday)
        if len(d) == 1:
            d = '0' + d

        sendmsg = str(loctim.tm_year) + '-' + m + '-' +  d
        return sendmsg

    #获取公司资料
    def moneyMsg(self):

        if not self.wdriver:
            if self.isCmdMode:
                print 'used phantomjs'
                import selenium.webdriver.phantomjs.webdriver as wd
                self.wdriver = wd.WebDriver('/usr/local/bin/phantomjs')       #test
                self.wdriver.maximize_window()
            else:
                print 'used chrome'
                import selenium.webdriver.chrome.webdriver as  wd
                self.wdriver = wd.WebDriver('/Users/mage/Documents/tool/cmdtool/chromedriver')       #test
                self.wdriver.maximize_window()

        self.wdriver.get(self.AllCoinURL)
        starttime = time.ctime(int(time.time()))
        
        #难度信息 
        datdic= self.getAllCoinFromWeb(self.wdriver)    
        print 'start', starttime
        print 'end',time.ctime(int(time.time()))                                           
        return datdic

    def getUrl(self,purl):
        try:
            req = urllib2.Request(purl)
            req.add_header('User-agent', 'Mozilla 5.10')
            res = urllib2.urlopen(req)
            html = self.conventStrTOUtf8(res.read())
            return html
        except Exception, e:
            print e
        return None

def main():

    sharetool = CryptoCoinTool(isCmdMode = True)

    coinsdats = sharetool.moneyMsg()

    out = '市值排名,名称,符号,价格USD,精确市值,缩略市值,24小时成交量,24小时量缩写,交易份额,价格BTC,1天(%),7天\n'
    for d in coinsdats:
        tmpstr = ''
        for t in d:
            tmpstr += str(t) + ','
        out += tmpstr[:-1] + '\n'

    out = out[:-1]

    f = open('coins.csv','w')
    f.write(out)
    f.close()

    raw_input('input enter for end.')

    sharetool.wdriver.quit()

    cmd = '/Users/mage/Documents/tool/cmdtool/killpswithflog phantomjs --cookies-file=/var/folders'
    os.system(cmd)

#测试
if __name__ == '__main__':
    main()
    # test()




