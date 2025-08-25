from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View ,CreateView  ,DeleteView ,DetailView ,UpdateView ,ListView
from UserData.models import User
from django.urls import reverse_lazy
from product.models import *
from product.forms import *
from django.utils.decorators import method_decorator
from django.db import IntegrityError


# Create your views here.




def is_user(fn):

    def wrapper(request,**kwargs):

        id = kwargs.get("pk")

        data = User.objects.get(id = id)

        if data.id == request.user:

            return fn(request,**kwargs)

        return redirect("login")

    return wrapper        


def is_login(fn):

    def wrapper(request,**kwargs):

        if not request.user.is_authenticated :

            return redirect("login")

        else:

            return fn(request,**kwargs)

    return wrapper           


# Category  add,update,list,delete

class Addcategory(CreateView):

    model = CategoryModel

    template_name ="addcategory.html"

    fields ="__all__"

    success_url=reverse_lazy("login")



class CategoryupdateView(UpdateView):


    model =CategoryModel

    template_name ="category_update.html"

    fields ="__all__"

    success_url =reverse_lazy("login")


class CategorylistView(ListView):

    model = CategoryModel

    template_name ="categorylistview.html"

    context_object_name ="data"

    success_url =reverse_lazy("login") 

class CategorydeleteView(DeleteView):

    model=CategoryModel

    template_name = "categorydelete.html"

    success_url = reverse_lazy("login")   


class CategoryDetailView(DetailView):

    model = CategoryModel

    template_name ="category_details.html"

    context_object_name="data"

    success_url = reverse_lazy("login")    






#products  add,update,detail,delete


class AddproductView(CreateView):

    model =ProductModel

    template_name ="addproductview.html"

    form_class =AddproductForm

    success_url = reverse_lazy("login")


class ProductlistView(ListView):

    model = ProductModel

    template_name ="productlistview.html"

    context_object_name ="data"

    success_url =reverse_lazy("login")    


class Product_updateView(UpdateView):

    model = ProductModel

    template_name ="Product_updateView.html"

    fields =["product_name","description","price","stock","Category","image"] 

    success_url = reverse_lazy("login")   


class Product_deleteView(DeleteView):

    model =ProductModel

    template_name = "productdelete.html"
 
    success_url = reverse_lazy("login")


class Product_detailView(DetailView):

    model =ProductModel

    template_name ="Product_detailView.html"

    context_object_name ="data"

    success_url =reverse_lazy ("login")




# Review 
# 

class ReviewaddView(CreateView):

    def get (self,request,**kwargs):

        id = kwargs.get("pk")

        data = ProductModel.objects.get(id=id)

        form = ReviewForm

        return render(request,"addreview.html" ,{'form':form,"data":data})
    
    def post(self, request,**kwargs):

        id =kwargs.get("pk")

        data =ProductModel.objects.get(id=id)

        form = ReviewForm(request.POST)

        if form.is_valid():

            ReviewModels.objects.create(**form.cleaned_data,user=request.user,product=data)

        form = ReviewForm

        return redirect("login") 


class ReviewUpdate(UpdateView):

    model=ReviewModels

    template_name ="reviewupdate.html"

    fields =["rating",'comment',]

    success_url = reverse_lazy("login")


class ReviewDelete(DeleteView):

    model = ReviewModels

    template_name ="reviewdelete.html"

    success_url =reverse_lazy("login")






# For Carts   
class AdditeamsView(View):
    def get(self, request, **kwargs):
        id = kwargs.get("pk")
        product = get_object_or_404(ProductModel, id=id)

        if product.stock > 0:
            cart, _ = Cart.objects.get_or_create(user=request.user)

            try:
                ItemModel.objects.create(cart=cart, product=product, quantity=1)
            except IntegrityError:
                item = ItemModel.objects.get(cart=cart, product=product)
                item.quantity += 1
                item.save()

            # ✅ Just access property, don’t assign
            print(cart.total_price)

        return redirect("cartlist")

@method_decorator(decorator=is_login, name="dispatch")
class CartiteamList(View):

    def get(self, request):
        # ✅ Prevent DoesNotExist by auto-creating a cart
        cart, created = Cart.objects.get_or_create(user=request.user)

        # ✅ Get cart items
        data = ItemModel.objects.filter(cart=cart)

        # ✅ Calculate subtotal for each item
        subtotal_list = [i.product.price * i.quantity for i in data]

        # ✅ Combine items with subtotals
        c_items = zip(data, subtotal_list)

        # ✅ Count items in cart
        count = len(data)

        # ✅ Total (calculated, don’t assign to cart)
        total = sum(subtotal_list)

        # Debugging
        print("Item count:", count)
        print("Subtotals:", subtotal_list)
        print("Cart total:", total)

        return render(
            request,
            "cart_list.html",
            {"c_items": c_items, "total": total, "count": count},
        )




@method_decorator(decorator=is_login, name="dispatch")
class Updatecart(View):

    def post(self, request, **kwargs):
        id = kwargs.get("pk")
        cart = Cart.objects.get(user=request.user)

        # Ensure the item belongs to the logged-in user’s cart
        data = get_object_or_404(ItemModel, id=id, cart=cart)

        new_quantity = int(request.POST.get("quantity"))

        if new_quantity > data.product.stock:
            data.quantity = data.product.stock
        else:
            data.quantity = new_quantity

        data.save()
        return redirect("cartlist")
# @method_decorator(decorator= is_user ,name="dispatch")
class Deletecarts(View):

    def get (self,request,**kwargs):

        id = kwargs.get("pk")

        cart = Cart.objects.get(user=request.user)

        data = ItemModel.objects.get(id =id,cart=cart)

        print(data)

        if data :

            data.delete()

            print("delete")

        return redirect("cartlist")    

        



#product list

class Addorderproduct(View):

    def get(self,request,**kwargs):

        id = kwargs.get("pk")

        item= ProductModel.objects.get(id=id)

        return render(request,"orderproduct.html",{'item':item})
    

    def post(self,request,**kwargs):

        id =kwargs.get("pk")

        item =ProductModel.objects.get(id=id)


        quantity =request.POST.get("quantity")

        total = item.price * int(quantity) 

        user_id = Ordermodel.objects.get(user=request.user)

        OrderItemModel.objects.create(order_id=user_id,quantity =quantity,item=item,status='pending')

        return render(request,"orderproduct.html",{"total":total})
class Addorder_cart(View):
    def post(self, request):
        user_cart = Cart.objects.get(user=request.user)
        items = ItemModel.objects.filter(cart=user_cart)

        total = user_cart.total_price

        # create order for user
        order = Ordermodel.objects.create(user=request.user)

        # create order items
        for i in items:
            OrderItemModel.objects.create(
                order=order,   # ✅ fixed
                item=i.product,
                quantity=i.quantity,
                status="pending"
            )

        # clear cart after ordering
        items.delete()

        return render(request, "orderpage.html", {"total": total})










# order payment 

class OrderitemsListview(View):
    def get(self,request):
        data =OrderItemModel.objects.filter(order_id =request.user.id)
        return render(request,"myiteams.html",{"data":data})


import razorpay

class Placeorder(View):

    def get(self,request):

        user = request.user
        # authentication btwn webserver and rzp
        client = razorpay.Client(auth=("rzp_test_pUWPD6sjoyG5uo", "5JGKBSKZNH7Okmsec6Fs0cQG"))

        user = Ordermodel.objects.get(user = request.user)

        order_items = OrderItemModel.objects.filter(order_id =user)

        total = sum(i.quantity * i.item.price for i in order_items)

        total = int(total*100)

        data =client.order.create(data={
           
            "amount": total,
            "currency": "INR",

       
         })
        
        print(data)

        return redirect("product_list")



# """
# {'amount': 452200, 'amount_due': 452200, 'amount_paid': 0, 'attempts': 0, 'created_at': 1744111386, 'currency': 'INR', 'entity': 'order', 'id': 'order_QGXsFjN9jTqiyS', 'notes': [], 'offer_id': None, 'receipt': None, 'status': 'created'}

# """

        
 



#search

class Searchfilter(View):

    def get(self,request):

        query=request.GET.get("q")

        data = ProductModel.objects.filter(product_name__icontains = query)

        return render(request,"searchproduct.html",{"data":data})





    





