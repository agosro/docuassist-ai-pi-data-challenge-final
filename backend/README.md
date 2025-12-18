# DocuAssist AI - Sistema RAG para Documentación Técnica

## 📖 Descripción del Proyecto

**DocuAssist AI** es un sistema de **Retrieval-Augmented Generation (RAG)** diseñado para asistir a empleados y técnicos de SERVIMAQ S.R.L. en la consulta de documentación técnica y manuales de sistemas.

El sistema procesa preguntas en lenguaje natural sobre:
- **Equipos técnicos**: Impresoras fiscales, balanzas electrónicas
- **Sistemas de software**: Manuales de configuración y uso de sistemas internos

### Características Principales

- ✅ **Clasificación de intenciones** mediante LangGraph (greeting, documentation, out_of_scope)
- ✅ **Filtros inteligentes** por categoría, marca, modelo y tipo de documentación
- ✅ **Reranking** con Cohere Rerank v4 para mejorar relevancia
- ✅ **Prompts dinámicos** (genéricos para categoría vs específicos para modelo)
- ✅ **Historial de conversaciones** persistente en SQLite
- ✅ **Guardrails pre-LLM** para detectar consultas prohibidas
- ✅ **API REST** documentada con FastAPI + Swagger
- ✅ **Tests automatizados** con pytest

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────┐
│     USUARIO → FastAPI (API REST)            │
└──────────────────┬──────────────────────────┘
                   │
         ┌─────────▼─────────┐
         │    LANGGRAPH      │
         │  (Orquestador)    │
         │ classify_intent   │
         └─────────┬─────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
    v              v              v
┌────────────┐ ┌─────────────┐ ┌──────────────┐
│conversational│ │documentation│ │out_of_scope │
│    node     │ │    node     │ │    node      │
└────────────┘ └──────┬──────┘ └──────────────┘
                      │
         ┌────────────┼────────────┐
         │            │            │
         v            v            v
    ┌────────┐  ┌─────────┐  ┌──────────┐
    │RETRIEVE│  │ RERANK  │  │ GENERATE │
    │ChromaDB│  │ Cohere  │  │  Cohere  │
    └────────┘  └─────────┘  └──────────┘
```

### Stack Tecnológico

| Componente | Tecnología | Descripción |
|------------|------------|-------------|
| **Backend** | FastAPI | Framework web con validación automática |
| **Orquestación** | LangGraph | Gestión de flujo conversacional con nodos |
| **LLM** | Cohere Command-R+ | Generación de respuestas y clasificación |
| **Embeddings** | Cohere Embed Multilingual v3 | Vectorización de documentos y queries |
| **Reranking** | Cohere Rerank v4 | Refinamiento de resultados por relevancia |
| **Vector DB** | ChromaDB | Almacenamiento persistente de embeddings |
| **Base de Datos** | SQLite | Historial y usuarios |
| **Testing** | pytest | Tests automatizados |

---

## 📁 Estructura del Proyecto

```
backend/
├── app/
│   ├── main.py                           # Entry point FastAPI
│   ├── api/
│   │   └── routes/
│   │       ├── chat_router.py            # POST /chat
│   │       └── history_router.py         # GET /history
│   ├── core/
│   │   └── config.py                     # Configuración (vacío)
│   ├── db/
│   │   ├── base.py                       # Base declarativa SQLAlchemy
│   │   ├── session.py                    # SessionLocal y engine
│   │   └── init_db.py                    # Script crear tablas
│   ├── graph/
│   │   ├── chat_graph.py                 # Definición del grafo LangGraph
│   │   ├── state.py                      # ChatState (TypedDict)
│   │   └── nodes/
│   │       ├── classify_intent.py        # Clasificación de intenciones
│   │       ├── conversational_node.py    # Respuestas conversacionales
│   │       ├── documentation_node.py     # Pipeline RAG completo
│   │       └── out_of_scope_node.py      # Respuestas fuera de alcance
│   ├── rag/
│   │   ├── retriever.py                  # Búsqueda semántica en ChromaDB
│   │   ├── reranker.py                   # Cohere Rerank
│   │   ├── generator.py                  # Generación de respuestas
│   │   ├── query_rewriter.py             # Reescritura de queries
│   │   ├── chunking.py                   # División de texto
│   │   └── prompts/
│   │       ├── intent_prompt.txt         # Prompt clasificación
│   │       ├── rag_prompt.txt            # Prompt específico (con modelo)
│   │       ├── rag_prompt_generic.txt    # Prompt genérico (sin modelo)
│   │       └── chat_prompt.txt           # Prompt conversacional
│   ├── metadata/
│   │   ├── infer.py                      # Extracción de metadata desde PDFs
│   │   ├── infer_filters.py              # Inferencia desde pregunta
│   │   ├── model_inference.py            # Inferencia de modelo
│   │   └── filter_resolution.py          # Merge de filtros
│   ├── vectorstore/
│   │   ├── client.py                     # Cliente ChromaDB
│   │   └── ingest.py                     # Script de ingesta de PDFs
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── base.py                       # Interfaz base LLM
│   │   └── cohere_client.py              # Implementación Cohere
│   ├── services/
│   │   ├── chat_service.py               # Lógica principal de chat
│   │   └── history_service.py            # Gestión de historial
│   ├── models/
│   │   └── history_model.py              # Modelo SQLAlchemy History
│   ├── repository/
│   │   └── history_repository.py         # Acceso a datos de historial
│   ├── schemas/
│   │   ├── chat.py                       # ChatRequest (Pydantic)
│   │   └── response.py                   # ChatResponse
│   ├── utils/
│   │   └── rag_validation.py             # Validaciones de chunks
│   ├── guardrails/
│   │   └── pre_llm.py                    # Detección de consultas prohibidas
│   └── debug/
│       ├── test_graph.py                 # Tests del grafo
│       └── test_retriever.py             # Tests del retriever
├── chroma_db/                            # Base de datos vectorial (generada)
├── data/
│   └── pdfs/
│       ├── tecnicos/                     # Manuales técnicos de equipos
│       └── sistemas/                     # Manuales de software
├── tests/
│   └── test_chat_flow.py                 # Tests principales
├── requirements.txt                      # Dependencias del proyecto
└── README.md                             # Este archivo
```

---

## 🚀 Instalación y Configuración

### Requisitos Previos

- Python 3.10+
- pip
- Cuenta en Cohere con API key

### Paso 1: Crear entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Paso 2: Instalar dependencias

```bash
pip install -r requirements.txt
```

**Dependencias principales:**
```
fastapi
uvicorn
python-dotenv
langchain
langgraph
cohere
chromadb
pypdf
langchain-text-splitters
sqlalchemy
pytest
```

### Paso 3: Configurar variables de entorno

Crear archivo `.env` en la raíz del proyecto:

```env
COHERE_API_KEY=tu_api_key_aqui
```

### Paso 4: Verificar la base de datos

El proyecto ya incluye `app.db` con la tabla `history` configurada. Si necesitas recrearla:

```bash
python -m app.db.init_db
```

### Paso 5: Preparar documentación (solo si usas tus propios PDFs)

**Nota:** El proyecto ya incluye ChromaDB pre-cargado en `chroma_db/`.

Si deseas usar tus propios documentos:
1. Coloca los PDFs en:
   - `data/pdfs/tecnicos/` → Manuales técnicos de equipos
   - `data/pdfs/sistemas/` → Manuales de sistemas/software

2. Ejecuta la ingesta:
```bash
python -m app.vectorstore.ingest
```

Este proceso:
- Lee los PDFs de `data/pdfs/`
- Extrae metadata automáticamente del nombre del archivo
- Genera embeddings con Cohere Embed v3
- Almacena en ChromaDB (`chroma_db/`)

---

## ▶️ Ejecución

### Iniciar el servidor

```bash
uvicorn app.main:app --reload
```

El servidor estará disponible en: **http://localhost:8000**

### Endpoints disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health` | Health check del servicio |
| POST | `/chat` | Endpoint principal de chat |
| GET | `/history` | Obtener historial de conversaciones |
| GET | `/docs` | Documentación Swagger interactiva |

### Documentación interactiva

Swagger UI: **http://localhost:8000/docs**

---

## 🧪 Testing

### Ejecutar tests

```bash
pytest tests/ -v
```

### Tests implementados

Los tests en [tests/test_chat_flow.py](tests/test_chat_flow.py) cubren:

```python
✅ test_greeting()           # Saludo conversacional (sin RAG)
✅ test_out_of_scope()       # Pregunta fuera de alcance
✅ test_system_question()    # Documentación de software
✅ test_technical_question() # Pregunta técnica específica
```

---

## 📊 Uso de la API

### POST /chat

**Esquema de Request (ChatRequest):**
```json
{
  "question": "string",              // REQUERIDO
  "categoria_equipo": "string",      // Opcional: impresora, balanza, etc.
  "tipo_documentacion": "string",    // Opcional: tecnica, sistema
  "sistema": "string",               // Opcional: nombre del sistema
  "subtipo": "string",               // Opcional: fiscal, no_fiscal, etc.
  "marca": "string",                 // Opcional: hasar, epson, toledo
  "modelo": "string"                 // Opcional: 320F, 2098, etc.
}
```

**Esquema de Response (ChatResponse):**
```json
{
  "answer": "string",
  "sources": [
    {
      "document": "string",
      "page": "integer"
    }
  ],
  "images": [],
  "used_rag": "boolean"
}
```

### Ejemplos de uso

#### 1. Saludo simple (sin RAG)

**Request:**
```json
{
  "question": "Hola"
}
```

**Response:**
```json
{
  "answer": "¡Hola! Soy el asistente de documentación técnica. ¿En qué puedo ayudarte?",
  "sources": [],
  "images": [],
  "used_rag": false
}
```

#### 2. Pregunta técnica específica con filtros explícitos

**Request:**
```json
{
  "question": "¿Cómo cambio la IP?",
  "marca": "hasar",
  "modelo": "320F",
  "categoria_equipo": "impresora"
}
```

**Response:**
```json
{
  "answer": "Para cambiar la dirección IP de la impresora Hasar 320F...",
  "sources": [
    {
      "document": "Impresora_Hasar_320F_Manual.pdf",
      "page": 45
    }
  ],
  "images": [],
  "used_rag": true
}
```

#### 3. Pregunta con inferencia automática de modelo

**Request:**
```json
{
  "question": "¿Cómo cambiar IP en la tmt20?"
}
```

**Inferencia automática (Nivel 1 - model_inference.py):**
El sistema detecta "tmt20" normalizado y lo mapea a:
```python
{
  "marca": "epson",
  "modelo": "Impresora_NO_fiscal_Epson_TM-T20",
  "categoria_equipo": "impresora"
}
```

Luego busca documentación específica de ese modelo.

#### 3b. Pregunta con inferencia de sistema

**Request:**
```json
{
  "question": "¿Cómo realizar cierre Z en StarPOS Market?"
}
```

**Inferencia automática (Nivel 2 - infer_filters.py):**
```python
{
  "sistema": "StarPOSMarketManual",
  "tipo_documentacion": "sistema"
}
```

#### 4. Pregunta sin documentación disponible

**Request:**
```json
{
  "question": "¿Qué mantenimientos necesita una impresora fiscal?",
  "categoria_equipo": "impresora",
  "subtipo": "fiscal"
}
```

Si no hay documentación específica en la base de datos para esta consulta genérica, el sistema:
- Intenta buscar en la documentación disponible
- Si no encuentra suficiente información relevante, informa que no tiene documentación específica

#### 5. Pregunta sobre sistema de software

**Request:**
```json
{
  "question": "¿Cómo agregar un producto al sistema StarPOS?",
  "tipo_documentacion": "sistema",
  "sistema": "StarPOSMarketManual"
}
```

#### 6. Pregunta fuera de alcance

**Request:**
```json
{
  "question": "¿Cuál es la capital de Francia?"
}
```

**Response:**
```json
{
  "answer": "Lo siento, solo puedo responder consultas relacionadas con documentación técnica y sistemas internos.",
  "sources": [],
  "images": [],
  "used_rag": false
}
```

---

## 🔍 Flujo de Procesamiento Detallado (Optimizado)

### Flujo Completo

```
1. USER → POST /chat
2. chat_router.py recibe request
3. ✅ Guardrails pre-LLM
4. ChatService.handle_question()
5. LangGraph ejecuta el grafo
6. classify_intent
   ├─ greeting → conversational_node (sin RAG, sin inferencia)
   ├─ out_of_scope → out_of_scope_node (sin RAG, sin inferencia)
   └─ documentation → documentation_node
       ├─ 🔍 AQUÍ SE INFIEREN FILTROS (solo si es necesario)
       ├─ Merge con filtros explícitos
       ├─ Pipeline RAG completo
       └─ Retorna respuesta + filtros finales
7. Guardar historial (con filtros finales)
8. Retornar respuesta al usuario
```

### 1. Guardrails Pre-LLM

Antes de enviar al LLM, se valida que la consulta no contenga patrones prohibidos:

```python
# app/guardrails/pre_llm.py
forbidden_patterns = [
    "ignora", "ignorá", "evadir",
    "respondé en inglés", "emojis",
    "mezclá", "usa conocimiento general"
]
```

Si se detecta, retorna mensaje de rechazo sin procesar.

### 2. Clasificación de Intenciones

```python
# classify_intent node (LangGraph)
Input: "Hola, ¿cómo estás?"
    ↓
LLM (temp=0.0) → "greeting"
    ↓
Router → conversational_node (✅ NO infiere filtros)
```

**Tipos de intención:**
- `greeting`: Saludos, despedidas → respuesta directa (SIN inferencia de filtros)
- `documentation`: Consultas técnicas → pipeline RAG (CON inferencia de filtros)
- `out_of_scope`: Fuera del dominio → rechazo educado (SIN inferencia de filtros)

### 3. Inferencia y Merge de Filtros (SOLO en documentation_node)

**⚡ OPTIMIZACIÓN:** Los filtros solo se infieren si `intent === "documentation"`

**Sistema de Inferencia de Filtros (Dos Niveles):**

**Nivel 1 - Inferencia de Modelos Específicos** (`model_inference.py` en el router):
- Detecta aliases de modelos en la pregunta:
  - "smhpt250f" → `{marca: "hasar", modelo: "Impresora_fiscal_Hasar_SMH-PT-250F", subtipo: "fiscal"}`
  - "smhp441f" → `{marca: "hasar", modelo: "Impresora_fiscal_Hasar_SMH-P-441F", subtipo: "fiscal"}`
  - "tmt20" → `{marca: "epson", modelo: "Impresora_NO_fiscal_Epson_TM-T20"}`
- Se ejecuta ANTES de pasar al ChatService
- Normaliza texto removiendo caracteres especiales para mejor matching

**Nivel 2 - Inferencia General** (`infer_filters.py` en documentation_node):
- `categoria_equipo`: Detecta "impresora", "balanza" en la pregunta
- `tipo_documentacion`: 
  - "sistema" si detecta palabras como "configurar", "instalar", "usar", "cargar", "cierre"
  - "tecnica" si detecta "especificaciones", "características", "tecnicas"
- `sistema`: Detecta nombres predefinidos usando diccionario con regex flexible:
  - "starpos", "star pos", "starpos market" → "StarPOSMarketManual"
  - "backupmaster", "backup master" → "BackupMaster"
  - "cloudsync", "cloud sync" → "CloudSync"
  - "datavault", "data vault" → "DataVault"

**Prioridad de Merge:**
Los filtros explícitos del frontend tienen prioridad absoluta. Los inferidos solo se usan si el filtro correspondiente está vacío (`None`).

```python
# Solo se ejecuta dentro de documentation_node

# 1. Filtros explícitos (del frontend)
explicit = {
    "marca": "hasar",
    "modelo": "320F"
}

# 2. Filtros inferidos de la pregunta
# Pregunta: "¿Cómo realizar un cierre Z en StarPOS Market?"
inferred = infer_filters_from_question(pregunta)
# → { 
#     "tipo_documentacion": "sistema",      (por "cierre")
#     "sistema": "StarPOSMarketManual"      (por "starpos market")
# }

# 3. Merge (explícitos tienen prioridad)
final = merge_filters(explicit, inferred)
# → { "marca": "hasar", "modelo": "320F", "tipo_documentacion": "sistema" }
```

### 4. Pipeline RAG (documentation_node)

**a) Query Rewriting:**
```python
# Enriquece la query con contexto
"¿Cómo cambiar IP?"
    ↓
"¿Cómo cambiar IP? hasar 320F"
```

**b) Retrieve:**
```python
# app/rag/retriever.py
- Embedding de query con Cohere Embed v3
- Búsqueda en ChromaDB con filtros de metadata
- Post-filtrado estricto por modelo (si aplica)
- Top 10-30 chunks (variable según tipo de doc)
```

**c) Validación y Filtrado:**
```python
# app/utils/rag_validation.py
if modelo:
    chunks = filter_chunks_by_model(chunks, modelo)
if sistema:
    chunks = filter_chunks_by_system(chunks, sistema)
```

**d) Rerank:**
```python
# app/rag/reranker.py
- Cohere Rerank v4
- Relevance score
- Top 5 chunks finales
```

**e) Generate:**
```python
# app/rag/generator.py
- Selección de prompt (genérico vs específico)
- Formateo del contexto
- Generación con Cohere Command-R+
- Extracción de fuentes (documento + página)
```

### 5. Persistencia del Historial

```python
# app/services/history_service.py
history_service.save_interaction(
    db=db,
    question=question,
    answer=answer
)
```

Guarda en tabla `history` de SQLite.

---

## 🎯 Características Avanzadas

### Prompts Dinámicos

El sistema utiliza **2 tipos de prompts** según el contexto:

**1. Prompt Específico** (`rag_prompt.txt`)
- Usado cuando hay marca + modelo explícito
- Incluye variables `{marca}` y `{modelo}` en el contexto
- Respuestas altamente específicas al equipo

**2. Prompt Genérico** (`rag_prompt_generic.txt`)
- Usado para consultas de categoría sin modelo
- Respuestas generales sobre tipos de equipos
- Ej: "¿Qué mantenimientos necesita una impresora fiscal?"

### Filtrado Estricto por Modelo

```python
# Triple validación de modelo:
1. WHERE clause en ChromaDB
2. Post-filtro en retriever.py
3. Validación final en generator.py
```

Garantiza que NUNCA se mezcle información de modelos diferentes.

### Fallback para Documentación de Sistemas

```python
if tipo_doc == "sistema" and len(chunks) < 5:
    # Ampliar búsqueda
    chunks = retriever.retrieve(top_k=30)
```

Los manuales de software tienen estructura diferente, por lo que se permite mayor cantidad de chunks para capturar contexto completo.

### Validación de Modelo Único

```python
# app/utils/rag_validation.py
def validate_single_model(chunks):
    modelos = {c["metadata"].get("modelo") for c in chunks}
    if len(modelos) > 1:
        # Retorna solo el modelo más frecuente
```

Evita contaminación cruzada entre modelos similares.

---

## 📂 Metadata de Documentos

### Estructura de Metadata

Cada chunk en ChromaDB tiene la siguiente metadata:

```python
{
    "document": "Impresora_Hasar_320F_Manual.pdf",
    "page": 12,
    "categoria_equipo": "impresora",
    "tipo_documentacion": "tecnica",
    "subtipo": "fiscal",
    "marca": "hasar",
    "modelo": "320F",           # Solo docs técnicos
    "sistema": None             # Solo docs de software
}
```

### Inferencia Automática

La metadata se infiere automáticamente del nombre del archivo durante la ingesta:

```python
# app/metadata/infer.py
"Impresora_Hasar_320F_Manual.pdf"
    ↓
{
    "categoria_equipo": "impresora",
    "marca": "hasar",
    "modelo": "320F",
    "subtipo": "fiscal"  # si contiene "fiscal" en el nombre
}
```

---

## 🗄️ Base de Datos

### Tablas SQLAlchemy

**History**
```python
# app/models/history_model.py
- id: Integer (PK)
- question: Text
- answer: Text
- created_at: DateTime
- tipo_documentacion: String (nullable)
- sistema: String (nullable)
- subtipo: String (nullable)
- marca: String (nullable)
- modelo: String (nullable)
```

Estos campos adicionales se agregaron para almacenar metadata de cada consulta.

### Inicialización

```bash
# Crear tablas
python -m app.db.init_db
```

---

## 🛠️ Scripts de Utilidad

### Ingesta de Documentos

```bash
python -m app.vectorstore.ingest
```

Procesa todos los PDFs en `data/pdfs/` y los almacena en ChromaDB.

**Características:**
- Procesa páginas completas de cada PDF
- Chunking inteligente con overlapping
- Rate limiting para evitar errores de API
- Batch processing (10 chunks a la vez)

### Debug del Retriever

```bash
python -m app.debug.test_retriever
```

Permite probar el retriever con queries específicas.

### Debug del Grafo

```bash
python -m app.debug.test_graph
```

Prueba el flujo completo del LangGraph con una pregunta de ejemplo.

---

## 📋 Variables de Entorno

```env
# .env
COHERE_API_KEY=tu_api_key_aqui
```

**Nota:** No se necesitan otras variables de configuración. El proyecto usa SQLite local y ChromaDB persistente en disco.


---

## 🎯 Requisitos del Challenge (Cumplimiento)

### Requisitos Obligatorios

| Requisito | Estado | Implementación |
|-----------|--------|----------------|
| Funcionamiento completo end-to-end | ✅ | Pipeline completo |
| API REST | ✅ | FastAPI + Swagger |
| 3+ preguntas test | ✅ | 4 tests unitarios |
| >100k caracteres | ✅ | ~187k caracteres |
| Vector DB persistente | ✅ | ChromaDB precargada |
| Solo temas pertinentes | ✅ | `out_of_scope_node` |
| Sin emojis | ✅ | Validado en prompts |
| Siempre español | ✅ | Forzado en prompts |
| Respuestas consistentes | ✅ | Sin temperatura aleatoria |

### Innovaciones Implementadas

| Innovación | Implementación |
|-----------|----------------|
| ✅ Reranking | Cohere Rerank v4 |
| ✅ Historial | SQLite + SQLAlchemy |
| ✅ Orquestador LLM | LangGraph con classify_intent |
| ✅ Framework IA | LangGraph |
| ✅ Metadata avanzada | Filtros multi-criterio en ChromaDB |
| ✅ Técnicas avanzadas | Inferencia automática de filtros |

---

## 🔧 Troubleshooting

### Error: "No module named 'cohere'"
```bash
pip install cohere
```

### Error: ChromaDB no encuentra documentos
```bash
# Re-ejecutar ingesta
python -m app.vectorstore.ingest
```

### Error: "Invalid API key"
Verificar que `.env` tenga tu Cohere API key válida

### API responde lento
- Primera llamada siempre es más lenta (cold start de Cohere)
- Siguientes llamadas ~2-3 segundos

---

## 🚀 Mejoras Futuras

- [ ] Fine-tuning de embeddings para dominio específico
- [ ] Búsqueda híbrida (semántica + keywords BM25)
- [ ] Feedback loop (👍/👎 para mejorar prompts)
- [ ] Multi-idioma (inglés, portugués)
- [ ] Integración con APIs externas (stock, precios)
- [ ] Dashboard de analytics del historial
- [ ] Cache de respuestas frecuentes
- [ ] Multi-tenancy para múltiples empresas

---


## 👤 Autor

**Agostina Torres**  
Get Talent - Pi Data  
Challenge Final - Diciembre 2025

---

