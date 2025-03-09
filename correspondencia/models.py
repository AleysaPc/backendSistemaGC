from django.db import models
from cliente.models import Cliente
from usuarios.models import Personal
from django.db import transaction
from django.db.models import F


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

    TIPO_CHOICES_PRIORIDAD = [('alta', 'Alta'), ('media', 'Media'), ('baja', 'Baja')]

    fecha_registro = models.DateTimeField(auto_now_add=True)
    remitente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    referencia = models.CharField(max_length=255)
    descripcion = models.TextField()
    paginas = models.IntegerField()
    #tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.SET_NULL, null=True)
    documento = models.ForeignKey('documento.Documento', on_delete=models.SET_NULL, null=True, related_name="correspondencias_relacionadas")
    prioridad = models.CharField(max_length=20, choices=TIPO_CHOICES_PRIORIDAD)
    estado = models.CharField(max_length=50)
    personal_destinatario = models.ForeignKey(Personal, on_delete=models.SET_NULL, null=True)
    

    
    def __str__(self):
        return f"{self.referencia}"
        
class CorrespondenciaEntrante(models.Model):
    nro_registro = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.nro_registro:
            with transaction.atomic():
            # Bloquea el último registro para evitar concurrencia
                last_record = CorrespondenciaEntrante.objects.select_for_update().order_by('-nro_registro').first()
            if last_record:
                # Extrae el número del último registro y lo incrementa
                last_number = int(last_record.nro_registro.split('-')[-1])
                self.nro_registro = f'Reg-{last_number + 1:03}'
            else:
                # Si no hay registros, comienza con "Reg-001"
                self.nro_registro = 'Reg-001'
    
        super().save(*args, **kwargs)

    fecha_recepcion = models.DateTimeField(blank=True, null=True)
    fecha_respuesta = models.DateTimeField(blank=True, null=True)
    correspondencia = models.OneToOneField(Correspondencia, on_delete=models.CASCADE, related_name='entrantes')

class CorrespondenciaSaliente(models.Model):
    cite = models.CharField(max_length=50, blank=True, null=True)
    fecha_hora_envio = models.DateTimeField(blank=True, null=True)
    fecha_hora_confirmacion_recepcion = models.DateTimeField(blank=True, null=True)
    fecha_proximo_seguimiento = models.DateTimeField(blank=True, null=True)
    correspondencia = models.OneToOneField(Correspondencia, on_delete=models.CASCADE, related_name='saliente')

class FlujoAprobacion(models.Model):

    ESTADO_CHOICES = [('pendiente', 'Pendiente'), ('aprobado', 'Aprobado'), ('rechazado', 'Rechazado')]

    correspondencia = models.ForeignKey(Correspondencia, on_delete=models.CASCADE, related_name='flujos_aprobacion')
    revisor = models.ForeignKey(Personal, on_delete=models.CASCADE)
    fecha_revision = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default="Pendiente")
    comentarios = models.TextField(blank=True, null=True)

class Notificacion(models.Model):

    ESTADO_NOTIFICACION_CHOICES = [('no_leido', 'No leido'), ('leido', 'Leido')]

    personal = models.ForeignKey(Personal, on_delete=models.CASCADE, related_name='notificaciones')
    mensaje = models.TextField()
    fecha_notificacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50)