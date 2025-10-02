from django.db import models

# =================================================================
# Models da Estrutura Organizacional
# =================================================================

class Filial(models.Model):
    # CharField = Campo de texto
    nome_filial = models.CharField(max_length=150, unique=True, verbose_name="Nome da Filial")

    def __str__(self):
        return self.nome_filial

    # Classe que ajusta o nome da tabela em caso de pluralidade
    class Meta:
        verbose_name = "Filial"
        verbose_name_plural = "Filiais"

class Departamento(models.Model):
    nome_departamento = models.CharField(max_length=150, verbose_name="Nome do Departamento")
    # ForeignKey = Chave Estrangeira (o campo que cria a LIGAÇÃO)
    # on_delete=models.CASCADE = Se a filial for apagada, apague os departamentos junto.
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome_departamento} ({self.filial.nome_filial})"

class Setor(models.Model):
    nome_setor = models.CharField(max_length=150, verbose_name="Nome do Setor")
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome_setor} ({self.departamento.nome_departamento} / {self.departamento.filial.nome_filial})"

    # Classe que ajusta o nome da tabela em caso de pluralidade
    class Meta:
        verbose_name = "Setor"
        verbose_name_plural = "Setores"

# =================================================================
# Models Principais do Inventário
# =================================================================

class Usuario(models.Model):
    # Adicionamos "verbose_name" para dar nomes mais amigáveis nos formulários do admin.
    matricula = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name="Matrícula")
    nome_usuario = models.CharField(max_length=255, verbose_name="Nome do Usuário")
    email = models.EmailField(unique=True, null=True, blank=True)
    cargo = models.CharField(max_length=150, null=True, blank=True)
    # null=True permite que o campo seja nulo no banco de dados.
    # blank=True permite que o campo seja deixado em branco nos formulários.
    grupo = models.CharField(max_length=5, null=True, blank=True)
    perfil_cargo = models.CharField(max_length=5, null=True, blank=True, verbose_name="Perfil do Cargo")
    setor = models.ForeignKey(Setor, on_delete=models.PROTECT) # PROTECT impede apagar setor se tiver usuário
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome_usuario

class Maquina(models.Model):
    patrimonio = models.CharField(max_length=100, unique=True, null=True, blank=True)
    hostname = models.CharField(max_length=150, unique=True)
    status = models.CharField(max_length=50, default='Em estoque')
    sistema_operacional = models.CharField(max_length=100, null=True, blank=True)
    processador = models.CharField(max_length=150, null=True, blank=True)
    # IntegerField = Campo de número inteiro
    ram_gb = models.IntegerField(null=True, blank=True, verbose_name="RAM (GB)")
    armazenamento_gb = models.IntegerField(null=True, blank=True, verbose_name="Armazenamento (GB)")
    # Ligação com o usuário (pode ser nula, significando "em estoque")
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    setor = models.ForeignKey(Setor, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return f"{self.hostname} ({self.patrimonio})"

# ... (Aqui entrarão os outros models: Monitores, Periféricos, etc., no futuro)
# Por agora, vamos focar nestes para garantir que o processo está claro.