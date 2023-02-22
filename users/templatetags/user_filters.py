from django import template
# В template.Library зарегистрированы все теги и фильтры шаблонов
# добавляем к ним и наш фильтр
register = template.Library()


@register.filter 
def addclass(field, css):
        return field.as_widget(attrs={"class": css})

@register.filter 
def uglify(word):
    ugly_word = ""
    i = 0
    for letter in word:
        i += 1
        
        if i % 2 == 0:
            ugly_word += letter.upper()
        else:
            ugly_word += letter.lower()
    
    return ugly_word

# синтаксис @register... , под которой описан класс addclass() - 
# это применение "декораторов", функций, обрабатывающих функции
# мы скоро про них расскажем. Не бойтесь соб@к