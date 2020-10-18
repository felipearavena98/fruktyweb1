from django.db import models


class Pais(models.Model):
    id_pais = models.AutoField(primary_key=True)
    detalle_pais = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'pais'

class Ciudad(models.Model):
    id_ciudad = models.AutoField(primary_key=True)
    detalle_ciudad = models.CharField(max_length=150)
    id_pais = models.ForeignKey('Pais', models.DO_NOTHING, db_column='id_pais')

    class Meta:
        managed = False
        db_table = 'ciudad'

class TipoUsuario(models.Model):
    id_tipo_usuario = models.AutoField(primary_key=True)
    nombre_tipo_usuario = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'tipo_usuario'





from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

# Create your models here.
class UsuarioManager(BaseUserManager):
    def _create_user(self,username,email,nombre,password,is_staff,is_superuser,**extra_fields):
        user = self.model(
            username = username,
            email = email,
            nombre = nombre,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self,username,email,nombre,password = None,**extra_fields):
        return self._create_user(username,email,nombre,password,False,False,**extra_fields)
    
    def create_superuser(self,username,email,nombre,password = None,**extra_fields):
        return self._create_user(username, email, nombre, password, True, True, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin, models.Model):
    id_cliente = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=12)
    username = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=15)
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    direccion = models.CharField(max_length=100)
    telefono = models.BigIntegerField()
    email = models.EmailField(max_length=30, unique=True)
    id_tipo_usuario = models.ForeignKey(TipoUsuario, models.DO_NOTHING, db_column='id_tipo_usuario')
    id_ciudad = models.ForeignKey(Ciudad, models.DO_NOTHING, db_column='id_ciudad')
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','nombre']


    class Meta:
        managed = False
        db_table = 'usuario'

    def __str__(self):
        return f'{self.nombre},{self.apellido}'