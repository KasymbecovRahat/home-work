from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator,MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class Category(models.Model):
    category_name = models.CharField(max_length=50,null=True,blank=True)

    def __str__(self):
        return self.category_name


class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(null=True,blank=True,
        validators=[MinValueValidator(12),MaxValueValidator(100)])

    date_registred = models.DateField(auto_now_add=True)
    phone_number = PhoneNumberField(blank=True,null=True,region='KG')
    STATUS_CHOICES = (
        ('gold','GOLD'),
        ('silver','SOLVER'),
        ('bronze','BRONZE'),
        ('simple','SIMPLE'),
    )
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,null=True,blank=True)

    def __str__(self):
        f'{self.first_name},{self.last_name}'


class Product(models.Model):
    product_name = models.CharField(max_length=50,null=True,blank=True)
    category = models.ForeignKey(Category,related_name='product',on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=15,decimal_places=2,default=1)
    date_created = models.DateTimeField(auto_now_add=True)
    video = models.FileField(upload_to='video/',null=True,blank=True, verbose_name='видео')
    description = models.TextField(null=True,blank=True)
    have = models.BooleanField(verbose_name='в наличии')
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name

    def get_average_raitings(self):
        raitings = self.raitings.all()
        if raitings.exists():
            return round(sum(raiting.stars for raiting in raitings) / raitings.count(),1)
        return 0



class ProductPhoto(models.Model):
    image = models.ImageField(upload_to='image/',verbose_name='изоброжение',null=True,blank=True)
    product = models.ForeignKey(Product,related_name='product_photo',on_delete=models.CASCADE)


class Raitings(models.Model):
    product = models.ForeignKey(Product,related_name='raitings',on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1,6)],verbose_name='Рейтинг')

    def __str__(self):
        return f'{self.stars}, {self.user},{self.product}'


class Review(models.Model):
    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name='review',on_delete=models.CASCADE)
    parent_review = models.ForeignKey('self',on_delete=models.CASCADE,related_name='replice',null=True,blank=True)
    text = models.TextField()

    def __str__(self):
        return f'{self.product},{self.author}'


class Cart(models.Model):
    user = models.OneToOneField(UserProfile,on_delete=models.CASCADE,related_name='cart')
    creat_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'

    def get_total_price(self):
        total_price = sum(item.get_total_price() for item in self.items.all())
        if self.user.status == 'gold':
            discount = 0.25
        elif self.user.status == 'silver':
            discount = 0.50
        elif self.user.status == 'bronze':
            discount = 0.75
        final_price = total_price * (1 - discount)
        return final_price



class CarItem(models.Model):
    cart = models.ForeignKey(Cart,related_name='items',on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity


