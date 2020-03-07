#!/urs/bin/env python
# -*- conding: utf-8 -*-
# @Author : Senci
# @Time   : 2020/2/14 20:35
# @File   : spider.py

from urllib.parse import quote
import requests
from bs4 import BeautifulSoup
import time
import random

class Spider():
    def __init__(self):
        self.keyword = '数据分析师'

    def GetPages(self):
        keyword = quote(self.keyword, safe='/:?=')
        url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,%25E6%2595%25B0%25E6%258D%25AE%25E5%2588%2586%25E6%259E%2590%25E5%25B8%2588,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        span = soup.find('div', class_='p_in').find('span', class_='td')
        page_num = span.get_text().replace('共', '').replace('页，到第', '')
        print(page_num)
        return page_num

    def GetUrls(self, page_num):
        keyword = quote(self.keyword, safe='/:?=')
        urls = []
        p = page_num+1
        for i in range(1, p):
            url = 'http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=000000%2C00&district=000000&funtype=0000&industrytype=00&issuedate=9&providesalary=99&keyword='+keyword + \
                '&keywordtype=2&curr_page=' + \
                str(i) + \
                '&lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&dibiaoid=0&confirmdate=9'
            html = requests.get(url)
            soup = BeautifulSoup(html.content, "html.parser")
            ps = soup.find_all('p', class_='t1')
            for p in ps:
                a = p.find('a')
                urls.append(str(a['href']))
            s = random.randint(5, 30)
            print(str(i)+'page done,'+str(s)+'s later')
            print(urls)
            time.sleep(s)
        return urls


    def GetContent(self,url, headers):
        html = requests.get(url, headers=headers)
        soup = BeautifulSoup(html.content, "html.parser").find('div',class_='tCompanyPage')
        if soup == None:
            record = '特殊网页'+ url
            return record
        else:
            if soup.find('div', class_='research') != None:
                record = soup.find('div', class_='research').get_text()
                print(record)
                return record
            PositionTitle = str(soup.find('h1')['title'])
            print('\n',PositionTitle)
            
            Location = soup.find('p', class_='msg ltype').get_text().strip().replace('\xa0\xa0', '').split('|')
            Adds = Location[0]
            Exp = Location[1]
            Degree = Location[2]
            RecruitNum = Location[-2]
            PostTime = Location[-1]
            #######Skll = Location[6:7]
            print(Adds,Exp,Degree,RecruitNum,PostTime)

            Salary = soup.find('strong').string
            if Salary == None:
                Salary = '空'
            print(Salary)

            CompanyName = soup.find('p', class_='cname').a['title']
            print(CompanyName)

            CompanyWelfare = soup.find_all('span', class_='sp4')
            Welfare = '|'.join([CompanyWelfare[i].get_text().strip() for i in range (0,len(CompanyWelfare)-1)])
            print(Welfare)

            PositionInfo = soup.find('div', class_='bmsg job_msg inbox').get_text(strip=True).strip().replace('\n', '')
            print(PositionInfo)

            CompanyType = soup.find('div', class_='com_tag').get_text().strip().replace('\n\n\n', '\n').replace('\n', '|')
            print(CompanyType)

            Contact = soup.find('div', class_='bmsg inbox')
            if str(type(Contact)) == "<class 'NoneType'>":
                Contact = ''
            else:
                Contact = Contact.get_text().strip().replace(
                    '   ', '').replace('    ', '').replace('地图', '').replace('\n', '')
                print(Contact)
            ConpanyInfo = soup.find('div', class_='tmsg inbox')
            if str(type(ConpanyInfo)) == "<class 'NoneType'>":
                ConpanyInfo = ''
            else:
                ConpanyInfo = ConpanyInfo.get_text().strip()
                print(ConpanyInfo)
            #try:
            record = PositionTitle+'\t'+Adds+'\t'+Salary+'\t'+CompanyName+'\t'+CompanyType+'\t'+Exp+'\t'+Degree+'\t' + \
                    RecruitNum+'\t'+PostTime+'\t'+Welfare+'\t'+PositionInfo + '\t'+str(Contact)+'\t'+str(ConpanyInfo)
            #except Exception as e:
                #record = ''
            #else:
                #pass
            #finally:
                #pass
            print('========================\n'+record+'\n========================')
            return record

    def main(self):
        # with open('keywords.txt', 'r', encoding='utf-8') as f:
        #     keywords = f.readlines()
        # for keyword in keywords[1:]:
        #     keyword = keyword.strip()
        #     print(keyword)
        #    keyword = '数据分析师'
            page_num = int(self.GetPages())
            urls = self.GetUrls(page_num)
            with open(self.keyword+'urls.txt', 'w', encoding='utf-8') as f:
                for url in urls:
                    f.write(url+'\n')
            User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
            cookie = 'guid=14842945278988500031; slife=indexguide%3D1'
            headers = {'User-Agent': User_Agent, 'cookie': cookie}
            with open(self.keyword+'urls.txt', 'r', encoding='utf-8') as f:
                urls = f.readlines()
            records = []
            i = 0
            print(urls)
            for url in urls:
                url = url.strip()
                if url != '':
                    records.append(self.GetContent(url, headers))
                    i += 1
                    s = random.randint(5, 30)
                    print(str(i)+'page done,'+str(s)+'s later')
                    time.sleep(s)
            with open(self.keyword+'.txt', 'w', encoding='utf-8') as f:
                for re in records:
                    f.write(re+'\n')
            print(self.keyword+' Done---------------------------')


if __name__ == '__main__':
    s=Spider()
    s.main()
    # User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    # cookie = 'guid=14842945278988500031; slife=indexguide%3D1'
    # headers = {'User-Agent': User_Agent, 'cookie': cookie}
    # GetContent(url='https://jobs.51job.com/suzhou-gsq/116905647.html?s=01&t=0', headers= headers)
    # # #https://jobs.51job.com/suzhou-gsq/116905647.html?s=01&t=0

