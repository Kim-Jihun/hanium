import requests
import json
from shop.models import Post, Tag, Rating
import os
from urllib.request import urlretrieve
from django.core.files import File
from bs4 import BeautifulSoup


def search(q):
    res_list =[]
    i = 1
    url = "https://m.store.naver.com/sogum/api/businesses"


    for k in range(0,3):
        params = {
            'query': q,
            'start' : i,
            'display': 20,
        }

        html = requests.get(url, params = params).text
        json_html = json.loads(html)
        items = json_html['items']

        if items not in res_list:
            res_list.extend(items)
            i = i + 20

        else:
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
            #print(res_basic_dic)
            content_dict['lnglat'] = str(res_basic_dic[res][0]).replace('(','').replace(')','').replace("'", '')
            content_dict['tag'] = str(res_basic_dic[res][1]).replace('[','').replace(']','').strip()
            content_dict['title'] = bs_obj.select('.biz_name')[0].text
            content_dict['address'] = bs_obj.select('.addr')[0].text
            content_dict['phone_number'] = bs_obj.select('.btn_tel')[0]['href']
            content_dict['avail_time'] = bs_obj.select('.txt > span')[4].text



            menu_list  = bs_obj.select('.menu  .menu_area span')
            menu_dict = {}
            for i in menu_list:
                if i.text == '대표':
                    continue

                #print(i.text)
                menu_dict[i.text] = None

            #print(menu_dict)
            price_list = bs_obj.select('.menu  li em')

            i = 0
            for key in menu_dict.keys():
                menu_dict[key] = price_list[i].text
                i = i+1
            menu_str = str(menu_dict)
            menu_str_strip = menu_str[1:len(menu_str)-1]
            content_dict['menu'] = menu_str_strip
            #print(menu_str_strip)
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
                content_dict['img_src'] = img_src
            except:
                print('Error! during image url..!')


            res_info.append(content_dict)
            #break
    return res_info


def post_rest(keyword):
    final_list = search(keyword)
    for rest in final_list:
        post_instance = Post(
            title = rest.get('title'),
            menu=rest.get('menu'),
            content=rest.get('content'),
            avail_time=rest.get('avail_time'),
            lnglat= rest.get('lnglat'),

            phone_number=rest.get('phone_number'),
        )
        post_instance.save()


        image = urlretrieve(rest.get('img_src'))
        #post_instance = Animal.objects.create(name='Dog')
        fname = os.path.basename(rest.get('img_src'))

        with open(image[0], 'rb') as fp:
            post_instance.image.save(fname, File(fp))
            post_instance.save()

        tag_instance = Tag(name=rest.get('tag'))
        tag_instance.save()

        post_instance.tag_set.add(tag_instance)
        post_instance.save()

        tag_instance = Tag(name=keyword)
        tag_instance.save()

        post_instance.tag_set.add(tag_instance)
        post_instance.save()



