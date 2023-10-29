from django import forms

from .models import Quote, Author


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["fullname", "born_date", "born_location", "description"]


class QuoteForm(forms.ModelForm):
    author = forms.ModelChoiceField(queryset=Author.objects.all().order_by("fullname"))
    tags = forms.CharField(
        label='Tags',
        help_text='Enter tags separated by commas.'
    )

    class Meta:
        model = Quote
        fields = ['author', 'quote']