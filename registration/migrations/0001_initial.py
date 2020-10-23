# Generated by Django 3.1.1 on 2020-10-22 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id_cliente', models.AutoField(primary_key=True, serialize=False)),
                ('rut', models.CharField(max_length=12)),
                ('username', models.CharField(max_length=15, unique=True)),
                ('password', models.CharField(max_length=15)),
                ('nombre', models.CharField(max_length=150)),
                ('apellido', models.CharField(max_length=150)),
                ('direccion', models.CharField(max_length=100)),
                ('telefono', models.BigIntegerField()),
                ('email', models.EmailField(max_length=30, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'usuario',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BrProductosProcesoDeVenta',
            fields=[
                ('id_productos_proceso', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField()),
            ],
            options={
                'db_table': 'br_productos_proceso_de_venta',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BrUsuariosProcesoDeVenta',
            fields=[
                ('id_br_usuarios_proceso', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'br_usuarios_proceso_de_venta',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CalidadProducto',
            fields=[
                ('id_calidad', models.AutoField(primary_key=True, serialize=False)),
                ('detalle_calidad', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'calidad_producto',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id_ciudad', models.AutoField(primary_key=True, serialize=False)),
                ('detalle_ciudad', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'ciudad',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Contrato',
            fields=[
                ('id_contrato', models.AutoField(primary_key=True, serialize=False)),
                ('detalle_contrato', models.CharField(max_length=150)),
                ('fecha_inicio', models.CharField(max_length=20)),
                ('fecha_actualizacion', models.CharField(max_length=20)),
                ('fecha_termino', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'contrato',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('id_dventa', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion_dventa', models.CharField(max_length=150)),
                ('iva', models.DecimalField(decimal_places=1, max_digits=2)),
                ('monto', models.BigIntegerField()),
                ('monto_total', models.BigIntegerField()),
                ('cuotas', models.BigIntegerField()),
                ('monto_envio', models.BigIntegerField(blank=True, null=True)),
                ('monto_aduana', models.BigIntegerField(blank=True, null=True)),
                ('pago_servicios', models.BigIntegerField(blank=True, null=True)),
                ('comision_empresa', models.BigIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'detalle_venta',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EstadoProducto',
            fields=[
                ('id_estado', models.BigIntegerField(primary_key=True, serialize=False)),
                ('descripcion_estado', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'estado_producto',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FormatoProducto',
            fields=[
                ('id_formato', models.BigIntegerField(primary_key=True, serialize=False)),
                ('nombre_formato', models.CharField(max_length=150)),
                ('descripcion_formato', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'formato_producto',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id_inventario', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=150)),
                ('cantidad', models.BigIntegerField()),
            ],
            options={
                'db_table': 'inventario',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Moneda',
            fields=[
                ('id_moneda', models.BigIntegerField(primary_key=True, serialize=False)),
                ('detalle_moneda', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'moneda',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id_pais', models.AutoField(primary_key=True, serialize=False)),
                ('detalle_pais', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'pais',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProcesoVenta',
            fields=[
                ('id_pventa', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_venta', models.CharField(max_length=100)),
                ('estado', models.CharField(max_length=20)),
                ('unidades_vendidas', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'proceso_venta',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id_producto', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_producto', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'producto',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Seguro',
            fields=[
                ('id_seguro', models.BigIntegerField(primary_key=True, serialize=False)),
                ('cobrado', models.CharField(max_length=1)),
            ],
            options={
                'db_table': 'seguro',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Subasta',
            fields=[
                ('id_subasta', models.BigIntegerField(primary_key=True, serialize=False)),
                ('plazo', models.DateField()),
                ('solicitud_ganadora', models.BigIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'subasta',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TipoUsuario',
            fields=[
                ('id_tipo_usuario', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_tipo_usuario', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'tipo_usuario',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Transporte',
            fields=[
                ('id_transporte', models.AutoField(primary_key=True, serialize=False)),
                ('tamanio', models.CharField(choices=[('Grande', 'Grande'), ('Mediano', 'Mediano'), ('Pequeño', 'Pequeño')], max_length=20)),
                ('capacidad_carga', models.CharField(max_length=150)),
                ('refrigeracion', models.CharField(choices=[('S', 'Si'), ('N', 'No')], max_length=1)),
            ],
            options={
                'db_table': 'transporte',
                'managed': False,
            },
        ),
    ]
