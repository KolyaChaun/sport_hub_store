from abc import ABC, abstractmethod

from rest_framework import generics
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from delivery.models import Order
from delivery.nova_post_api_client import NovaPostApiClient
from delivery.serializers import OrderSerializer
from order.models import Basket, BasketItem
from products.models import IN_STOCK, SOLD, WarehouseItem


class NovaPostView(APIView, ABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.page = 1
        self.limit = 25
        self.client = NovaPostApiClient()

    @abstractmethod
    def _get_data(self, **kwargs):
        pass

    def get(self, request, **kwargs):
        self.limit = request.query_params.get("limit", self.limit)
        self.page = request.query_params.get("page", self.page)
        return Response(data=self._get_data(**kwargs))


class SettlementsView(NovaPostView):
    def _get_data(self, settlement_name, **kwargs):
        return self.client.get_settlements(settlement_name, self.limit, self.page)


class WarehousesView(NovaPostView):
    def _get_data(self, ref_settlement, **kwargs):
        return self.client.get_warehouses(ref_settlement, self.limit, self.page)


class WarehouseTypeView(NovaPostView):
    def _get_data(self, **kwargs):
        return self.client.get_warehouse_types()


class AddressesView(NovaPostView):
    def _get_data(self, street_name, ref, **kwargs):
        return self.client.search_settlement_streets(
            street_name, ref, self.limit, self.page
        )


def update_status_warehouse_items(basket_id, order):
    basket_items = BasketItem.objects.filter(basket_id=basket_id)
    for item in basket_items:
        warehouse_item = WarehouseItem.objects.filter(
            product=item.product, color=item.color, size=item.size, status=IN_STOCK
        ).first()

        if warehouse_item:
            warehouse_item.status = SOLD
            warehouse_item.order = order
            warehouse_item.save()
    basket = Basket.objects.get(id=basket_id)
    basket.delete()


class CreateOrderView(CreateAPIView):
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        try:
            basket_id = request.data.get("basket_id")
            basket = Basket.objects.get(pk=basket_id)
            basket_items = BasketItem.objects.filter(basket=basket)
            if request.user.id != basket.user_id:
                return Response(
                    data=dict(
                        msg="You cannot place an order from someone else's basket"
                    ),
                    status=HTTP_403_FORBIDDEN,
                )
            if not basket_items:
                return Response(
                    data=dict(
                        msg="Your basket is empty. Please add items to cart before checkout."
                    ),
                    status=HTTP_404_NOT_FOUND,
                )
        except Basket.DoesNotExist:
            return Response(
                data=dict(msg="Basket does not exist!"),
                status=HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        update_status_warehouse_items(
            basket_id=serializer.initial_data.get("basket_id"), order=order
        )

        return Response(
            data=dict(
                msg="Your order has been created successfully! Go to checkout!",
                order=order.id,
            )
        )


class OrderHistoryView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        user = request.user

        orders = Order.objects.filter(user=user)
        order_data = []

        for order in orders:
            items = order.wh_items.all()
            order_info = {
                "id": order.id,
                "date": order.created_at,
                "delivery_status": order.status,
                "payment_method": order.payment_method,
                "delivery_method": order.delivery_method,
                "delivery_branch": order.branch,
                "delivery_city": order.city,
                "address": f" {order.street}, {order.apartment}",
                "items": [
                    {
                        "product": item.product.title,
                        "size_id": item.product.size.all().first().value,
                        "color_id": item.product.color.all().first().title,
                        "price": item.product.price,
                    }
                    for item in items
                ],
            }
            order_data.append(order_info)

        return Response(
            data=dict(
                msg="Your order history has been shown successfully!",
                order_data=order_data,
            ),
            status=HTTP_200_OK,
        )
