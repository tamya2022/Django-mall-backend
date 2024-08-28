import json
from django.db.models import F
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *


class commodityView(APIView):
    '''
    商品列表页
    '''
    authentication_classes = []
    permission_classes = []

    # GET请求
    def get(self, request):
        types = request.GET.get('types', '')
        search = request.GET.get('search', '')
        sort = request.GET.get('sort', 'sold')
        context = {'state': 'success', 'msg': '获取成功', 'data': {}}
        context['data']['types'] = []
        firsts = Types.objects.values_list('firsts', flat=True).distinct()
        for f in firsts:
            t = Types.objects.filter(firsts=f).values_list('seconds', flat=True).all()
            context['data']['types'].append(dict(name=f, value=t))
        cf = CommodityInfos.objects.all()
        if types:
            cf = cf.filter(types=types)
        if sort:
            cf = cf.order_by('-' + sort)
        if search:
            cf = cf.filter(name__contains=search)
        count = cf.count()
        # 分页查询，需要在settings.py设置REST_FRAMEWORK属性
        pg = PageNumberPagination()
        p = pg.paginate_queryset(queryset=cf, request=request)
        # 将分页后的数据传递MySerializer，生成JSON数据对象
        c = CommodityInfosSerializer(instance=p, many=True)
        # 获取前一页、后一页和总页的页数
        pageCount = pg.page.paginator.num_pages
        try:
            next = pg.page.next_page_number()
        except:
            next = pageCount
        try:
            previous = pg.page.previous_page_number()
        except:
            previous = 0
        d = dict(data=c.data, previous=previous,
                 next=next, count=count, pageCount=pageCount)
        context['data']['commodityInfos'] = d
        return Response(context)


class detailView(APIView):
    '''
    商品详情页
    '''
    authentication_classes = []
    permission_classes = []

    # GET请求
    def get(self, request, id):
        context = {'state': 'success', 'msg': '获取成功', 'data': {}}
        c = CommodityInfos.objects.filter(id=id).first()
        context['data']['commoditys'] = CommodityInfosSerializer(instance=c).data
        r = CommodityInfos.objects.exclude(id=id).order_by('-sold')[:5]
        context['data']['recommend'] = CommodityInfosSerializer(instance=r, many=True).data
        if id in request.session.get('likes', []):
            context['data']['likes'] = True
        else:
            context['data']['likes'] = False
        return Response(context)


class collectView(APIView):
    '''
    商品收藏
    '''
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        json_str = json.loads(request.body.decode())
        id = json_str.get('id', '')
        context = {'state': 'fail', 'msg': '收藏失败'}
        likes = request.session.get('likes', [])
        if id and not int(id) in likes:
            # 对商品的收藏数量执行自增加1
            CommodityInfos.objects.filter(id=id).update(likes=F('likes') + 1)
            # 根据Session信息判断用户是否已收藏
            request.session['likes'] = likes + [int(id)]
            context = {'state': 'success', 'msg': '收藏成功'}
        return Response(context)
