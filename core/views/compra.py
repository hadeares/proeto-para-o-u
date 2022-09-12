from rest_framework.viewsets import ModelViewSet
from core.models import Compra
from core.serealizers import CompraSerializer, CriarEditarCompraSerializer


class CompraViewSet(ModelViewSet):
    queryset = Compra.objects.all()
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrive':
            return CompraSerializer
        return CriarEditarCompraSerializer


    def get_serializer_class(self):
        usuario = self.request.user
        if usuario.groups.filter(name="Administradores"):
            return Compra.objects.all()
        return Compra.objects.filter(usuario=usuario)
