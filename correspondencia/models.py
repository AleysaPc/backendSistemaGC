from django.db import models
from cliente.models import Cliente
from django.db import transaction
from django.core.validators import MinValueValidator
from django.utils.timezone import now
from usuarios.models import CustomUser as User
#TipoDocumento debemos revisar?
class TipoDocumento(models.Model):
    id_tipo_documento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre
    @staticmethod
    def cargar_tipos_documento():
        """Carga automáticamente los tipos de documentos con sus descripciones si no existen en la BD"""
        tipos = [
            ("Memorando", "Comunicación interna entre áreas de la organización."),
            ("Oficio", "Documento formal dirigido a entidades externas."),
            ("Carta", "Comunicación formal entre instituciones o personas."),
            ("Informe", "Documento con análisis o reportes sobre un tema específico."),
            ("Acta", "Registro oficial de reuniones o decisiones tomadas."),
            ("Resolución", "Documento que expresa una decisión oficial."),
            ("Circular", "Comunicación masiva para informar sobre disposiciones o novedades."),
        ]

        for nombre, descripcion in tipos:
            TipoDocumento.objects.get_or_create(nombre=nombre, defaults={"descripcion": descripcion})

class Correspondencia(models.Model):
    id_correspondencia = models.AutoField(primary_key=True)

    TIPO_CHOICES_ESTADO = [('borrador', 'Borrador'),('en_revision', 'En revisión'), ('aprobado', 'Aprobado'), ('rechazado', 'Rechazado')]
    TIPO_CHOICES_PRIORIDAD = [('alta', 'Alta'), ('media', 'Media'), ('baja', 'Baja')]

    fecha_registro = models.DateTimeField(auto_now_add=True)
    remitente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    referencia = models.CharField(max_length=255)
    descripcion = models.TextField()
    paginas = models.IntegerField(validators=[MinValueValidator(1)], null=True, blank=True)
    #tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.SET_NULL, null=True)
    documento = models.ForeignKey('documento.Documento', on_delete=models.SET_NULL, null=True, blank=True, related_name="correspondencias_relacionadas")
    prioridad = models.CharField(max_length=20, choices=TIPO_CHOICES_PRIORIDAD)
    estado = models.CharField(max_length=20, choices=TIPO_CHOICES_ESTADO, default='en_revision')
    personal_destinatario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        abstract = False

    def __str__(self):
        return f"{self.referencia} " 
      
class CorrespondenciaEntrante(Correspondencia):
    id_correspondencia_entrante = models.AutoField(primary_key=True)
    nro_registro = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.nro_registro:
            with transaction.atomic():
                # Obtiene el último número de registro
                ultimo = CorrespondenciaEntrante.objects.order_by('-id_correspondencia_entrante').first()
                nuevo_numero = (int(ultimo.nro_registro.split('-')[1]) + 1 if ultimo and ultimo.nro_registro else 1)
                self.nro_registro = f'Reg-{nuevo_numero:03}'
    
        super().save(*args, **kwargs)

    fecha_recepcion = models.DateTimeField(blank=True, null=True)
    fecha_respuesta = models.DateTimeField(blank=True, null=True)

class CorrespondenciaSaliente(Correspondencia):
    id_correspondencia_saliente = models.AutoField(primary_key=True)
    cite = models.CharField(max_length=50, blank=True, null=True)
    fecha_envio = models.DateTimeField(blank=True, null=True)
    fecha_recepcion = models.DateTimeField(blank=True, null=True)
    fecha_seguimiento = models.DateTimeField(blank=True, null=True)
    archivo_word = models.FileField(upload_to='documentos_borrador/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.cite:
            with transaction.atomic():
                # Obtiene el último cite registrado y lo incrementa
                ultimo = CorrespondenciaSaliente.objects.order_by('-id_corres   pondencia_saliente').first()
                nuevo_cite = (int(ultimo.cite.split('-')[-1]) + 1 if ultimo and ultimo.cite else 1)
                self.cite = f'CITE:FTL-FTA/DLP/Nro.-{nuevo_cite:04}'

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cite}"

class TipoDocumentoInterno(models.Model):
    id_tipo_documento_interno = models.AutoField(primary_key=True)
    nombre  = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.nombre

class CorrespondenciaInterna(models.Model):
    id_correspondencia_interna = models.AutoField(primary_key=True)
    tipo = models.ForeignKey(TipoDocumentoInterno, on_delete=models.CASCADE)
    numero = models.PositiveIntegerField(editable=False)  # Número secuencial único
    gestion = models.PositiveIntegerField(default=now().year, editable=False)  # Año de gestión
    cite = models.CharField(max_length=100, unique=True, blank=True)  # Código único del documento
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    contenido = models.TextField()
    personal_destinatario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('tipo', 'numero', 'gestion')  # Evita duplicados por tipo y año

    def save(self, *args, **kwargs):
        if not self.id_correspondencia_interna:  # Si es un nuevo documento
            # Buscar el último número registrado del mismo tipo y año
            ultimo_documento = CorrespondenciaInterna.objects.filter(
                tipo=self.tipo, 
                gestion=self.gestion
            ).order_by('-numero').first()

            # Si existe un documento previo, incrementar el número; de lo contrario, iniciar en 1
            self.numero = (ultimo_documento.numero + 1) if ultimo_documento else 1

            # Generar el código CITE
            self.cite = f"{self.tipo.nombre[:3].upper()}-{self.numero:03d}/{self.gestion}"

        super().save(*args, **kwargs)  # Guardar en la BD

    def __str__(self):
        return f"{self.cite} - {self.tipo.nombre}"

#Por el  momento no los estamos utilizando
class Notificacion(models.Model):
    id_notificacion = models.AutoField(primary_key=True)

    ESTADO_NOTIFICACION_CHOICES = [('no_leido', 'No leido'), ('leido', 'Leido')]

    personal = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones')
    mensaje = models.TextField()
    fecha_notificacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50)

class FlujoAprobacion(models.Model):
    id_flujo_aprobacion = models.AutoField(primary_key=True)

    ESTADO_CHOICES = [('pendiente', 'Pendiente'), ('aprobado', 'Aprobado'), ('rechazado', 'Rechazado')]

    correspondencia = models.ForeignKey(Correspondencia, on_delete=models.CASCADE, related_name='flujos_aprobacion')
    revisor = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_revision = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default="Pendiente")
    comentarios = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.revisor.username} - {self.estado}"