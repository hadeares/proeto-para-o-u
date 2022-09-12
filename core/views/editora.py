from rest_framework.viewsets import ModelViewSet
from core.models import Editora
from core.serealizers import EditoraSerializer

class EditoraViewSet(ModelViewSet):
    queryset = Editora.objects.all()
    serializer_class = EditoraSerializer
