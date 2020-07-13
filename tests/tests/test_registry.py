from django.test import Client
from ajax_views.registry import registry
from app import views


def test_fbv_path():
    assert registry['tests.simple'].path == 'app.views.simple_override_view'


def test_cbv_path():
    assert registry['tests.simple_cbv'].path == 'app.views.SimpleView'


def test_view_singleton():
    lazy_objects = [
        registry['tests.first'],
        registry['tests.second'],
        registry['tests.third'],
    ]
    assert lazy_objects[0] is lazy_objects[1] is lazy_objects[2]


def test_laziness():
    lazy_objects = [
        registry['tests.first'],
        registry['tests.second'],
        registry['tests.third'],
        registry['tests.method-get'],
    ]
    assert all(obj.view_func is None for obj in lazy_objects) is True


def test_lazy_resolving():
    client = Client()
    response = client.get('/ajax/tests.first/')
    assert response.status_code == 200
    assert response.content == b'Hoping to find some old forgotten words or ancient melodies'

    # check object resolved
    lazy_objects = [
        registry['tests.first'],
        registry['tests.second'],
        registry['tests.third'],
    ]
    assert all(obj.view_func is not None for obj in lazy_objects) is True
    assert registry['tests.method-get'].view_func is None
