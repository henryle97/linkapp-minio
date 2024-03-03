# a view allow user upload a file and return a link to download the file, use django rest framework
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import (FileUploadParser, FormParser,
                                    MultiPartParser)
from rest_framework.response import Response
from rest_framework.views import APIView

from .minio import MinioHandler
from .serializers import FileUploadSerializer


class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FileUploadSerializer

    @swagger_auto_schema(
        operation_description="Upload file", request_body=FileUploadSerializer
    )
    def post(self, request, *args, **kwargs):
        file_serializer = FileUploadSerializer(data=request.data)
        # upload to miniostorage
        minio_handler = MinioHandler.get_instance()
        minio_file_info = minio_handler.put_object(
            file_data=request.data["file"],
            file_name=request.data["file"].name,
            content_type=request.data["file"].content_type,
        )
        print(minio_file_info)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
