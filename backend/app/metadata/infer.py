def infer_metadata(doc_type: str, filename: str) -> dict:
    name = filename.lower()

    tipo_documentacion = "tecnica" if doc_type == "tecnicos" else "sistema"

    if "impresora" in name:
        categoria_equipo = "impresora"
    elif "balanza" in name:
        categoria_equipo = "balanza"
    else:
        categoria_equipo = "otro"

    if "hasar" in name:
        marca = "hasar"
    elif "epson" in name:
        marca = "epson"
    elif "toledo" in name:
        marca = "toledo"
    else:
        marca = "desconocida"

    if categoria_equipo == "impresora":
        if "fiscal" in name:
            subtipo = "fiscal"
        elif "no_fiscal" in name or "nofiscal" in name:
            subtipo = "no_fiscal"
        else:
            subtipo = "desconocido"
    else:
        subtipo = "desconocido"

    # 🔹 CLAVE
    if tipo_documentacion == "sistema":
        modelo = None
        sistema = filename.replace(".pdf", "")
    else:
        modelo = filename.replace(".pdf", "")
        sistema = None

    metadata = {
        "categoria_equipo": categoria_equipo,
        "tipo_documentacion": tipo_documentacion,
        "subtipo": subtipo,
        "marca": marca,
        "modelo": modelo,
        "sistema": sistema,
        "document": filename
    }

    metadata = {k: v for k, v in metadata.items() if v is not None}

    return metadata