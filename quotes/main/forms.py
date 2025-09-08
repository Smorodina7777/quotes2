from django import forms
from dal import autocomplete
from .models import Quote, Source

# class QuoteForm(forms.ModelForm):
#     class Meta:
#         model = Quote
#         fields = ['text', 'source', 'weight']
#         widgets = {
#             'source': autocomplete.ModelSelect2(
#                 url='source-autocomplete',
#                 forward=['name'],
#             ),
#         }

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['text', 'source', 'weight']
        widgets = {
            'source': autocomplete.Select2(
                url='source-autocomplete',
            ),
        }
