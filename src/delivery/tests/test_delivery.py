import uuid

import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_get_settlements_api_nova_post(api_client):
    url = reverse("nova-post-settlements", kwargs={"settlement_name": "Київ"})
    response = api_client.get(url)

    assert response.status_code == HTTP_200_OK
    assert len(response.data["data"]) > 0
    assert response.data.get("success") is True


@pytest.mark.django_db
def test_get_warehouse_types_api_nova_post(api_client):
    url = reverse("nova-get-warehouses-type")
    response = api_client.get(url)

    assert response.status_code == HTTP_200_OK
    assert len(response.data["data"]) > 0
    assert response.data.get("success") is True


@pytest.mark.django_db
def test_get_warehouses_api_nova_post(api_client):
    url = reverse(
        "nova-get-warehouses",
        kwargs={"ref_settlement": "e718a680-4b33-11e4-ab6d-005056801329"},
    )
    response = api_client.get(url)

    assert response.status_code == HTTP_200_OK
    assert len(response.data["data"]) > 0
    assert response.data.get("success") is True
    assert response.data["data"][0]["SiteKey"] == "105"


@pytest.mark.django_db
def test_search_settlement_streets_api_nova_post(api_client):
    url = reverse(
        "nova-search-street",
        kwargs={
            "street_name": "Пирогівський шлях",
            "ref": "1ec09d88-e1c2-11e3-8c4a-0050568002cf",
        },
    )
    response = api_client.get(url)

    assert response.status_code == HTTP_200_OK
    assert len(response.data["data"]) > 0
    assert response.data.get("success") is True


@pytest.mark.django_db
def test_user_cannot_create_order_from_someone_else_basket(
    api_client, test_user_mark, another_user, another_users_basket, order_data
):
    api_client.force_authenticate(user=test_user_mark)
    order_data["basket_id"] = another_users_basket.id
    response = api_client.post(reverse("order-create"), data=order_data)

    assert response.status_code == HTTP_403_FORBIDDEN
    assert (
        response.data["msg"] == "You cannot place an order from someone else's basket"
    )


@pytest.mark.django_db
def test_create_order_from_non_existing_basket(api_client, test_user_mark, order_data):
    api_client.force_authenticate(user=test_user_mark)
    order_data["basket_id"] = str(uuid.uuid4())

    response = api_client.post(reverse("order-create"), data=order_data)
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.data["msg"] == "Basket does not exist!"


@pytest.mark.django_db
def test_user_can_create_order(
    api_client,
    test_user_mark,
    basket,
    order_data,
    basket_items,
):
    api_client.force_authenticate(user=test_user_mark)
    response = api_client.post(reverse("order-create"), data=order_data)

    assert response.status_code == HTTP_200_OK
    assert (
        response.data["msg"]
        == "Your order has been created successfully! Go to checkout!"
    )


@pytest.mark.django_db
def test_user_cannot_create_order_with_empty_basket(
    api_client, test_user_mark, empty_basket, order_data
):
    api_client.force_authenticate(user=test_user_mark)
    order_data["basket_id"] = empty_basket.id
    response = api_client.post(reverse("order-create"), data=order_data)

    assert response.status_code == HTTP_404_NOT_FOUND
    assert (
        response.data["msg"]
        == "Your basket is empty. Please add items to cart before checkout."
    )
