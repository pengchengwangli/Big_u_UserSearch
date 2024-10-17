import json
from django.core.management.base import BaseCommand
from hddata.models import Organization, Major


class Command(BaseCommand):
    help = 'Import colleges and their corresponding majors from a JSON file'

    def handle(self, *args, **kwargs):
        import requests

        cookies = {
            'HWWAFSESID': '2791b73a3d9e83ba93',
            'HWWAFSESTIME': '1729073932628',
            'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22fb7b1e44-c213-4341-aa43-3132db9ec233%22%2C%22first_id%22%3A%221929066f98f1ca0-03df696b86eb002-4c657b58-3686400-1929066f9902608%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkyOTA2NmY5OGYxY2EwLTAzZGY2OTZiODZlYjAwMi00YzY1N2I1OC0zNjg2NDAwLTE5MjkwNjZmOTkwMjYwOCIsIiRpZGVudGl0eV9sb2dpbl9pZCI6ImZiN2IxZTQ0LWMyMTMtNDM0MS1hYTQzLTMxMzJkYjllYzIzMyJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22fb7b1e44-c213-4341-aa43-3132db9ec233%22%7D%7D',
            'MOD_AUTH_CAS': 'ST-iap:1018615878631905:ST:93cf67ff-4f91-4b17-a66c-43854f4bbf3c:20241016205227',
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
            # 'Cookie': 'HWWAFSESID=2791b73a3d9e83ba93; HWWAFSESTIME=1729073932628; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22fb7b1e44-c213-4341-aa43-3132db9ec233%22%2C%22first_id%22%3A%221929066f98f1ca0-03df696b86eb002-4c657b58-3686400-1929066f9902608%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkyOTA2NmY5OGYxY2EwLTAzZGY2OTZiODZlYjAwMi00YzY1N2I1OC0zNjg2NDAwLTE5MjkwNjZmOTkwMjYwOCIsIiRpZGVudGl0eV9sb2dpbl9pZCI6ImZiN2IxZTQ0LWMyMTMtNDM0MS1hYTQzLTMxMzJkYjllYzIzMyJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22fb7b1e44-c213-4341-aa43-3132db9ec233%22%7D%7D; MOD_AUTH_CAS=ST-iap:1018615878631905:ST:93cf67ff-4f91-4b17-a66c-43854f4bbf3c:20241016205227',
        }

        response = requests.get(
            'https://hlju.campusphere.net/wec-campushoy-pc-contacts-apps/v9/user/address-book/student/users-and-org?type=student&grades&orgId&orgKind=1&pageNum=1&pageSize=20&category',
            cookies=cookies, headers=headers, verify=False)
        try:
            data = json.loads(response.text)['data']['orgInfo']['orgs']
            for entry in data:
                org_name = entry.get('name')
                org_id = entry.get('id')
                print(org_name, org_id)
                response = requests.get(
                    f'https://hlju.campusphere.net/wec-campushoy-pc-contacts-apps/v9/user/address-book/student/users-and-org?type=student&grades&orgId={org_id}&orgKind=2&pageNum=1&pageSize=100&category',
                    cookies=cookies, headers=headers, verify=False)
                majors = json.loads(response.text)['data']['orgInfo']['orgs']

                # 创建或获取学院
                organization, created = Organization.objects.get_or_create(
                    org_name=org_name,
                    org_id=org_id
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created organization: {org_name}'))
                # 批量导入专业
                for major in majors:
                    major_name = major.get('name')
                    major_id = major.get('id')
                    print(major_name, major_id)
                    # 创建或获取专业
                    major_obj, major_created = Major.objects.get_or_create(
                        major_name=major_name,
                        major_id=major_id,
                        organization=organization
                    )
                    if major_created:
                        self.stdout.write(
                            self.style.SUCCESS(f'Created major: {major_name} for organization {org_name}'))

            self.stdout.write(self.style.SUCCESS('Data import completed successfully.'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('File not found. Please provide a valid JSON file path.'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Invalid JSON format. Please check the input file.'))
