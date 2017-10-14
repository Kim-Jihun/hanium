import requests
import json
from shop.models import Post, Tag, Rating
import os
from urllib.request import urlretrieve
from django.core.files import File
from bs4 import BeautifulSoup

def crawling_data(q):
    res_list =[]
    count = 1
    url = "https://m.store.naver.com/sogum/api/businesses"


    for k in range(0, 5):
        params = {
            'query': q,
            'start' : count,
            'display': 20,
        }

        html = requests.get(url, params = params).text
        json_html = json.loads(html)
        items = json_html['items']

        if items not in res_list:
            res_list.extend(items)
            count = count + 20

        else:
            print("이미 있는 데이")
            break

        res_info = []
        res_basic_dic = {}

        for res_id in res_list:
            temp_list = []
            lnglat_set = (res_id['x'], res_id['y'])
            temp_list.append(lnglat_set)
            temp_list.append(res_id['category'])
            res_basic_dic[res_id['id']] = temp_list


        detail_contents_list  = []
        for res in res_basic_dic.keys():
            detail_url = 'https://m.store.naver.com/restaurants/detail'
            detail_params= {
                'id': res,
            }

            detail_html = requests.get(detail_url, params = detail_params).text
            bs_obj = BeautifulSoup(detail_html, 'html.parser')
            content_dict = {}
            blog_dict = {}
            try:
                content_dict['lnglat'] = str(res_basic_dic[res][0]).replace('(','').replace(')','').replace("'", '')
                content_dict['tag'] = str(res_basic_dic[res][1]).replace('[','').replace(']','').strip()
                content_dict['title'] = bs_obj.select('.biz_name')[0].text
                content_dict['address'] = bs_obj.select('.addr')[0].text
                content_dict['phone_number'] = bs_obj.select('.btn_tel')[0]['href']
                content_dict['avail_time'] = bs_obj.select('.txt > span')[4].text

                    #추가한부분

                content_dict['title1'] =bs_obj.select('#content > div.sc_box.review > ul > li > a > div.info_area > div.tit.ellp2')[0].text
                content_dict['content1'] =bs_obj.select('#content > div.sc_box.review > ul > li > a > div.info_area > div.txt')[0].text
                content_dict['link1'] =bs_obj.select('#content > div.sc_box.review > ul > li > a')[0].get('href')
                content_dict['title2'] =bs_obj.select('#content > div.sc_box.review > ul > li > a > div.info_area > div.tit.ellp2')[1].text
                content_dict['content2'] =bs_obj.select('#content > div.sc_box.review > ul > li > a > div.info_area > div.txt')[1].text
                content_dict['link2'] =bs_obj.select('#content > div.sc_box.review > ul > li > a')[1].get('href')
                content_dict['title3'] =bs_obj.select('#content > div.sc_box.review > ul > li > a > div.info_area > div.tit.ellp2')[2].text
                content_dict['content3'] =bs_obj.select('#content > div.sc_box.review > ul > li > a > div.info_area > div.txt')[2].text
                content_dict['link3'] =bs_obj.select('#content > div.sc_box.review > ul > li > a')[2].get('href')




                menu_list = bs_obj.select('.menu  .menu_area span')
                menu_dict = {}
                for i in menu_list:
                    if i.text == '대표':
                        continue
                    menu_dict[i.text] = None

                price_list = bs_obj.select('.menu  li em')
                price_list_numbers = []

                p = 0
                for key in menu_dict.keys():
                    price = price_list[p].text
                    menu_dict[key] = price
                    price_list_numbers.append(price)
                    p = p+1

                import string
                import math

                # Thanks to Martijn Pieters for this improved version

                # This uses the 3-argument version of str.maketrans
                # with arguments (x, y, z) where 'x' and 'y'
                # must be equal-length strings and characters in 'x'
                # are replaced by characters in 'y'. 'z'
                # is a string (string.punctuation here)
                # where each character in the string is mapped
                # to None
                translator = str.maketrans('', '', string.punctuation)

                # This is an alternative that creates a dictionary mapping
                # of every character from string.punctuation to None (this will
                # also work)
                #translator = str.maketrans(dict.fromkeys(string.punctuation))

                s = 'string with "punctuation" inside of it! Does this work? I hope so.'

                # pass the translator to the string's
                #print(s.translate(translator))

                #print(price_list_numbers)
                sum = 0
                for r in price_list_numbers:
                    temp = r[0:len(r)-1]
                    sum += math.floor(int(temp.translate(translator)))

                avg_price = math.floor(sum/len(price_list_numbers))
                #print(avg_price)

                menu_str = str(menu_dict)
                menu_str_strip = menu_str[1:len(menu_str)-1]
                content_dict['menu'] = menu_str_strip
                content_dict['avg_price'] = avg_price

            except:
                print("one of lgnlat, tag, title, address, phone_number, avail_time, menu, avg_price error!")

            try:
                contents_str= bs_obj.select('.info .ellipsis_area')[0].text
                contents_str_strip = contents_str[0:len(contents_str)-2]
                content_dict['content'] = contents_str_strip.strip()
            except:
                print('Error! during contents!')

            try:
                img_src = str(bs_obj.select('div._flick-ct')[0])
                src_start_idx = img_src.find('https://')
                src_end_idx = img_src.find('&')
                img_src = img_src[src_start_idx:src_end_idx]
                #print(img_src)
                if img_src== "":
                    continue
                else:
                    content_dict['img_src'] = img_src
            except:
                print('Error! during image url..!')


            res_info.append(content_dict)



    return res_info



def post_rest(keyword):
    final_list = crawling_data(keyword)
    for rest in final_list:
        try:
            post_instance = Post(
                title = rest.get('title'),
                menu=rest.get('menu'),
                content=rest.get('content'),
                avail_time=rest.get('avail_time'),
                lnglat= rest.get('lnglat'),

                phone_number=rest.get('phone_number'),

                blog_title1 = rest.get('title1'),
                blog_content1 = rest.get('content1'),
                link1 = rest.get('link1'),

                blog_title2 = rest.get('title2'),
                blog_content2 = rest.get('content2'),
                link2 = rest.get('link2'),

                blog_title3 = rest.get('title3'),
                blog_content3 = rest.get('content3'),
                link3 = rest.get('link3'),



            )
            post_instance.save()

            tag_instance = Tag(
                title = rest.get('title'),
                menu=rest.get('menu'),
                location= keyword,
                avg_price=rest.get('avg_price'),
            )
            tag_instance.save()


            image = urlretrieve(rest.get('img_src'))

            fname = os.path.basename(rest.get('img_src'))

            with open(image[0], 'rb') as fp:
                post_instance.image.save(fname, File(fp))
                post_instance.save()

            post_instance.tag_set.add(tag_instance)
            post_instance.save()

            post_instance.tag_set.add(tag_instance)
            post_instance.save()

        except:
            print("DB storing error!")



