from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser


private_storage = FileSystemStorage(location=settings.STATICFILES_DIRS)


class GetProxyInfo(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # return Response(settings.PROXY)
        return Response('Secret!')


class FileUploadView(APIView):
    permission_classes = [AllowAny]
    
    parser_class = (FileUploadParser, )
    def put(self, request):
        file_object  = request.FILES.get('file')
        file_name = str(file_object)
        with open('./backend/static/'+file_name, 'wb+') as f:
            for chunk in file_object.chunks():
                f.write(chunk)

        return Response(status=204)