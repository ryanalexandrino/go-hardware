from django.contrib import admin
from .models import Filial, Departamento, Setor, Usuario, Maquina

# Registrando os models para que eles apareçam na área de administração
# Cada linha abaixo faz um dos nossos "móveis" (tabelas) aparecer no painel.
admin.site.register(Filial)
admin.site.register(Departamento)
admin.site.register(Setor)
admin.site.register(Usuario)
admin.site.register(Maquina)