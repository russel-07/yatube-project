
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.views.generic import CreateView

from .forms import ContactForm, ExchangeForm


def tariffs(request):
    plans = [
        {
            "name": "Бесплатно",
            "price": "0",
            "options": {"users": 10, "space": 10, "support": "Почтовая рассылка"},
        },
        {
            "name": "Профессиональный",
            "price": "49",
            "options": {"users": 50, "space": 100, "support": "Телефон и email"},
        },
        {
            "name": "Корпоративный",
            "price": "99",
            "options": {"users": 100, "space": 500, "support": "Персональный менеджер"},
        },
    ]

    return render(request, 'tariffs.html', {"plans": plans})


class ContactView(CreateView):
    form_class = ContactForm
    success_url = "/plans"
    template_name = "cd.html"


def send_msg(email, name, title, artist, genre, price, comment):
    subject = f"Обмен {artist}-{title}"
    body = f"""Предложение на обмен диска от {name} ({email})

    Название: {title}
    Исполнитель: {artist}
    Жанр: {genre}
    Стоимость: {price}
    Комментарий: {comment}

    """
    send_mail(subject, body, email, ["admin@rockenrolla.net", ],)


def exchange(request):
    if request.method == 'POST':
        form = ExchangeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            title = form.cleaned_data['title']
            artist = form.cleaned_data['artist']
            genre = form.cleaned_data['genre']
            price = form.cleaned_data['price']
            comment = form.cleaned_data['comment']
            send_msg(email, name, title, artist, genre, price, comment)
            return redirect('/thank-you/')
        return render(request, 'exchange.html', {'form': form})
    form = ExchangeForm()
    return render(request, 'new_post.html', {'form': form})


def thank_you(request):
    return render(request, 'thankyou.html')