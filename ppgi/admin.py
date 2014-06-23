# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from ppgi.models import Aluno, SituacaoMatricula, Disciplina, Area, Professor, Bolsa, OrgaoFomento,\
    AlunoMestradoIrregular, AlunoMestradoPrazoMax, AlunoMestradoEsperaBolsa, BolsistaMestrado,\
    AlunoDoutoradoPrazoMax, BolsistaDoutorado, AlunoDoutoradoIrregular,\
    AlunoDoutoradoEsperaBolsa
from ppgi.forms import AreaDisciplinasForm
from django.contrib.admin.filters import SimpleListFilter
from django.utils.translation import ugettext_lazy as _
from django.utils.datetime_safe import datetime
from ppgi.util import htmlIconTrue, htmlIconFalse

#admin.site.disable_action('delete_selected')

class AreaAdmin(ModelAdmin):
    form = AreaDisciplinasForm
    
class AlunoReprovacaoFiltro(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Reprovação')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'alunoreprovacao'

    def lookups(self, request, model_admin):

        return (
            ('1', _('Uma Reprovação')),
            ('2+', _('Duas ou mais Reprovações')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """

        if self.value() == '1':
            return queryset.filter(id__in=[a.pk for a in Aluno.objects.comReprovacao('1')])
        if self.value() == '2+':
            return queryset.filter(id__in=[a.pk for a in Aluno.objects.comReprovacao('2+')])

class AlunoMestradoIrregularFiltro(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Regulamento')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'reg'

    def lookups(self, request, model_admin):

        return (
            ('cra', _('CRA')),
            ('con', _('Conceito')),
            ('abn', _('Abandono')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """

        if self.value() == 'cra':
            listaIdsIrregCra       = [a.pk for a in Aluno.objects.regulamentoMestradoCra()]
            return queryset.filter(id__in=listaIdsIrregCra)
        if self.value() == 'con':
            listaIdsIrregConceito  = [a.pk for a in Aluno.objects.regulamentoMestradoConceito()]
            return queryset.filter(id__in=listaIdsIrregConceito)
        if self.value() == 'abn':
            listaIdsIrregAbandono  = [a.pk for a in Aluno.objects.filter(situacaomatricula_id=SituacaoMatricula.objects.get(codigo='C03'))]
            return queryset.filter(id__in=listaIdsIrregAbandono)
        
class AlunoDoutoradoIrregularFiltro(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Regulamento')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'reg'

    def lookups(self, request, model_admin):

        return (
            ('cra', _('CRA')),
            ('con', _('Conceito')),
            ('abn', _('Abandono')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """

        if self.value() == 'cra':
            listaIdsIrregCra       = [a.pk for a in Aluno.objects.regulamentoDoutoradoCra()]
            return queryset.filter(id__in=listaIdsIrregCra)
        if self.value() == 'con':
            listaIdsIrregConceito  = [a.pk for a in Aluno.objects.regulamentoDoutoradoConceito()]
            return queryset.filter(id__in=listaIdsIrregConceito)
        if self.value() == 'abn':
            listaIdsIrregAbandono  = [a.pk for a in Aluno.objects.filter(situacaomatricula_id=SituacaoMatricula.objects.get(codigo='C03'))]
            return queryset.filter(id__in=listaIdsIrregAbandono)
        
class AlunoFiltroRecente(SimpleListFilter):
    title = ('Alunos Recentes')
    
    parameter_name = 'tempo'
    
    def lookups(self, request, model_admin):
        return (
                ('4', 'Últimos 4 anos'),
                )
        
    def queryset(self, request, queryset):
        anoAtual = datetime.now().year
        if self.value() == '4':
            return queryset.filter(anoingresso__gte=(anoAtual-4))

class AlunoOuvinteFiltro(SimpleListFilter):
    title = ('Alunos Ouvintes')
    
    parameter_name = 'ouvinte'
    
    def lookups(self, request, model_admin):
        return (
                ('T', 'Ouvintes'),
                )
        
    def queryset(self, request, queryset):
        if self.value() == 'T':
            return queryset.filter(ouvinte=True)
            

class DisciplinaCreditoFiltro(SimpleListFilter):
    title = _('Crédito')
    parameter_name = 'cred'
    
    def lookups(self, request, model_admin):
        return (
                ('0', _('Zero')),
                )
    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(creditos='0')

class DisciplinaNucleoBasicoFiltro(SimpleListFilter):
    title = _('Núcleo Básico')
    parameter_name = 'nb'
    
    def lookups(self, request, model_admin):
        return (
                ('0', _('Núcleo Básico')),
                )
    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(nucleobasico=True)
        
class AlunoMestradoPrazoMaxRegulamentoFiltro(SimpleListFilter):
    title = 'Regulamento'
    parameter_name='reg'
    
    def lookups(self, request, model_admin):
        return (
                ('cra', 'CRA'),
                ('ch', 'Carga horária'),
                ('prof', 'Proficiência'),
                ('art', 'Artigo'),
                ('qual', 'Qualificação')
                )
    
    def queryset(self, request, queryset):
        if self.value() == 'ch':
            return queryset.filter(id__in=[a.pk for a in Aluno.objects.regulamentoMestradoCargaHr()])
        if self.value() == 'cra':
            return queryset.filter(id__in=[a.pk for a in Aluno.objects.regulamentoMestradoCraPrazoMax()])
        if self.value() == 'prof':
            return queryset.exclude(proficiencia=True)
        if self.value() == 'art':
            return queryset.exclude(artigo=True)
        if self.value() == 'qual':
            return queryset.exclude(qualificacao=True)
        
class AlunoDoutoradoPrazoMaxRegulamentoFiltro(SimpleListFilter):
    title = 'Regulamento'
    parameter_name='reg'
    
    def lookups(self, request, model_admin):
        return (
                ('cra', 'CRA'),
                ('ch', 'Carga horária'),
                ('prof', 'Proficiência'),
                ('art', 'Artigo'),
                ('qual', 'Qualificação')
                )
    
    def queryset(self, request, queryset):
        if self.value() == 'ch':
            return queryset.filter(id__in=[a.pk for a in Aluno.objects.regulamentoDoutoradoCargaHr()])
        if self.value() == 'cra':
            return queryset.filter(id__in=[a.pk for a in Aluno.objects.regulamentoDoutoradoCraPrazoMax()])
        if self.value() == 'prof':
            return queryset.exclude(proficiencia=True)
        if self.value() == 'art':
            return queryset.exclude(artigo=True)
        if self.value() == 'qual':
            return queryset.exclude(qualificacao=True)
        
class BolsistaMestradoRegulamentoFiltro(SimpleListFilter):
    title = 'Regulamento'
    parameter_name = 'reg'
    
    def lookups(self, request, model_admin):
        return (('cra' , 'CRA'),
                ('ch', 'Carga Horária'),
                ('con', 'Conceito')
                )
        
    def queryset(self, request, queryset):
        if self.value() == 'cra':
            listaIdsIrregCra = [a.pk for a in Aluno.objects.regulamentoMestradoCraBolsa()]
            return queryset.filter(id__in=listaIdsIrregCra)
        if self.value() == 'ch':
            listaIdsIrregCargaHr = [a.pk for a in Aluno.objects.regulamentoMestradoCargaHrBolsa()]
            return queryset.filter(id__in=listaIdsIrregCargaHr)
        if self.value() == 'con':
            listaIdsIrregConceito = [a.pk for a in Aluno.objects.regulamentoMestradoConceitoBolsa()]
            return queryset.filter(id__in=listaIdsIrregConceito)
        
class BolsistaDoutoradoRegulamentoFiltro(SimpleListFilter):
    title = 'Regulamento'
    parameter_name = 'reg'
    
    def lookups(self, request, model_admin):
        return (('cra' , 'CRA'),
                ('ch', 'Carga Horária'),
                ('con', 'Conceito')
                )
        
    def queryset(self, request, queryset):
        if self.value() == 'cra':
            listaIdsIrregCra = [a.pk for a in Aluno.objects.regulamentoDoutoradoCraBolsa()]
            return queryset.filter(id__in=listaIdsIrregCra)
        if self.value() == 'ch':
            listaIdsIrregCargaHr = [a.pk for a in Aluno.objects.regulamentoDoutoradoCargaHrBolsa()]
            return queryset.filter(id__in=listaIdsIrregCargaHr)
        if self.value() == 'con':
            listaIdsIrregConceito = [a.pk for a in Aluno.objects.regulamentoDoutoradoConceitoBolsa()]
            return queryset.filter(id__in=listaIdsIrregConceito)
    
class AlunoAdmin(ModelAdmin):
    list_filter  = [AlunoFiltroRecente, AlunoReprovacaoFiltro, AlunoOuvinteFiltro]
    list_display = ('drevisualizar', 'visualizar', 'cursonivel', 'anoingresso', 'situacaomatricula', 'modificar')
    search_fields = ['dre', 'nome', 'anoingresso', 'situacaomatricula__situacao']
    ordering = ('nome',)
    list_max_show_all = 1000
    
    def modificar(self, obj):
        return "<a class='changelink' href='%d'>Modificar</a> <a class='deletelink' href='%d/delete'>Apagar</a>" %(obj.id, obj.id)
    modificar.allow_tags = True
    modificar.short_description = 'Opcoes'
    
    def visualizar(self, obj):
        return "<a href='visualizar/?id=%d'>%s</a>" %(obj.id, obj.nome)
    visualizar.allow_tags = True
    visualizar.short_description = 'Nome'
    visualizar.admin_order_field = 'nome'
    
    def drevisualizar(self, obj):
        return "<a href='visualizar/?id=%d'>%s</a>" %(obj.id, obj.dre)
    drevisualizar.allow_tags = True
    drevisualizar.short_description = 'DRE'
    drevisualizar.admin_order_field = 'dre'
    
class AlunoMestradoIrregularAdmin(admin.ModelAdmin):
    list_display = ('drevisualizar', 'visualizar', 'anoingresso', 'situacaomatricula', 'regulamentoMestradoCra',
                     'regulamentoMestradoConceito', 'regulamentoAbandono')
    search_fields = ['dre', 'nome', 'anoingresso', 'situacaomatricula__situacao']
    ordering = ('nome',)
    list_filter = [AlunoFiltroRecente, AlunoMestradoIrregularFiltro, AlunoOuvinteFiltro]
    list_max_show_all = 1000
    
    def queryset(self, request):
        listaIds = []
        self.listaIdsIrregCra       = [a.pk for a in Aluno.objects.regulamentoMestradoCra()]
        self.listaIdsIrregConceito  = [a.pk for a in Aluno.objects.regulamentoMestradoConceito()]
        self.listaIdsIrregAbandono  = [a.pk for a in Aluno.objects.filter(situacaomatricula_id=SituacaoMatricula.objects.get(codigo='C03'))]
        listaIds.extend(self.listaIdsIrregCra)
        listaIds.extend(self.listaIdsIrregConceito)
        listaIds.extend(self.listaIdsIrregAbandono)
        
        alunosIrregulares = Aluno.objects.filter(id__in=listaIds).filter(cursonivel='Mestrado')
        return alunosIrregulares
    
    def visualizar(self, obj):
        return "<a href='visualizar/?id=%d'>%s</a>" %(obj.id, obj.nome)
    visualizar.allow_tags = True
    visualizar.short_description = 'Nome'
    visualizar.admin_order_field = 'nome'
    
    def drevisualizar(self, obj):
        return "<a href='visualizar/?id=%d'>%s</a>" %(obj.id, obj.dre)
    drevisualizar.allow_tags = True
    drevisualizar.short_description = 'DRE'
    drevisualizar.admin_order_field = 'dre'
    
    def regulamentoMestradoCra(self, obj):
        if obj.id in self.listaIdsIrregCra:
            return htmlIconFalse()
        else:
            return htmlIconTrue()
    regulamentoMestradoCra.short_description = "CRA"
    regulamentoMestradoCra.allow_tags = True
    
    def regulamentoMestradoConceito(self, obj):
        if obj.id in self.listaIdsIrregConceito:
            return htmlIconFalse()
        else:
            return htmlIconTrue()
    regulamentoMestradoConceito.short_description = "Conceito"
    regulamentoMestradoConceito.allow_tags = True
    
    def regulamentoAbandono(self, obj):
        if obj.id in self.listaIdsIrregAbandono:
            return htmlIconFalse()
        else:
            return htmlIconTrue()
    regulamentoAbandono.short_description = "Abandono"
    regulamentoAbandono.allow_tags = True
    
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request):
        return False


class AlunoDoutoradoIrregularAdmin(admin.ModelAdmin):
    list_display = ('drevisualizar', 'visualizar', 'anoingresso', 'situacaomatricula', 'regulamentoMestradoCra',
                     'regulamentoMestradoConceito', 'regulamentoAbandono')
    search_fields = ['dre', 'nome', 'anoingresso', 'situacaomatricula__situacao']
    ordering = ('nome',)
    list_filter = [AlunoFiltroRecente, AlunoDoutoradoIrregularFiltro, AlunoOuvinteFiltro]
    list_max_show_all = 1000
    
    def queryset(self, request):
        listaIds = []
        self.listaIdsIrregCra       = [a.pk for a in Aluno.objects.regulamentoDoutoradoCra()]
        self.listaIdsIrregConceito  = [a.pk for a in Aluno.objects.regulamentoDoutoradoConceito()]
        self.listaIdsIrregAbandono  = [a.pk for a in Aluno.objects.filter(situacaomatricula_id=SituacaoMatricula.objects.get(codigo='C03'))]
        listaIds.extend(self.listaIdsIrregCra)
        listaIds.extend(self.listaIdsIrregConceito)
        listaIds.extend(self.listaIdsIrregAbandono)
        
        alunosIrregulares = Aluno.objects.filter(id__in=listaIds).filter(cursonivel='Doutorado')
        return alunosIrregulares
    
    def visualizar(self, obj):
        return "<a href='visualizar/?id=%d'>%s</a>" %(obj.id, obj.nome)
    visualizar.allow_tags = True
    visualizar.short_description = 'Nome'
    visualizar.admin_order_field = 'nome'
    
    def drevisualizar(self, obj):
        return "<a href='visualizar/?id=%d'>%s</a>" %(obj.id, obj.dre)
    drevisualizar.allow_tags = True
    drevisualizar.short_description = 'DRE'
    drevisualizar.admin_order_field = 'dre'
    
    def regulamentoMestradoCra(self, obj):
        if obj.id in self.listaIdsIrregCra:
            return htmlIconFalse()
        else:
            return htmlIconTrue()
    regulamentoMestradoCra.short_description = "CRA"
    regulamentoMestradoCra.allow_tags = True
    
    def regulamentoMestradoConceito(self, obj):
        if obj.id in self.listaIdsIrregConceito:
            return htmlIconFalse()
        else:
            return htmlIconTrue()
    regulamentoMestradoConceito.short_description = "Conceito"
    regulamentoMestradoConceito.allow_tags = True
    
    def regulamentoAbandono(self, obj):
        if obj.id in self.listaIdsIrregAbandono:
            return htmlIconFalse()
        else:
            return htmlIconTrue()
    regulamentoAbandono.short_description = "Abandono"
    regulamentoAbandono.allow_tags = True
    
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request):
        return False

class AlunoMestradoPrazoMaxAdmin(admin.ModelAdmin):
    list_display=['drevisualizar','visualizar', 'anoingresso', 'situacaomatricula', 'regulamentoCRA', 
                  'regulamentoCH', 'regulamentoCHBasico', 'regulamentoProficiencia', 'regulamentoArtigo', 'regulamentoQualificacao']
    ordering = ['nome']
    search_fields = ['dre', 'nome', 'anoingresso', 'situacaomatricula__situacao']
    list_filter = [AlunoFiltroRecente, AlunoMestradoPrazoMaxRegulamentoFiltro, AlunoOuvinteFiltro]
    list_max_show_all = 1000
    
    listaIdsIrregCH  = Aluno.objects.regulamentoMestradoCargaHr()
    listaIdsIrregCRA = Aluno.objects.regulamentoMestradoCraPrazoMax()
    listaIdsIrregCHBasico = Aluno.objects.regulamentoMestradoCargaHrBasico()
    
    def visualizar(self, obj):
        return "<a href='visualizar/?id=%s'>%s</a>" %(obj.id, obj.nome)
    visualizar.allow_tags=True
    visualizar.short_description='Nome'
    visualizar.admin_order_field='nome'
    
    def drevisualizar(self, obj):
        return "<a href='visualizar/?id=%d'>%s</a>" %(obj.id, obj.dre)
    drevisualizar.allow_tags = True
    drevisualizar.short_description = 'DRE'
    drevisualizar.admin_order_field = 'dre'
    
    def regulamentoCRA(self, obj):
        if obj in self.listaIdsIrregCRA:
            return htmlIconFalse()
        else: return htmlIconTrue()
    regulamentoCRA.allow_tags = True
    regulamentoCRA.short_description = 'CRA'
        
    def regulamentoCH(self, obj):
        if obj in self.listaIdsIrregCH:
            return htmlIconFalse()
        else: return htmlIconTrue()
    regulamentoCH.allow_tags = True
    regulamentoCH.short_description = 'Carga Horária'
    
    def regulamentoCHBasico(self, obj):
        if obj in self.listaIdsIrregCHBasico:
            return htmlIconFalse()
        else: return htmlIconTrue()
    regulamentoCHBasico.allow_tags=True
    regulamentoCHBasico.short_description = 'CH N. Básico'
    
    def regulamentoProficiencia(self, obj):
        if obj.proficiencia:
            return htmlIconTrue()
        else: return htmlIconFalse()
    regulamentoProficiencia.allow_tags = True
    regulamentoProficiencia.short_description = 'Proficiência'
    
    def regulamentoArtigo(self, obj):
        if obj.artigo:
            return htmlIconTrue()
        else: return htmlIconFalse()
    regulamentoArtigo.allow_tags = True
    regulamentoArtigo.short_description = "Artigo"
    
    def regulamentoQualificacao(self, obj):
        if obj.qualificacao:
            return htmlIconTrue()
        else: return htmlIconFalse()
    regulamentoQualificacao.allow_tags = True
    regulamentoQualificacao.short_description = "Qualificação"
    
    def has_add_permission(self, request):
        return False
    
    def queryset(self, request):
        return Aluno.objects.regulamentoMestradoPrazoMax().filter(cursonivel='Mestrado')
    

#Atualizar para implementar regulamentos referentes ao Doutorado
class AlunoDoutoradoPrazoMaxAdmin(admin.ModelAdmin):
    list_display=['drevisualizar','visualizar', 'anoingresso', 'situacaomatricula', 'regulamentoCRA', 
                  'regulamentoCH', 'regulamentoCHBasico', 'regulamentoProficiencia', 'regulamentoArtigo', 'regulamentoQualificacao']
    ordering = ['nome']
    search_fields = ['dre', 'nome', 'anoingresso', 'situacaomatricula__situacao']
    list_filter = [AlunoFiltroRecente, AlunoDoutoradoPrazoMaxRegulamentoFiltro, AlunoOuvinteFiltro]
    list_max_show_all = 1000
    
    listaIdsIrregCH  = Aluno.objects.regulamentoDoutoradoCargaHr()
    listaIdsIrregCRA = Aluno.objects.regulamentoDoutoradoCraPrazoMax()
    listaIdsIrregCHBasico = Aluno.objects.regulamentoDoutoradoCargaHrBasico()
    
    def visualizar(self, obj):
        return "<a href='visualizar/?id=%s'>%s</a>" %(obj.id, obj.nome)
    visualizar.allow_tags=True
    visualizar.short_description='Nome'
    visualizar.admin_order_field='nome'
    
    def drevisualizar(self, obj):
        return "<a href='visualizar/?id=%d'>%s</a>" %(obj.id, obj.dre)
    drevisualizar.allow_tags = True
    drevisualizar.short_description = 'DRE'
    drevisualizar.admin_order_field = 'dre'
    
    def regulamentoCRA(self, obj):
        if obj in self.listaIdsIrregCRA:
            return htmlIconFalse()
        else: return htmlIconTrue()
    regulamentoCRA.allow_tags = True
    regulamentoCRA.short_description = 'CRA'
        
    def regulamentoCH(self, obj):
        if obj in self.listaIdsIrregCH:
            return htmlIconFalse()
        else: return htmlIconTrue()
    regulamentoCH.allow_tags = True
    regulamentoCH.short_description = 'Carga Horária'
    
    def regulamentoCHBasico(self, obj):
        if obj in self.listaIdsIrregCHBasico:
            return htmlIconFalse()
        else: return htmlIconTrue()
    regulamentoCHBasico.allow_tags=True
    regulamentoCHBasico.short_description = 'CH N. Básico'
    
    def regulamentoProficiencia(self, obj):
        if obj.proficiencia:
            return htmlIconTrue()
        else: return htmlIconFalse()
    regulamentoProficiencia.allow_tags = True
    regulamentoProficiencia.short_description = 'Proficiência'
    
    def regulamentoArtigo(self, obj):
        if obj.artigo:
            return htmlIconTrue()
        else: return htmlIconFalse()
    regulamentoArtigo.allow_tags = True
    regulamentoArtigo.short_description = "Artigo"
    
    def regulamentoQualificacao(self, obj):
        if obj.qualificacao:
            return htmlIconTrue()
        else: return htmlIconFalse()
    regulamentoQualificacao.allow_tags = True
    regulamentoQualificacao.short_description = "Qualificação"
    
    def has_add_permission(self, request):
        return False
    
    def queryset(self, request):
        return Aluno.objects.regulamentoDoutoradoPrazoMax().filter(cursonivel='Doutorado')

class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nome', 'area', 'nucleobasico']
    ordering = ['nome']
    search_fields = ['nome', 'codigo']
    list_filter = [DisciplinaCreditoFiltro, DisciplinaNucleoBasicoFiltro]
    
class BolsaAdmin(admin.ModelAdmin):
    exclude = ['aluno', 'datainicio', 'datafim']
    list_display = ['orgao', 'area', 'codigo', 'alunovisualizar', 'disponibilidade']
    
    def disponibilidade(self, obj):
        if obj.aluno == None or obj.aluno == "":
            return htmlIconTrue()
        else:
            return htmlIconFalse()
    disponibilidade.allow_tags = True
    
    def alunovisualizar(self, obj):
        if obj.aluno != None:
            if obj.aluno.cursonivel == "Doutorado":
                return "<a href='../bolsistadoutorado/visualizar/?id=%s'>%s</a>" %(obj.aluno.id, obj.aluno.nome)
            else:
                return "<a href='../bolsistamestrado/visualizar/?id=%s'>%s</a>" %(obj.aluno.id, obj.aluno.nome)
        else:
            return ""
    alunovisualizar.allow_tags=True
    alunovisualizar.short_description = 'Bolsista'
    alunovisualizar.admin_order_field = 'aluno'
    
class AlunoMestradoEsperaBolsaAdmin(admin.ModelAdmin):
    list_display=['drevisualizar', 'visualizar', 'grauingresso', 'grauesperabolsa', 'alocarBolsa']
    ordering = ['-grauesperabolsa']
    list_max_show_all = 1000
    
    def drevisualizar(self, obj):
        return "<a href='visualizar/?id=%d'>%s</a>" %(obj.id, obj.dre)
    drevisualizar.allow_tags = True
    drevisualizar.short_description = 'DRE'
    drevisualizar.admin_order_field = 'dre'
    
    def visualizar(self, obj):
        return "<a href='visualizar/?id=%s'>%s</a>" %(obj.id, obj.nome)
    visualizar.allow_tags=True
    visualizar.short_description='Nome'
    visualizar.admin_order_field='nome'
    
    def alocarBolsa(self, obj):
        return "<center><a href='#%s' class='alocarBolsa addlink' id=''> Alocar <input type='hidden' id='%s' name='aluno%s' value='%s'></a> </center>" %(obj.id, obj.id, obj.id, obj.nome)
    alocarBolsa.allow_tags=True
    alocarBolsa.short_description='Alocar Bolsa'
    
    
    def changelist_view(self, request, extra_context=None):
        dicAlunos = dict()
        
        for a in Aluno.objects.all():
            dicAlunos[a.id] = a
        
        dicDados = {
                 'bolsas':Bolsa.objects.filter(aluno_id__isnull=True),
                 'dicAlunos':dicAlunos
                 }
        return admin.ModelAdmin.changelist_view(self, request, extra_context=dicDados)
    
    def queryset(self, request):
        return Aluno.objects.exclude(id__in=[b.aluno.pk for b in Bolsa.objects.filter(aluno_id__isnull=False)]).filter(cursonivel='Mestrado', permissaobolsa=True) 
    
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class AlunoDoutoradoEsperaBolsaAdmin(admin.ModelAdmin):
    list_display=['drevisualizar', 'visualizar', 'grauingresso', 'grauesperabolsa', 'alocarBolsa']
    ordering = ['-grauesperabolsa']
    list_max_show_all = 1000
    
    def drevisualizar(self, obj):
        return "<a href='visualizar/?id=%d'>%s</a>" %(obj.id, obj.dre)
    drevisualizar.allow_tags = True
    drevisualizar.short_description = 'DRE'
    drevisualizar.admin_order_field = 'dre'
    
    def visualizar(self, obj):
        return "<a href='visualizar/?id=%s'>%s</a>" %(obj.id, obj.nome)
    visualizar.allow_tags=True
    visualizar.short_description='Nome'
    visualizar.admin_order_field='nome'
    
    def alocarBolsa(self, obj):
        return "<center><a href='#%s' class='alocarBolsa addlink' id=''> Alocar <input type='hidden' id='%s' name='aluno%s' value='%s'></a> </center>" %(obj.id, obj.id, obj.id, obj.nome)
    alocarBolsa.allow_tags=True
    alocarBolsa.short_description='Alocar Bolsa'
    
    
    def changelist_view(self, request, extra_context=None):
        dicAlunos = dict()
        
        for a in Aluno.objects.all():
            dicAlunos[a.id] = a
        
        dicDados = {
                 'bolsas':Bolsa.objects.filter(aluno_id__isnull=True),
                 'dicAlunos':dicAlunos
                 }
        return admin.ModelAdmin.changelist_view(self, request, extra_context=dicDados)
    
    def queryset(self, request):
        return Aluno.objects.exclude(id__in=[b.aluno.pk for b in Bolsa.objects.filter(aluno_id__isnull=False)]).filter(cursonivel='Doutorado', permissaobolsa=True) 
    
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class BolsistaMestradoAdmin(admin.ModelAdmin):
    list_display=['drevisualizar', 'visualizar', 'bolsa', 'regulamentoMestradoCra', 'regulamentoCargaHr', 'regulamentoMestradoConceito', 'desalocarBolsa']
    list_filter = [BolsistaMestradoRegulamentoFiltro]
    list_max_show_all = 1000
    
    def bolsa(self, obj):
        return Bolsa.objects.get(aluno_id=obj.id)
    
    def queryset(self, request):
        self.listaIdsIrregCargaHrBolsa = [a.pk for a in Aluno.objects.regulamentoMestradoCargaHrBolsa()]
        self.listaIdsIrregCraBolsa = [a.pk for a in Aluno.objects.regulamentoMestradoCraBolsa()]
        self.listaIdsIrregConceitoBolsa = [a.pk for a in Aluno.objects.regulamentoMestradoConceitoBolsa()]
        
        return Aluno.objects.filter(id__in=[b.aluno.id for b in Bolsa.objects.exclude(aluno_id__isnull=True)]).filter(cursonivel='Mestrado')
    
    def regulamentoCargaHr(self, obj):
        if obj.id in self.listaIdsIrregCargaHrBolsa:
            return htmlIconFalse()
        else:
            return htmlIconTrue()
    regulamentoCargaHr.allow_tags=True
    regulamentoCargaHr.short_description = "Carga Horária"
    
    def regulamentoMestradoCra(self, obj):
        if obj.id in self.listaIdsIrregCraBolsa:
            return htmlIconFalse()
        else:
            return htmlIconTrue()
    regulamentoMestradoCra.allow_tags=True
    regulamentoMestradoCra.short_description = "CRA"
    
    def regulamentoMestradoConceito(self, obj):
        if obj.id in self.listaIdsIrregConceitoBolsa:
            return htmlIconFalse()
        else:
            return htmlIconTrue()
    regulamentoMestradoConceito.allow_tags=True
    regulamentoMestradoConceito.short_description = "Conceito"
    
    def desalocarBolsa(self, obj):
        return "<center><a href='desalocarBolsa/?id=%s&nivel=%s' class='deletelink' onclick=\"return confirm('Deseja desalocar a Bolsa de: %s ' )\" >Desalocar</a></center>" %(obj.id,'M', obj.nome) 
    desalocarBolsa.allow_tags=True
    desalocarBolsa.short_description="Desalocar"
    
    def visualizar(self, obj):
        return "<a href='visualizar/?id=%s'>%s</a>" %(obj.id, obj.nome)
    visualizar.allow_tags=True
    visualizar.short_description='Nome'
    visualizar.admin_order_field='nome'
    
    def drevisualizar(self, obj):
        return "<a href='visualizar/?id=%d'>%s</a>" %(obj.id, obj.dre)
    drevisualizar.allow_tags = True
    drevisualizar.short_description = 'DRE'
    drevisualizar.admin_order_field = 'dre'
    
    
    def has_add_permission(self, request):
        return False
    
class BolsistaDoutoradoAdmin(admin.ModelAdmin):
    list_display=['drevisualizar', 'visualizar', 'bolsa', 'regulamentoMestradoCra', 'regulamentoCargaHr', 'regulamentoMestradoConceito', 'desalocarBolsa']
    list_filter = [BolsistaDoutoradoRegulamentoFiltro]
    list_max_show_all = 1000
    
    def bolsa(self, obj):
        return Bolsa.objects.get(aluno_id=obj.id)
    
    def queryset(self, request):
        self.listaIdsIrregCargaHrBolsa = [a.pk for a in Aluno.objects.regulamentoDoutoradoCargaHrBolsa()]
        self.listaIdsIrregCraBolsa = [a.pk for a in Aluno.objects.regulamentoDoutoradoCraBolsa()]
        self.listaIdsIrregConceitoBolsa = [a.pk for a in Aluno.objects.regulamentoDoutoradoConceitoBolsa()]
        
        return Aluno.objects.filter(id__in=[b.aluno.id for b in Bolsa.objects.exclude(aluno_id__isnull=True)]).filter(cursonivel='Doutorado')
    
    def regulamentoCargaHr(self, obj):
        if obj.id in self.listaIdsIrregCargaHrBolsa:
            return htmlIconFalse()
        else:
            return htmlIconTrue()
    regulamentoCargaHr.allow_tags=True
    regulamentoCargaHr.short_description = "Carga Horária"
    
    def regulamentoMestradoCra(self, obj):
        if obj.id in self.listaIdsIrregCraBolsa:
            return htmlIconFalse()
        else:
            return htmlIconTrue()
    regulamentoMestradoCra.allow_tags=True
    regulamentoMestradoCra.short_description = "CRA"
    
    def regulamentoMestradoConceito(self, obj):
        if obj.id in self.listaIdsIrregConceitoBolsa:
            return htmlIconFalse()
        else:
            return htmlIconTrue()
    regulamentoMestradoConceito.allow_tags=True
    regulamentoMestradoConceito.short_description = "Conceito"
    
    def desalocarBolsa(self, obj):
        return "<center><a href='desalocarBolsa/?id=%s&nivel=%s' class='deletelink' onclick=\"return confirm('Deseja desalocar a Bolsa de: %s ' )\" >Desalocar</a></center>" %(obj.id,'D', obj.nome) 
    desalocarBolsa.allow_tags=True
    desalocarBolsa.short_description="Desalocar"
    
    def visualizar(self, obj):
        return "<a href='visualizar/?id=%s'>%s</a>" %(obj.id, obj.nome)
    visualizar.allow_tags=True
    visualizar.short_description='Nome'
    visualizar.admin_order_field='nome'
    
    def drevisualizar(self, obj):
        return "<a href='visualizar/?id=%d'>%s</a>" %(obj.id, obj.dre)
    drevisualizar.allow_tags = True
    drevisualizar.short_description = 'DRE'
    drevisualizar.admin_order_field = 'dre'
    
    
    def has_add_permission(self, request):
        return False
    
admin.site.register(Aluno, AlunoAdmin)
admin.site.register(SituacaoMatricula)
admin.site.register(Area, AreaAdmin)
admin.site.register(Disciplina, DisciplinaAdmin)
admin.site.register(Professor)
admin.site.register(Bolsa, BolsaAdmin)
admin.site.register(OrgaoFomento)
admin.site.register(AlunoMestradoIrregular, AlunoMestradoIrregularAdmin)
admin.site.register(AlunoMestradoPrazoMax, AlunoMestradoPrazoMaxAdmin)
admin.site.register(AlunoMestradoEsperaBolsa, AlunoMestradoEsperaBolsaAdmin)
admin.site.register(BolsistaMestrado, BolsistaMestradoAdmin)
admin.site.register(AlunoDoutoradoPrazoMax, AlunoDoutoradoPrazoMaxAdmin)
admin.site.register(BolsistaDoutorado, BolsistaDoutoradoAdmin)
admin.site.register(AlunoDoutoradoIrregular, AlunoDoutoradoIrregularAdmin)
admin.site.register(AlunoDoutoradoEsperaBolsa, AlunoDoutoradoEsperaBolsaAdmin)
