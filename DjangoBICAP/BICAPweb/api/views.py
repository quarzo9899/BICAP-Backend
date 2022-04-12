from django.shortcuts import get_object_or_404
from rest_framework import generics

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from BICAPweb.models import *
from .serializers import *
from BICAPweb.api.permissions import IsMobileOrStaffUser, IsStaffUser

########################################################################
#########################      ADMIN ONLY      #########################
########################################################################
class IndagineListCreateAPIView(generics.ListCreateAPIView):
    """
    API che restituisce tutte le indagini che sono state create
    """
    queryset = Indagine.objects.all().order_by("id")
    serializer_class = IndagineSerializer
    permission_classes = [IsStaffUser]


class DistribuzioneListCreateAPIView(generics.ListCreateAPIView):
    """
    API che restituisce tutte le distribuzioni che sono state create
    """
    queryset = Distribuzione.objects.all().order_by("id")
    serializer_class = DistribuzioneSerializer
    permission_classes = [IsStaffUser]


########################################################################
#########################       APP-USER       #########################
########################################################################
class IndagineBodyAPIView(generics.RetrieveAPIView):
    queryset = Indagine.objects.all()
    serializer_class = IndagineBodySerializer
    permission_classes = [IsMobileOrStaffUser]

class IndagineHeadListAPIView(APIView):
    """ 
    API che accetta come parametro la mail e restituisce una lista di indagineHead 
    """
    permission_classes = [IsMobileOrStaffUser]

    def getIndaginiFromDistribuzioni(self, distribuzioni):
        """ 
        Metodo che data una lista di distrubizioni crea una lista di indagini 
        """
        indagineList = []
        for distribuzione in distribuzioni:
            indagineList.append(distribuzione.indagine)
        return indagineList

    def SetFullUrl(self, request, response):
        for indagine in response['indagine']:
            indagine['imgUrl'] = ''.join([request.build_absolute_uri('/')[:-1].strip("/"), indagine['imgUrl']])
        return response

    def get(self, request):
        email = self.request.query_params.get('email')   
        utente = get_object_or_404(Utente, email=email)
        distribuzioni = Distribuzione.objects.all().filter(utente=utente, terminata=False)
        serializer = IndagineHeadSerializer(self.getIndaginiFromDistribuzioni(distribuzioni), many=True)
        response = { 'indagine' : serializer.data }     
        return Response(self.SetFullUrl(request, response))


class DistribuzioneMinimalDetailAPIView(APIView):
    """ 
    API che accetta come parametro la mail e id dell'indagine e restituisce una distribuzione 
    """
    permission_classes = [IsMobileOrStaffUser]

    def get_object(self):
        email = self.request.query_params.get('email')   
        idIndagine = self.request.query_params.get('idIndagine')  
        utente = get_object_or_404(Utente, email=email)
        distribuzione = get_object_or_404(Distribuzione, utente=utente, indagine=idIndagine)
        return distribuzione

    def get(self, request):
        distribuzione = self.get_object()
        serializer = DistribuzioneMinimalSerializer(distribuzione)
        return Response(serializer.data)

    def put(self, request):
        distribuzione = self.get_object()
        serializer = DistribuzioneMinimalSerializer(distribuzione, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)