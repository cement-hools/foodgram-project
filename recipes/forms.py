from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    """Форма создания рецепта."""

    class Meta:
        model = Recipe
        fields = ('title', 'cooking_time', 'description', 'image', 'tags',)
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'class': 'form__textarea'}),
        }