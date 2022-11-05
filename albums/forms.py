from django import forms
from django.core.exceptions import ValidationError
from .models import *

class AlbumForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AlbumForm, self).__init__(*args, **kwargs)
        self.fields['approved'].help_text = '> Approve the album if its name is not explicit'




    class Meta:
        model = Album
        fields = '__all__'

class BaseSongFormSet(forms.BaseInlineFormSet):

    def clean(self):
        '''Checks if the album has atleast 1 song.'''
        if any(self.errors):
            return

        songsNum = 0

        ## Iterate over all the form songs
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            ##if the current form isnt empty(has a song)
            if len(form.cleaned_data) > 0:
                songsNum+=1 ## increment Counter

        if songsNum == 0: ## If No songs were added, raise an exception
            raise ValidationError("An Album Must have atleast 1 song.")

