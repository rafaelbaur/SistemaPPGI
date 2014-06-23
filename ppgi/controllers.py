import xlrd
from sistemappgi.settings import SITE_ROOT, DADOS_PPGI_ROOT
from ppgi.models import Aluno, SituacaoMatricula, Disciplina,\
    Aluno_DisciplinasCursadas,\
    Aluno_DisciplinaInconsistente
from django.db.models import Max

class CtrlXLS():
    xls = None
    planilha = None        
    
    def inicializarAlunosBD(self, url):
        
        self.xls = xlrd.open_workbook(DADOS_PPGI_ROOT+'\\'+url)
        self.planilha = self.xls.sheet_by_index(0)
        
        i=1
        
        while i < self.planilha.nrows:
            colunas = [c for c in self.planilha.row_values(i)]
             
            sitMatricula = SituacaoMatricula.objects.get(codigo=colunas[6])
            dre          = int(colunas[1])
            
            
            
            if not Aluno.objects.filter(dre=dre).exists():
                aluno = Aluno()
                aluno.dre                     = dre
                aluno.ouvinte                 = False
                aluno.permissaobolsa          = True
            #    Aluno.objects.create(
            #        anoingresso             = int(colunas[0]),
            #        dre                     = dre,
            #        nome                    = colunas[2],
            #        periodoingresso         = int(colunas[3]),
            #        sexo                    = colunas[4],
            #        situacaomatricula_id    = sitMatricula.pk,
            #        ouvinte                 = False,
            #        permissaobolsa          = True,
            #        cursonivel              = colunas[7]
            #       )   
            else:
                aluno = Aluno.objects.get(dre=dre)
            
            aluno.anoingresso             = int(colunas[0])
            aluno.nome                    = colunas[2]
            aluno.periodoingresso         = int(colunas[3])
            aluno.sexo                    = colunas[4]
            aluno.situacaomatricula_id    = sitMatricula.pk
            aluno.cursonivel              = colunas[7]
            
            aluno.save()
             
            i = i + 1
        
        Aluno.objects.filter(situacaomatricula_id=(SituacaoMatricula.objects.get(codigo='C02'))).delete()
        return True
    
    def inicializarSituacaoMatriculaBD(self, url):
        
        self.xls = xlrd.open_workbook(DADOS_PPGI_ROOT+'\\'+url)
        self.planilha = self.xls.sheet_by_index(0)
        
        i=1
        
        while i < self.planilha.nrows:
            colunas = [c for c in self.planilha.row_values(i)]
            
            cod = colunas[1]
            
            if not SituacaoMatricula.objects.filter(codigo=cod).exists():   
                SituacaoMatricula.objects.create(
                        
                    codigo      = cod,
                    situacao    = colunas[0]              
                )
                 
            i = i + 1
        return True
    
    
    def inicializarDisciplinasBD(self, url):
        self.xls = xlrd.open_workbook(DADOS_PPGI_ROOT+'\\disciplinasSiga.xls')
        self.planilha = self.xls.sheet_by_index(0)
        
        self.xlsPanda = xlrd.open_workbook(DADOS_PPGI_ROOT+'\\disciplinas.xls')
        self.planilhaPanda = self.xlsPanda.sheet_by_index(0)
        
        i = 1
        
        while i < self.planilha.nrows:
            colunas = [c for c in self.planilha.row_values(i)]
            
            cod = colunas[1]
            
            if not Disciplina.objects.filter(codigo=cod).exists():
                
                Disciplina.objects.create(
                                          
                 codigo         = cod,
                 nome           = colunas[3],
                 nivel          = colunas[0],
                 creditos       = colunas[4],
                 cargahoraria   = colunas[7]+colunas[8],
                 nucleobasico   = False
                 )
            
            i = i + 1
            
        i = 1
        
        while i < self.planilhaPanda.nrows:
            colunas = [c for c in self.planilhaPanda.row_values(i)]
            
            cod = colunas[0]
            
            if not Disciplina.objects.filter(codigo=cod).exists():
                
                Disciplina.objects.create(
                                          
                 codigo         = cod,
                 nome           = colunas[1],
                 nivel          = colunas[2],
                 creditos       = 0,
                 cargahoraria   = 0,
                 nucleobasico   = False
                 )
            
            i = i + 1
        
        return True
    
    def inicializarDisciplinasCursadasBD(self, url):
        
        self.xls = xlrd.open_workbook(DADOS_PPGI_ROOT+'\\'+url)
        self.planilha = self.xls.sheet_by_index(0)
        
        i = 1
        
        #As seguintes disciplinas sao cursadas em mais de um periodo, Estagio e Pesquisa Tese - Mestrado, Doutorado
        discPermitidasPeriodosDistintos = Disciplina.objects.filter(codigo__in = ['MAB816', 'MAB716', 'MAB708',
                                                                                    'MAC808', 'MAB808'])
        Aluno_DisciplinasCursadas.objects.all().delete()
        while i < self.planilha.nrows:
            
            colunas = [c for c in self.planilha.row_values(i)]
            print colunas
            
            dre             = int(colunas[0])
            alunoId         = Aluno.objects.get(dre=dre).pk
            codDisciplina   = colunas[3]
            disciplinaId    = Disciplina.objects.get(codigo=codDisciplina).pk
            anoletivo       = colunas[1]
            conceito        = str(colunas[2]).split('.')[0]
            periodo         = int(colunas[4])
            situacaofinal   = colunas[5]
            creditos        = colunas[6]
            
            alunoDisc = Aluno_DisciplinasCursadas(aluno_id=alunoId, disciplina_id=disciplinaId, 
                                                  anoletivo=anoletivo, periodoletivo=periodo, conceito=conceito, 
                                                  situacaofinal=situacaofinal, creditos=creditos)
            
            #Verificar se ja existe na base a disciplina cursada e aprovada. Se sim, armazenar apenas a
            #mais recente
            discJaAprovada = Aluno_DisciplinasCursadas.objects.filter(aluno_id=alunoId, 
                           disciplina_id=disciplinaId, situacaofinal='AP')
            
            discJaCursadaAnoPeriodo = Aluno_DisciplinasCursadas.objects.filter(aluno_id=alunoId, 
                                    disciplina_id=disciplinaId, anoletivo=anoletivo, 
                                    periodoletivo=periodo)
            
            #Retorna as tentativas anteriores, onde aluno nao eh aprovado                       
            discJaCursada = Aluno_DisciplinasCursadas.objects.filter(aluno_id=alunoId, 
                                    disciplina_id=disciplinaId).exclude(situacaofinal='AP')
            
            
            if not discJaCursadaAnoPeriodo.exists():
           
                #Caso seja uma disciplina permitida cursada em mais de um periodo, sera inserido apenas 
                #se nao for repetida no ano e periodo
                if disciplinaId in [d.pk for d in discPermitidasPeriodosDistintos]:
                            
                    alunoDisc.save()
                    #print 'imprimindo disciplinas nao normais: ' + str(disciplinaId)
                      
                #Caso seja uma disciplina normal, apenas pode ser aprovada uma vez. Aqui sera deixada no banco
                #a disciplina cursada mais recentemente caso ja tenha sido aprovada 
                elif discJaAprovada.exists():
    
                    maisrecente = discJaAprovada.annotate(Max('anoletivo')).annotate(Max('periodoletivo'))[0]
        
                    if maisrecente.anoletivo > anoletivo or (maisrecente.anoletivo == anoletivo and maisrecente.periodoletivo >= periodo):
                        discJaAprovada.delete()
                        maisrecente.save()
                        
                        #Caso seja tentativa anterior eh inserido normalmente, senao eh detectado uma inconsistencia
                        if situacaofinal != 'AP':
                            alunoDisc.save()
                        else:
                            Aluno_DisciplinaInconsistente.objects.get_or_create(aluno_id=alunoId, disciplina_id=disciplinaId)
                            
                        print str(alunoId) + '-' + str(discJaAprovada[0].pk)
                        #print 'Mantendo disciplina mais recente no banco: ' + str(maisrecente.pk)
                    else:
                        discJaAprovada.delete()
                        alunoDisc.save()
                      
                        Aluno_DisciplinaInconsistente.objects.get_or_create(aluno_id=alunoId, disciplina_id=maisrecente.disciplina.pk)
                        
                        #print 'Salvando nova disciplina aprovada: ' + str(alunoId) + '-' + str(disciplinaId) + '-' + str(anoletivo) + '-' + str(periodo) + '-' + situacaofinal
                
                #Inserir caso nao haja uma reprovacao mais recente do que a disciplina aprovada que pretendo adicionar
                elif situacaofinal == 'AP' and discJaCursada.exists():
                    maisrecente = discJaCursada.annotate(Max('anoletivo')).annotate(Max('periodoletivo'))[0]
                    
                    if anoletivo > maisrecente.anoletivo or (maisrecente.anoletivo == anoletivo and periodo > maisrecente.periodoletivo):
                        alunoDisc.save()
                    else:
                        Aluno_DisciplinaInconsistente.objects.get_or_create(aluno_id=alunoId, disciplina_id=disciplinaId)
                else:
                    alunoDisc.save()
                       
            #Caso ja haja no banco a disciplina cursada no ano e periodo, apenas atualiza caso estivesse com conceito I
            elif discJaCursadaAnoPeriodo.filter(conceito='I').exists() and conceito != 'I':
                
                discJaCursadaAnoPeriodo.filter(conceito='I').update(conceito=conceito, situacaofinal=situacaofinal)
                #print 'Salvando nova disciplina NAO aprovada: ' + str(alunoId) + '-' + str(disciplinaId) + '-' + str(anoletivo) + '-' + str(periodo) + '-' + situacaofinal
            
            i = i + 1
    
        
        return True



    
                    
                    