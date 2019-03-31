import  json
import  requests
import time
import  pandas as pd
from lxml import etree


class BaiduPOI(object):
    def __init__(self, itmey, loc):
        self.itemy =itmey
        self.loc =loc

    def urls(self):
        api_key ='ZOyGTIqLP3Q0aWAGRQCKUBhx72jTEUbE'
        urls =[]
        for page_num in range(0, 40):
            url ='http://api.map.baidu.com/place/v2/search?query='+self.itemy+'&bounds='+self.loc+\
                 '&output=json&page_num='+str(page_num)+'&scope=2&ak='+str(api_key)
            urls.append(url)
        return urls

    def requests_get(self):
        data =[]
        try:
                for url in self.urls():
                        r =requests.get(url)   #使用requests获取到网页内容
                        decodejson =r.json()    #转化为json格式
                        print(decodejson)
                        if decodejson['total'] != 0 :
                            for item in decodejson['results']:
                                    print(item)
                                    name = item['name']
                                    address = item['address']
                                    address.replace('福建省厦门市' ,' ')
                                    province = item['province']
                                    city = item['city']
                                    area = item['area']
                                    lat =item['location']['lat']
                                    lng =item['location']['lng']
                                    if 'telephone' in item:
                                           telephone = item['telephone']
                                    else:
                                            telephone = '暂无'
                                    detail_url = item['detail_info']['detail_url']
                                    detail =requests.get(detail_url)
                                    html =etree.HTML(detail.text)     #使用xpath 来获取图片url
                                    picture=html.xpath("/html/body/div[@id='main']/div[@id='content']/div[@id='MainLeft']/div[@id='basicInfo']/div[@class='bd clearfix']/div[@class='meta meta-img']/a/img/@src")
                                    if 'overall_rating' in item['detail_info']:
                                            overall_rating = item['detail_info']['overall_rating']
                                    else:
                                            overall_rating = '暂无评分'
                                    if 'comment_num' in item['detail_info']:
                                            cumment_num = item['detail_info']['comment_num']
                                    else:
                                            cumment_num = '暂无评论'
                                    data.append([name, telephone,address, province, city, area, lat, lng, picture, detail_url, overall_rating, cumment_num])   #将每一个样本存入临时list data
                                # print(data)
        except  Exception as e:
                print('over-requests error:', e)
        df = pd.DataFrame(data, columns=['名称', '联系电话', '地址', '省份', '城市', '区域', '纬度', '经度', '图片', '详情', '评分', '评论数'])  # 存成dataframe格式
        print(df)
        df.to_csv('kindergarten_info.csv', encoding='utf_8_sig', index=False, mode='a+')  # 写入csv文件


class LocaDiv(object):
    def __init__(self,loc_all):
        self.loc_all =loc_all

    def lat_all(self):     #经度获取   对经度进行划分
        lat_sw = float(self.loc_all.split(',')[0])    #获取左下标经度
        lat_ne = float(self.loc_all.split(',')[2])   #获取右上标经度
        lat_list =[]
        for i in range(0 ,int((lat_ne - lat_sw + 0.000001 ) / 0.05)):
            # print(i)
            lat_list.append(lat_sw + 0.05 * i)   #每次递增0.05
        lat_list.append(lat_ne)
        # print(lat_list)
        return lat_list

    def lng_all(self):    #获取纬度   对纬度进行划分
        lng_sw = float(self.loc_all.split(',')[1])
        lng_ne = float(self.loc_all.split(',')[3])
        lng_list =[]
        for i in range(0, int((lng_ne - lng_sw + 0.000001) / 0.05)):
            lng_list.append(lng_sw + 0.05 * i)    #每次递增0.05
        lng_list.append(lng_ne)
        # print(lng_list)
        return lng_list

    def ls_com(self):
        l1 = self.lat_all()
        l2 = self.lng_all()
        ab_list = []
        for i  in range(0, len(l1)):
            a = str(l1[i])
            # print(a)
            for j in range(0 ,len(l2)):
                b = str(l2[j])
                # print(b)
                ab = a + ',' + b
                ab_list.append(ab)
        # print(ab_list)
        return ab_list

    def ls_row(self):
        l1 = self.lat_all()
        l2 = self.lng_all()
        ls_com_v = self.ls_com()
        ls = []
        for n in range(0, len(l1)-1):
                for i in  range(0+len(l1) * n,len(l2) + (len(l2))*n -1):
                    a = ls_com_v[i]
                    # print(a)
                    b = ls_com_v[i + len(l2) + 1]
                    ab = a + ',' + b
                    ls.append(ab)
        return ls

if __name__ =='__main__':
    loc =LocaDiv('24.427050, 117.956295,24.906820, 118.360321')
    loc_to_use =loc.ls_row()
    data = []
    # df =pd.DataFrame( data,columns=['名称', '联系电话', '地址', '省份', '城市', '区域', '纬度', '经度', '图片', '详情', '评论数'])
    for loc_to_use in loc_to_use:
        print(loc_to_use)
        par = BaiduPOI('幼儿园', loc_to_use)
        data.append(par.requests_get())
    print(data)
    # for i in len(data):
    #     df = pd.DataFrame(data[i], columns=['名称', '联系电话', '地址', '省份', '城市', '区域', '纬度', '经度', '图片', '详情', '评分', '评论数'], index=False)  # 存成dataframe格式
    # print(df)
    # df.to_csv('kindergarten_info.csv', encoding='utf_8_sig', index=False, mode='a+')  # 写入csv文件