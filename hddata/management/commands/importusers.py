import json
import time

from django.core.management.base import BaseCommand
from hddata.models import UserProfile
import requests


class Command(BaseCommand):
    help = 'Import users from a JSON file'

    def handle(self, *args, **kwargs):
        cookies = {
            'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22fb7b1e44-c213-4341-aa43-3132db9ec233%22%2C%22first_id%22%3A%221929066f98f1ca0-03df696b86eb002-4c657b58-3686400-1929066f9902608%22%2C%22props%22%3A%7B%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkyOTA2NmY5OGYxY2EwLTAzZGY2OTZiODZlYjAwMi00YzY1N2I1OC0zNjg2NDAwLTE5MjkwNjZmOTkwMjYwOCIsIiRpZGVudGl0eV9sb2dpbl9pZCI6ImZiN2IxZTQ0LWMyMTMtNDM0MS1hYTQzLTMxMzJkYjllYzIzMyJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22fb7b1e44-c213-4341-aa43-3132db9ec233%22%7D%7D',
            'HWWAFSESID': '2791b73a3d9e83ba93',
            'HWWAFSESTIME': '1729073932628',
            'MOD_AUTH_CAS': 'ST-iap:1018615878631905:ST:96add431-3aec-4fb8-ae5b-c9b8a38dcac3:20241016181853',
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            # 'Accept-Encoding': 'gzip, deflate, br, zstd',
            'sec-ch-ua': '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ja;q=0.5',
            # Requests sorts cookies= alphabetically
            # 'Cookie': 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22fb7b1e44-c213-4341-aa43-3132db9ec233%22%2C%22first_id%22%3A%221929066f98f1ca0-03df696b86eb002-4c657b58-3686400-1929066f9902608%22%2C%22props%22%3A%7B%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkyOTA2NmY5OGYxY2EwLTAzZGY2OTZiODZlYjAwMi00YzY1N2I1OC0zNjg2NDAwLTE5MjkwNjZmOTkwMjYwOCIsIiRpZGVudGl0eV9sb2dpbl9pZCI6ImZiN2IxZTQ0LWMyMTMtNDM0MS1hYTQzLTMxMzJkYjllYzIzMyJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22fb7b1e44-c213-4341-aa43-3132db9ec233%22%7D%7D; HWWAFSESID=2791b73a3d9e83ba93; HWWAFSESTIME=1729073932628; MOD_AUTH_CAS=ST-iap:1018615878631905:ST:96add431-3aec-4fb8-ae5b-c9b8a38dcac3:20241016181853',
        }


        for i in range(133,1000):
            time.sleep(1)
            print(f"-----------------------------------------------------------------------------------------------------------------------------------{i}")
            url = f"https://hlju.campusphere.net/wec-campushoy-pc-contacts-apps/v9/user/address-book/student/users-and-org?type=student&pageNum={i}&pageSize=200"
            # response = requests.get(url)
            response = requests.get(
                url, headers=headers, cookies=cookies, verify=False)
            jsontext = response.text
            print(jsontext)
            data = json.loads(jsontext)['data']['userInfo']['result']
            for row in data:
                # 创建或更新 UserProfile 对象
                user_profile, created = UserProfile.objects.update_or_create(
                    open_id=row['openId'],
                    defaults={
                        'user_name': row['userName'],
                        'nickname': row['nickname'] or row['userName'],
                        'avatar': row['avatar'] or "NULL",
                        # 'enrollment_photo': "",
                        # 'current_photo': "",
                        # 'graduation_photo': "",
                        # 'id_card_photo': "",
                        'grade': row['grade'] or "NULL",
                        'org_name': row['orgName'] or "NULL",
                        'org_id': row['orgId'] or "NULL",
                        'class_id': row['classId'] or "NULL",
                        'major_id': row['majorId'],
                        'uid': row['id'] or "NULL",
                        'dormitory': "",
                        'phone_number': row['mobilePhone'] or "NULL",
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created user: {row["userName"]}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Updated user: {row["userName"]}'))
