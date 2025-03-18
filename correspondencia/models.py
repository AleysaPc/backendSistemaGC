from django.db import models
from cliente.models import Cliente
from usuarios.models import Personal
from django.db import transaction
from django.core.validators import MinValueValidator

class TipoDocumento(models.Model):
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

    TIPO_CHOICES_ESTADO = [('en_revision', 'En revisión'), ('aprobado', 'Aprobado'), ('rechazado', 'Rechazado')]
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
    personal_destinatario = models.ForeignKey(Personal, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        abstract = False

    def __str__(self):
        return f"{self.referencia} " 
    
#Contardor para notas recibidas
class ContadorRegistroEntrante(models.Model):
    ultimo_registro = models.IntegerField(default=0)
class CorrespondenciaEntrante(Correspondencia):
    nro_registro = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.nro_registro:
            with transaction.atomic():
            # Bloquea el último registro para evitar concurrencia
                contador, created = ContadorRegistroEntrante.objects.select_for_update().get_or_create(id=1)
                contador.ultimo_registro += 1
                contador.save()
                self.nro_registro = f'Reg-{contador.ultimo_registro:03}'
    
        super().save(*args, **kwargs)

    fecha_recepcion = models.DateTimeField(blank=True, null=True)
    fecha_respuesta = models.DateTimeField(blank=True, null=True)

####Correspondencia Saliente
#Contador para cites
class ContadorCiteSaliente(models.Model):
    ultimo_cite = models.IntegerField(default=0)
class CorrespondenciaSaliente(Correspondencia):
    cite = models.CharField(max_length=50, blank=True, null=True)
    fecha_envio = models.DateTimeField(blank=True, null=True)
    fecha_recepcion = models.DateTimeField(blank=True, null=True)
    fecha_seguimiento = models.DateTimeField(blank=True, null=True)
    archivo_word = models.FileField(upload_to='documentos_borrador/', blank=True, null=True)
    
    def save(self, *args, **kwargs):
            if not self.cite:
                with transaction.atomic():
                    # Bloquea el último registro para evitar concurrencia
                    contador, created = ContadorCiteSaliente.objects.select_for_update().get_or_create(id=1)
                    contador.ultimo_cite += 1
                    contador.save()
                    self.cite = f'CITE:FTL-FTA/DLP/Nro.-{contador.ultimo_cite:04}'
            
            super().save(*args, **kwargs)

    def __str__(self):
            return f"{self.cite}"

class FlujoAprobacion(models.Model):

    ESTADO_CHOICES = [('pendiente', 'Pendiente'), ('aprobado', 'Aprobado'), ('rechazado', 'Rechazado')]

    correspondencia = models.ForeignKey(Correspondencia, on_delete=models.CASCADE, related_name='flujos_aprobacion')
    revisor = models.ForeignKey(Personal, on_delete=models.CASCADE)
    fecha_revision = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default="Pendiente")
    comentarios = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.revisor.usuario} - {self.estado}"

class DescargaDocumento(models.Model):
    usuario = models.ForeignKey(Personal, on_delete=models.CASCADE)
    documento = models.ForeignKey('CorrespondenciaSaliente', on_delete=models.CASCADE)
    fecha_descarga = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} descargó {self.documento.cite}"

#Por el  momento no lo estamos utilizando
class Notificacion(models.Model):

    ESTADO_NOTIFICACION_CHOICES = [('no_leido', 'No leido'), ('leido', 'Leido')]

    personal = models.ForeignKey(Personal, on_delete=models.CASCADE, related_name='notificaciones')
    mensaje = models.TextField()
    fecha_notificacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50)