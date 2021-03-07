from django import forms

from .models import Recipe, Tag


class RecipeForm(forms.ModelForm):
    """Форма создания рецепта."""

    title = forms.CharField(max_length=256)

    cooking_time = forms.IntegerField(min_value=1)
    # image = forms.ImageField()

    class Meta:
        model = Recipe
        fields = ('title', 'cooking_time', 'description', 'image', 'tags',)
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'class': 'form__textarea'}),
        }