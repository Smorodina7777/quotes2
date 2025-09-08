from django.db import connection
from django.forms import widgets as widgets_django
import pickle

from django.template.loader import render_to_string


class AutocompleteWidget(object):

    def _parse_queryset(self):
        self._application = self._queryset.model.__module__.split('.')[-1]
        self._model_name = self._queryset.model.__name__

        where_node = self._queryset.query.__dict__['where']
        where, where_params = where_node.as_sql(connection.ops.quote_name, connection)

        if where:
            self._queryset_where = where.replace('"', '\"')
            self._queryset_where_params = pickle.dumps(where_params)
        else:
            self._queryset_where = ""
            self._queryset_where_params = ""

class SelectAutocomplete(widgets_django.Select, AutocompleteWidget):

    def __init__(self, queryset, attrs=None):
        super(SelectAutocomplete, self).__init__(attrs)
        self._queryset = queryset
        self._parse_queryset()

    def render(self, name, value, attrs=None, choices=()):
        application = self._queryset.model.__module__.split('.')[-1]
        model_name = self._queryset.model.__name__

        return render_to_string('forms_custom/autocomplete.html', {'value': value,
            'attrs': attrs,
            'application': application,
            'model_name': model_name,
            'expression': 'title__startswith',
            'name': name,
            'where': self._queryset_where,
            'where_params': self._queryset_where_params
        })