from rest_framework.viewsets import ModelViewSet
from core.models import Livros
from core.serealizers import LivrosSerializer, LivrosDatailSerializer

class LivrosViewSet(ModelViewSet):
    queryset = Livros.objects.all()
    def get_serializer_class(self):
        if self.action == "List" or self.action == "Retrieve":
            return LivrosDatailSerializer
        return LivrosSerializer
        