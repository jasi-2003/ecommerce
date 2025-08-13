from django import forms

from product.models import ProductModel ,ReviewModels



class AddproductForm(forms.ModelForm):

    class Meta :

        model =ProductModel

        fields = ["product_name","description","price","stock","Category","image"]


class ReviewForm(forms.ModelForm):

    class Meta :

        model = ReviewModels 

        fields =["rating","comment"]    
        

