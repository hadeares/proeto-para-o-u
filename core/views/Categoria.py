from rest_framework.viewsets import ModelViewSet
from core.models import Categoria
from core.serealizers import CategoriaSerializer

class CategoriasViewSet(ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class  = CategoriaSerializer