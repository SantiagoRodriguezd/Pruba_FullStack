from django.db import models


class Rol(models.Model):
    nombre_rol = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_rol


class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length=100)
    contrasena = models.CharField(max_length=100)
    rol_id = models.ManyToManyField("Rol", related_name="usuarios")

    def __str__(self):
        return self.nombre_usuario

    def verificar_contrasena(self, contrasena):
        # Verificar la contraseña del usuario
        if self.contrasena == contrasena:
            return True
        return False


class Cliente(models.Model):
    documento = models.BigIntegerField(primary_key=True)
    tipo_documento = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    imagen_perfil = models.CharField(max_length=200)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)


class Proveedor(models.Model):
    nit = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)
    numero_contacto = models.CharField(max_length=20)


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    unidades_stock = models.IntegerField()
    descripcion = models.TextField()
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)


class Transaccion(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_compra = models.DateField()
