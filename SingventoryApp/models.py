from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.
class AccountManager(BaseUserManager):
    
    def create_superuser(self, email, name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        # activated = True

        # other_fields.is_active = True
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True'
            )
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True'
            )
 
        return self.create_user(email, name, password, **other_fields)


    def create_user(self, email, name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **other_fields)
        user.set_password(password)
        user.save()
        return user



class SVUser(AbstractBaseUser, PermissionsMixin):
    # username = models.CharField(max_length=32, unique=True, blank=True)
    email = models.EmailField(_('email Address'), unique=True)
    name = models.CharField(max_length=150, blank=True)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)


    CAT_CHOICES = (
        # ('Admin', 'Admin'),
        ('Admin', 'Admin'),
        ('User', 'User'),
    )

    ACTIVATION = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    category = models.CharField(
        _('category'),
        choices=CAT_CHOICES,
        max_length=15,
        default='User'
    )

    activated = models.CharField(
        _('activated'),
        choices=ACTIVATION,
        max_length=15,
        default='Inactive'
    )


    objects = AccountManager()  
 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = 'SV User'

    def __str__(self):
        return str(self.email)    

class Profile(models.Model):
    user = models.OneToOneField(SVUser, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile' 


class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Equipment(models.Model):
    name = models.CharField(max_length=256, unique=True)
    alt_name = models.TextField(null = True)
    description = models.TextField()
    image = models.ImageField(default='default.jpg', upload_to='menu_items')
    quantity = models.IntegerField(default=0,blank=True,null=True)
    category = models.ForeignKey(Category, null=True, verbose_name="Category", on_delete = models.CASCADE)
    VISIBLE = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )
    visibility = models.CharField(
        _('Visibility'),
        choices=VISIBLE,
        max_length=15,
        default='Active'
    )

    def __str__(self):
        return self.name


class BorrowManager(models.Manager):
    def create_borrow(self, user, equipment, quantity, status):
        borrow = self.create(user=user, equipment=equipment, quantity=quantity, status=status)
        return borrow

class Borrow(models.Model):
    user = models.ForeignKey(SVUser, null=True,blank=True, verbose_name="User",to_field = 'email', on_delete = models.CASCADE)
    equipment = models.ForeignKey(Equipment, null=True, blank=True,verbose_name="Equipment", to_field = 'name',on_delete = models.CASCADE)
    quantity = models.IntegerField(default = 1)
    date = models.DateTimeField(auto_now=True)
    STATUS = (
        ('Pending', 'Pending'),
        ('Cancelled', 'Cancelled'),
        ('Approved', 'Approved'),
        ('Possession', 'Possession'),
        ('Rejected', 'Rejected'),
        ('Return', 'Return'),
        ('Returned', 'Returned'),
    )
    status = models.CharField(
        _('status'),
        choices=STATUS,
        max_length=15,
        default=STATUS[0][0]
    )

    objects = BorrowManager()

    def __str__(self):
        return str(self.pk)


class NotificationManager(models.Manager):
    def create_notification(self, user, equipment, status):
        notification = self.create(user=user, equipment=equipment, status=status)
        return notification

class Notification(models.Model):
    user = models.ForeignKey(SVUser, null=True,blank=True, verbose_name="User",to_field = 'email', on_delete = models.CASCADE)
    equipment = models.ForeignKey(Equipment, null=True, blank=True,verbose_name="Equipment", to_field = 'name',on_delete = models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    STATUS = (
        ('request', 'request'),
        ('approved', 'approved'),
        ('rejected', 'rejected'),
        ('cancelled', 'cancelled'),
        ('return', 'return'),
        ('returned', 'returned'),
    )
    READSTATUS = (
        ('unread', 'unread'),
        ('read', 'read'),
    )
    status = models.CharField(
        _('status'),
        choices=STATUS,
        max_length=15,
        # default=STATUS[0][0]
    )

    readStatus = models.CharField(
        _('readStatus'),
        choices=READSTATUS,
        max_length=15,
        default=READSTATUS[0][0]
    )

    objects = NotificationManager()

    def __str__(self):
        return str(self.pk)