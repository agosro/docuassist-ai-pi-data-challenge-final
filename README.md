# 📚 DocuAssist AI - Sistema RAG para Documentación Técnica

> **Sistema inteligente de consulta de documentación técnica usando Retrieval-Augmented Generation (RAG)**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18%2B-61dafb)](https://react.dev/)
[![Cohere](https://img.shields.io/badge/Cohere-API-orange)](https://cohere.com/)
[![License](https://img.shields.io/badge/License-MIT-black)](LICENSE)

---

## 🎯 Descripción del Proyecto

**DocuAssist AI** es un sistema RAG (*Retrieval-Augmented Generation*) diseñado para asistir a empleados y técnicos en la consulta inteligente de documentación técnica y manuales de sistemas.

El sistema procesa **preguntas en lenguaje natural** sobre:
- 🖨️ **Equipos técnicos**: Impresoras fiscales
- 💻 **Sistemas de software**: Manuales de configuración y uso de sistemas internos
- ⚙️ **Procedimientos**: Instalación, configuración, troubleshooting

### ✨ Características Principales

- ✅ **Clasificación inteligente de intenciones** con LangGraph (greeting, documentation, out_of_scope)
- ✅ **Filtros automáticos** por categoría, marca, modelo, sistema y tipo de documentación
- ✅ **Reranking avanzado** con Cohere Rerank v4 para maximizar relevancia
- ✅ **Prompts dinámicos** (genéricos para categoría vs específicos para modelo)
- ✅ **Historial persistente** de conversaciones en SQLite
- ✅ **Guardrails pre-LLM** para detectar consultas prohibidas
- ✅ **API REST completa** documentada con FastAPI + Swagger
- ✅ **Interfaz moderna** con React + Tailwind CSS
- ✅ **Sistema de inferencia automática** de filtros desde lenguaje natural
- ✅ **Detección de nombres de sistemas** con regex-flexible matching
- ✅ **Tests automatizados** con pytest

---

## 🏗️ Arquitectura del Sistema

```
┌──────────────────────────────────────────────────────────┐
│              FRONTEND (React 18+)                        │
│  Dashboard | SearchHistory | ChatUI |                    │
└──────────────────────┬───────────────────────────────────┘
                       │ HTTP/JSON
┌──────────────────────▼──────────────────────────────────┐
│           BACKEND (FastAPI)                             │
│  ┌──────────────────────────────────────────────────┐   │
│  │         LANGGRAPH (Orquestador)                  │   │
│  │  classify_intent → routing a nodos específicos   │   │
│  └──────────────────┬───────────────────────────────┘   │
│                     │                                   │
│     ┌───────────────┼───────────────┐                   │
│     ▼               ▼               ▼                   │
│  greeting     documentation      out_of_scope           │
│  (sin RAG)    (con RAG)          (sin RAG)              │
│                     │                                   │
│     ┌───────────────▼───────────────┐                   │
│     │  Pipeline RAG                 │                   │
│     │  • Inferencia de filtros      │                   │
│     │  • Retrieval (ChromaDB)       │                   │
│     │  • Reranking (Cohere)         │                   │
│     │  • Generation (Cohere)        │                   │
│     └───────────────┬───────────────┘                   │
│                     │                                   │
│  ┌──────────────────▼────────────────┐                  │
│  │  Historial (SQLite)               │                  │
│  │  + Metadata (tipo, sistema, etc)  │                  │
│  └───────────────────────────────────┘                  │
└─────────────────────────────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
    ChromaDB                    Cohere API
   (Vector Store)              (LLM + Embeddings)
```

### Stack Tecnológico

#### Backend

| Componente | Tecnología | Propósito |
|------------|-----------|----------|
| Framework | FastAPI | API REST con validación automática |
| Orquestación | LangGraph | Gestión de flujo conversacional |
| LLM | Cohere Command-R+ | Generación y clasificación |
| Embeddings | Cohere Embed v3 | Vectorización de documentos |
| Reranking | Cohere Rerank v4 | Refinamiento de relevancia |
| Vector DB | ChromaDB | Storage de embeddings |
| Base de Datos | SQLite | Historial de conversaciones |
| Testing | pytest | Tests automatizados |

#### Frontend

| Componente | Tecnología | Propósito |
|------------|-----------|----------|
| Framework | React 18+ | UI interactiva |
| Bundler | Vite | Build rápido y HMR |
| Styling | Tailwind CSS | Diseño responsivo |
| HTTP Client | Fetch API | Comunicación con backend |
| Routing | React Router | Navegación entre páginas |

---

## 📁 Estructura del Proyecto

```
DocuAssist-AI/
├── README.md                          # Este archivo
│
├── backend/
│   ├── README.md                      # Documentación específica del backend
│   ├── requirements.txt               # Dependencias de Python
│   ├── .env.example                   # Template de variables
│   ├── app.db                         # Base de datos SQLite
│   ├── app/
│   │   ├── main.py                    # Entry point FastAPI
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── chat_router.py     # POST /chat
│   │   │       └── history_router.py  # GET /history
│   │   ├── graph/
│   │   │   ├── chat_graph.py          # Definición LangGraph
│   │   │   ├── state.py               # ChatState (TypedDict)
│   │   │   └── nodes/
│   │   │       ├── classify_intent.py
│   │   │       ├── conversational_node.py
│   │   │       ├── documentation_node.py
│   │   │       └── out_of_scope_node.py
│   │   ├── rag/                       # Pipeline RAG
│   │   │   ├── retriever.py
│   │   │   ├── reranker.py
│   │   │   ├── generator.py
│   │   │   ├── query_rewriter.py
│   │   │   ├── chunking.py
│   │   │   └── prompts/
│   │   │       ├── intent_prompt.txt
│   │   │       ├── chat_prompt.txt
│   │   │       ├── rag_prompt.txt
│   │   │       └── rag_prompt_generic.txt
│   │   ├── metadata/                  # Inferencia de filtros
│   │   │   ├── infer.py
│   │   │   ├── infer_filters.py       # Extrae filtros de pregunta
│   │   │   ├── model_inference.py
│   │   │   └── filter_resolution.py
│   │   ├── guardrails/                # Validaciones pre-LLM
│   │   │   └── pre_llm.py
│   │   ├── llm/                       # Clientes LLM
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   └── cohere_client.py
│   │   ├── services/
│   │   │   ├── chat_service.py
│   │   │   └── history_service.py
│   │   ├── models/
│   │   │   └── history_model.py
│   │   ├── repository/
│   │   │   └── history_repository.py
│   │   ├── schemas/
│   │   │   ├── chat.py
│   │   │   └── response.py
│   │   ├── utils/
│   │   │   └── rag_validation.py
│   │   ├── vectorstore/
│   │   │   ├── client.py
│   │   │   └── ingest.py              # Ingesta de PDFs
│   │   └── db/
│   │       ├── base.py
│   │       ├── session.py
│   │       └── init_db.py
│   ├── chroma_db/                     # Base de datos vectorial (generada)
│   ├── data/
│   │   └── pdfs/
│   │       ├── tecnicos/              # Manuales de equipos
│   │       └── sistemas/              # Manuales de software
│   └── tests/
│       └── test_chat_flow.py
│
└── frontend/
    ├── README.md                      # Documentación del frontend
    ├── package.json                   # Dependencias de Node.js
    ├── vite.config.js                 # Configuración de Vite
    ├── tailwind.config.js             # Configuración de Tailwind
    ├── postcss.config.js              # Configuración PostCSS
    ├── eslint.config.js               # Configuración ESLint
    ├── index.html                     # Entry point HTML
    ├── src/
    │   ├── main.jsx                   # Bootstrap de React
    │   ├── App.jsx                    # Componente raíz
    │   ├── App.css                    # Estilos del App
    │   ├── index.css                  # Estilos globales
    │   ├── pages/
    │   │   ├── Dashboard.jsx          # Dashaboard
    │   │   ├── AskAI.jsx              # Chat interactivo
    │   │   ├── SearchHistory.jsx      # Historial completo
    │   ├── components/
    │   │   ├── chat/
    │   │   │   ├── ChatMessages.jsx
    │   │   │   ├── ChatInput.jsx
    │   │   │   ├── ChatMessage.jsx
    │   │   │   ├── ChatLoader.jsx
    │   │   │   ├── ChatHeader.jsx
    │   │   │   └── EmptyState.jsx
    │   │   ├── layout/
    │   │   │   ├── AppLayout.jsx
    │   │   │   ├── Sidebar.jsx
    │   │   │   └── Topbar.jsx
    │   │   └── ui/
    │   ├── services/
    │   │   ├── chatService.js
    │   │   └── historyService.js
    │   ├── assets/
    │   └── public/
```

---

## 🚀 Instalación Rápida

### Requisitos Previos

- **Python** 3.10+
- **Node.js** 16+
- **npm** o **yarn**
- **Cohere API Key** (obtener en https://cohere.com)

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/DocuAssist-AI.git
cd DocuAssist-AI
```

### Paso 2: Configurar Backend

#### 2.1 Crear entorno virtual

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### 2.2 Instalar dependencias

```bash
pip install -r requirements.txt
```

#### 2.3 Configurar variables de entorno

Crear archivo `.env` en la raíz del backend:

```env
COHERE_API_KEY=tu_api_key_aqui
```


**Nota:** El proyecto tal como está, ya tiene ChromaDB y la base de datos configuradas.

### Paso 3: Configurar Frontend

```bash
cd ../frontend
npm install
```

---

## ▶️ Ejecución

### Terminal 1: Backend

```bash
cd backend

# Activar entorno
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Iniciar servidor
uvicorn app.main:app --reload
```

El backend estará en **http://localhost:8000**

#### Documentación interactiva:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Terminal 2: Frontend

```bash
cd frontend

# Modo desarrollo
npm run dev
```

El frontend estará en **http://localhost:5173** (o el puerto mostrado)

---

## 📊 Uso de la API

### POST /chat

Enviar una pregunta y obtener respuesta con contexto.

**Request:**
```json
{
  "question": "¿Qué indica el LED rojo encendido en la Hasar SMH/PT-250F?",
  "categoria_equipo": "impresora",
  "tipo_documentacion": "tecnica",
  "subtipo": "fiscal"
  "marca": "hasar",
  "modelo": "Impresora_fiscal_Hasar_SMH-PT-250F"
}
```

**Response:**
```json
{
  "answer": "El LED rojo encendido en la impresora Hasar SMH/PT-250F indica...",
  "sources": [
    {
      "document": "Impresora_fiscal_Hasar_SMH-PT-250F",
      "page": 8
    }
  ],
  "images": [],
  "used_rag": true
}
```

### GET /history

Obtener historial de conversaciones.

**Request:**
```
GET /history?limit=10
```

**Response:**
```json
[
  {
    "id": 1,
    "question": "¿Qué indica el LED rojo encendido en la Hasar SMH/PT-250F?",
    "answer": "El LED rojo encendido en la impresora Hasar SMH/PT-250F indica...",
    "tipo_documentacion": "tecnica",
    "marca": "hasar",
    "modelo": "Impresora_fiscal_Hasar_SMH-PT-250F",
    "created_at": "2025-12-18T10:30:00"
  }
]
```

---

## 💡 Ejemplos de Uso

### Ejemplo 1: Saludo (sin RAG)

```
Usuario: "Hola"

Sistema responde sin usar RAG:
- used_rag: false
- No infiere filtros
- Respuesta conversacional directa
Tiempo: ~100ms
```

### Ejemplo 2: Pregunta Técnica con Filtros Explícitos

```
Usuario: "¿Qué indica el LED rojo encendido en la Hasar SMH/PT-250F?"
Filtros enviados desde el frontend:
{
  "marca": "hasar",
  "modelo": "Impresora_fiscal_Hasar_SMH-PT-250F",
  "categoria_equipo": "impresora"
}

Sistema:
- Usa RAG con filtros específicos
- Busca solo en documentación de Hasar_SMH-PT-250F
- Retorna respuesta específica del manual
```

### Ejemplo 3: Pregunta con Inferencia Automática de Sistema

```
Usuario: "¿Cómo realizar cierre Z en StarPOS Market?"
Sin filtros explícitos

Sistema infiere automáticamente (Nivel 2):
{
  "sistema": "StarPOSMarketManual",
  "tipo_documentacion": "sistema"
}

Luego busca en documentación del sistema StarPOS Market
```

### Ejemplo 4: Pregunta con Inferencia de Modelo

```
Usuario: "¿Qué señales indican que el controlador fiscal SMH/P-441F está bloqueado?"
Sin filtros explícitos

Sistema infiere automáticamente (Nivel 1 - model_inference):
{
  "marca": "hasar",
  "modelo": "Impresora_fiscal_Hasar_SMH-P-441F",
  "categoria_equipo": "impresora",
  "subtipo": "fiscal"
}

Luego busca en documentación específica de ese modelo
```

### Ejemplo 5: Pregunta Fuera de Alcance

```
Usuario: "¿Cuál es la capital de Francia?"

Sistema:
- classify_intent detecta "out_of_scope"
- No usa RAG
- No infiere filtros
- Responde educadamente que solo puede ayudar con documentación técnica
```

---

## 🔍 Flujo de Procesamiento

```
1. REQUEST → POST /chat
    ↓
2. Guardrails Pre-LLM (detectar consultas prohibidas)
    ↓
3. LangGraph: Clasificación de Intención
    ├─ Greeting → Respuesta directa (sin RAG)
    ├─ Out_of_Scope → Rechazo educado (sin RAG)
    └─ Documentation → Pipeline RAG
        ├─ Inferencia de Filtros
        ├─ Merge con Filtros Explícitos
        ├─ Query Rewriting
        ├─ Retrieval (ChromaDB)
        ├─ Reranking (Cohere)
        └─ Generation (Cohere)
    ↓
4. Guardar en Historial (con metadata)
    ↓
5. Response → JSON con respuesta + sources
```

### 🎯 Optimización: Lazy Evaluation

**Problema anterior:** Todos los requests hacían inferencia de filtros (incluso saludos)

**Solución:** Solo se infieren filtros en `documentation_node` cuando la intención es "documentation"

**Beneficio:** ~200-300ms más rápido para ~60% de requests (greetings y out_of_scope)

---

## 🧪 Testing

### Ejecutar Tests

```bash
cd backend
pytest tests/ -v
```

### Tests Implementados

```python
✅ test_greeting()           # Saludo conversacional (sin RAG)
✅ test_out_of_scope()       # Pregunta fuera de alcance
✅ test_system_question()    # Documentación de software
✅ test_technical_question() # Pregunta técnica específica
```

---

## 🔐 Guardrails y Validaciones

### Pre-LLM Guardrails

Se valida que la consulta no contenga patrones prohibidos:

```python
forbidden_patterns = [
    "ignora", "evadir",
    "respondé en inglés",
    "usa conocimiento general"
]
```

### Validaciones de Chunks

- ✅ Filtrado estricto por modelo (evita contaminación cruzada)
- ✅ Validación de metadata
- ✅ Rechazo de chunks con score bajo

---

## 🔄 Inferencia Automática de Filtros

El sistema puede inferir automáticamente ciertos filtros de la pregunta natural:

### Filtros que SE infieren ✅

El sistema tiene DOS niveles de inferencia:

**Nivel 1 - Inferencia de modelos específicos (en el router):**
- `modelo`, `marca`, `subtipo`, `categoria_equipo`: Se infieren usando aliases de modelos específicos
  - Ejemplo: "tmt20" → modelo="Impresora_NO_fiscal_Epson_TM-T20", marca="epson"
  - Ejemplo: "smhpt250f" → modelo="Impresora_fiscal_Hasar_SMH-PT-250F", marca="hasar", subtipo="fiscal"

**Nivel 2 - Inferencia general (en documentation_node):**
- `categoria_equipo`: "impresora", "balanza" (de palabras en la pregunta)
- `tipo_documentacion`: "tecnica" o "sistema" (según palabras clave)
- `sistema`: Nombres de software predefinidos
  - "starpos", "star pos", "starpos market" → "StarPOSMarketManual"

**Prioridad:** Los filtros explícitos del frontend SIEMPRE tienen prioridad sobre los inferidos.

### Ejemplo de Detección

```
Pregunta: "¿Cómo realizar cierre Z en StarPOS Market?"
    ↓
SISTEMAS_CONOCIDOS = {
    "StarPOSMarketManual": ["starpos", "star pos", "starpos market", "star-pos"],
    ...
}
    ↓
Inferido: { sistema: "StarPOSMarketManual", tipo_documentacion: "sistema" }
```

---

## 🐛 Troubleshooting

### Backend

#### Error: "No module named 'cohere'"
```bash
pip install cohere
```

#### Error: "Invalid API key"
- Verificar que `.env` tiene una API key válida de Cohere
- Obtenerla en https://cohere.com

#### Error: "ChromaDB no encuentra documentos"
```bash
# Re-ejecutar ingesta de documentos
python -m app.vectorstore.ingest
```

### Frontend

#### Error: "Cannot find module 'react'"
```bash
npm install
```

#### Error: "Port 5173 is already in use"
```bash
# Usar puerto diferente
npm run dev -- --port 3000
```

#### Error: "CORS error when calling backend"
- Verificar que backend está corriendo en http://localhost:8000
- Verificar que chatService.js tiene la URL correcta

---

## 🚀 Mejoras Futuras

- [ ] **Memoria conversacional:** Contexto de chat history en las preguntas de seguimiento
- [ ] **Ingesta incremental:** Hash de archivos para evitar re-embedding; usar LlamaParse para tablas
- [ ] **Búsqueda híbrida:** Combinar BM25 (keywords exactos) + embeddings (semántica)
- [ ] **Configuración dinámica:** Mover `MODEL_ALIASES` a JSON o base de datos sin redeploy
- [ ] Fine-tuning de embeddings para dominio específico
- [ ] Feedback loop (👍/👎 para mejorar iterativamente)
- [ ] Integración con APIs externas
- [ ] Dashboard de analytics
- [ ] Autenticación y autorización
- [ ] Implementar respuestas con imágenes descriptivas

---

## 🛠️ Scripts Útiles

### Backend

```bash
# Ingesta de documentos
python -m app.vectorstore.ingest

# Inicializar base de datos
python -m app.db.init_db

# Tests
pytest tests/ -v

# Debug del retriever
python -m app.debug.test_retriever

# Debug del grafo
python -m app.debug.test_graph
```

### Frontend

```bash
# Instalar dependencias
npm install

# Desarrollo con HMR
npm run dev

# Build para producción
npm run build

# Preview del build
npm run preview

# Linting
npm run lint
```

---

## 👥 Autor

**Agostina Torres**  
Get Talent - Pi Data  
Challenge Final - Diciembre 2025

---
