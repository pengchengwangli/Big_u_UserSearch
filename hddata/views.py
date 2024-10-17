from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.paginator import Paginator

from hddata.models import UserProfile, Major
from hddata.models import Organization


@csrf_exempt  # 仅在测试时使用，正式项目需要加上CSRF Token
def user_search(request):
    if request.method == 'POST':
        try:
            # 解析前端传来的 JSON 数据
            data = json.loads(request.body)
            search_query = data.get('search_query', '')
            college = data.get('college', '')
            major = data.get('major', '')
            grade = data.get('grade', '')
            page_number = data.get('page', 1)  # 获取请求的页码，默认为 1
            page_size = data.get('page_size', 10)  # 每页显示的条数，默认为 10

            # 根据条件查询
            results = UserProfile.objects.all()

            if search_query:
                results = results.filter(open_id__icontains=search_query) | results.filter(
                    user_name__icontains=search_query) | results.filter(
                    dormitory__icontains=search_query)
            # if college:
            #     results = results.filter(org_id=college)
            if major:
                results = results.filter(major_id=major)
            if grade:
                results = results.filter(grade=grade)

            # 使用 Paginator 进行分页
            paginator = Paginator(results, page_size)
            page = paginator.get_page(page_number)

            # 返回结果
            response_data = []
            for result in page:
                major_name = Major.objects.get(major_id=result.major_id).major_name
                response_data.append({
                    'open_id': result.open_id,
                    'nickname': result.user_name,
                    'org_name': result.org_name,
                    'major_name': major_name,
                    'hometown': f'[{result.grade}]/{result.dormitory}',
                    'photo_url': 'https://xgxl.hlju.edu.cn/xsfw/sys/jbxxapp/modules/infoManage/showImage.do?imagePath=' + result.current_photo,
                })

            return JsonResponse({
                'results': response_data,
                'page': page.number,
                'total_pages': paginator.num_pages,
                'total_results': paginator.count
            }, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return render(request, 'search.html')


def get_cookie(request):
    # 获取用户的 Cookie 或执行其他逻辑
    # 然后可以跳转到其他页面或者处理完返回结果
    return redirect('https://authserver.hlju.edu.cn/authserver/login')  # 可以跳转到另一个页面


def get_colleges(request):
    if request.method == 'GET':
        colleges = Organization.objects.all()
        data = [{'id': college.org_id, 'name': college.org_name} for college in colleges]
        return JsonResponse({'colleges': data})


def get_majors(request, college_id):
    if request.method == 'GET':
        majors = Organization.objects.get(org_id=college_id)  # 根据学院筛选专业
        majors = majors.major_set.all()
        data = [{'id': major.major_id, 'name': major.major_name} for major in majors]
        return JsonResponse({'majors': data})
