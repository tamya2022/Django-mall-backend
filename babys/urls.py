from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(('index.urls', 'index'), namespace='index')),
    path('api/v1/commodity/', include(('commodity.urls', 'commodity'), namespace='commodity')),
    path('api/v1/shopper/', include(('shopper.urls', 'shopper'), namespace='shopper')),
    # 配置媒体资源的路由信息
    re_path('media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    # 定义静态资源的路由信息
    re_path('static/(?P<path>.*)', serve, {'document_root': settings.STATIC_ROOT}, name='static'),
]

# 设置404和500
from index import views

handler404 = views.page_not_found
handler500 = views.page_error
