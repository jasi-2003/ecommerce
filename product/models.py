from django.db import models

from UserData.models import User

# Create your models here.



class CategoryModel(models.Model):

    name = models.CharField(max_length=100,null=True)

    description = models.TextField(null=True)

    def __str__(self):
        return self.name



class ProductModel(models.Model):

    product_name = models.CharField(max_length=100,null=True)

    description = models.TextField(null=True)

    price = models.DecimalField(max_digits=10,decimal_places=2,null=True)

    stock = models.PositiveIntegerField(null=True)

    Category= models.ForeignKey(CategoryModel,on_delete=models.CASCADE,null=True)

    image = models.ImageField(upload_to='prodect_images',null=True)

    created_date = models.DateField(auto_now_add=True,null=True)

    def __str__(self):
        return self.product_name
    


class ReviewModels(models.Model):

    product =models.ForeignKey(ProductModel,on_delete=models.CASCADE)

    user = models.ForeignKey(User,on_delete=models.CASCADE)

    rating=models.IntegerField(choices=[(i,i) for i in range(1,6)])

    comment =models.TextField()

    create_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.comment




class Cart(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    @property

    def total_price(self):
        return sum(i.product.price * i.quantity for i in self.itemmodel_set.all())
    




class ItemModel(models.Model):  #cartitem models

    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)

    product = models.ForeignKey(ProductModel,on_delete=models.CASCADE)
    
    quantity = models.PositiveIntegerField(default=1)

    class Meta:

        unique_together =("cart","product")


    









#oder 
class Ordermodel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 👈 change here
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateField(auto_now_add=True)

    



class OrderItemModel(models.Model):
    order = models.ForeignKey(Ordermodel, on_delete=models.CASCADE)  # 👈 renamed
    item = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.CharField(max_length=20)





# order payment id


class Order_summary(models.Model):

    order_item_id =models.ForeignKey(OrderItemModel,on_delete=models.CASCADE,null=True)

    order_id = models.CharField(max_length=100)

    payment_status =models.BooleanField(default=False)

    payment_id=models.CharField(max_length=100,null=True,blank=True)

    total = models.FloatField()

    data =models.DateField(auto_now_add=True)





