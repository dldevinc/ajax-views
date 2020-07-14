from django.http import HttpResponse
from django.views.generic import View, TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET, require_POST
from ajax_views.decorators import ajax_view


class IndexView(TemplateView):
    template_name = 'app/index.html'


@ajax_view('tests.simple')
def simple_view(request):
    return HttpResponse(b'I hear the drums echoing tonight')


@ajax_view('tests.simple')
def simple_override_view(request):
    return HttpResponse(b'But she hears only whispers of some quiet conversation')


@require_GET
@ajax_view('tests.method-get')
def get_view(request):
    return HttpResponse(b'She\'s coming in twelve-thirty flight')


@require_POST
@ajax_view('tests.method-post')
def post_view(request):
    return HttpResponse(b'Her moonlit wings reflect the stars that guide me towards salvation')


@never_cache
@ajax_view('tests.decorated')
def decorated_view(request):
    return HttpResponse(b'I stopped an old man along the way')


@ajax_view(['tests.first', 'tests.second', 'tests.third'])
def multinamed_view(request):
    return HttpResponse(b'Hoping to find some old forgotten words or ancient melodies')


@ajax_view(['tests.foo', 'tests.bar', 'tests.baz'])
def another_multinamed_view(request):
    return HttpResponse(b'He turned to me as if to say: Hurry boy, it\'s waiting there for you')


@csrf_exempt
@require_POST
@ajax_view('tests.csrf_exempt')
def csrf_exempt_view(request):
    return HttpResponse(b'It\'s gonna take a lot to drag me away from you')


@ajax_view('tests.simple_cbv')
class SimpleView(View):
    def get(self, request):
        return HttpResponse(b'There\'s nothing that a hundred men or more could ever do')
