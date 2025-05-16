from django.views.generic import TemplateView


class FB登入SDK(TemplateView):
    template_name = "socialaccount/snippets/login_extra.html"
