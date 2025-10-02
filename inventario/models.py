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
        return f"{self.nome_setor} ({self.departamento.filial.nome_filial})"

    # Classe que ajusta o nome da tabela em caso de pluralidade
    class Meta:
        verbose_name = "Setor"
        verbose_name_plural = "Setores"

# =================================================================
# Models Principais do Inventário
# =================================================================

class Usuario(models.Model):
    # Adicionamos "verbose_name" para dar nomes mais amigáveis nos formulários do admin.
    cod_interno = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name="Código Interno")
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
    # --- OPÇÕES PARA OS CAMPOS DE ESCOLHA (DROPDOWNS) ---
    TIPO_CHOICES = [
        ('DT', 'Desktop'),
        ('NB', 'Notebook'),
        ('MP', 'Mini PC'),
    ]
    STATUS_CHOICES = [
        ('Em uso', 'Em uso'),
        ('Disponível', 'Disponível'),
        ('Em manutenção', 'Em manutenção')
    ]
    TIPO_ARMAZENAMENTO_CHOICES = [
        ('HDD', 'HDD'),
        ('SSD', 'SSD'),
        ('NVMe', 'NVMe'),
    ]
    GERACAO_MEMORIA_CHOICES = [
        ('DDR2', 'DDR2'),
        ('DDR3', 'DDR3'),
        ('DDR4', 'DDR4'),
        ('DDR5', 'DDR5'),
    ]

    # Identificação e Status
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES, default='NB', verbose_name="Tipo de Máquina")
    id_maquina = models.CharField(max_length=10, unique=True, editable=False, verbose_name="ID Interno")
    patrimonio = models.CharField(max_length=100, unique=True, null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Disponível')
    ativo = models.BooleanField(default=True)

    # Detalhes de Rede e Sistema
    hostname = models.CharField(max_length=150, unique=True)
    mac_address_lan = models.CharField(max_length=17, unique=True, null=True, blank=True,
                                       verbose_name="MAC Address LAN")
    mac_address_wifi = models.CharField(max_length=17, unique=True, null=True, blank=True,
                                        verbose_name="MAC Address Wi-Fi")
    dominio = models.CharField(max_length=100, null=True, blank=True, verbose_name="Domínio")
    sistema_operacional = models.CharField(max_length=100, null=True, blank=True, verbose_name="Sistema Operacional")

    # Detalhes de Hardware
    placa_mae = models.CharField(max_length=150, null=True, blank=True, verbose_name="Placa Mãe")
    processador = models.CharField(max_length=150, null=True, blank=True)
    geracao_memoria = models.CharField(max_length=4, choices=GERACAO_MEMORIA_CHOICES, null=True, blank=True,
                                       verbose_name="Geração da Memória")
    frequencia_memoria_mhz = models.IntegerField(null=True, blank=True,
                                                 verbose_name="Frequência da Memória (MHz)")
    ram_gb = models.IntegerField(null=True, blank=True, verbose_name="RAM (GB)")
    tipo_armazenamento = models.CharField(max_length=4, choices=TIPO_ARMAZENAMENTO_CHOICES, null=True, blank=True,
                                          verbose_name="Tipo de Armazenamento")  # CAMPO ATUALIZADO
    armazenamento_gb = models.IntegerField(null=True, blank=True, verbose_name="Armazenamento (GB)")

    # Alocação
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    setor = models.ForeignKey(Setor, on_delete=models.PROTECT, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            ultimo_id = Maquina.objects.filter(tipo=self.tipo).count()
            novo_id_numerico = ultimo_id + 1
            self.id_maquina = f"{self.tipo}-{novo_id_numerico:05d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id_maquina} ({self.hostname})"

# ... (Aqui entrarão os outros models: Monitores, Periféricos, etc., no futuro)
# Por agora, vamos focar nestes para garantir que o processo está claro.