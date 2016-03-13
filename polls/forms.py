from django import forms

class PollForm(forms.Form):
	question = forms.CharField(max_length=300,required=True,
		widget=forms.Textarea(attrs={'cols': 60, 'rows': 4}))
	choices = forms.CharField(max_length=600,required=True,
		widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}),
		help_text='One choice in one line')