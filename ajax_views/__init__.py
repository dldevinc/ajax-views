"""
    =========================
      Simple AJAX framework
    =========================

    AJAX-представления регистрируются с помощью декоратора ajax_view:

        @ajax_view(name='myapp.form')
        def form_view(request):
            ...

        @ajax_view(name='myapp.form_cbv')
        class AjaxView(View):
            ...

    Декоратор ajax_view должен указываться самым первым,
    если используется совместно с другими декораторами:

        @ajax_view(name='myapp.form')
        @csrf_exempt
        def form_view(request):
            ...

        @ajax_view(name='myapp.form_cbv')
        @method_decorator(csrf_exempt, name='dispatch')
        class AjaxView(View):

    Для получения URL любого представления из JavaScript,
    можно вывести JSON в глобальную переменную:

        <script>
            window.ajax_views = {% ajax_views_json %};
        </script>

    Для упрощения вывода URL AJAX-представления в шаблоне,
    добавлена шаблонный тэг ajax_url:

        <form action="{% ajax_url 'contact_form' %}" method="post">
            ...

    Установка
    ---------
    Добавить "ajax_views" в INSTALLED_APPS:
        INSTALLED_APPS = [
            ...
            'ajax_views',
        ]

    Пример
    ------
    # views.py
        from ajax_views.decorators import ajax_view

        @ajax_view(name='example.form')
        def example_view(request):
            ...

        @ajax_view(name='example.form')
        class ExampleFormView(FormView):
            ...

    # index.html (Django)
        {% load ajax_views %}

        <form action="{% ajax_url 'example.form' %}" method="post">
            ...
        </form>

        <script>
            window.ajax_views = {% ajax_views_json %};
        </script>

    # index.html (Jinja2)
        <form action="{{ ajax_url('example.form') }}" method="post">
            ...
        </form>

        <script>
            window.ajax_views = {% ajax_views_json %};
        </script>

    # index.js
        $.ajax({
            url: window.ajax_views.example.form,
            ...
        });

"""
default_app_config = 'ajax_views.apps.Config'
