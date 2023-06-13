from django.contrib import admin
from django.urls import path, include
from tasks import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    # registro y autenticacion
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/login/", views.login, name="login"),
    path("api/registro/", views.registro, name="registro"),
    # Url´s crud clientes
    path("api/clientes/", views.obtener_clientes, name="obtener_clientes"),
    path("api/clientes/crear/", views.crear_cliente, name="crear_cliente"),
    path(
        "api/clientes_actualizar/<int:documento>/",
        views.actualizar_cliente,
        name="actualizar_cliente",
    ),
    path(
        "api/clientes/<int:documento>/eliminar/",
        views.eliminar_cliente,
        name="eliminar_cliente",
    ),
    # consultar cliente en especifico
    path(
        "api/cliente/<int:documento>/",
        views.cliente_detalle_view,
        name="cliente_detalle",
    ),
    # Url´s crud producto
    path("api/crear_producto/", views.crear_producto, name="crear_producto"),
    path(
        "api/productos/<int:producto_id>/",
        views.actualizar_producto,
        name="actualizar_producto",
    ),
    path(
        "api/productos/<int:producto_id>/eliminar/",
        views.eliminar_producto,
        name="eliminar_producto",
    ),
    path("api/productos/", views.listar_productos, name="listar_productos"),
    path(
        "api/detalle_producto/<int:producto_id>/",
        views.detalle_producto,
        name="detalle_producto",
    ),
    # Url´s listar usuario con rol
    path("api/usuarios/", views.usuarios_view, name="usuarios"),
    path(
        "usuarios_eliminar/<int:usuario_id>/",
        views.eliminar_usuario,
        name="eliminar_usuario",
    ),
]
