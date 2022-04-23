from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.contrib.postgres.fields import ArrayField
     


# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self,fname,email,lname=None,phone=None,city=None,password=None,**kwargs):
        if not email:
            raise ValueError('Users must have an email address')
    
        user = self.model(
            fname       = fname,
            lname       = lname,
            phone       = phone,
            city        = city,
            email      = self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self,fname,email,password,lname=None,phone=None,city=None):
        user = self.create_user(
            fname       = fname,
            lname       = lname,
            phone       = phone,
            city        = city,
            email      = self.normalize_email(email),
            password   = password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    fname            = models.CharField(max_length=30)
    lname            = models.CharField(max_length=30,default=None,null=True,blank=True)
    email           = models.EmailField(max_length=50, unique=True)
    phone           = models.CharField(max_length=15,default=None,null=True,blank=True)
    city            = models.CharField(max_length=50,default=None,null=True,blank=True)
    last_login      = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)

    
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['fname']

    objects = MyUserManager()

    
    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True
   


class PastRecommendations(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    past_recom = ArrayField(models.IntegerField(), size=10)
