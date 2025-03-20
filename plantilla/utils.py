from io import BytesIO
from django.http import HttpResponse
from docx import Document

def generar_documento_word(correspondencia_saliente):
    """Genera un documento Word a partir de un objeto CorrespondenciaSaliente."""

    doc = Document()
    doc.add_paragraph(f"La Paz {correspondencia_saliente.fecha_envio.strftime('%Y-%m-%d')}")
    doc.add_paragraph(correspondencia_saliente.cite)
    doc.add_paragraph(correspondencia_saliente.remitente.nombre)
    doc.add_paragraph(correspondencia_saliente.remitente.apellido)
    doc.add_paragraph(correspondencia_saliente.remitente.cargo)
    doc.add_paragraph(str(correspondencia_saliente.remitente.institucion))
    doc.add_paragraph("De nuestra mayor consideracion:")
    doc.add_paragraph(f"Ref.: {correspondencia_saliente.referencia}")
    doc.add_paragraph(correspondencia_saliente.descripcion)

    # Guardar el archivo en un buffer
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    # Devolver el archivo como respuesta
    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = f'attachment; filename=correspondencia_{correspondencia_saliente.cite}.docx'
    
    return response
