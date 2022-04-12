from rest_framework import serializers
from BICAPweb.models import *

########################################################################
#########################       GENERIC        #########################
########################################################################
class InformazioneQuestionarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = InformazioneQuestionario
        fields = "__all__"


class QuestionarioSerializer(serializers.ModelSerializer):
    informazioni  = InformazioneQuestionarioSerializer(many=True, read_only=True)

    class Meta:
        model = Questionario
        fields = "__all__"


class InformazioneIndagineSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformazioneIndagine
        fields = "__all__"


class IndagineSerializer(serializers.ModelSerializer):
    informazioni  = InformazioneIndagineSerializer(many=True, read_only=True)
    questionari = QuestionarioSerializer(many=True, read_only=True)
    #SlugRelatedField serve per ottenere il nome dell'utente invece del suo id
    creato_da = serializers.SlugRelatedField(
        slug_field='username', 
        read_only=True)
    #SlugRelatedField serve per ottenere il nome dell'gruppo invece del suo id
    gruppi = serializers.SlugRelatedField(
        many=True, 
        read_only=True, 
        slug_field='nome')

    class Meta:
        model = Indagine
        fields = "__all__"


class UtenteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Utente
        fields = "__all__"


class DistribuzioneSerializer(serializers.ModelSerializer):
    indagine = IndagineSerializer(read_only=True)
    utente = UtenteSerializer(read_only=True)

    class Meta:
        model = Distribuzione
        fields = "__all__"


########################################################################
#########################       APP-USER       #########################
########################################################################

class IndagineBodySerializer(IndagineSerializer):

    class Meta:
        model = Indagine
        fields  = ('informazioni', 'questionari', 'tematica')


class IndagineHeadSerializer(IndagineSerializer):

    class Meta:
        model = Indagine
        fields  = ('id', 'titoloIndagine','erogatore', 'imgUrl', 'ultimaModifica')


class DistribuzioneMinimalSerializer(DistribuzioneSerializer):

    class Meta:
        model = Distribuzione
        fields = ('terminata', )