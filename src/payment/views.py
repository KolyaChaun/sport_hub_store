from django.http import HttpResponseNotFound, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from config import settings
from config.settings import (
    LIQPAY_PRIVATE_KEY,
    LIQPAY_PUBLIC_KEY,
    RESULT_URL,
    SERVER_URL,
)
from delivery.models import PAYMENT_OK, Order
from payment.liqpay_client import LiqPay
from payment.serializers import PaymentSerializer
from products.models import IN_STOCK, SOLD, WarehouseItem


class PayCallbackView(CreateAPIView):
    @method_decorator(csrf_exempt, name="dispatch")
    def post(self, request, *args, **kwargs):
        liqpay = LiqPay(LIQPAY_PUBLIC_KEY, LIQPAY_PRIVATE_KEY)
        data = request.POST.get("data")
        signature = request.POST.get("signature")
        sign = liqpay.str_to_sign(LIQPAY_PRIVATE_KEY + data + LIQPAY_PRIVATE_KEY)
        if sign == signature:
            response = liqpay.decode_data_from_str(data)
            order_id = response.get("order_id")
            payment_status = response.get("status")

            if order_id:
                try:
                    order = Order.objects.get(pk=order_id)
                    if payment_status == "success":
                        order.status = PAYMENT_OK
                        order.save()
                    elif payment_status in ["failure", "reversed"]:
                        warehouse_items = WarehouseItem.objects.filter(
                            order=order, status=SOLD
                        )
                        for item in warehouse_items:
                            item.status = IN_STOCK
                            item.order = None
                            item.save()

                except Order.DoesNotExist:
                    return HttpResponseNotFound("Order not found")

            return JsonResponse(response)


class CreatePaymentFormView(CreateAPIView):
    serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):
        try:
            order_id = request.data.get("order_id")
            order = Order.objects.get(pk=order_id)

            warehouse_items = WarehouseItem.objects.filter(order=order, status=SOLD)

            if not warehouse_items.exists():
                return Response(
                    data=dict(msg="No items linked to this order."),
                    status=HTTP_404_NOT_FOUND,
                )

            total_amount = float(sum(item.product.price for item in warehouse_items))

        except Order.DoesNotExist:
            return Response(
                data=dict(msg="Order does not exist."),
                status=HTTP_404_NOT_FOUND,
            )

        liqpay = LiqPay(LIQPAY_PUBLIC_KEY, LIQPAY_PRIVATE_KEY)
        params = {
            "version": "3",
            "action": "pay",
            "amount": total_amount,
            "currency": "UAH",
            "description": f"Payment for Order #{order.id}",
            "sandbox": 1,
            "order_id": str(order.id),
            "public_key": LIQPAY_PUBLIC_KEY,
            "server_url": SERVER_URL,
            "result_url": RESULT_URL,
        }

        payment_form = liqpay.cnb_form(params)

        return Response(
            data=dict(
                payment_form=payment_form,
                order=order.id,
            ),
        )


class CheckPaymentStatusView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        try:
            order_id = request.data.get("order_id")
            if not order_id:
                return Response(
                    data=dict(msg="Missing order_id in request data"),
                    status=HTTP_400_BAD_REQUEST,
                )
            liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
            params = {
                "action": "status",
                "version": "3",
                "order_id": str(order_id),
            }
            response = liqpay.api("request", params)
            return Response(
                data=dict(response),
                status=HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                data=dict(
                    msg=str(e),
                    status=HTTP_500_INTERNAL_SERVER_ERROR,
                )
            )
