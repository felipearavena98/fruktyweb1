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

    def __str__(self):
        return str(self.id_tipo_usuario)


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
        return f'{self.nombre} {self.apellido}'

class Seguro(models.Model):
    id_seguro = models.BigIntegerField(primary_key=True)
    cobrado = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'seguro'

class Subasta(models.Model):
    id_subasta = models.BigIntegerField(primary_key=True)
    plazo = models.DateField()
    solicitud_ganadora = models.BigIntegerField(blank=True, null=True)
    id_seguro = models.ForeignKey(Seguro, models.DO_NOTHING, db_column='id_seguro', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subasta'

OPCION_TAMANIO = [
    ('Grande','Grande'),
    ('Mediano', 'Mediano'),
    ('Pequeño', 'Pequeño'),
]

OPCION_REFRI = [
    ('S','Si'),
    ('N', 'No'),
]

class Transporte(models.Model):
    id_transporte = models.AutoField(primary_key=True)
    tamanio = models.CharField(max_length=20, choices=OPCION_TAMANIO)
    capacidad_carga = models.CharField(max_length=150)
    refrigeracion = models.CharField(max_length=1, choices=OPCION_REFRI)
    id_cliente = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_cliente')

    class Meta:
        managed = False
        db_table = 'transporte'

class Moneda(models.Model):
    id_moneda = models.BigIntegerField(primary_key=True)
    detalle_moneda = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'moneda'

class DetalleVenta(models.Model):
    id_dventa = models.AutoField(primary_key=True)
    descripcion_dventa = models.CharField(max_length=150)
    iva = models.DecimalField(max_digits=2, decimal_places=1)
    monto = models.BigIntegerField()
    monto_total = models.BigIntegerField()
    cuotas = models.BigIntegerField()
    monto_envio = models.BigIntegerField(blank=True, null=True)
    monto_aduana = models.BigIntegerField(blank=True, null=True)
    pago_servicios = models.BigIntegerField(blank=True, null=True)
    comision_empresa = models.BigIntegerField(blank=True, null=True)
    id_moneda = models.ForeignKey('Moneda', models.DO_NOTHING, db_column='id_moneda')

    class Meta:
        managed = False
        db_table = 'detalle_venta'

class Contrato(models.Model):
    id_contrato = models.AutoField(primary_key=True)
    detalle_contrato = models.CharField(max_length=150)
    fecha_inicio = models.CharField(max_length=20)
    fecha_actualizacion = models.CharField(max_length=20)
    fecha_termino = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'contrato'

class ProcesoVenta(models.Model):
    id_pventa = models.AutoField(primary_key=True)
    tipo_venta = models.CharField(max_length=100)
    estado = models.CharField(max_length=20,default='Pendiente')
    unidades_vendidas = models.CharField(max_length=150)
    id_contrato = models.ForeignKey(Contrato, models.DO_NOTHING, db_column='id_contrato', blank=True, null=True)
    id_dventa = models.ForeignKey(DetalleVenta, models.DO_NOTHING, db_column='id_dventa', blank=True, null=True)
    id_subasta = models.ForeignKey('Subasta', models.DO_NOTHING, db_column='id_subasta', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proceso_venta'

class BrProductosProcesoDeVenta(models.Model):
    id_productos_proceso = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey('Producto', models.DO_NOTHING, db_column='id_producto')
    id_pventa = models.ForeignKey('ProcesoVenta', models.DO_NOTHING, db_column='id_pventa')
    cantidad = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'br_productos_proceso_de_venta'

class BrUsuariosProcesoDeVenta(models.Model):
    id_br_usuarios_proceso = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_cliente')
    id_pventa = models.ForeignKey('ProcesoVenta', models.DO_NOTHING, db_column='id_pventa')

    class Meta:
        managed = False
        db_table = 'br_usuarios_proceso_de_venta'

class CalidadProducto(models.Model):
    id_calidad = models.AutoField(primary_key=True)
    detalle_calidad = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'calidad_producto'

class EstadoProducto(models.Model):
    id_estado = models.BigIntegerField(primary_key=True)
    descripcion_estado = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'estado_producto'

class FormatoProducto(models.Model):
    id_formato = models.BigIntegerField(primary_key=True)
    nombre_formato = models.CharField(max_length=150)
    descripcion_formato = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'formato_producto'

class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=150)
    cantidad = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'inventario'

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=150)
    id_estado = models.ForeignKey(EstadoProducto, models.DO_NOTHING, db_column='id_estado')
    id_calidad = models.ForeignKey(CalidadProducto, models.DO_NOTHING, db_column='id_calidad')
    id_formato = models.ForeignKey(FormatoProducto, models.DO_NOTHING, db_column='id_formato')
    id_inventario = models.ForeignKey(Inventario, models.DO_NOTHING, db_column='id_inventario', blank=True, null=True)
    precio_unitario = models.IntegerField(db_column='precio_unitario')

    class Meta:
        managed = False
        db_table = 'producto'

    def __str__(self):
        return f'{self.nombre} {self.id_formato}'

