from django.urls import path, re_path, include
# from django.conf.urls.static import static
from django.shortcuts import redirect

from hddata import views

# from django.conf import settings

from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    # 用户查询的路由

    # 获取Cookie的路由
    path('get-cookie/', views.get_cookie, name='get_cookie'),
    path('get-colleges/', views.get_colleges, name='get_colleges'),
    path('get-majors/<int:college_id>/', views.get_majors, name='get_majors'),
    path('user-search/', views.user_search, name='user_search'),
    path('', views.user_search)

    # 其他页面或者视图的路由
    # path('some-other-page/', views.some_other_view, name='some_other_page'),
]

app_name = 'hddata'
