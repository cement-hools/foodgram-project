from django import template

# В template.Library зарегистрированы все теги и фильтры шаблонов
# добавляем к ним и наш фильтр
register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


# синтаксис @register... , под которой описан класс addclass() -
# это применение "декораторов", функций, обрабатывающих функции
# мы скоро про них расскажем. Не бойтесь соб@к

@register.filter
def uglify(value):
    res = [
        x.lower()
        if i % 2 != 0
        else x.upper()
        for i, x in enumerate(value)
    ]
    return ''.join(res)


@register.filter
def favorite_recipe(things, recipe):
    return things.filter(recipe=recipe)


@register.filter
def follow_author(things, author):
    return things.filter(author=author)
