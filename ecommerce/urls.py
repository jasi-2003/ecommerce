"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from UserData import views
from UserData.views import profile_view,Homepage,ForgotpasswordView,Otp_verify,ConformPassword
from product.views import *
from django.conf import settings
from django.conf.urls.static import static

def redirct_home(request):

    return redirect("ecommerce")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',redirct_home),
    path('AuraMart',Homepage.as_view(),name ="ecommerce"),

    #userdata
    path("userdata/reg/",views.Registration.as_view(),name='registration'),
    path('userdata/login/',views.Login.as_view(),name="login"),
    path("userdata/logout",views.LogoutView.as_view(),name="logout"),
    path('profile/', profile_view, name='profile'),
    path("updateprofile/<int:pk>",views.ProfileUpdate.as_view(),name="updateprofile"),
    path("userdata/profileinfo/<int:pk>",views.ProfileDetailView.as_view(),name="profileinfo"),
    path("forgotpassword/",views.ForgotpasswordView.as_view(),name="forgotpassword"),
    path("otp_verify/",views.Otp_verify.as_view(),name="otpverify"),
    path("restpassord/",views.ConformPassword.as_view(),name="restpassword"),

    #products
    path("product/addcategory/",Addcategory.as_view(),name="addcategory"),
    path("product/updatecategory/<int:pk>",CategoryupdateView.as_view(),name="updatecategory"),
    path("product/addproduct/",AddproductView.as_view(),name="addproduct"),
    path("product/categorylist/",CategorylistView.as_view(),name="categortlist"),
    path('product/productlist/',ProductlistView.as_view(),name="product_list"),
    path("product/product_update/<int:pk>",Product_updateView.as_view(),name="productupdate"),
    path("product/productdelete/<int:pk>",Product_deleteView.as_view(),name="productdelete"),
    path("product/categorydelete/<int:pk>",CategorydeleteView.as_view(),name="categorydelete"),
    path("product/productdetails/<int:pk>",Product_detailView.as_view(),name="productdetails"),
    path('product/categorydetails/<int:pk>',CategoryDetailView.as_view(),name="categorydetails"),
    path("searchproduct/",Searchfilter.as_view(),name="search"),

    #review
    path('product/<int:pk>/addreview',ReviewaddView.as_view(),name="add_review"),
    path("product/<int:pk>/review_update",ReviewUpdate.as_view(),name="reviewupdate"),
    path("product/<int:pk>/review_delete",ReviewDelete.as_view(),name="Review_Delete"),



    #Carts

    path('product/addcart/<int:pk>',AdditeamsView.as_view(),name="addcart"),
    path("product/cartupdate/<int:pk>",Updatecart.as_view(),name="cart_update"),
    path("product/cartlist",CartiteamList.as_view(),name="cartlist"), 
    path("product/cartdelete/<int:pk>",Deletecarts.as_view(),name="cartdelete"),



    #order
    path("order/product/<int:pk>",Addorderproduct.as_view(),name="addoder"),
    path("order/addoder_cart/",Addorder_cart.as_view(),name="addoder_cart"),


    #payment
    path("OrderitemsListview/",OrderitemsListview.as_view(),name="OrderitemsListview"),
    path("checkout/",Placeorder.as_view(),name="checkout")
    
    


    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  