from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class TeamDocument(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user = request.user
