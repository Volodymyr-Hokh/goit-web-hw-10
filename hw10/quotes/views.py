from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404

from .models import Quote, Tag, Author
from .forms import AuthorForm, QuoteForm


def get_top_10_tags():
    top_10_tags = Tag.objects.annotate(amount_quotes=Count("quote")).order_by("-amount_quotes")[:10]
    font_sizes = list(range(28, 9, -2))
    for i, tag in enumerate(top_10_tags):
        tag.font_size = font_sizes[i]
    return top_10_tags



def main(request, page=1):
    quotes = Quote.objects.all()
    top_10_tags = get_top_10_tags()

    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)

    context = {"quotes": quotes_on_page, "top_tags": top_10_tags}
    return render(request, "quotes/index.html", context)

@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quotes:index')
    else:
        form = AuthorForm()
    context = {'form': form}
    return render(request, 'quotes/add_author.html', context)


@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            tags = form.cleaned_data['tags']
            tags = [tag.strip() for tag in tags.split(' ')]
            quote = form.save(commit=False)
            quote.author = form.cleaned_data['author']
            quote.save()

            for tag_text in tags:
                tag = Tag.objects.get_or_create(name=tag_text)[0]
                quote.tags.add(tag)
            return redirect("quotes:index")
    else:
        form = QuoteForm()

    context = {'form': form}
    return render(request, 'quotes/add_quote.html', context)


def about_author(request, author_fullname):
    author = get_object_or_404(Author, fullname=author_fullname)
    context = {'author': author}
    return render(request, 'quotes/about_author.html', context)


def show_quotes(request, tag_name, page=1):
    quotes = Quote.objects.filter(tags__name=tag_name)

    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)

    context = {"quotes": quotes_on_page, "tag": tag_name}
    return render(request, "quotes/show_quotes.html", context)
    