import os
import mimetypes

from django.db.models.signals import m2m_changed, post_save, post_delete, pre_save
from django.dispatch import receiver
from django.conf import settings
from preview_generator.manager import PreviewManager
from BICAPweb.models import *


""" 
Metodo usato per gestire(creare e/o eliminare) i record della tabella 
Distribuzione che è la tabella che collega un utente ad un indagine.
"""
@receiver(m2m_changed, sender=Indagine.gruppi.through)
def CreateDistribuzione(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == 'post_add' or action == 'post_remove':
        senderObjects = instance.gruppi.all()
        indagine = instance
        utenti = []
        for gruppo in senderObjects:
            idGruppo = gruppo.id
            utenti += Utente.objects.all().filter(gruppi=idGruppo)
        if action == 'post_add':
            for utente in utenti:
            # Controllo che il record utente-indagine non sia già presente 
                if len(Distribuzione.objects.filter(utente=utente, indagine=indagine)) == 0:
                    Distribuzione.objects.get_or_create(utente=utente, indagine=indagine, terminata=False)
        if action == 'post_remove':
            distribuzioni = Distribuzione.objects.filter(indagine=instance)
            for utente in utenti:
                distribuzioni = distribuzioni.exclude(utente=utente)
            distribuzioni.delete()


""" 
Meotodo richiamato dopo il salvataggio di una modifica o della creazione di un
InformazioneIndagine.
Questo metodo si occupa di ottenere e salvare il mime type e di creare una 
thumbnail.
"""        
@receiver(post_save, sender=InformazioneIndagine)
def post_save_InformazioneIndagine(sender, instance, **kwargs):
    post_save_informazione_helper(sender, instance)


""" 
Meotodo richiamato dopo il salvataggio di una modifica o della creazione di un
InformazioneQuestionario.
Questo metodo si occupa di ottenere e salvare il mime type e di creare una 
thumbnail se necessario.
""" 
@receiver(post_save, sender=InformazioneQuestionario)
def post_save_InformazioneQuestionario(sender, instance, **kwargs):
    post_save_informazione_helper(sender, instance)


"""
Metodo richiamato da post_save_InformazioneQuestionario e 
post_save_InformazioneIndagine che si occupa di ottenere e salvare il mime type
e di creare una thumbnail se necessario.
"""
def post_save_informazione_helper(sender, instance): 
    if instance.thumbnailUrl.name == '' or instance.tipoFile == '':
        if instance.tipoFile == '':
            tipoFile = get_tipoFile(sender, instance)
        if instance.thumbnailUrl.name == '':
            thumbnailUrl = create_thumb(sender, instance)      
        sender.objects.filter(pk=instance.pk).update(tipoFile=tipoFile, thumbnailUrl=thumbnailUrl)


"""
Metodo che ricava il tipo di mime dal nome del file caricato
"""
def get_tipoFile(sender, instance):
    instance.tipoFile = mimetypes.guess_type(instance.fileUrl.name)[0]
    return instance.tipoFile


"""
Metodo che crea una thumbnail a partire da un file
"""
def create_thumb(sender, instance):
    #Se il file è un audio gli assegno una thumbnail prefatta
    if 'audio' in instance.tipoFile:
        return '/thumb/audio.png'
    else:
        filepath = instance.fileUrl.file.name
        cache_path = settings.MEDIA_ROOT + '/thumb'
        manager = PreviewManager(cache_path, create_folder=True)
        FullPathToimage = manager.get_jpeg_preview(filepath)
        return '/thumb/' + os.path.basename(FullPathToimage)