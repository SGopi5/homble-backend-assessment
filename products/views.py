from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED, 
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from .models import *
from .serializers import ProductListSerializer, SkuSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def products_list(request):
    """
    List of all products.
    """
    """
    This code checks is  refrigerated or not and get saved.
    """
    refrigerated_param = request.query_params.get('refrigerated')
    if refrigerated_param is not None:
        refrigerated = bool(int(refrigerated_param))  
        products = Product.objects.filter(is_refrigerated=refrigerated)
    else:
        products = Product.objects.all()

    serializer = ProductListSerializer(products, many=True)
    return Response({"products": serializer.data}, status=HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def create_sku(request):
    """
    Create an SKU with default status.
    """
    if request.method == "POST":
        serializer = SkuSerializer(data=request.data)
        if serializer.is_valid():
            # Customize the logic to set default values for the SKU, like status
            serializer.save(status=Sku.DEFAULT_STATUS)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Method not allowed"}, status=HTTP_404_NOT_FOUND)
    

@api_view(["PUT"])
@permission_classes([IsAdminUser])
def update_sku_status(request, sku_id):
    """
    Update the status of an SKU (admin-only view).
    """
    try:
        sku = Sku.objects.get(id=sku_id)
        serializer = SkuSerializer(instance=sku, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    except Sku.DoesNotExist:
        return Response({'message': 'SKU not found'}, status=HTTP_404_NOT_FOUND)