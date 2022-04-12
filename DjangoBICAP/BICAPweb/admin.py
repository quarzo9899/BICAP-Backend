from django.contrib import admin
from .models import *
from nested_admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline, NestedInlineModelAdmin

class AppartenenzaInline(admin.TabularInline):
    model = Utente.gruppi.through
    extra = 0


class GruppoAdmin(admin.ModelAdmin):
    inlines = [AppartenenzaInline]


class InformazioneQuestionarioInline(NestedTabularInline):
    model = InformazioneQuestionario
    extra = 0
    exclude = ('thumbnailUrl', 'tipoFile', 'ultimaModifica')


class InformazioneIndagineInline(NestedTabularInline):
    model = InformazioneIndagine
    extra = 0
    exclude = ('thumbnailUrl', 'tipoFile', 'ultimaModifica')
    

class QuestionarioInline(NestedStackedInline):
    model = Questionario
    extra = 0
    inlines = [InformazioneQuestionarioInline]


"""
Classe che ci permette di nascondere i campi creato_da e ultimaModifica e anche
di visualizzare solo le proprie indagini se l'utente non è admin
"""
class IndagineAdmin(NestedModelAdmin):
    inlines = [InformazioneIndagineInline, QuestionarioInline]
    exclude = ('creato_da', 'ultimaModifica')

    def save_model(self, request, obj, form, change):
        obj.creato_da = request.user
        super(IndagineAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(IndagineAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(creato_da=request.user)


"""
Classe che ci permette di nascondere il campo gruppi riferito alla modello 
utenti
"""
class UtenteAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False
    exclude = ('gruppi',)


"""
Classe che ci permette di nascondere i modelli nella homepage admin se non si è
un membro dello staff usata con Questionario, InformazioneIndagine e 
InformazioneQuestionario.
"""
class HideModelIndexAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.is_superuser


"""
Classe che ci permette la crezione/modifica di un utente con la possibilità di 
assegnargli un gruppo
"""
class UtenteConGruppo(Utente):
    class Meta:
        verbose_name = "Utente"
        verbose_name_plural = "Utenti"
        proxy = True


admin.site.register(Gruppo, GruppoAdmin)
admin.site.register(Utente, UtenteAdmin)
admin.site.register(UtenteConGruppo)
admin.site.register(Distribuzione)
admin.site.register(Indagine, IndagineAdmin)
admin.site.register(Questionario, HideModelIndexAdmin)
admin.site.register(InformazioneIndagine, HideModelIndexAdmin)
admin.site.register(InformazioneQuestionario, HideModelIndexAdmin)