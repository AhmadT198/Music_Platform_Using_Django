from django import forms
from django.contrib import admin
from .models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):

    def formfield_for_dbfield(self, db_field, **kwargs): ## Overriding formfield_for_dbfield to display bio Charfield as a TextArea
        formfield = super(UserAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'bio':
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield


admin.site.register(User,UserAdmin)