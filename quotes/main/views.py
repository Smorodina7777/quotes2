import random

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import QuoteForm
from .models import Quote, Source
from dal import autocomplete
import re

def index(request):
    if request.method == 'POST':
        quote_id = request.POST.get('quote_id')
        quote = get_object_or_404(Quote, id=quote_id)
        if 'like' in request.POST:
            quote.likes += 1
        elif 'dislike' in request.POST:
            quote.dislikes += 1
        quote.save()
        return redirect('index')

    quotes = Quote.objects.all()
    weighted_quotes = []

    for quote in quotes:
        weighted_quotes.extend([quote] * quote.weight)

    quote = random.choice(weighted_quotes) if weighted_quotes else None

    if quote:
        quote.views_count += 1
        quote.save()

    return render(request, 'main/index.html', {'quote': quote})

def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            source = form.cleaned_data['source']
            if Quote.objects.filter(text=text).exists():
                messages.error(request, 'Такая цитата уже существует.')
                # return redirect('add_quote')
                return render(request, 'main/add_quote.html', {'form': form})
            if Quote.objects.filter(source=source).count() >= 3:
                messages.error(request, 'У этого источника уже есть 3 цитаты. Нельзя добавить больше.')
                return render(request, 'main/add_quote.html', {'form': form})
            form.save()
            return redirect('index')
    else:
        form = QuoteForm()
    return render(request, 'main/add_quote.html', {'form': form})


def popular_quotes(request):
    quotes = Quote.objects.order_by('-likes')[:10]
    return render(request, 'main/popular_quotes.html', {'quotes': quotes})

def quotes_by_source(request, source_id):
    quotes = Quote.objects.filter(source_id=source_id)
    return render(request, 'main/quotes_by_source.html', {'quotes': quotes})

def select_source(request):
    sources = Source.objects.all()
    return render(request, 'main/select_source.html', {'sources': sources})

def edit_quote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    if request.method == 'POST':
        form = QuoteForm(request.POST, instance=quote)
        if form.is_valid():
            form.save()
            return redirect('quotes_by_source', source_id=quote.source.id)
    else:
        form = QuoteForm(instance=quote)
    return render(request, 'main/edit_quote.html', {'form': form})

@require_POST
def add_source(request):
    name = request.POST.get('name')
    if name:
        source, created = Source.objects.get_or_create(name=name)
        if created:
            return JsonResponse({'success': True, 'message': f'Источник "{name}" добавлен!', 'source_id': source.id})
        else:
            return JsonResponse({'success': False, 'error': f'Источник "{name}" уже существует.'})
    else:
        return JsonResponse({'success': False, 'error': 'Название источника не указано.'})

class SourceAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Source.objects.all()
        if self.q:
            # Убираем знаки препинания и приводим к нижнему регистру
            query = re.sub(r'[^\w\s]', '', self.q).lower()
            qs = qs.filter(name__iregex=r'[^\w\s]*' + re.escape(query) + r'[^\w\s]*')
        return qs

    def create_object(self, text):
        return Source.objects.create(name=text)
