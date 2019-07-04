from django.test import TestCase, Client
from ajax_views.registry import registry


class RegistryTest(TestCase):
    def test_fbv_path(self):
        self.assertEqual(registry['tests.simple'].path, 'tests.app.views.simple_duplicate_view')

    def test_cbv_path(self):
        self.assertEqual(registry['tests.simple_cbv'].path, 'tests.app.views.SimpleView')

    def test_lazy_object(self):
        lazy_objects = [
            registry['tests.first'],
            registry['tests.second'],
            registry['tests.third'],
        ]
        with self.subTest('check equality'):
            self.assertIs(lazy_objects[0], lazy_objects[1])
            self.assertIs(lazy_objects[1], lazy_objects[2])

        # check object is not resolved
        self.assertTrue(all(obj.view_func is None for obj in lazy_objects))

        client = Client()
        response = client.get('/ajax/tests.first/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Hoping to find some old forgotten words or ancient melodies')

        # check object resolved
        self.assertTrue(all(obj.view_func is not None for obj in lazy_objects))


class HTTPTest(TestCase):
    def test_404(self):
        client = Client()
        response = client.get('/ajax/nothing/')
        self.assertEqual(response.status_code, 404)

    def test_overriden_view(self):
        client = Client()
        response = client.get('/ajax/tests.simple/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'But she hears only whispers of some quiet conversation')

    def test_get(self):
        client = Client()
        get_response = client.get('/ajax/tests.method-get/')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.content, b'She\'s coming in twelve-thirty flight')

        post_response = client.post('/ajax/tests.method-get/')
        self.assertEqual(post_response.status_code, 405)

        head_response = client.head('/ajax/tests.method-get/')
        self.assertEqual(head_response.status_code, 405)

    def test_post(self):
        client = Client()
        get_response = client.get('/ajax/tests.method-post/')
        self.assertEqual(get_response.status_code, 405)

        post_response = client.post('/ajax/tests.method-post/')
        self.assertEqual(post_response.status_code, 200)
        self.assertEqual(post_response.content, b'Her moonlit wings reflect the stars that guide me towards salvation')

    def test_decorated(self):
        client = Client()
        response = client.get('/ajax/tests.decorated/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'I stopped an old man along the way')
        self.assertEqual(response['Cache-Control'], 'max-age=0, no-cache, no-store, must-revalidate')

    def test_csrf_exempt(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post('/ajax/tests.csrf_exempt/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'It\'s gonna take a lot to drag me away from you')

    def test_cbv(self):
        client = Client()
        get_response = client.get('/ajax/tests.simple_cbv/')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.content, b'There\'s nothing that a hundred men or more could ever do')

        head_response = client.head('/ajax/tests.simple_cbv/')
        self.assertEqual(head_response.status_code, 200)

        post_response = client.post('/ajax/tests.simple_cbv/')
        self.assertEqual(post_response.status_code, 405)

    def test_multiname(self):
        client = Client()
        response = client.get('/ajax/tests.foo/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'He turned to me as if to say: Hurry boy, it\'s waiting there for you')

        response = client.get('/ajax/tests.bar/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'He turned to me as if to say: Hurry boy, it\'s waiting there for you')

        response = client.get('/ajax/tests.baz/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'He turned to me as if to say: Hurry boy, it\'s waiting there for you')
