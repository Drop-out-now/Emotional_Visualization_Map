from rest_framework.views import APIView
from rest_framework.response import Response
import json
from ..views import make_lola,array_lola

class ExampleAPI(APIView):
    def get(self, request):
      data = make_lola(array_lola)
      json_data = json.dumps(data,ensure_ascii=False)
      return Response(json_data)