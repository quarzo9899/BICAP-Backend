from django.db import models
from django.contrib.auth.models import User

class Gruppo(models.Model):
    nome = models.CharField(max_length=20)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Gruppo"
        verbose_name_plural = "Gruppi"

class Utente(models.Model):
    email = models.EmailField()
    gruppi = models.ManyToManyField(Gruppo, related_name='gruppi')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Utente"
        verbose_name_plural = "Utenti"

class Indagine(models.Model):
    titoloIndagine = models.CharField(max_length=20)
    erogatore = models.CharField(max_length=20)
    creato_da = models.ForeignKey(User, on_delete=models.CASCADE)
    imgUrl = models.ImageField()
    tematica = models.TextField()
    gruppi = models.ManyToManyField(Gruppo, related_name='gruppi_interessati')
    ultimaModifica = models.TimeField(auto_now=True)

    def __str__(self):
        return self.titoloIndagine

    class Meta:
        verbose_name = "Indagine"
        verbose_name_plural = "Indagini"


class Distribuzione(models.Model):
    utente = models.ForeignKey(Utente, on_delete=models.CASCADE, related_name="indagini")
    indagine = models.ForeignKey(Indagine, on_delete=models.CASCADE, related_name="utenti")
    terminata = models.BooleanField()

    def __str__(self):
        return "Utente: " + self.utente.__str__() + " Indagine: " + self.indagine.__str__()

    class Meta:
        verbose_name = "Distribuzione"
        verbose_name_plural = "Distribuzioni"


class Questionario(models.Model):
    titolo = models.CharField(max_length=20)
    qualtricsUrl = models.CharField(max_length=250)
    indagine = models.ForeignKey(Indagine, on_delete=models.CASCADE, related_name="questionari")

    def __str__(self):
        return self.titolo

    class Meta:
        ordering = ['pk']
        verbose_name = "Questionario"
        verbose_name_plural = "Questionari"


# Classe padre informazione, viene ereditata per distinguere le informazioni dei questionari da quelle
# dell'indagine stessa
class Informazione(models.Model):
    nomeFile = models.CharField(max_length=20)
    fileUrl = models.FileField()
    thumbnailUrl = models.FileField()
    tipoFile = models.CharField(max_length=200)
    ultimaModifica = models.TimeField(auto_now=True)
    __original_fileUrl = None

    def __str__(self):
        return self.nomeFile

    def __init__(self, *args, **kwargs):
        super(Informazione, self).__init__(*args, **kwargs)
        self.__original_fileUrl = self.fileUrl

    """
    Overraide del metodo save, che permette di controllare se l'informazione
    è stata aggiornata con un nuovo file e in quel caso il tipoFile e la 
    thumbnailUrl verranno settati a null per essere poi generati.
    Questa operazione di generazione avverrà grazie al signal post_save.
    """
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.fileUrl != self.__original_fileUrl:
            self.tipoFile = ''
            self.thumbnailUrl = ''
            self.__original_fileUrl = self.fileUrl
        super(Informazione, self).save(force_insert, force_update, *args, **kwargs)

    class Meta:
        ordering = ['pk']

class InformazioneQuestionario(Informazione):
    questionario = models.ForeignKey(Questionario, on_delete=models.CASCADE, related_name="informazioni")

    class Meta:
        verbose_name = "Informazione Questionario"
        verbose_name_plural = "Informazioni Questionari"

class InformazioneIndagine(Informazione):
    questionario = models.ForeignKey(Indagine, on_delete=models.CASCADE, related_name="informazioni")

    class Meta:
        verbose_name = "Informazione Indagine"
        verbose_name_plural = "Informazioni Indagini"