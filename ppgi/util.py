from django.utils.datetime_safe import datetime

def getPeriodo(mes):
    
    if mes >= 1 and mes <= 3:
        periodo = 1
    elif mes >= 4 and mes <=6:
        periodo = 2
    elif mes >= 7 and mes <= 9:
        periodo = 3
    elif mes >= 10 and mes <= 12:
        periodo = 4
        
    return periodo

def getPeriodosDecorridos(anoIngresso, periodoIngresso):
    mesAtual = datetime.now().month
    anoAtual = datetime.now().year
        
    periodosAnoAtual = getPeriodo(mesAtual)
        
    #desconsiderar periodoAtual
    numPeriodosDecorridos = ((anoAtual - anoIngresso)*4 - (periodoIngresso-1) + (periodosAnoAtual-1)) 
    
    return numPeriodosDecorridos

def htmlIconTrue():
    return "<center> <img src='/static/admin/img/icon-yes.gif' alt='True' />  </center>"

def htmlIconFalse():
    return "<center> <img src='/static/admin/img/icon-no.gif' alt='False' />  </center>"

def handle_uploaded_file(f, dest):
    destino = open(dest+'/'+f.name, 'wb+')

    for chunk in f.chunks():
        destino.write(chunk)
    destino.close()
    
    