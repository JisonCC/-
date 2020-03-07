#!/urs/bin/env python
# -*- conding: utf-8 -*-
# @Author : Senci
# @Time   : 2020/3/6 14:45
# @File   : house-data.py

import requests
from bs4 import BeautifulSoup
import re

import pandas as pd
import random
import time

proxies={}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'cookie': 'global_cookie=ndhzo4i3v9myct7aqau6zp6si10k0ncoeps; __utmz=147393320.1568695301.1.1.utmcsr=shbbs.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/esf~-1/538150834_538150842.htm; __utma=147393320.1476417876.1568695301.1568695301.1568771948.2; __utmc=147393320; Captcha=434D58793841766F7637624862786B682B684D4B454431767946477634343578436B6978474361474C45335739576D5139355553557463676C6150554F45377962612B456F624974536F383D; newhouse_user_guid=35B671E8-BF35-888C-AC78-ED09FB6489C8; newhouse_chat_guid=3262F18D-7EFB-AE4D-CC6E-D47888369019; g_sourcepage=esf_xq%5Elb_pc; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; unique_cookie=U_7eu0ocfmua6k7nyn858kd6mb727k0omb896*20; __utmb=147393320.60.10.1568771948'
}
url_souce = 'https://sz.esf.fang.com'


def get_true_url(old_url):
    '''获得正确的url'''
    # print(old_url)
    r = requests.get(url=old_url, headers=headers)
    if r'<title>跳转...</title>' in r.text:
        soup = BeautifulSoup(r.text, 'lxml')
        new_url = soup.find(name='a', attrs={'class': 'btn-redir'}).attrs['href']
        return new_url
    return old_url


def get_num():
    '''获取总页数'''

    true_url = r"https://sz.esf.fang.com/housing/85__1_0_0_0_1_0_0_0/"
    true_url = get_true_url(true_url)
    r = requests.get(url=true_url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    a = soup.find('div', class_='fanye gray6').find('span',class_='txt').get_text()
    pag_num=int(re.findall(r"\d+",a)[0])
    print('===========================共{}页数==========================='.format(pag_num))
    return pag_num

def getUrls(page_num):
    '''当前页中小区的url'''
    urls = []
    p = page_num
    url_list=[]
    print('获取当前页中小区的URL中....')
    for i in range(1, p):
        url = 'https://sz.esf.fang.com/housing/85__1_0_0_0_'+str(i)+'_0_0_0/'
        #url = r"https://sz.esf.fang.com/housing/85__0_0_0_0_1_0_0_0/"https://antongdasha.fang.com/
        #print(url)
        reg_url = []
        true_url = get_true_url(url)
        try:
            r = requests.get(url=true_url, headers=headers)
        except:
            time.sleep(3)
            r = requests.get(url=true_url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        for i in range(1, 20):
            if i < 10:
                i = "0" + str(i)
            reg_url.append('https:'+soup.find('div', id='houselist_B09_' + str(i)).find('a')[
                'href'])
            #print(reg_url)
        url_list.append(reg_url)
        #print(url_list)

    return url_list

def get_map_info(old_url):
    '''地图地理位置获取'''
    print('地图地理位置获取中....\n')
    #old_url = "https://sz.esf.fang.com/newsecond/map/NewHouse/NewProjMap.aspx?newcode=2810022810"
    true_url = get_true_url(old_url)
    r = requests.get(url=true_url, headers=headers)
    time.sleep(2)
    r.encoding = 'gb2312'
    soup = BeautifulSoup(r.text, 'lxml')
    a = soup.select('head script')[-2].text.strip()
    #print(a)
    x = re.findall(r'px:"(.*?)",',a)[0]
    y = re.findall(r'py:"(.*?)",',a)[0]
    map_info = [x,y]
    #print(map_info)
    return map_info



def get_house_deep_url(old_url):
    '''获得小区的详请URL'''
    # old_url ='https://doushihuayuan.fang.com/'
    true_url = get_true_url(old_url)
    r = requests.get(url=true_url, headers=headers,proxies=proxies)
    r.encoding = 'gb2312'
    soup = BeautifulSoup(r.text, 'lxml')
    deep_url = 'https:' + soup.find('li',id='kesfxqxq_A01_03_01').a['href']
    #print(deep_url)
    #print(type(deep_url))
    return deep_url



def get_house_info(old_url):
    '''获得小区的详细信息'''
    House_list = []
    House_dict = {'url':'空',
                   '小区名称': '空',
                   '别名':'空',
                   '本月均价':'空',
                   '小区地址':'空',
                   '行政区': '空',
                   '片区': '空',
                   '邮编': '空',
                   '产权描述': '空',
                   '物业类别': '空',
                   '建筑年代': '空',
                   '开发商': '空',
                   '建筑类型': '空',
                   '建筑面积': '空',
                   '占地面积': '空',
                   '房屋总数': '空',
                   '楼栋总数': '空',
                   '绿化率': '空',
                   '容积率': '空',
                   '物业费': '空',
                   '停车位': '空',
                   '交通状况': '空',
                   '周边信息': '空',
                   '地理位置': '空',
                   '更新时间': '空'
}
    deep_url = get_house_deep_url(old_url)
    true_url = get_true_url(deep_url)
    r = requests.get(url=true_url, headers=headers,proxies=proxies)
    time.sleep(3)
    r.encoding = 'gb2312'
    soup = BeautifulSoup(r.text, 'lxml')
    name = soup.find('div', class_='ceninfo_sq').find('a', class_="tt").get_text()

    print(name)
    print(true_url)
    print('获得小区的详细信息中....')
    try:
        other_name= soup.find('div', class_='ceninfo_sq').find('span', class_="bm_title").get_text().split("别名：")[-1]
    except:
        other_name = '无别名'
    Average_price_info = soup.find('div', class_="box detaiLtop mt20 clearfix").find_all('span')
    Average_price_current_month = Average_price_info[0].get_text()
    Average_price_last_month = Average_price_info[1].get_text()
    Average_price_last_year = Average_price_info[-1].get_text()
    House_info = soup.find('div', class_='inforwrap clearfix').find_all('dd')
    Supporting_facilities = soup.find_all('dl', class_='clearfix mr30')[-1]
    Traffic_info = soup.find_all('dl', class_='floatl mr30')[0]
    Address_info = soup.select('body > div.wrap > div.con.clearfix > div.con_left > div:nth-child(6) > div.detailMapwrap > dt > iframe')
    #print(Address_info)
    # print(type(Address_info[0]))
    #print(true_url)
    # print(add_re)
    info = soup.find_all('dl', class_='floatl mr30')[-1]
    House_dict['url'] = true_url
    House_dict['小区名称'] = name
    House_dict['别名'] = other_name
    House_dict['本月均价'] = Average_price_current_month
    House_list.append(true_url)
    House_list.append(name)
    House_list.append(other_name)
    House_list.append(Average_price_current_month)
    try:
        add_re = 'https:' + re.findall(r'src="(.*?)"',str(Address_info))[-1]
    except:
        Address_info = soup.select('body > div.wrap > div.con.clearfix > div.con_left > div:nth-child(5) > div.detailMapwrap > dt > iframe')
        add_re = 'https:' + re.findall(r'src="(.*?)"', str(Address_info))[-1]
    #print(add_re)
    map_info = get_map_info(add_re)
    House_dict['地理位置'] = map_info
    # print(name)
    # print(other_name)
    # print(Average_price_current_month)
    # print(Average_price_last_month)
    # print(Average_price_last_year)
    # print(Traffic_info)
    # print(info)

    for item in House_info:
        #print(item)
        #print(item.find('strong').get_text())
        if item.find('strong').get_text() == '小区地址：':
            address = item.get('title')
            House_dict['小区地址']=address
            House_list.append(address)
            #print(address)
        elif item.find('strong').get_text() == '所属区域：':
            area1 = item.get_text().replace('所属区域：','')
            area1_1 = area1.split(' ')[0]
            area1_2 = area1.split(' ')[-1]
            House_dict['行政区'] = area1_1
            House_dict['片区'] = area1_2
            House_list.append(area1_1)
            House_list.append(area1_2)
            #print(area1.split(' ')[0])
            #print(area1.split(' ')[-1])
        elif item.find('strong').get_text() == '邮    编：':
            area2 = item.get_text().replace('邮    编：','')
            House_dict['邮编'] = area2
            House_list.append(area2)
            #print(area2)
        #########
        elif item.find('strong').get_text() == '产权描述：':
            area3 = item.get_text().replace('产权描述：','')
            House_dict['产权描述'] = area3
            House_list.append(area3)
            #print(area3)
            #print(House_dict['产权描述'])
        #########
        elif item.find('strong').get_text() == '物业类别：':
            area4 = item.get_text().replace('物业类别：','')
            House_dict['物业类别'] = area4
            House_list.append(area4)
            #print(area4)
        elif item.find('strong').get_text() == '建筑年代：':
            area5 = item.get_text().replace('建筑年代：', '')
            House_dict['建筑年代'] = area5
            House_list.append(area5)
            #print(area5)
        elif item.find('strong').get_text() == '开 发 商：':
            area6 = item.get_text().replace('开 发 商：','')
            House_dict['开发商'] = area6
            House_list.append(area6)
            #print(area6)
        elif item.find('strong').get_text() == '建筑类型：':
            area7 = item.get_text().replace('建筑类型：','')
            House_dict['建筑类型'] = area7
            House_list.append(area7)
            #print(area7)

        elif item.find('strong').get_text() == '建筑面积：':
            area8 = item.get_text().replace('建筑面积：','')
            House_dict['建筑面积'] = area8
            House_list.append(area8)
            #print(area9)
        elif item.find('strong').get_text() == '占地面积：':
            area9 = item.get_text().replace('占地面积：','')
            House_dict['占地面积'] = area9
            House_list.append(area9)
            #print(area10)
        elif item.find('strong').get_text() == '房屋总数：':
            area10 = item.get_text().replace('房屋总数：','')
            House_dict['房屋总数'] = area10
            House_list.append(area10)
            #print(area11)
        elif item.find('strong').get_text() == '楼栋总数：':
            area11 = item.get_text().replace('楼栋总数：','')
            House_dict['楼栋总数'] = area11
            House_list.append(area11)
            #print(area12)
        elif item.find('strong').get_text() == '绿 化 率：':
            area12 = item.get_text().replace('绿 化 率：','')
            House_dict['绿化率'] = area12
            House_list.append(area12)
            #print(area13)
        elif item.find('strong').get_text() == '容 积 率：':
            area13 = item.get_text().replace('容 积 率：','')
            House_dict['容积率'] = area13
            House_list.append(area13)
            #print(area14)
        elif item.find('strong').get_text() == '物 业 费：':
            area14 = item.get_text().replace('物 业 费：','')
            House_dict['物业费'] = area14
            House_list.append(area14)
            #print(area15)
    for item in Traffic_info:
        try:
            if '本段合作编辑者' not in item.get_text():
                Traffic = item.get_text()
                House_dict['交通状况'] = Traffic
                #print(House_dict['交通状况'])
                House_list.append(Traffic)
                #print(Traffic)
        except AttributeError as AE:
            pass
    info_list = []
    for item in info:
        try:
            if '本段合作编辑者' not in item.get_text():
                other_info = item.get_text()
                info_list.append(other_info)
                # print("-----")
                #info_list.append(other_info)
        except AttributeError as AE:
            pass
    info_str = '|'.join(info_list)
    House_dict['周边信息'] = info_str
    House_list.append(info_list)
    for item in Supporting_facilities:
        try:
            if item.find('strong').get_text() == '停 车 位：':
                part1 = item.get_text().replace('停 车 位：', '')
                House_dict['停车位'] = part1
                House_list.append(part1)

        except AttributeError as AE:
            pass

    House_list.append(None)
    #时间
    Now_time = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
    House_dict['更新时间'] = Now_time
    House_list.append(Now_time)

    #print(House_dict)
    return House_dict

def get_ip():
    '''获取ip'''
    r = ['192.168.100.198:8888','Error004','Error888']
    return random.choice(r)




def dic2pd(House_All_list):
    '''数据转换为pandas'''
    print('数据转换为pandas中....')
    House_All_DF = pd.DataFrame(House_All_list)
    print(House_All_DF)

    return House_All_DF


# def list2pd(House_All_list):
#
#     columns_list = ['url','小区名称','别名','本月均价',
#                    '小区地址','行政区','片区','邮编','产权描述','物业类别',
#                    '建筑年代','开发商','建筑类型','建筑面积','占地面积','房屋总数',
#                    '楼栋总数','绿化率','容积率','物业费','停车位','交通状况','周边信息','地理位置','更新时间']
#     House_DF = pd.DataFrame(House_All_list,columns=columns_list)
#     print(House_DF.head())
#     return House_DF


def pd2csv(House_DF,file_name):
    '''存储csv文件'''
    print('存储csv文件中....')
    #file_name = 'test1.csv'
    file_name = file_name+'.csv'
    try:
        House_DF.to_csv(file_name,encoding="utf_8_sig")
    except UnicodeEncodeError:
        print("编码错误, 该数据无法写到文件中, 直接忽略该数据")

def run_log(start_time,end_time,ip_num,house_cout):
    '''日志生成'''
    print('日志生成中....')
    with open('run_log.txt', 'a', encoding='utf-8') as file:
        file.write(start_time+'\t'+end_time+'\t'+ip_num+'\t'+house_cout)
        file.write('\n')

def ip_proxy():
    '''检查代理ip是否正常'''
    print('检查代理ip是否正常中....')
    ip_num = 0
    ip = get_ip()
    Error004_status=False
    proxies_inter={}
    while 'Error' in ip:
        if 'Error004' in ip:
            print("Error004 异常,结束程序....")
            ip_num += 1
            Error004_status = True
            #print(ip_num)
            break
        else:
            print('进入十秒等待....')
            time.sleep(10)
            ip = get_ip()
            ip_num += 1
            continue
    else:
        ip_num += 1
        proxy_ip=('http://' + ip)
        proxies_inter = {'http': proxy_ip}

    #print(proxies_inter)
    #print(ip_num)
    return (proxies_inter,ip_num,Error004_status)



def main():
    '''入口函数'''

    file_name = input("请输入文件名：")
    ip_num = 0
    house_cout = 1
    start_time = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
    House_All_list = []
    ##########################################
    # proxies,ip_num,Error004_status= ip_proxy()
    # if Error004_status == True:
    #     print("关闭程序，日志提前结束")
    #     end_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
    #     print(house_cout)
    #     print(start_time)
    #     print(end_time)
    #     run_log(start_time, end_time, str(ip_num), str(house_cout))
    #     exit()
    ##########################################
    pag_num = get_num()
    reg_urls_list = getUrls(pag_num)
    for i,each in enumerate(reg_urls_list):
        print('===========================当前页数：%d===========================\n'%(i+1))
        for url in each:
            House_All = get_house_info(url)
            House_All_list.append(House_All)
            house_cout +=1
    House_DF = dic2pd(House_All_list)
    pd2csv(House_DF,file_name)
    end_time = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
    run_log(start_time,end_time,str(ip_num),str(house_cout))
    print('===========================完成爬取===========================')


if __name__ == '__main__':
    main()
    #get_house_info()
    #get_house_deep_url()

