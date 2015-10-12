# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
import sorl
from sorl.thumbnail import ImageField
from sorl.thumbnail import get_thumbnail
from django.core.files.base import ContentFile
from accounts.models import AuthUser
# Create your models here.
from django_resized import ResizedImageField

class CommonActiveManager(models.Manager):
    def get_query_set(self):
        return super(CommonActiveManager, self).get_query_set().filter(is_active=True)

class FeauturedProductManager(models.Manager):

    def get_query_set(self):
        return super(FeauturedProductManager, self).get_query_set().filter(is_active=True, is_featured=True)



class Category(MPTTModel):
    name = models.CharField(_(u'Name'), max_length=150, unique=True)
    slug = models.SlugField(_(u'Slug'), max_length=150, unique=True,
                            help_text=_(u'Slug for product url created from name.'))
    title = models.CharField(_(u'Title'), max_length=150, help_text=_(u'Не уникальное имя для отображения в шаблонах'))
    # description = models.TextField(_(u'Description'))
    is_active = models.BooleanField(_(u'Active'), default=True)

    created_at = models.DateTimeField(_(u'Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_(u'Updated at'), auto_now=True)
    parent = TreeForeignKey('self', verbose_name=_(u'Parent category'),
                            related_name='children', blank=True,
                            help_text=_(u'Parent-category for current category'), null=True)
    active = CommonActiveManager()

    class Meta:

        ordering = ['-created_at']
        verbose_name_plural = _(u'Categories')

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return ('catalog_category', (), {'category_slug': self.slug})


class Product(models.Model):
    title = models.CharField(_(u'Имя'), max_length=255, unique=True)
    small_description = models.TextField(_(u'Пред_описание'), null=True, blank=True)
    description = models.TextField(_(u'Описание'), null=True, blank=True)
    price = models.IntegerField(_(u'Цена'),  default=30000)
    old_price = models.IntegerField(_(u'Старая цена'),  default=0)
    brand = models.CharField(_(u'Brand'), max_length=50, default="NoName")
    quantity = models.IntegerField(_(u'Количество'),default=1)
    slug = models.SlugField(_(u'Slug'),  max_length=255, unique=True,
                            help_text=_(u'Уникальное значения для URL продукта'))
    created_at = models.DateTimeField(_(u'Время созданія'), auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(_(u'Время обновлені'), auto_now_add=False, auto_now=True)
    categories = models.ManyToManyField(Category, verbose_name=_(u'Категории'),
                                        help_text=_(u'Категории продукта'))
    views = models.IntegerField(_(u'Количество просмотров'),null=True, blank=True)
    average_review = models.DecimalField(_(u'Средний рейтинг'), decimal_places=1, max_digits=100, default=0.0)
    is_active = models.BooleanField(_(u'Active'), default=True)
    is_new = models.BooleanField(_(u'Новинка'), default=False)
    is_bestseller = models.BooleanField(_(u'Bestseller'), default=False) # Лучшие продажи
    is_featured = models.BooleanField(_(u'Featured'), default=False) # Отображать на главной


    objects = models.Manager()
    active = CommonActiveManager()
    feautured = FeauturedProductManager()



    class Meta:
        ordering = ['-created_at']
        unique_together = ('title', 'slug')

    def __unicode__(self):
        return self.title


    @permalink
    def get_absolute_url(self):
        return ('products.views.product_view', (), {'brand_slug': self.brand,'product_slug': self.slug, 'id':self.id})

    def get_price(self):
        return self.price


    def sale(self):
        return self.sale_price

class ProductImage(models.Model):
    product = models.ForeignKey(Product)
    image  = ImageField(upload_to='images')
    image20 = ResizedImageField(size=[200, 200], upload_to='thumb',default="")
    image30 = ResizedImageField(size=[300, 300], upload_to='thumb',default="")

    featured = models.BooleanField(default=False)
    thumbnail = models.BooleanField()
    is_active = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.product.title

    @property
    def url(self):
        return self.image.url

    @property
    def url20(self):
        return self.image20.url

    def url30(self):
        return self.image30.url

    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         super(ProductImage, self).save(*args, **kwargs)
    #         resized = get_thumbnail(self.image, "100x100" )
    #         print self.image.name
    #         self.image.save(('thumb/'+self.image.name.split('.')[0]+'_100x100.'+self.image.name.split('.')[1]), ContentFile(resized.read()), True)
    #         sorl.thumbnail.delete(resized)
    #     super(ProductImage, self).save(*args, **kwargs)

class ProductReview(models.Model):
    user = models.ForeignKey(AuthUser)
    score = models.DecimalField( decimal_places=1, max_digits=5, default=0.0)
    review = models.TextField()
    created_at = models.DateTimeField(_(u'Время созданія'), auto_now_add=True, auto_now=False)
    product = models.ForeignKey(Product)


    class META:
        unique_together = ('user','product')

    def __unicode__(self):
        return self.review

    def save(self, *args, **kwargs):
        super(ProductReview,self).save(*args, **kwargs)
        rws = ProductReview.objects.filter(product=self.product)
        score = 0
        for review in rws:
            score+=review.score
        if len(rws)>0:
            self.product.average_review = (score/len(rws))
        else:
            self.product.average_review = 0

        Product.objects.filter(id=self.product.id).update(average_review = self.product.average_review)

    def delete(self, *args, **kwargs):
        super(ProductReview,self).delete(*args, **kwargs)
        rws = ProductReview.objects.filter(product=self.product)
        score = 0
        for review in rws:
            score+=review.score
        if len(rws)>0:
            self.product.average_review = (score/len(rws))
        else:
            self.product.average_review = 0

        Product.objects.filter(id=self.product.id).update(average_review = self.product.average_review)

class CharacteristicType(models.Model):
    """Словарная таблица характеристик продуктов"""
    name = models.CharField(_(u'Name'), max_length=255)
    slug = models.SlugField(_(u'Slug'), max_length=150, unique=True,
                            help_text=_(u'Slug for product url created from name.'))
    class Meta:

        ordering = ['name']
        verbose_name_plural = _(u'Characteristics Types')
        unique_together = ('name',)

    def __unicode__(self):
        return self.slug


class Characteristic(models.Model):
    """Характеристики продуктов"""
    characteristic_type = models.ForeignKey(CharacteristicType)
    value = models.CharField(_(u'Value'), max_length=255)
    product = models.ForeignKey(Product, verbose_name=_(u'Product'),
                                help_text=_(u'Referenced product'))

    class Meta:
        ordering = ['characteristic_type', 'value']
        verbose_name_plural = _(u'Characteristics')
        # составной ключ, для избежания повторения одинковых характеристик у продукта
        unique_together = (('product', 'characteristic_type'),)

    def __unicode__(self):
        return self.characteristic_type.slug

