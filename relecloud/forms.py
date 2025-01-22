from django import forms
from .models import Review, Destination, Cruise

class ReviewForm(forms.ModelForm):
    # Opciones para los destinos y cruceros
    destination = forms.ModelChoiceField(queryset=Destination.objects.all(), required=False, label='Destino')
    cruise = forms.ModelChoiceField(queryset=Cruise.objects.all(), required=False, label='Crucero')

    class Meta:
        model = Review
        fields = ['user_name', 'comment', 'rating', 'destination', 'cruise']
        
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        # Personalizar el campo de rating con un widget numérico de 1 a 5
        self.fields['rating'].widget = forms.NumberInput(attrs={'min': 1, 'max': 5})  
        self.fields['comment'].widget = forms.Textarea(attrs={'rows': 4, 'cols': 40})
        
    def clean(self):
        cleaned_data = super().clean()
        destination = cleaned_data.get('destination')
        cruise = cleaned_data.get('cruise')
        
        # Validación personalizada: al menos un destino o un crucero debe ser seleccionado
        if not destination and not cruise:
            raise forms.ValidationError('Debes seleccionar un destino o un crucero para dejar una reseña.')
        
        return cleaned_data

class InfoRequestForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Name",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name',
        })
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
        })
    )
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Write your message here...',
        })
    )

