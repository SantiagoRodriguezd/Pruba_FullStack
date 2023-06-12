from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from tasks.models import Cliente, Producto, Usuario, Rol, Proveedor
from django.core import serializers
from django.http import JsonResponse
from .serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import re
import json


class TokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = TokenObtainPairSerializer


from rest_framework_simplejwt.tokens import RefreshToken


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    if request.method == "POST":
        username = request.data.get("username")
        password = request.data.get("password")

        if username and password:
            try:
                user = Usuario.objects.get(nombre_usuario=username)
                cliente = user.cliente_set.first()
                roles = user.rol_id.all()  # Obtener los roles asociados al usuario
            except Usuario.DoesNotExist:
                return JsonResponse(
                    {"error": "Usuario o contraseña inválida."}, status=400
                )

            if user.verificar_contrasena(password) and cliente:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                cliente_data = {
                    "documento": cliente.documento,
                    "tipo_documento": cliente.tipo_documento,
                    "nombre": cliente.nombre,
                    "apellido": cliente.apellido,
                    "direccion": cliente.direccion,
                    "telefono": cliente.telefono,
                    "fecha_nacimiento": cliente.fecha_nacimiento,
                    "imagen_perfil": cliente.imagen_perfil,
                }
                roles_data = [rol.nombre_rol for rol in roles]
                response_data = {
                    "access_token": access_token,
                    "message": "Inicio de sesión exitoso",
                    "cliente": cliente_data,
                    "roles": roles_data,
                }
                return JsonResponse(response_data)
            else:
                return JsonResponse(
                    {"error": "Usuario o contraseña inválida."}, status=400
                )
        else:
            return JsonResponse(
                {"error": "Falta el nombre de usuario o la contraseña."}, status=400
            )

    return JsonResponse({"error": "Método de solicitud inválido."}, status=405)


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def registro(request):
    if request.method == "POST":
        username = request.data.get("username")
        password = request.data.get("password")

        if username and password:
            if Usuario.objects.filter(nombre_usuario=username).exists():
                return JsonResponse(
                    {"error": "El nombre de usuario ya existe."}, status=400
                )

            if len(password) < 8:
                return JsonResponse(
                    {"error": "La contraseña debe tener al menos 8 caracteres."},
                    status=400,
                )
            if not re.search(r"\d", password):
                return JsonResponse(
                    {"error": "La contraseña debe contener al menos un dígito."},
                    status=400,
                )
            if not re.search(r"[A-Z]", password):
                return JsonResponse(
                    {
                        "error": "La contraseña debe contener al menos una letra mayúscula."
                    },
                    status=400,
                )
            if not re.search(r"[a-z]", password):
                return JsonResponse(
                    {
                        "error": "La contraseña debe contener al menos una letra minúscula."
                    },
                    status=400,
                )
            if not re.search(r"[!@#$%^&*()_\-+=~`[\]{}|:;\"'<>,.?/]", password):
                return JsonResponse(
                    {
                        "error": "La contraseña debe contener al menos un carácter especial."
                    },
                    status=400,
                )

            usuario = Usuario(nombre_usuario=username, contrasena=password)
            usuario.save()

            return JsonResponse({"message": "Registro exitoso"})
        else:
            return JsonResponse(
                {"error": "Falta el nombre de usuario o la contraseña."}, status=400
            )

    return JsonResponse({"error": "Método de solicitud inválido."}, status=405)


# Lista de usuarios con rol
@api_view(["GET"])
def usuarios_view(request):
    usuarios_roles = Usuario.objects.values(
        "id", "nombre_usuario", "rol_id__nombre_rol"
    )
    return Response(usuarios_roles)


# crud clientes
@csrf_exempt
def crear_cliente(request):
    if request.method == "POST":
        data = json.loads(request.body)
        documento = data.get("documento")
        tipo_documento = data.get("tipo_documento")
        nombre = data.get("nombre")
        apellido = data.get("apellido")
        direccion = data.get("direccion")
        telefono = data.get("telefono")
        fecha_nacimiento = data.get("fecha_nacimiento")
        imagen_perfil = data.get("imagen_perfil")
        id_usuario = data.get("id_usuario")

        if (
            documento
            and tipo_documento
            and nombre
            and apellido
            and direccion
            and telefono
            and fecha_nacimiento
            and imagen_perfil
        ):
            cliente = Cliente(
                documento=documento,
                tipo_documento=tipo_documento,
                nombre=nombre,
                apellido=apellido,
                direccion=direccion,
                telefono=telefono,
                fecha_nacimiento=fecha_nacimiento,
                imagen_perfil=imagen_perfil,
            )
            cliente.save()
            return JsonResponse({"message": "Cliente creado exitosamente"})

        return JsonResponse({"error": "Faltan datos requeridos"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def obtener_clientes(request):
    if request.method == "GET":
        clientes = Cliente.objects.all()
        data = [
            {
                "documento": cliente.documento,
                "tipo_documento": cliente.tipo_documento,
                "nombre": cliente.nombre,
                "apellido": cliente.apellido,
                "direccion": cliente.direccion,
                "telefono": cliente.telefono,
                "fecha_nacimiento": cliente.fecha_nacimiento,
                "imagen_perfil": cliente.imagen_perfil,
            }
            for cliente in clientes
        ]
        return JsonResponse(data, safe=False)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def actualizar_cliente(request, documento):
    try:
        cliente = Cliente.objects.get(documento=documento)
    except Cliente.DoesNotExist:
        return JsonResponse({"error": "Cliente no encontrado"}, status=404)

    if request.method == "PUT":
        tipo_documento = request.POST.get("tipo_documento")
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        direccion = request.POST.get("direccion")
        telefono = request.POST.get("telefono")
        fecha_nacimiento = request.POST.get("fecha_nacimiento")
        imagen_perfil = request.POST.get("imagen_perfil")

        if tipo_documento:
            cliente.tipo_documento = tipo_documento
        if nombre:
            cliente.nombre = nombre
        if apellido:
            cliente.apellido = apellido
        if direccion:
            cliente.direccion = direccion
        if telefono:
            cliente.telefono = telefono
        if fecha_nacimiento:
            cliente.fecha_nacimiento = fecha_nacimiento
        if imagen_perfil:
            cliente.imagen_perfil = imagen_perfil

        cliente.save()
        return JsonResponse({"message": "Cliente actualizado exitosamente"})

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def eliminar_cliente(request, documento):
    try:
        cliente = Cliente.objects.get(documento=documento)
    except Cliente.DoesNotExist:
        return JsonResponse({"error": "Cliente no encontrado"}, status=404)

    if request.method == "DELETE":
        cliente.delete()
        return JsonResponse({"message": "Cliente eliminado exitosamente"})

    return JsonResponse({"error": "Invalid request method"}, status=405)


# obtener cliente un unico usuario con documento
@csrf_exempt
def cliente_detalle_view(request, documento):
    try:
        cliente = Cliente.objects.get(documento=documento)
    except Cliente.DoesNotExist:
        return JsonResponse({"error": "Cliente no encontrado"}, status=404)

    if request.method == "GET":
        data = {
            "documento": cliente.documento,
            "tipo_documento": cliente.tipo_documento,
            "nombre": cliente.nombre,
            "apellido": cliente.apellido,
            "direccion": cliente.direccion,
            "telefono": cliente.telefono,
            "fecha_nacimiento": cliente.fecha_nacimiento.strftime("%Y-%m-%d"),
            "imagen_perfil": cliente.imagen_perfil,
        }
        return JsonResponse(data)

    return JsonResponse({"error": "Invalid request method"}, status=405)


# Crud Productos


@csrf_exempt
def crear_producto(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Formato de datos JSON inválido"}, status=400)

        nombre = data.get("nombre")
        categoria = data.get("categoria")
        marca = data.get("marca")
        valor_unitario = data.get("valor_unitario")
        unidades_stock = data.get("unidades_stock")
        descripcion = data.get("descripcion")
        proveedor_id = data.get("proveedor")

        if (
            nombre
            and categoria
            and marca
            and valor_unitario
            and unidades_stock
            and descripcion
            and proveedor_id is not None
        ):
            try:
                proveedor = Proveedor.objects.get(pk=proveedor_id)
            except Proveedor.DoesNotExist:
                return JsonResponse({"error": "Proveedor no encontrado"}, status=400)

            producto = Producto(
                nombre=nombre,
                categoria=categoria,
                marca=marca,
                valor_unitario=valor_unitario,
                unidades_stock=unidades_stock,
                descripcion=descripcion,
                proveedor=proveedor,
            )
            producto.save()

            # Retornar una respuesta JSON con los datos del producto creado
            data = {
                "nombre": producto.nombre,
                "categoria": producto.categoria,
                "marca": producto.marca,
                "valor_unitario": str(producto.valor_unitario),
                "unidades_stock": producto.unidades_stock,
                "descripcion": producto.descripcion,
                "proveedor": producto.proveedor.nombre,  # Obtener el nombre del proveedor
            }
            return JsonResponse(data)

        # Enviar una respuesta de error indicando los campos faltantes
        campos_faltantes = []
        if not nombre:
            campos_faltantes.append("nombre")
        if not categoria:
            campos_faltantes.append("categoria")
        if not marca:
            campos_faltantes.append("marca")
        if not valor_unitario:
            campos_faltantes.append("valor_unitario")
        if not unidades_stock:
            campos_faltantes.append("unidades_stock")
        if not descripcion:
            campos_faltantes.append("descripcion")
        if proveedor_id is None:
            campos_faltantes.append("proveedor")

        mensaje_error = f"Faltan datos requeridos: {', '.join(campos_faltantes)}"
        return JsonResponse({"error": mensaje_error}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def actualizar_producto(request, producto_id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Formato de datos JSON inválido"}, status=400)

        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            return JsonResponse({"error": "Producto no encontrado"}, status=404)

        producto.nombre = data.get("nombre", producto.nombre)
        producto.categoria = data.get("categoria", producto.categoria)
        producto.marca = data.get("marca", producto.marca)
        producto.valor_unitario = data.get("valor_unitario", producto.valor_unitario)
        producto.unidades_stock = data.get("unidades_stock", producto.unidades_stock)
        producto.descripcion = data.get("descripcion", producto.descripcion)

        proveedor_id = data.get("proveedor")
        if proveedor_id:
            try:
                proveedor = Proveedor.objects.get(id=proveedor_id)
                producto.proveedor = proveedor
            except Proveedor.DoesNotExist:
                return JsonResponse({"error": "Proveedor no encontrado"}, status=400)

        producto.save()

        data = {
            "id": producto.id,
            "nombre": producto.nombre,
            "categoria": producto.categoria,
            "marca": producto.marca,
            "valor_unitario": str(producto.valor_unitario),
            "unidades_stock": producto.unidades_stock,
            "descripcion": producto.descripcion,
            "proveedor": producto.proveedor.nombre,
        }
        return JsonResponse(data)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def eliminar_producto(request, producto_id):
    if request.method == "DELETE":
        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            return JsonResponse({"error": "Producto no encontrado"}, status=404)

        producto.delete()

        return JsonResponse({"mensaje": "Producto eliminado correctamente"})

    return JsonResponse({"error": "Invalid request method"}, status=405)


def listar_productos(request):
    productos = Producto.objects.all()
    productos_data = serializers.serialize("json", productos)
    return JsonResponse(productos_data, safe=False)


def detalle_producto(request, producto_id):
    if request.method == "GET":
        try:
            producto = Producto.objects.get(id=producto_id)
            producto_data = serializers.serialize("json", [producto])
            return JsonResponse(producto_data, safe=False)
        except Producto.DoesNotExist:
            return JsonResponse({"error": "Producto no encontrado"}, status=404)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)
