import logging
from typing import Union

from django_catalog.settings.env_config import env_config
from yandex_geocoder import Client


logger = logging.getLogger()


def get_coordinates(address: str):
    """
    Получение координат по адресу.
    -> lat, lon
    """
    client = Client(env_config.YANDEX_MAPS_API_KEY)
    lon, lat = client.coordinates(address)
    return float(lat), float(lon)


def reorder_coordinates(coords: Union[tuple, list]) -> Union[tuple, list]:
    """
    Преобразует координаты

    lat, lon -> lon, lat
    lon, lat -> lat, lon
    """
    if isinstance(coords, tuple):
        return (coords[1], coords[0])
    elif isinstance(coords, list):
        return [(second, first) for first, second in coords]


def get_address_from_coordinates(orders, coord):
    for order in orders:
        if order.latitude == coord[1] and order.longitude == coord[0]:
            return order.delivery_address
    return "Не найден адрес"
