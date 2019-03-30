import  requests
import  pandas as pd
import  os
path =os.getcwd()
print(path)
def getjson ():
        urls =[]
        data =[]
        for i in range(0, 17):
                page_num =str(i)
                # print(page_num)
                url ='http://api.map.baidu.com/place/v2/search?query=幼儿园&region=厦门&output=json&page_num='+str(page_num)+'&scope=2&ak=BihFFqmv7WtPSZh8ftXApC89jX9dYNsG'
                urls.append(url)      #通过控制page_num来获取到所有的url
        try:
                for i in range(0,17):
                        r =requests.get(urls[i])   #使用requests获取到网页内容
                        decodejson =r.json()    #转化为json格式
                        for item in decodejson['results']:
                                name = item['name']
                                address = item['address']
                                area = item['area']
                                if 'telephone' in item:
                                       telephone = item['telephone']
                                else:
                                        telephone = '暂无'
                                # uid = item['uid']
                                detail_url = item['detail_info']['detail_url']
                                if 'overall_rating' in item['detail_info']:
                                        overall_rating = item['detail_info']['overall_rating']
                                else:
                                        overall_rating = '暂无评分'
                                if 'comment_num' in item['detail_info']:
                                        cumment_num = item['detail_info']['comment_num']
                                else:
                                        cumment_num = '暂无评论'
                                data.append([name, address, telephone, area, detail_url, overall_rating, cumment_num])   #将每一个样本存入临时list data

        except  Exception as e:
                getjson()
                print('over-requests error:', e)
        df = pd.DataFrame(data, columns=['名称', '地址', '联系电话', '区域', '详情', '评分', '评论数'])     #存成dataframe格式
        df.to_csv('kindergarten_info.csv',encoding='utf_8_sig', index=False, mode='a+')   #写入csv文件
getjson()

