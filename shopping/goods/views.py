#encoding:utf-8
from django.shortcuts import render
from django.views.generic import ListView, DetailView, View, TemplateView
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse

from django.db.models import Q
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from django.contrib import messages

from account.mixins import LoginRequiredMixin

from .models import Goods, ShoppingCar, Order, GoodsBuied
from account.models import UserAddress


class GoodsListView(ListView):
    template_name = 'index.html'
    model=Goods
    ordering=['-create_time']   #显示排序
    paginate_by = 3    #每页几个

    def get_queryset(self):
        q = str(self.request.GET.get('q','')).strip()
        queryset=super().get_queryset()
        queryset=queryset.filter(status=1)
        if q:
            queryset=queryset.filter(Q(name__icontains=q) | Q(desc__icontains=q) | Q(category__name__icontains=q))
            #  按照商品名，描述，商品分类进行查找，引入了Q函数(或的方法)
        return queryset

class GoodsDetailView(DetailView):
    template_name="goods/goods_detail.html"
    model=Goods

    def get_queryset(self):     #解决商品删除后删除，可以手动添加url访问。
        queryset=super().get_queryset()
        queryset =queryset.filter(status=1)
        return queryset

class ShoppingCarCreateView(LoginRequiredMixin,View):
    def post(self, request, *args, **kwargs):
        goods_id = request.POST.get("goods_id", 0)
        num = request.POST.get("num", 1)
        goods = Goods.objects.get(pk=goods_id)

        car = None
        try:
            car = ShoppingCar.objects.get(user=request.user, goods=goods)
            car.num += int(num)
        except ObjectDoesNotExist as e:
            car = ShoppingCar(goods=goods, num=num, user=request.user)

        car.save()

        return JsonResponse({'status' : 200, "result" : None, "errors" : []})

class ShoppingCarNumView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        cars = ShoppingCar.objects.filter(user=request.user)
        total = 0
        for car in cars:
            total += car.num

        return JsonResponse({'status' : 200, 'result' : total, "errors" : []})

class ShoppingCarView(LoginRequiredMixin,TemplateView):
    template_name = "goods/shopping_car.html"
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['shopping_cars']=ShoppingCar.objects.filter(user=self.request.user)
        context['user_addresses']=UserAddress.objects.filter(user=self.request.user,status=1)
        print(context['user_addresses'])
        return context

class ShoppingCarDeleteView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        shopping_car_id = request.POST.get('shopping_car', 0)
        try:
            shopping_car = ShoppingCar.objects.get(pk=shopping_car_id, user=request.user)
            shopping_car.delete()
        except ObjectDoesNotExist as e:
            pass
        return JsonResponse({'status' : 200, 'result' : None, 'errors' : None})


class OrderCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user_address = request.POST.get('user_address', 0)
        shopping_car = request.POST.getlist('shopping_car')

        try:
            print(2222222222222222222222222)
            user_address_obj = UserAddress.objects.get(pk=user_address, user=request.user, status=1)
            print()
            shopping_car_objlist = ShoppingCar.objects.filter(pk__in=shopping_car, user=request.user)
            if not shopping_car_objlist:
                messages.add_message(request, messages.INFO, '请将商品加入到购物车')
                return HttpResponseRedirect(reverse('index'))
            price = 0
            for car in shopping_car_objlist:
                price += car.num * car.goods.price

            with transaction.atomic():  #with以下为事务
                order = Order(user=request.user, user_address=user_address_obj, price=price)
                order.save()

                for car in shopping_car_objlist:
                    goods = GoodsBuied(order=order, price=car.goods.price, num=car.num, goods=car.goods)
                    goods.save()
                    car.delete()

                # 付款方式
                #
        except ObjectDoesNotExist as e:
            print(e)
            pass
        except BaseException as e:
            print(e)

        return HttpResponseRedirect(reverse('goods:orders'))



class OrderListView(LoginRequiredMixin, ListView):
    template_name = 'goods/order.html'
    model = Order
    ordering = ['-create_time']
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class OrderOperateView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        order_id = self.request.POST.get('order_id', 0)
        operate = self.request.POST.get('operate', '')

        try:
            print(11111111111111111111111111111111111111)
            order = Order.objects.get(pk=order_id, user=request.user)
            if operate == 'cancel' and order.status == 0:
                order.status = 3
                order.save()
            elif operate == 'makesure' and order.status == 1:
                order.status = 2
                order.save()
        except ObjectDoesNotExist as e:
            print(e)

        return JsonResponse({'status' : 200, 'result' : None, 'errors' : None})

