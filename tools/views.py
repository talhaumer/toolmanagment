from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from api.permissions import IsOauthAuthenticated
from tools.models import Tools, UserTools, GetBackSignature
from tools.serializers import ToolSerializer, ToolAllocation, GetBackSerializers
from user.models import User
from rest_framework.filters import OrderingFilter, SearchFilter


class ToolsView(APIView):
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['name', 'model']
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOauthAuthenticated,)

    def get(self, request, pk=None):
        try:
            if pk:
                tool = Tools.objects.get(id=pk)
                serializer = ToolSerializer(tool)
                return Response(serializer.data, status=status.HTTP_200_OK)
            tools = Tools.objects.all()
            serializer = ToolSerializer(tools, many=True)
            res = {"data": serializer.data,
                   "count": tools.count()}
            return Response(res, status=status.HTTP_200_OK)
        except Tools.DoesNotExist:
            return Response({'message': "This Tool is not in system"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            serializer = ToolSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            res = {'message': "product is created successfully"}
            return Response(res, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ToolsAllocationView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOauthAuthenticated,)

    def get(self, request):
        try:
            tools = Tools.objects.filter(allocated_tools__user_account__id=request.user.id)
            serializer = ToolSerializer(tools, many=True)
            res = {"data": serializer.data,
                   "count": tools.count()}
            return Response(res, status=status.HTTP_200_OK)
        except Tools.DoesNotExist:
            return Response({'message': "This Tool is not in system"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            serializer = ToolAllocation(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            validated_data = serializer.validated_data
            validated_data["allocated"] = True
            validated_data["user_account"] = User.objects.get(id=request.user.id)
            validated_data["tool"] = Tools.objects.get(id=request.data.pop("tool_id"))
            serializer.save(**validated_data)
            res = {'message': "Tool is allocated successfully"}
            return Response(res, status=status.HTTP_201_CREATED)
        except Tools.DoesNotExist:
            return Response({'message': "This Tool is not in system"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': "User is not in system"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AvailableToolsView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOauthAuthenticated,)

    def get(self, request):
        try:
            tools = Tools.objects.all().exclude(allocated_tools__allocated=True)
            serializer = ToolSerializer(tools, many=True)
            res = {"data": serializer.data,
                   "count": tools.count()}
            return Response(res, status=status.HTTP_200_OK)
        except Tools.DoesNotExist:
            return Response({'message': "This Tool is not in system"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ToolListingView(GenericAPIView):
    queryset = Tools.objects.all()
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    listing_fields = ['tool', 'name', 'model', 'manufacturer', 'date_of_purchase',
                      'cost', 'cost_depreciation_percentage_per_year', 'initial_location',
                      'calibrated_date', 'next_calibration_due_date'
                      ]
    search_fields = ordering_fields = filterset_fields = listing_fields

    def get(self, request):
        allocated = request.query_params.get('allocated_tools__allocated')
        limit = int(request.query_params.get("limit", 10))
        offset = int(request.query_params.get("offset", 0))
        query = self.filter_queryset(Tools.objects.all())
        if allocated:
            if allocated == 'False':
                query = query.exclude(allocated_tools__allocated=True)
            else:
                query = query.filter(allocated_tools__allocated=True)
        serializer = ToolSerializer(query[offset: offset + limit], many=True)

        res = {"data": serializer.data,
               "count": len(serializer.data),
               "total count": query.count()}
        return Response(res, status=status.HTTP_200_OK)


class ToolsGetBackView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOauthAuthenticated,)

    def post(self, request):
        try:
            serializer = GetBackSerializers(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            validated_data = serializer.validated_data
            tool = UserTools.objects.get(tool__id=validated_data['tool_id'])
            validated_data["user_signature_back"] = tool
            serializer.save(**validated_data)
            tool.allocated = False
            tool.save()
            res = {'message': "Tool is allocated successfully"}
            return Response(res, status=status.HTTP_201_CREATED)
        except GetBackSignature.DoesNotExist:
            return Response({'message': "This Tool is not in system"}, status=status.HTTP_400_BAD_REQUEST)
        except UserTools.DoesNotExist:
            return Response({'message': "This allocation is not in system"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
