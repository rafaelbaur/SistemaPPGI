# -*- coding: utf-8 -*-
from django.db import models
from django.db import connection
from django.utils.datetime_safe import datetime
from ppgi.util import getPeriodo, getPeriodosDecorridos

# Create your models here.

class Area(models.Model):
    area        = models.CharField(max_length=50)
    sigla       = models.CharField(max_length=10)
    
    def __unicode__(self):
        return self.area
    
    class Meta(object):
        verbose_name='Área'
        verbose_name_plural = 'Áreas'

class SituacaoMatricula(models.Model):
    codigo      = models.CharField(max_length=20, unique=True)
    situacao    = models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.situacao
    class Meta(object):
        verbose_name        = 'Situação de Matrícula'
        verbose_name_plural = 'Situações de Matrícula'

class AlunoManager(models.Manager):
    
    #Retorna alunos que possuem cra abaixo de 1.6 em 2 ou mais periodos
    def regulamentoMestradoCra(self):
        alunos=[]
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM (SELECT a.id, 
                            (SELECT SUM((dc2.conceito*dc2.creditos)/10)/SUM(dc2.creditos) 
                                FROM ppgi_disciplina d2, ppgi_aluno_disciplinascursadas dc2
                                WHERE dc2.aluno_id=a.id
                                AND (dc2.anoletivo < dc.anoletivo OR (dc2.anoletivo=dc.anoletivo AND dc2.periodoletivo <= dc.periodoletivo))
                                AND d2.id=dc2.disciplina_id 
                                AND dc2.conceito NOT IN ('I', 'J', 'T')) as cra
                            FROM ppgi_aluno a, ppgi_aluno_disciplinascursadas dc, ppgi_disciplina d
                            WHERE a.id=dc.aluno_id AND dc.disciplina_id=d.id
                            GROUP BY a.id, dc.anoletivo, dc.periodoletivo ORDER BY a.id) t 
                        WHERE t.cra<1.6 OR t.cra IS NULL GROUP BY t.id HAVING COUNT(t.id)>=2 """)
        for linha in cursor.fetchall():
            alunos.append(Aluno.objects.get(id=linha[0]))
        return alunos
    
    #Atualizar Posteriormente
    def regulamentoDoutoradoCra(self):
        alunos=[]
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM (SELECT a.id, 
                            (SELECT SUM((dc2.conceito*dc2.creditos)/10)/SUM(dc2.creditos) 
                                FROM ppgi_disciplina d2, ppgi_aluno_disciplinascursadas dc2
                                WHERE dc2.aluno_id=a.id
                                AND (dc2.anoletivo < dc.anoletivo OR (dc2.anoletivo=dc.anoletivo AND dc2.periodoletivo <= dc.periodoletivo))
                                AND d2.id=dc2.disciplina_id 
                                AND dc2.conceito NOT IN ('I', 'J', 'T')) as cra
                            FROM ppgi_aluno a, ppgi_aluno_disciplinascursadas dc, ppgi_disciplina d
                            WHERE a.id=dc.aluno_id AND dc.disciplina_id=d.id
                            GROUP BY a.id, dc.anoletivo, dc.periodoletivo ORDER BY a.id) t 
                        WHERE t.cra<1.6 OR t.cra IS NULL GROUP BY t.id HAVING COUNT(t.id)>=2 """)
        for linha in cursor.fetchall():
            alunos.append(Aluno.objects.get(id=linha[0]))
        return alunos
    
    #Alunos com 2 ou mais reprovacoes
    def regulamentoMestradoConceito(self):
        alunos=[]
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM ppgi_aluno a, ppgi_aluno_disciplinascursadas dc, ppgi_disciplina d
                            WHERE a.id=dc.aluno_id AND dc.disciplina_id=d.id
                            AND dc.conceito='0'
                            GROUP BY a.id HAVING COUNT(dc.conceito)>=2 ORDER BY a.id """)
        for linha in cursor.fetchall():
            alunos.append(Aluno.objects.get(id=linha[0]))
        return alunos
    
    #Atualizar posteriormente
    def regulamentoDoutoradoConceito(self):
        alunos=[]
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM ppgi_aluno a, ppgi_aluno_disciplinascursadas dc, ppgi_disciplina d
                            WHERE a.id=dc.aluno_id AND dc.disciplina_id=d.id
                            AND dc.conceito='0'
                            GROUP BY a.id HAVING COUNT(dc.conceito)>=2 ORDER BY a.id """)
        for linha in cursor.fetchall():
            alunos.append(Aluno.objects.get(id=linha[0]))
        return alunos
    
    #Alunos que ja cursaram 8 ou mais periodos
    def regulamentoMestradoPrazoMax(self):
        idAlunos=[]
        cursor = connection.cursor()
        cursor.execute("""SELECT id FROM (SELECT a.id, a.situacaomatricula_id, dc.anoletivo, dc.periodoletivo
                                            FROM ppgi_aluno a, ppgi_aluno_disciplinascursadas dc, ppgi_disciplina d
                                            WHERE a.id=dc.aluno_id AND dc.disciplina_id=d.id
                                            GROUP BY a.id, dc.anoletivo, dc.periodoletivo ORDER BY a.id) t
                            WHERE t.situacaomatricula_id != 9
                            GROUP BY t.id HAVING count(t.anoletivo)>=8 """)
        for linha in cursor.fetchall():
            idAlunos.append(linha[0])
        return Aluno.objects.filter(id__in=idAlunos)
    
    #Atualizar posteriormente
    def regulamentoDoutoradoPrazoMax(self):
        idAlunos=[]
        cursor = connection.cursor()
        cursor.execute("""SELECT id FROM (SELECT a.id, a.situacaomatricula_id, dc.anoletivo, dc.periodoletivo
                                            FROM ppgi_aluno a, ppgi_aluno_disciplinascursadas dc, ppgi_disciplina d
                                            WHERE a.id=dc.aluno_id AND dc.disciplina_id=d.id
                                            GROUP BY a.id, dc.anoletivo, dc.periodoletivo ORDER BY a.id) t
                            WHERE t.situacaomatricula_id != 9
                            GROUP BY t.id HAVING count(t.anoletivo)>=8 """)
        for linha in cursor.fetchall():
            idAlunos.append(linha[0])
        return Aluno.objects.filter(id__in=idAlunos)
    
    #Alunos que possuem reprovacao
    def comReprovacao(self, filtro):
        idalunos=[]
        
        if filtro == '1':
            filtro = ' = 1 '
        if filtro == '2+':
            filtro = ' >= 2'
        
        cursor = connection.cursor()
        cursor.execute("""SELECT a.id FROM ppgi_aluno a, ppgi_aluno_disciplinascursadas dc, ppgi_disciplina d
                                    WHERE a.id=dc.aluno_id AND dc.disciplina_id=d.id
                                    AND dc.conceito='0'
                                    GROUP BY a.id HAVING COUNT(dc.conceito) """+filtro+""" ORDER BY a.id """)
        
        for linha in cursor.fetchall():
            idalunos.append(linha[0])
            
        return Aluno.objects.filter(id__in=idalunos)
    
    #Alunos que atingiram prazo maximo e possuem carga horaria inferior a 360 e carga horaria nucleo basico inferior a
    def regulamentoMestradoCargaHr(self):
        idalunos=[]
        
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM (SELECT a.id, a.nome, (SELECT SUM(d2.cargahoraria)
                                FROM ppgi_disciplina d2, ppgi_aluno_disciplinascursadas dc2
                                WHERE dc2.aluno_id=a.id
                                AND d2.id=dc2.disciplina_id 
                                AND dc2.conceito NOT IN ('I', 'J', 'T', '0')) as choraria,
                                (SELECT SUM(d2.cargahoraria)
                                        FROM ppgi_disciplina d2, ppgi_aluno_disciplinascursadas dc2
                                        WHERE dc2.aluno_id=a.id
                                        AND d2.id=dc2.disciplina_id 
                                        AND dc2.conceito NOT IN ('I', 'J', 'T', '0')
                                        AND d2.nucleobasico=TRUE) as chorarianb
                                FROM ppgi_aluno a, ppgi_aluno_disciplinascursadas dc, ppgi_disciplina d
                                WHERE a.id=dc.aluno_id AND dc.disciplina_id=d.id
                                GROUP BY a.id) t 
                        WHERE t.choraria < 360 OR t.choraria IS NULL""")
        
        for linha in cursor.fetchall():
            idalunos.append(linha[0])
            
        return Aluno.objects.filter(id__in=idalunos)
    
    def regulamentoMestradoCargaHrBasico(self):
        idalunos=[]
        
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM (SELECT a.id, a.nome, (SELECT SUM(d2.cargahoraria)
                                FROM ppgi_disciplina d2, ppgi_aluno_disciplinascursadas dc2
                                WHERE dc2.aluno_id=a.id
                                AND d2.id=dc2.disciplina_id 
                                AND dc2.conceito NOT IN ('I', 'J', 'T', '0')) as choraria,
                                (SELECT SUM(d2.cargahoraria)
                                        FROM ppgi_disciplina d2, ppgi_aluno_disciplinascursadas dc2
                                        WHERE dc2.aluno_id=a.id
                                        AND d2.id=dc2.disciplina_id 
                                        AND dc2.conceito NOT IN ('I', 'J', 'T', '0')
                                        AND d2.nucleobasico=TRUE) as chorarianb
                                FROM ppgi_aluno a, ppgi_aluno_disciplinascursadas dc, ppgi_disciplina d
                                WHERE a.id=dc.aluno_id AND dc.disciplina_id=d.id
                                GROUP BY a.id) t 
                        WHERE t.chorarianb < 135 OR t.chorarianb IS NULL""")
        
        for linha in cursor.fetchall():
            idalunos.append(linha[0])
            
        return Aluno.objects.filter(id__in=idalunos)
    
    #Atualizar Posteriormente
    def regulamentoDoutoradoCargaHr(self):
        idalunos=[]
        
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM (SELECT a.id, a.nome, (SELECT SUM(d2.cargahoraria)
                                FROM ppgi_disciplina d2, ppgi_aluno_disciplinascursadas dc2
                                WHERE dc2.aluno_id=a.id
                                AND d2.id=dc2.disciplina_id 
                                AND dc2.conceito NOT IN ('I', 'J', 'T', '0')) as choraria,
                                (SELECT SUM(d2.cargahoraria)
                                        FROM ppgi_disciplina d2, ppgi_aluno_disciplinascursadas dc2
                                        WHERE dc2.aluno_id=a.id
                                        AND d2.id=dc2.disciplina_id 
                                        AND dc2.conceito NOT IN ('I', 'J', 'T', '0')
                                        AND d2.nucleobasico=TRUE) as chorarianb
                                FROM ppgi_aluno a, ppgi_aluno_disciplinascursadas dc, ppgi_disciplina d
                                WHERE a.id=dc.aluno_id AND dc.disciplina_id=d.id
                                GROUP BY a.id) t 
                        WHERE t.choraria < 360 OR t.choraria IS NULL""")
        
        for linha in cursor.fetchall():
            idalunos.append(linha[0])
            
        return Aluno.objects.filter(id__in=idalunos)
    
    def regulamentoDoutoradoCargaHrBasico(self):
        idalunos=[]
        
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM (SELECT a.id, a.nome, (SELECT SUM(d2.cargahoraria)
                                FROM ppgi_disciplina d2, ppgi_aluno_disciplinascursadas dc2
                                WHERE dc2.aluno_id=a.id
                                AND d2.id=dc2.disciplina_id 
                                AND dc2.conceito NOT IN ('I', 'J', 'T', '0')) as choraria,
                                (SELECT SUM(d2.cargahoraria)
                                        FROM ppgi_disciplina d2, ppgi_aluno_disciplinascursadas dc2
                                        WHERE dc2.aluno_id=a.id
                                        AND d2.id=dc2.disciplina_id 
                                        AND dc2.conceito NOT IN ('I', 'J', 'T', '0')
                                        AND d2.nucleobasico=TRUE) as chorarianb
                                FROM ppgi_aluno a, ppgi_aluno_disciplinascursadas dc, ppgi_disciplina d
                                WHERE a.id=dc.aluno_id AND dc.disciplina_id=d.id
                                GROUP BY a.id) t 
                        WHERE t.chorarianb < 135 OR t.chorarianb IS NULL""")
        
        for linha in cursor.fetchall():
            idalunos.append(linha[0])
            
        return Aluno.objects.filter(id__in=idalunos)
    
    #Alunos que possuem cra menor que 2.0
    def regulamentoMestradoCraPrazoMax(self):
        idAlunos=[]
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM (SELECT a.id, 
                            (SELECT SUM((dc2.conceito*dc2.creditos)/10)/SUM(dc2.creditos) 
                                FROM ppgi_disciplina d2, ppgi_aluno_disciplinascursadas dc2
                                WHERE dc2.aluno_id=a.id
                                AND d2.id=dc2.disciplina_id 
                                AND dc2.conceito NOT IN ('I', 'J', 'T')) as cra
                            FROM ppgi_aluno a, ppgi_aluno_disciplinascursadas dc, ppgi_disciplina d
                            WHERE a.id=dc.aluno_id AND dc.disciplina_id=d.id
                            GROUP BY a.id ORDER BY a.id) t 
                        WHERE t.cra<2 OR t.cra IS NULL """)
        for linha in cursor.fetchall():
            idAlunos.append(linha[0])
        return Aluno.objects.filter(id__in=idAlunos)
    
    #Atualizar posteriormente
    def regulamentoDoutoradoCraPrazoMax(self):
        idAlunos=[]
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM (SELECT a.id, 
                            (SELECT SUM((dc2.conceito*dc2.creditos)/10)/SUM(dc2.creditos) 
                                FROM ppgi_disciplina d2, ppgi_aluno_disciplinascursadas dc2
                                WHERE dc2.aluno_id=a.id
                                AND d2.id=dc2.disciplina_id 
                                AND dc2.conceito NOT IN ('I', 'J', 'T')) as cra
                            FROM ppgi_aluno a, ppgi_aluno_disciplinascursadas dc, ppgi_disciplina d
                            WHERE a.id=dc.aluno_id AND dc.disciplina_id=d.id
                            GROUP BY a.id ORDER BY a.id) t 
                        WHERE t.cra<2 OR t.cra IS NULL """)
        for linha in cursor.fetchall():
            idAlunos.append(linha[0])
        return Aluno.objects.filter(id__in=idAlunos)
    
    def regulamentoMestradoConceitoBolsa(self):
        idAlunos=[]
        cursor = connection.cursor()
        cursor.execute("""SELECT a.id FROM ppgi_aluno a, ppgi_bolsa b, ppgi_aluno_disciplinascursadas dc
                            WHERE a.id = b.aluno_id AND a.id=dc.aluno_id AND dc.conceito='0' 
                            GROUP BY dc.conceito HAVING COUNT(dc.conceito)>=1""")
        for linha in cursor.fetchall():
            idAlunos.append(linha[0])
        return Aluno.objects.filter(id__in=idAlunos)
    
    #Atualizar posteriormente
    def regulamentoDoutoradoConceitoBolsa(self):
        idAlunos=[]
        cursor = connection.cursor()
        cursor.execute("""SELECT a.id FROM ppgi_aluno a, ppgi_bolsa b, ppgi_aluno_disciplinascursadas dc
                            WHERE a.id = b.aluno_id AND a.id=dc.aluno_id AND dc.conceito='0' 
                            GROUP BY dc.conceito HAVING COUNT(dc.conceito)>=1""")
        for linha in cursor.fetchall():
            idAlunos.append(linha[0])
        return Aluno.objects.filter(id__in=idAlunos)
    
    def regulamentoMestradoCraBolsa(self):
        idAlunos = []
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM (SELECT a.id, 
                            (SELECT SUM((dc2.conceito*dc2.creditos)/10)/SUM(dc2.creditos) 
                                FROM ppgi_disciplina d2, ppgi_aluno_disciplinascursadas dc2
                                WHERE dc2.aluno_id=a.id
                                AND (dc2.anoletivo < dc.anoletivo OR (dc2.anoletivo=dc.anoletivo AND dc2.periodoletivo <= dc.periodoletivo))
                                AND d2.id=dc2.disciplina_id 
                                AND dc2.conceito NOT IN ('I', 'J', 'T')) as cra
                            FROM ppgi_aluno a, ppgi_aluno_disciplinascursadas dc, ppgi_disciplina d,
                                 ppgi_bolsa b
                            WHERE a.id=dc.aluno_id AND dc.disciplina_id=d.id AND a.id=b.aluno_id
                            GROUP BY a.id, dc.anoletivo, dc.periodoletivo ORDER BY a.id) t 
                        WHERE t.cra<1.6 OR t.cra IS NULL GROUP BY t.id HAVING COUNT(t.id)>=1 """)
        
        for linha in cursor.fetchall():
            idAlunos.append(linha[0])
        return Aluno.objects.filter(id__in=idAlunos)
    
    #Atualizar posteriormente
    def regulamentoDoutoradoCraBolsa(self):
        idAlunos = []
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM (SELECT a.id, 
                            (SELECT SUM((dc2.conceito*dc2.creditos)/10)/SUM(dc2.creditos) 
                                FROM ppgi_disciplina d2, ppgi_aluno_disciplinascursadas dc2
                                WHERE dc2.aluno_id=a.id
                                AND (dc2.anoletivo < dc.anoletivo OR (dc2.anoletivo=dc.anoletivo AND dc2.periodoletivo <= dc.periodoletivo))
                                AND d2.id=dc2.disciplina_id 
                                AND dc2.conceito NOT IN ('I', 'J', 'T')) as cra
                            FROM ppgi_aluno a, ppgi_aluno_disciplinascursadas dc, ppgi_disciplina d,
                                 ppgi_bolsa b
                            WHERE a.id=dc.aluno_id AND dc.disciplina_id=d.id AND a.id=b.aluno_id
                            GROUP BY a.id, dc.anoletivo, dc.periodoletivo ORDER BY a.id) t 
                        WHERE t.cra<1.6 OR t.cra IS NULL GROUP BY t.id HAVING COUNT(t.id)>=1 """)
        
        for linha in cursor.fetchall():
            idAlunos.append(linha[0])
        return Aluno.objects.filter(id__in=idAlunos)
    
    #Carga Horaria necessaria ate o final de 5 periodos desde a inscricao
    def regulamentoMestradoCargaHrBolsa(self):
        idalunos=[]
        anoAtual = datetime.now().year
        mesAtual = datetime.now().month
        periodoAtual = getPeriodo(mesAtual)
        
        periodoMinimo = periodoAtual - 1
        
        #Regulamento para 5 periodos - Equivalentes a 1 ano e 1 periodo
        if (periodoMinimo) > 0:
            anoMinimo = anoAtual - 1
        else:
            anoMinimo = anoAtual - 2
            periodoMinimo = 4
            

        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM 
                                (SELECT a.id, a.nome, (SELECT SUM(d2.cargahoraria)
                                FROM ppgi_disciplina d2, ppgi_aluno_disciplinascursadas dc2
                                WHERE dc2.aluno_id=a.id
                                AND d2.id=dc2.disciplina_id 
                                AND dc2.conceito NOT IN ('I', 'J', 'T', '0')) as choraria,
                                (SELECT SUM(d2.cargahoraria)
                                        FROM ppgi_disciplina d2, ppgi_aluno_disciplinascursadas dc2
                                        WHERE dc2.aluno_id=a.id
                                        AND d2.id=dc2.disciplina_id 
                                        AND dc2.conceito NOT IN ('I', 'J', 'T', '0')
                                        AND d2.nucleobasico=TRUE) as chorarianb
                                FROM ppgi_aluno a, ppgi_aluno_disciplinascursadas dc, ppgi_disciplina d
                                WHERE a.id=dc.aluno_id AND dc.disciplina_id=d.id
                                AND (a.anoingresso<='"""+str(anoMinimo-1)+"""' OR (a.anoingresso='"""+str(anoMinimo)+"""' 
                                AND a.periodoingresso<='"""+str(periodoMinimo)+"""'))
                                GROUP BY a.id) t 
                        WHERE t.choraria < 360 OR t.choraria IS NULL""")

        for linha in cursor.fetchall():
            idalunos.append(linha[0])

        return Aluno.objects.filter(id__in=idalunos)
    
    #Atualizar posteriormente se necessario
    def regulamentoDoutoradoCargaHrBolsa(self):
        idalunos=[]
        anoAtual = datetime.now().year
        mesAtual = datetime.now().month
        periodoAtual = getPeriodo(mesAtual)
        
        periodoMinimo = periodoAtual - 1
        
        #Regulamento para 5 periodos - Equivalentes a 1 ano e 1 periodo
        if (periodoMinimo) > 0:
            anoMinimo = anoAtual - 1
        else:
            anoMinimo = anoAtual - 2
            periodoMinimo = 4
            

        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM 
                                (SELECT a.id, a.nome, (SELECT SUM(d2.cargahoraria)
                                FROM ppgi_disciplina d2, ppgi_aluno_disciplinascursadas dc2
                                WHERE dc2.aluno_id=a.id
                                AND d2.id=dc2.disciplina_id 
                                AND dc2.conceito NOT IN ('I', 'J', 'T', '0')) as choraria,
                                (SELECT SUM(d2.cargahoraria)
                                        FROM ppgi_disciplina d2, ppgi_aluno_disciplinascursadas dc2
                                        WHERE dc2.aluno_id=a.id
                                        AND d2.id=dc2.disciplina_id 
                                        AND dc2.conceito NOT IN ('I', 'J', 'T', '0')
                                        AND d2.nucleobasico=TRUE) as chorarianb
                                FROM ppgi_aluno a, ppgi_aluno_disciplinascursadas dc, ppgi_disciplina d
                                WHERE a.id=dc.aluno_id AND dc.disciplina_id=d.id
                                AND (a.anoingresso<='"""+str(anoMinimo-1)+"""' OR (a.anoingresso='"""+str(anoMinimo)+"""' 
                                AND a.periodoingresso<='"""+str(periodoMinimo)+"""'))
                                GROUP BY a.id) t 
                        WHERE t.choraria < 360 OR t.choraria IS NULL""")

        for linha in cursor.fetchall():
            idalunos.append(linha[0])
    
        return Aluno.objects.filter(id__in=idalunos)
        
    def irregularesMestrado(self):
        listaIds = []
        listaIdsIrregCRA = [a.pk for a in Aluno.objects.regulamentoMestradoCra()]
        listaIdsIrregCon = [a.pk for a in Aluno.objects.regulamentoMestradoConceito()]
        listaIdsIrregAbn = [a.pk for a in Aluno.objects.filter(situacaomatricula_id=SituacaoMatricula.objects.get(codigo='C03'))]
        listaIds.extend(listaIdsIrregCRA)
        listaIds.extend(listaIdsIrregCon)
        listaIds.extend(listaIdsIrregAbn)
        
        return Aluno.objects.filter(id__in=listaIds).filter(cursonivel='Mestrado')
    
    def irregularesDoutorado(self):
        listaIds = []
        listaIdsIrregCRA = [a.pk for a in Aluno.objects.regulamentoDoutoradoCra()]
        listaIdsIrregCon = [a.pk for a in Aluno.objects.regulamentoDoutoradoConceito()]
        listaIdsIrregAbn = [a.pk for a in Aluno.objects.filter(situacaomatricula_id=SituacaoMatricula.objects.get(codigo='C03'))]
        listaIds.extend(listaIdsIrregCRA)
        listaIds.extend(listaIdsIrregCon)
        listaIds.extend(listaIdsIrregAbn)
        
        return Aluno.objects.filter(id__in=listaIds).filter(cursonivel='Doutorado')
    
    def atualizarGrauEsperaBolsa(self):
        for a in Aluno.objects.all():
            if Aluno_DisciplinasCursadas.objects.filter(aluno_id=a.pk).exists():
                a.grauesperabolsa = a.calcularGrauEsperaBolsa()
                a.save()
    
class Aluno(models.Model):
    M = 'M'
    F = 'F'
    sexo_choices = ((M , 'Masculino'), (F, 'Feminino'))
    nivel_choices = (('Mestrado' , 'Mestrado'), ('Doutorado', 'Doutorado'))
    dre                 = models.IntegerField(unique=True, verbose_name='DRE')
    nome                = models.CharField(max_length=100, null = False)
    sexo                = models.CharField(max_length=1, choices=sexo_choices, null=False, default=M)
    cursonivel          = models.CharField(max_length=10, choices=nivel_choices, verbose_name='Nível')
    anoingresso         = models.IntegerField(max_length=4, verbose_name="Ano de Ingresso")
    periodoingresso     = models.IntegerField(max_length=1, verbose_name='Período de Ingresso')
    situacaomatricula   = models.ForeignKey(SituacaoMatricula, verbose_name='Situacao Matricula')
    grauingresso        = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name='Grau de Ingresso')
    grauesperabolsa     = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name='Grau de Espera por Bolsa')
    area                = models.ForeignKey(Area, null=True, blank=True)
    ouvinte             = models.BooleanField()
    permissaobolsa      = models.BooleanField(default=True, verbose_name='Permissão para receber bolsa')
    proficiencia        = models.BooleanField(default=False, verbose_name='Proficiência')
    qualificacao        = models.BooleanField(default=False, verbose_name='Qualificação')
    artigo              = models.BooleanField(default=False)
    
    objects = AlunoManager()
    
    def cra(self):
        cursor = connection.cursor()
        cursor.execute("""
            SELECT (SELECT SUM((dc2.conceito*dc2.creditos)/10)/SUM(dc2.creditos) 
                        FROM ppgi_disciplina d2, ppgi_aluno_disciplinascursadas dc2
                        WHERE dc2.aluno_id=a.id
                        AND (dc2.anoletivo < dc.anoletivo OR (dc2.anoletivo=dc.anoletivo AND dc2.periodoletivo <= dc.periodoletivo))
                        AND d2.id=dc2.disciplina_id 
                        AND dc2.conceito NOT IN ('I', 'J', 'T')) as cra
                FROM ppgi_aluno a, ppgi_aluno_disciplinascursadas dc, ppgi_disciplina d
                WHERE a.id=dc.aluno_id AND dc.disciplina_id=d.id AND a.id=%s 
                AND dc.anoletivo = (SELECT MAX(anoletivo) FROM ppgi_aluno_disciplinascursadas WHERE aluno_id=%s)
                AND dc.periodoletivo = (SELECT MAX(periodoletivo) FROM ppgi_aluno_disciplinascursadas 
                                        WHERE aluno_id=%s
                                        AND anoletivo=(SELECT MAX(anoletivo) FROM ppgi_aluno_disciplinascursadas WHERE aluno_id=%s))
                GROUP BY a.id, dc.anoletivo, dc.periodoletivo ORDER BY a.id """, [self.id, self.id, self.id, self.id])
       
        craAluno = cursor.fetchall()[0][0]

        if craAluno == None:
            craAluno = '0.00'
        #return "%.3f" %craAluno
        return round(float(craAluno), 3)
    
    def dicCraPeriodos(self):
        cursor = connection.cursor()
        cursor.execute("""
            SELECT dc.anoletivo, dc.periodoletivo, (SELECT SUM((dc2.conceito*dc2.creditos)/10)/SUM(dc2.creditos) 
                        FROM ppgi_disciplina d2, ppgi_aluno_disciplinascursadas dc2
                        WHERE dc2.aluno_id=a.id
                        AND (dc2.anoletivo < dc.anoletivo OR (dc2.anoletivo=dc.anoletivo AND dc2.periodoletivo <= dc.periodoletivo))
                        AND d2.id=dc2.disciplina_id 
                        AND dc2.conceito NOT IN ('I', 'J', 'T')) as cra
                FROM ppgi_aluno a, ppgi_aluno_disciplinascursadas dc, ppgi_disciplina d
                WHERE a.id=dc.aluno_id AND dc.disciplina_id=d.id AND a.id=%s 
                GROUP BY a.id, dc.anoletivo, dc.periodoletivo ORDER BY dc.anoletivo, dc.periodoletivo """, [self.id])
       
        dicCra = dict()
        
        for registro in cursor.fetchall():
            anoletivo = registro[0]
            craPeriodo = registro[2]
            if craPeriodo == None:
                craPeriodo = '0.00'
            else:
                craPeriodo = "%.2f" %craPeriodo
            dicCra.setdefault(anoletivo,[]).append(craPeriodo)  
            
        return dicCra
    
    def cargaHoraria(self):
        cursor = connection.cursor()
        cursor.execute("""SELECT t.choraria FROM 
                                (SELECT a.id, a.nome, (SELECT SUM(d2.cargahoraria)
                                    FROM ppgi_disciplina d2, ppgi_aluno_disciplinascursadas dc2
                                    WHERE dc2.aluno_id=a.id
                                    AND d2.id=dc2.disciplina_id 
                                    AND dc2.conceito NOT IN ('I', 'J', 'T', '0')) as choraria
                                FROM ppgi_aluno a, ppgi_aluno_disciplinascursadas dc, ppgi_disciplina d
                                WHERE a.id=dc.aluno_id AND dc.disciplina_id=d.id
                                AND a.id=%s
                                GROUP BY a.id) t """ % (self.id))
        
        linha = cursor.fetchall()[0]
        cHoraria = linha[0]
        if cHoraria == None:
            cHoraria = '0'
            
        return cHoraria
    
    def cargaHorariaNucleoBasico(self):
        cursor = connection.cursor()
        cursor.execute("""SELECT t.chorarianb FROM (SELECT a.id, a.nome,
                                (SELECT SUM(d2.cargahoraria)
                                        FROM ppgi_disciplina d2, ppgi_aluno_disciplinascursadas dc2
                                        WHERE dc2.aluno_id=a.id
                                        AND d2.id=dc2.disciplina_id 
                                        AND dc2.conceito NOT IN ('I', 'J', 'T', '0')
                                        AND d2.nucleobasico=TRUE) as chorarianb
                                FROM ppgi_aluno a, ppgi_aluno_disciplinascursadas dc, ppgi_disciplina d
                                WHERE a.id=dc.aluno_id AND dc.disciplina_id=d.id
                                AND a.id=%s
                                GROUP BY a.id) t """ % (self.id))
        
        linha = cursor.fetchall()[0]
        cHoraria = linha[0]
        if cHoraria == None:
            cHoraria = '0'
            
        return cHoraria
    
    def calcularGrauEsperaBolsa(self):

        numPeriodosDecorridos = getPeriodosDecorridos(self.anoingresso, self.periodoingresso)
        
        p = numPeriodosDecorridos*0.2
        
        if p > 0.8:
            p = 0.8
            
        
        grau = (self.cra() * (10.0/3) * p) + (float(self.grauingresso)*(1-p))
        
        return grau
    
    
    def __unicode__(self):
        return self.nome

class AlunoMestradoPrazoMax(Aluno):
    class Meta(object):
        proxy = True
        verbose_name_plural = 'Alunos com Prazo Máximo atingido - Mestrado'
        
class AlunoDoutoradoPrazoMax(Aluno):
    class Meta(object):
        proxy = True
        verbose_name_plural = 'Alunos com Prazo Máximo atingido - Doutorado'
        
class BolsistaMestrado(Aluno):
    class Meta(object):
        proxy = True
        verbose_name_plural = 'Bolsistas - Mestrado'
        
class BolsistaDoutorado(Aluno):
    class Meta(object):
        proxy = True
        verbose_name_plural = 'Bolsistas - Doutorado'
        
class AlunoMestradoIrregular(Aluno):
    class Meta(object):
        proxy = True
        verbose_name_plural = 'Alunos com matrícula irregular - Mestrado'

class AlunoDoutoradoIrregular(Aluno):
    class Meta(object):
        proxy = True
        verbose_name_plural = 'Alunos com matrícula irregular - Doutorado'
        
class AlunoMestradoEsperaBolsa(Aluno):
    class Meta(object):
        proxy = True
        verbose_name_plural = 'Lista de espera por Bolsa - Mestrado'
        
class AlunoDoutoradoEsperaBolsa(Aluno):
    class Meta(object):
        proxy = True
        verbose_name_plural = 'Lista de espera por Bolsa - Doutorado'
   
class Disciplina(models.Model):
    nivel_choices = (('Mestrado' , 'Mestrado'), ('Doutorado', 'Doutorado'))
    codigo          = models.CharField(max_length=20, unique=True)
    nome            = models.CharField(max_length=50)
    nivel           = models.CharField(max_length=10, choices=nivel_choices)
    creditos        = models.IntegerField(max_length=1)
    cargahoraria    = models.IntegerField(max_length=2, verbose_name='Carga Horária')
    nucleobasico    = models.BooleanField(default=False, verbose_name='Núcleo Básico')
    area            = models.ForeignKey(Area, null=True, blank=True)
    
    def __unicode__(self):
        return self.nome
    
class Aluno_DisciplinasCursadas(models.Model):
    aluno           = models.ForeignKey(Aluno)
    disciplina      = models.ForeignKey(Disciplina)
    anoletivo       = models.IntegerField(max_length=4)
    periodoletivo   = models.IntegerField(max_length=1)
    conceito        = models.CharField(max_length=4)
    situacaofinal   = models.CharField(max_length=4)
    creditos        = models.IntegerField(max_length=1)
    
    def __unicode__(self):
        return str(self.aluno) + "-" + str(self.disciplina) 

class Aluno_DisciplinaInconsistente(models.Model):
    aluno           = models.ForeignKey(Aluno)
    disciplina      = models.ForeignKey(Disciplina)
    
    class meta:
        unique_together = (('aluno', 'disciplina'),)
        
class Aluno_CRAAnoPeriodo(models.Model):
    aluno           = models.ForeignKey(Aluno)
    cra             = models.DecimalField(max_digits=3, decimal_places=2)
    ano             = models.IntegerField(max_length=4)
    periodoletivo   = models.IntegerField(max_length=1)
        
class Professor(models.Model):
    nome                = models.CharField(max_length=100)
    orientaDoutorado    = models.BooleanField(default=False)
    orientacao          = models.ManyToManyField(Aluno)
    
    class Meta(object):
        verbose_name_plural = 'Professores'
    
class OrgaoFomento(models.Model):
    nome        = models.CharField(max_length=50, unique=True)
    
    class Meta(object):
        verbose_name = 'Órgão de Fomento'
        verbose_name_plural = 'Orgãos de Fomento'
        
    def __unicode__(self):
        return self.nome

class Bolsa(models.Model):
    tipo_choices = (('Mestrado' , 'Mestrado'), ('Doutorado', 'Doutorado'))
    codigo      = models.CharField(max_length=15, unique=True, verbose_name='Código')
    orgao       = models.ForeignKey(OrgaoFomento, verbose_name='Órgão')
    area        = models.ForeignKey(Area, null=True, blank=True, verbose_name='Área')
    professor   = models.ForeignKey(Professor, blank=True, null=True)
    tipo        = models.CharField(max_length=10, choices=tipo_choices, default='Mestrado')
    aluno       = models.ForeignKey(Aluno, related_name='bolsista', null=True, blank=True, unique=True )
    datainicio  = models.DateField(null=True, blank=True)
    datafim     = models.DateField(null=True, blank=True)
    historico   = models.ManyToManyField(Aluno, related_name='bolsa_historico', through='Bolsa_Historico')
    
    def __unicode__(self):
        if self.area != None and self.area != "":
            return str(self.orgao) + " - " +str(self.area.sigla)+ " - " + str(self.codigo)
        else:
            return str(self.orgao) + " - " + str(self.codigo)
        

#Tabela de relacionamento entre bolsa e alunos. Uma bolsa pode pertencer a diferentes alunos em tempos distintos   
class Bolsa_Historico(models.Model):
    bolsa       = models.ForeignKey(Bolsa)
    aluno       = models.ForeignKey(Aluno, related_name='bolsa_historico_aluno')
    datainicio  = models.DateField()
    datafim     = models.DateField()

    
    