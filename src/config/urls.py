from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from delivery.views import (
    AddressesView,
    CreateOrderView,
    OrderHistoryView,
    SettlementsView,
    WarehousesView,
    WarehouseTypeView,
)
from order.views import CreateBasket, MergeBasket, RetrieveUpdateDestroyBasketAPIView
from payment.views import CheckPaymentStatusView, PayCallbackView
from products.views import (
    AvailableProductStockAPIView,
    ProductFilterView,
    ProductListAPIView,
    ProductRetrieveAPIView,
    ProductSearchView,
    ProductSortingView,
)
from users.views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    LogoutView,
    ResendActivationEmailView,
    UserActivationView,
    UserCreateAPIView,
    UserInfoView,
    UserRetrieveUpdateDestroyView,
)


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        return schema


schema_view = get_schema_view(
    openapi.Info(
        title="Sport Hub | SportHub API",
        default_version="v1",
        contact=openapi.Contact(
            email="vitasyushchyk@gmail.com, chaiunmykola@gmail.com"
        ),
    ),
    public=True,
    generator_class=BothHttpAndHttpsSchemaGenerator,  # API schema that supports both HTTP and HTTPS protocols.
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("docs/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # ADMIN
    path("admin/", admin.site.urls),
    # TOKEN
    path(
        "auth/token/refresh/",
        CustomTokenRefreshView.as_view(),
        name="token-refresh",
    ),
    # USER
    path(
        "user/registration/",
        UserCreateAPIView.as_view(),
        name="user-registration",
    ),
    path(
        "user/confirm_email/<str:activation_key>/",
        UserActivationView.as_view(),
        name="confirm-email",
    ),
    path(
        "user/resend/activation/",
        ResendActivationEmailView.as_view(),
        name="resend-activation",
    ),
    path(
        "user/login/",
        CustomTokenObtainPairView.as_view(),
        name="user-login",
    ),
    path(
        "user/logout/",
        LogoutView.as_view(),
        name="user-logout",
    ),
    path(
        "user/view/",
        UserInfoView.as_view(),
        name="user-view",
    ),
    path(
        "user/profile/<int:pk>/",
        UserRetrieveUpdateDestroyView.as_view(),
        name="user-retrieve-update-destroy",
    ),
    path(
        "user/password_reset/",
        include(
            "django_rest_passwordreset.urls",
            namespace="password-reset",
        ),
    ),
    # PRODUCTS
    path(
        "products/",
        ProductListAPIView.as_view(),
        name="product-list",
    ),
    path(
        "products/<int:id>/",
        ProductRetrieveAPIView.as_view(),
        name="product-retrieve",
    ),
    path(
        "products/<int:product_id>/<int:color_id>/<int:size_id>/available/",
        AvailableProductStockAPIView.as_view(),
        name="product-available-stock",
    ),
    path(
        "products/search/",
        ProductSearchView.as_view(),
        name="product-search",
    ),
    path(
        "products/sort/",
        ProductSortingView.as_view(),
        name="product-sorting",
    ),
    path(
        "products/filter/",
        ProductFilterView.as_view(),
        name="filter-products",
    ),
    # NOVA POST
    path(
        "nova-post/settlements/<str:settlement_name>/",
        SettlementsView.as_view(),
        name="nova-post-settlements",
    ),
    path(
        "nova-post/warehouses/<str:ref_settlement>/",
        WarehousesView.as_view(),
        name="nova-get-warehouses",
    ),
    path(
        "nova-post/warehous/type/",
        WarehouseTypeView.as_view(),
        name="nova-get-warehouses-type",
    ),
    path(
        "nova-post/search_streets/<str:street_name>/<str:ref>/",
        AddressesView.as_view(),
        name="nova-search-street",
    ),
    # DELIVERY
    path(
        "delivery/orders/create/",
        CreateOrderView.as_view(),
        name="delivery-create",
    ),
    path(
        "delivery/history/",
        OrderHistoryView.as_view(),
        name="delivery-history",
    ),
    # PAYMENT
    path(
        "payment/status/",
        CheckPaymentStatusView.as_view(),
        name="check-payment-status",
    ),
    path(
        "payment/callback/",
        PayCallbackView.as_view(),
        name="pay_callback",
    ),
    path(
        "baskets/merge/",
        MergeBasket.as_view(),
        name="bind-basket",
    ),
]

router = DefaultRouter()
router.register(
    r"baskets/(?P<basket_id>[\w-]+)/items",
    RetrieveUpdateDestroyBasketAPIView,
    basename="basket_item",
)
router.register(r"baskets", CreateBasket, basename="basket")
urlpatterns += router.urls
