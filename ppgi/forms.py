from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from ppgi import models
from ppgi.models import Disciplina
from django.contrib.localflavor.generic.forms import DateField
from django.db.models.fields import TextField
from django.forms.fields import FileField
from django.forms.models import ModelForm

class AreaDisciplinasFormBackup(forms.ModelForm):
    discform = forms.ModelMultipleChoiceField(
        queryset=models.Disciplina.objects.all(), required=False,
        widget=FilteredSelectMultiple(('Disciplinas'), False, attrs={'rows':'10'}), label='Disciplinas')

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            initial = kwargs.setdefault('initial', {})
            initial['discform'] = [t.disciplina.pk for t in kwargs['instance'].area_disciplinas_set.all()]

        forms.ModelForm.__init__(self, *args, **kwargs)

    def save(self, commit=True):
        instance = forms.ModelForm.save(self, commit)

        old_save_m2m = self.save_m2m
        def save_m2m():
            old_save_m2m()

            disciplinas = [s for s in self.cleaned_data['discform']]
            for disc in instance.area_disciplinas_set.all():
                if disc.pk not in disciplinas:
                    disc.delete()
                else:
                    disciplinas.remove(disc.pk)

            #for disc in disciplinas:
            #    Area_Disciplinas.objects.create(area=instance, disciplina=disc)
        
        #self.save_m2m = save_m2m

        #return instance
        return 0

    class Meta:
        model = models.Disciplina
        
class AreaDisciplinasForm(forms.ModelForm):
    discform = forms.ModelMultipleChoiceField(
        queryset=models.Disciplina.objects.all(), required=False,
        widget=FilteredSelectMultiple(('Disciplinas'), False, attrs={'rows':'10'}), label='Disciplinas')
    
    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            initial = kwargs.setdefault('initial', {})
            initial['discform'] = [t.pk for t in Disciplina.objects.filter(area_id=kwargs['instance'].pk)]

        forms.ModelForm.__init__(self, *args, **kwargs)

    def save(self, commit=True):
        instance = forms.ModelForm.save(self, commit)
        
        disciplinas = [s for s in self.cleaned_data['discform']]
        for disc in Disciplina.objects.filter(area_id=instance.pk):
            if disc.pk not in disciplinas:
                disc.area = None
                disc.save()
            else:
                disciplinas.remove(disc.pk)

        for disc in disciplinas:
            d = Disciplina.objects.get(id=disc.pk)
            d.area = instance
            d.save()

        return instance
    
    class Meta:
        model = models.Disciplina
        
class AlocarBolsaForm(forms.ModelForm):
    datainicio = DateField
    datafim     = DateField
    nome        = TextField

class uploadDadosPpgiForm(forms.Form):
    uploadAlunos = FileField(label="Dados de Alunos")
    uploadDisciplinas = FileField(label="Dados de Disciplinas")
    uploadDisciplinasCursadas = FileField(label="Dados de Disciplinas Cursadas")
