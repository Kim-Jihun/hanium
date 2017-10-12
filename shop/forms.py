from django import forms
from .models import Rating, Review
from .validators import min_length_1_validator

class RatingForm(forms.ModelForm):

    class Meta:
        model = Rating
        # fields = '__all__'
        fields = ['score']



CHOICES_location = (('왕십리', '왕십리',), ('서울대입구', '서울대입구',), ('신촌', '신촌',) , ('건대입구', '건대입구',))
CHOICES_price = (('4000', '4,000~6,000',), ('6000', '6,000~8,000',), ('8000', '8,000~10,000',), ('10,000', '10,000~12,000',), ('12000', '12,000~14,000',))

class IndexForm(forms.Form):
    #title = forms.CharField(validators=[min_length_1_validator], label="상호 검색")
    location = forms.ChoiceField(widget=forms.Select, choices=CHOICES_location, label="식당 위치")
    menu = forms.CharField(validators=[min_length_1_validator], label="메뉴검색")
    price = forms.ChoiceField(widget=forms.Select, choices=CHOICES_price, label="평균 가격대")

class ReviewForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 70, 'rows': 4}))
    
    
    class Meta:
        model = Review
        #fields = '__all__'
        fields = ['content']





