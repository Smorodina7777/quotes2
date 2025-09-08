from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('popular_quotes/', views.popular_quotes, name='popular_quotes'),
    path('quotes_by_source/<int:source_id>/', views.quotes_by_source, name='quotes_by_source'),
    path('source-autocomplete/', views.SourceAutocomplete.as_view(create_field='name'), name='source-autocomplete'),
    path('add_source/', views.add_source, name='add_source'),
    path('select_source/', views.select_source, name='select_source'),
    path('edit_quote/<int:quote_id>/', views.edit_quote, name='edit_quote'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
