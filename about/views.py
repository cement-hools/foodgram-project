from django.views.generic import TemplateView


class AboutAuthorView(TemplateView):
    template_name = 'author.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['text'] = (
            'На создание этой страницы у меня ушло пять минут! Ай да я.'
        )
        return context


class AboutTechView(TemplateView):
    template_name = 'tech.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tech_list = [
            'Python 3+',
            'Django 3+',
            'PostgreSQL',
            'Sorl - thumbnail',
        ]
        context['tech_list'] = tech_list
        context['text'] = (
            'При разработке проекта были использованы:'
        )
        return context
