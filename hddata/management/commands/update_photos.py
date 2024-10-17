import json
import time

import requests
from django.core.management.base import BaseCommand
from hddata.models import UserProfile


class Command(BaseCommand):
    help = 'Update user profile photos by fetching URLs from API based on student ID (open_id)'

    def handle(self, *args, **kwargs):
        count = 0
        cookies = {
            'route': 'c989f54c8f3eb77eb4c1b7c70b410e9f',
            'EMAP_LANG': 'zh',
            'THEME': 'indigo',
            '_WEU': '3*dxcebnJjYfQ_Y4zPQK7BGa5vcT8MVwqPRct_RTd9nG2_T6EutOfb8XcnZJNYGGYlSMaMlrC72T709MFpSRITdQgrDJV4EGnVZrOXqLyR1hM3Q1L3l1JHfN3rsIzs82TmppvnMsMbcm*Dk7KxhNvmyaiRtpruUJweJdS9YhoR1ipefnus1IIFhNmdN7Nt9QogRbmO9errJn4LxN6LrU*Utz2_Mu_VBVh4xI4DuaQ9nciNKQPowIbx89umtFZEiECzJspZGzcxdiATW7moKJOBatk1WvR8UVQw1X6RFXrib9TzdMtWJ67vov92S2syPLKG73AGnS4i_XvP149EixSz*9TyJNPLqkV79cqUg0mwLMGePzoc9eNTKlsyD4tIgbXj5AoYuQ05pGoCa3xrwIsS..',
            'iPlanetDirectoryPro': 'AQIC5wM2LY4Sfcw3Ux1dYx%2BvB8VqCejVwyDkijovZL4CkJw%3D%40AAJTSQACMDI%3D%23',
            'route': 'ea831a8589e8d9b075a0568e28623406',
            'MOD_AUTH_CAS': 'MOD_AUTH_ST-13506298-9NQMOqoN6kfB5UHqDxP21729134620024-2Mtq-cas',
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            # 'Accept-Encoding': 'gzip, deflate, br, zstd',
            'sec-ch-ua-platform': '"Windows"',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'sec-ch-ua-mobile': '?0',
            'Origin': 'https://xgxl.hlju.edu.cn',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://xgxl.hlju.edu.cn/xsfw/sys/jbxxapp/*default/index.do?THEME=indigo',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ja;q=0.5',
            # Requests sorts cookies= alphabetically
            # 'Cookie': 'route=c989f54c8f3eb77eb4c1b7c70b410e9f; EMAP_LANG=zh; THEME=indigo; _WEU=3*dxcebnJjYfQ_Y4zPQK7BGa5vcT8MVwqPRct_RTd9nG2_T6EutOfb8XcnZJNYGGYlSMaMlrC72T709MFpSRITdQgrDJV4EGnVZrOXqLyR1hM3Q1L3l1JHfN3rsIzs82TmppvnMsMbcm*Dk7KxhNvmyaiRtpruUJweJdS9YhoR1ipefnus1IIFhNmdN7Nt9QogRbmO9errJn4LxN6LrU*Utz2_Mu_VBVh4xI4DuaQ9nciNKQPowIbx89umtFZEiECzJspZGzcxdiATW7moKJOBatk1WvR8UVQw1X6RFXrib9TzdMtWJ67vov92S2syPLKG73AGnS4i_XvP149EixSz*9TyJNPLqkV79cqUg0mwLMGePzoc9eNTKlsyD4tIgbXj5AoYuQ05pGoCa3xrwIsS..; iPlanetDirectoryPro=AQIC5wM2LY4Sfcw3Ux1dYx%2BvB8VqCejVwyDkijovZL4CkJw%3D%40AAJTSQACMDI%3D%23; route=ea831a8589e8d9b075a0568e28623406; MOD_AUTH_CAS=MOD_AUTH_ST-13506298-9NQMOqoN6kfB5UHqDxP21729134620024-2Mtq-cas',
        }

        # api_url = 'https://example.com/api/photo'  # 替换为实际的API地址
        chunk_size = 100  # 每次处理 100 条记录，可以根据需要调整大小

        users = UserProfile.objects.filter(enrollment_photo='').iterator(chunk_size=chunk_size)
        for user in users:
            print(f"--------------------------------------------------------------------------------------------------------------------------{count}")
            count = count+1
            open_id = user.open_id
            print(open_id)
            try:
                # 通过学号请求API获取照片URL
                response = requests.post('https://xgxl.hlju.edu.cn/xsfw/sys/jbxxapp/modules/xszpck/xszpxqbd.do',
                                         cookies=cookies, headers=headers, data={
                        'XSBH': open_id,
                    },verify=False)
                # time.sleep(0.2)
                # response = requests.get(f'{api_url}/{open_id}')

                # 获取返回的照片数据
                # data = json.loads(response.text)['datas']['xszpxqbd']['rows'][0]
                data = json.loads(response.text).get('datas').get('xszpxqbd').get('rows')
                if(len(data)==0):
                    continue
                data = data[0]
                # 假设API返回的JSON包含照片URL字段
                user.enrollment_photo = data.get('RXZP_1') or "NULL"
                user.current_photo = data.get('ZXZP_1') or "NULL"
                user.graduation_photo = data.get('BYZP_1') or "NULL"
                user.id_card_photo = data.get('SFZZP_1') or "NULL"
                user.dormitory = data.get('SYDDM_DISPLAY') or "NULL"
                print(data.get('RXZP_1'))

                # 保存用户数据
                user.save()

                self.stdout.write(self.style.SUCCESS(f'Updated photos for user {open_id}'))

            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(f'Error updating user {open_id}: {e}'))
