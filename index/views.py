from rest_framework.views import APIView
from rest_framework.response import Response
from commodity.serializers import *


class indexView(APIView):
    '''
    首页
    '''

    # GET请求
    def get(self, request):
        context = {'state': 'success', 'msg': '获取成功', 'data': {}}
        context['data']['commodityInfos'] = []
        c = CommodityInfos.objects.order_by('-sold')[:8].all()
        context['data']['commodityInfos'].append(CommodityInfosSerializer(instance=c[0:4], many=True).data)
        context['data']['commodityInfos'].append(CommodityInfosSerializer(instance=c[4:8], many=True).data)
        types = Types.objects.all()
        # 儿童服饰
        cl = [x.seconds for x in types if x.firsts == '儿童服饰']
        clothes = CommodityInfos.objects.filter(types__in=cl).order_by('-sold')[:5].all()
        context['data']['clothes'] = CommodityInfosSerializer(instance=clothes, many=True).data
        # 奶粉辅食
        fl = [x.seconds for x in types if x.firsts == '奶粉辅食']
        food = CommodityInfos.objects.filter(types__in=fl).order_by('-sold')[:5].all()
        context['data']['food'] = CommodityInfosSerializer(instance=food, many=True).data
        # 儿童用品
        gl = [x.seconds for x in types if x.firsts == '儿童用品']
        goods = CommodityInfos.objects.filter(types__in=gl).order_by('-sold')[:5].all()
        context['data']['goods'] = CommodityInfosSerializer(instance=goods, many=True).data
        return Response(context)


def page_not_found(request, exception):
    data = {'state': 'fail', 'msg': '页面丢失了'}
    return Response(data, status=404)


def page_error(request):
    data = {'state': 'fail', 'msg': '服务器异常'}
    return Response(data, status=500)
