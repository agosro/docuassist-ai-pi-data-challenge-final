from pydantic import BaseModel, Field
from typing import Optional

class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        description="Pregunta del usuario en lenguaje natural"
    )

    categoria_equipo: Optional[str] = Field(
        None,
        description="Categoría del equipo (impresora, balanza, etc.)"
    )

    tipo_documentacion: Optional[str] = Field(
        None,
        description="Tipo de documentación (tecnica o sistema)"
    )

    sistema: Optional[str] = Field(
        None, 
        description="Nombre del sistema/software (ej: StarPOSMarketManual)"
    )

    subtipo: Optional[str] = Field(
        None,
        description="Subtipo del equipo (fiscal, no_fiscal, electronica, etc.)"
    )

    marca: Optional[str] = Field(
        None,
        description="Marca del equipo (Hasar, Epson, Toledo, etc.)"
    )

    modelo: Optional[str] = Field(
        None,
        description="Modelo específico del equipo"
    )