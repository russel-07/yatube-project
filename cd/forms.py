from django import forms

from .models import Contact, CD


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "subject", "body"]


class ExchangeForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=100)
    email = forms.EmailField(label='Электронная почта для обратной связи')
    title = forms.CharField(label='Название альбома', max_length=100)
    artist = forms.CharField(label='Исполнитель', max_length=40)
    genre = forms.ChoiceField(label='Жанр', choices=(("R", "Рок"), ("E", "Электроника"), ("P", "Поп"), ("C", "Классика"), ("O", "Саундтреки"),))
    price = forms.IntegerField(label='Стоимость', required=False)
    comment = forms.CharField(label='Комментарий', widget=forms.Textarea, required=False)

    def clean_artist(self):
        artist = self.cleaned_data['artist']
        if CD.objects.filter(artist=artist).count() == 0:
            raise forms.ValidationError('Данный диск не предназначен для обмена')
        return artist