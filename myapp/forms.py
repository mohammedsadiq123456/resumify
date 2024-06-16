# myapp/forms.py

from django import forms

class UploadFileForm(forms.Form):
    resume = forms.FileField(label='Select a PDF file')
