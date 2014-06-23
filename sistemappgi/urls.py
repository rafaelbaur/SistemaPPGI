from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'ppgi.views.index'),
    url(r'^admin/ppgi/cancelamentoMatricula/$', 'ppgi.views.sugerirCancelamentoMatricula'),
    url(r'^admin/ppgi/(aluno|alunomestradoirregular|alunomestradoprazomax|alunomestradoesperabolsa|bolsistamestrado)/visualizar/$', 'ppgi.views.visualizarAluno'),
    url(r'^admin/ppgi/(alunodoutoradoirregular|alunodoutoradoprazomax|bolsistadoutorado|alunodoutoradoesperabolsa)/visualizar/$', 'ppgi.views.visualizarAluno'),
    url(r'^admin/ppgi/(bolsista)/visualizar/$', 'ppgi.views.visualizarAluno'),
    url(r'^admin/ppgi/(alunomestradoirregular|alunodoutoradoirregular)/print/$', 'ppgi.views.printAlunoIrregular'),
    url(r'^admin/ppgi/(alunomestradoprazomax|alunodoutoradoprazomax)/print/$', 'ppgi.views.printAlunoPrazoMax'),
    url(r'^admin/ppgi/(alunomestradoesperabolsa|alunodoutoradoesperabolsa)/ajax_alunoInfo/$', 'ppgi.views.ajax_alunoInfo'),
    url(r'^admin/ppgi/(alunomestradoesperabolsa|alunodoutoradoesperabolsa)/alocarBolsa/$', 'ppgi.views.alocarBolsa'),
    url(r'^admin/ppgi/(bolsistamestrado|bolsistadoutorado)/desalocarBolsa/$', 'ppgi.views.desalocarBolsa'),
    url(r'^admin/ppgi/uploadDadosPpgi/$', 'ppgi.views.uploadDadosPpgi', name="uploadDadosPpgi"),
    url(r'^admin/ppgi/inicializarBD/$', 'ppgi.views.inicializarBD'),
    url(r'^admin/ppgi/inicializarBD/inicializar/$', 'ppgi.views.ajax_inicializarBD'),
    url(r'^admin/ppgi/(alunomestradoesperabolsa|alunodoutoradoesperabolsa)/atualizarGrauEsperaBolsa/$', 'ppgi.views.atualizarGrauEsperaBolsa', name='atualizarGrauEsperaBolsa'),
    
    
    # Examples:
    # url(r'^$', 'sistemappgi.views.home', name='home'),
    # url(r'^sistemappgi/', include('sistemappgi.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', 'index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
)


from sistemappgi import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',  
         {'document_root':     settings.MEDIA_ROOT}),
    )
