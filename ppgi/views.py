# -*- coding: utf-8 -*-
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from ppgi.controllers import CtrlXLS
from ppgi.models import Aluno, SituacaoMatricula,\
    Aluno_DisciplinasCursadas, Bolsa, Bolsa_Historico
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.admin.views.decorators import staff_member_required
from django.core import serializers
from django.contrib import messages
from django.utils.datetime_safe import datetime
from ppgi import forms
from ppgi.util import handle_uploaded_file
from sistemappgi.settings import DADOS_PPGI_ROOT
from django.db import transaction

def index(request):
    return redirect('/admin/')

@transaction.commit_manually
@staff_member_required
def ajax_inicializarBD(request):
    
    ctrlXLS = CtrlXLS()
    
    transaction_savepoint = transaction.savepoint()
    
    try:
        ctrlXLS.inicializarSituacaoMatriculaBD('situacaoMatricula.xls')
        ctrlXLS.inicializarAlunosBD('alunos.xls')
        ctrlXLS.inicializarDisciplinasBD('disciplinas.xls')
        ctrlXLS.inicializarDisciplinasCursadasBD('disciplinasCursadas.xls')
        
        Aluno.objects.atualizarGrauEsperaBolsa()
        
        messages.success(request, 'Os dados foram carregados e atualizados com sucesso.')
        
        transaction.savepoint_commit(transaction_savepoint)
        
    except:
        transaction.savepoint_rollback(transaction_savepoint)
        messages.error(request, 'Houve um erro ao carregar os dados.')
    
    transaction.commit()
    #return render_to_response('inicializarBD.html', '', context_instance=RequestContext(request))
    return HttpResponse()

@staff_member_required
def inicializarBD(request):
    return render_to_response('inicializarBD.html', '', context_instance=RequestContext(request))

def atualizarGrauEsperaBolsa(request, self):
    Aluno.objects.atualizarGrauEsperaBolsa()
    messages.success(request, 'Atualização realizada com sucesso.')
    return HttpResponseRedirect('../')

@staff_member_required
def uploadDadosPpgi(request):
    
    if request.method == 'POST':
        form = forms.uploadDadosPpgiForm(request.POST, request.FILES)
        
        if form.is_valid():
            request.FILES['uploadAlunos'].name = "alunos.xls";
            request.FILES['uploadDisciplinas'].name = "disciplinas.xls";
            request.FILES['uploadDisciplinasCursadas'].name = "disciplinasCursadas.xls";
            
            handle_uploaded_file(request.FILES['uploadAlunos'], DADOS_PPGI_ROOT)
            handle_uploaded_file(request.FILES['uploadDisciplinas'], DADOS_PPGI_ROOT)
            handle_uploaded_file(request.FILES['uploadDisciplinasCursadas'], DADOS_PPGI_ROOT)
            
            #messages.success(request, 'Dados enviados com sucesso')
            return HttpResponseRedirect('../inicializarBD/')
    else:
        form = forms.uploadDadosPpgiForm()
    
    dados = {'form':form,}
    
    return render_to_response('uploadDadosPpgi.html', dados, context_instance = RequestContext(request))

@staff_member_required
def sugerirCancelamentoMatricula(request):
    
    alunosIrregularesCra        = Aluno.objects.regulamentoMestradoCra()
    alunosIrregularesConceito   = Aluno.objects.regulamentoMestradoConceito()
    alunosIrregularesAbandono   = Aluno.objects.filter(situacaomatricula_id=SituacaoMatricula.objects.get(codigo='C03'))
    
    alunosIrregularesHash = dict()
    
    for a in alunosIrregularesCra:
        #alunoIrregular = AlunoIrregular(a)
        #alunoIrregular.regulamentoMestradoCra = True
        #alunosIrregularesHash[a.pk] = alunoIrregular
        pass
    
    for a in alunosIrregularesConceito:
        if a.pk in alunosIrregularesHash:
            alunosIrregularesHash[a.pk].regulamentoMestradoConceito = True
        else:
            #alunoIrregular = AlunoIrregular(a)
            #alunoIrregular.regulamentoMestradoConceito = True
            #alunosIrregularesHash[a.pk] = alunoIrregular
            pass
       
    for a in alunosIrregularesAbandono:
        if a.pk in alunosIrregularesHash:
            alunosIrregularesHash[a.pk].regulamentoAbandono = True 
        else:
            #alunoIrregular = AlunoIrregular(a)
            #alunoIrregular.regulamentoAbandono = True
            #alunosIrregularesHash[a.pk] = alunoIrregular
            pass
    
    #print alunosIrregularesCra.__len__()
    #print alunosIrregularesConceito.__len__()
    #print alunosIrregularesAbandono.__len__()
    
    #print alunosIrregularesHash.__len__()
    #for key, value in alunosIrregularesHash.iteritems():
    #    print str(value.aluno) + ": cra - " + str(value.regulamentoMestradoCra) + "| abandono: " + str(value.regulamentoAbandono)
    
    #pag = request.GET.get('pag')
    #alunosIrregulares = sorted(alunosIrregularesHash.values(), key=lambda x:x.aluno.nome)
    #paginator = Paginator(alunosIrregulares, 30)
    
    #try:
    #    alunosIrregulares = paginator.page(pag)
    #except PageNotAnInteger:
    #    alunosIrregulares = paginator.page(1)
    #except EmptyPage:
    #    alunosIrregulares = paginator.page(paginator.num_pages)
    
    #dicDados={'alunosIrregulares': alunosIrregulares}
    
    #return render(request, 'cancelamento.html', dicParametros)
    #return render_to_response('cancelamentoMatricula.html', dicDados,
    #                         context_instance=RequestContext(request))
    return HttpResponse()

@staff_member_required
def visualizarAluno(request, self):
    
    idaluno = request.GET.get('id')
    
    aluno           = Aluno.objects.get(id=idaluno)
    discCursadas    = Aluno_DisciplinasCursadas.objects.filter(aluno_id=idaluno).order_by('anoletivo', 'periodoletivo')
    dicCraPeriodos  = aluno.dicCraPeriodos()
    
    dicDados={'aluno'           : aluno,
              'discCursadas'    : discCursadas,
              'dicCraPeriodos'  : dicCraPeriodos}

    return render_to_response('visualizarAluno.html', dicDados,
                              context_instance=RequestContext(request))

@staff_member_required
def alocarBolsa(request, self):
    
    if request.method == 'POST':
        idAluno = request.POST['idAluno']
        idBolsa = request.POST['idBolsa']
        nivel   = request.POST['nivel']
        
        if nivel == 'M':
            urlReverse = 'admin:ppgi_alunomestradoesperabolsa_changelist'
        else:
            urlReverse = 'admin:ppgi_alunodoutoradoesperabolsa_changelist'
            
        try:
            dataInicioBD    = datetime.strptime(request.POST['dataInicio'], '%d/%m/%Y')
            dataFimBD       = datetime.strptime(request.POST['dataFim'], '%d/%m/%Y')
            bolsa = Bolsa.objects.get(id=idBolsa)
            
            if idAluno=='' or idBolsa=='' or dataInicioBD=='' or dataFimBD=='':
                messages.error(request, 'Preencha os campos corretamente.')
                
            elif bolsa.aluno != None:
                messages.error(request, 'Esta bolsa já foi alocada.')
            elif Bolsa.objects.filter(aluno_id=idAluno).exists():
                messages.error(request, 'Este(a) aluno(a) já possui Bolsa.')
            else:
                bolsa.aluno = Aluno.objects.get(id=idAluno)
                bolsa.datainicio = dataInicioBD
                bolsa.datafim    = dataFimBD
                bolsa.save()
            
                messages.success(request, 'Bolsa alocada com sucesso.')
                
            return redirect(urlReverse)
        
        except ValueError:
            messages.error(request, 'Preencha os campos corretamente.')
            return redirect(urlReverse)


@staff_member_required
def desalocarBolsa(request, self):
    
    if request.method == 'GET':
        idAluno = request.GET.get('id')
        nivel   = request.GET.get('nivel')
        
        if nivel == 'M':
            urlReverse = "admin:ppgi_bolsistamestrado_changelist"
        else:
            urlReverse = "admin:ppgi_bolsistadoutorado_changelist"
        
        try:
            bolsa = Bolsa.objects.get(aluno_id=idAluno)
            bolsa.aluno = None
            bolsa.save()
            
            aluno = Aluno.objects.get(id=idAluno)
            aluno.permissaobolsa = False
            aluno.save()
            
            dataAtualBD = datetime.now().date() 
            Bolsa_Historico.objects.create(aluno_id=idAluno, bolsa_id=bolsa.id, datainicio=bolsa.datainicio,
                                           datafim=dataAtualBD )
            
            messages.success(request, "Bolsa desalocada com sucesso")
            return redirect(urlReverse)
        except Bolsa.DoesNotExist:
            messages.error(request, "Bolsa não existente.")
            return redirect(urlReverse)

def printAlunoIrregular(request,self):
    anoAtual = datetime.now().year
    nivel = request.GET.get('nivel')
    
    
    if nivel=='M':
        alunosIrregulares = Aluno.objects.irregularesMestrado().filter(anoingresso__gte=(anoAtual-4)).order_by('-anoingresso', 'nome')
        listaIdsIrregCra       = [a.pk for a in Aluno.objects.regulamentoMestradoCra()]
        listaIdsIrregConceito  = [a.pk for a in Aluno.objects.regulamentoMestradoConceito()]
    elif nivel=='D':
        alunosIrregulares      = Aluno.objects.irregularesDoutorado().filter(anoingresso__gte=(anoAtual-4)).order_by('-anoingresso', 'nome')
        listaIdsIrregCra       = [a.pk for a in Aluno.objects.regulamentoDoutoradoCra()]
        listaIdsIrregConceito  = [a.pk for a in Aluno.objects.regulamentoDoutoradoConceito()]
        
    listaIdsIrregAbandono  = [a.pk for a in Aluno.objects.filter(situacaomatricula_id=SituacaoMatricula.objects.get(codigo='C03'))]
    
    listaDicDados = []
    
    
    for a in alunosIrregulares:
        dicDados = dict()
        
        dicDados['aluno'] = a
        dicDados['cra'] = True
        dicDados['conceito'] = True
        dicDados['abandono'] = True
        
        if a.id in listaIdsIrregCra:
            dicDados['cra'] = False
        if a.id in listaIdsIrregConceito:
            dicDados['conceito'] = False
        if a.id in listaIdsIrregAbandono:
            dicDados['abandono'] = False
        
        listaDicDados.append(dicDados)
        
    dados = {'listaDicDados' : listaDicDados,
                 'nivel': nivel}
    
    return render_to_response('printAlunoIrregular.html', dados, context_instance=RequestContext(request))

def printAlunoPrazoMax(request, self):
    
    anoAtual = datetime.now().year
    nivel = request.GET.get('nivel')
    
    
    if nivel=='M':
        alunosIrregulares      = Aluno.objects.regulamentoMestradoPrazoMax().filter(cursonivel='Mestrado', anoingresso__gte=(anoAtual-4)).order_by('-anoingresso', 'nome')
        listaIdsIrregCra       = [a.pk for a in Aluno.objects.regulamentoMestradoCraPrazoMax()]
        listaIdsIrregCH  = [a.pk for a in Aluno.objects.regulamentoMestradoCargaHr()]
    elif nivel=='D':
        alunosIrregulares      = Aluno.objects.regulamentoDoutoradoPrazoMax().filter(cursonivel='Doutorado', anoingresso__gte=(anoAtual-4)).order_by('-anoingresso', 'nome')
        listaIdsIrregCra       = [a.pk for a in Aluno.objects.regulamentoDoutoradoCraPrazoMax()]
        listaIdsIrregCH  = [a.pk for a in Aluno.objects.regulamentoDoutoradoCargaHr()]
    
    listaDicDados = []
    
    
    for a in alunosIrregulares:
        dicDados = dict()
        
        dicDados['aluno'] = a
        dicDados['cra'] = True
        dicDados['cargahoraria'] = True
        
        if a.id in listaIdsIrregCra:
            dicDados['cra'] = False
        if a.id in listaIdsIrregCH:
            dicDados['cargahoraria'] = False
        
        listaDicDados.append(dicDados)
        
    dados = {'listaDicDados' : listaDicDados,
                 'nivel': nivel}
    
    return render_to_response('printAlunoPrazoMax.html', dados, context_instance=RequestContext(request))
 
def ajax_alunoInfo(request, self):
    
    idAluno = request.GET.get('id')
    aluno   = Aluno.objects.filter(id=idAluno)
    
    jsonAluno = serializers.serialize("json", aluno)
    return HttpResponse(jsonAluno, mimetype='text/javascript')
    