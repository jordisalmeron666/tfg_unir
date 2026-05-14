import sys, logging
import chromadb
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.readers.file import PDFReader
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    Settings as LlamaSettings,
)

from config import settings
from indexes import INDEX_CONFIG

#FIXME no todos los jeugos del taco siempre, parametrizar o configurar cuales indexar cada vez
# ===========================
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


###
# Configura los servicios globales de LlamaIndex (Azure OpenAI Embeddings).
###
def setup_llamaindex_settings():
    """
    Configura los servicios globales de LlamaIndex para el proceso de indexación.

    Rol:
        Inicializa el modelo de embeddings de Azure OpenAI para que todas las operaciones de indexación utilicen este modelo.
    Entradas:
        Ninguna (usa variables globales de configuración desde settings).
    Salidas:
        Ninguna (afecta el estado global de LlamaIndex).
    Notas:
        No configura un LLM, ya que solo se requiere embeddings para indexar documentos.
    """
    logging.info(f"Configurando LlamaIndex con Azure OpenAI Embedding: {settings.aoai_embedding_model}")
    LlamaSettings.embed_model = AzureOpenAIEmbedding(
        model=settings.aoai_embedding_model,
        deployment_name=settings.aoai_embedding_model,
        api_key=settings.aoai_api_key,
        azure_endpoint=settings.aoai_endpoint,
        api_version=settings.aoai_api_version,
    )
    LlamaSettings.llm = None  # no LLM necesario para indexación


###
# Devuelve un cliente ChromaDB autenticado.
###
def get_chroma_client():
    """
    Crea y devuelve un cliente autenticado para ChromaDB.

    Rol:
        Permite interactuar con la base de datos vectorial ChromaDB para crear/eliminar colecciones y almacenar embeddings.
    Entradas:
        Ninguna (usa configuración global de settings).
    Salidas:
        Instancia de chromadb.HttpClient autenticada.
    """
    return chromadb.HttpClient(
        host=settings.chroma_host,
        port=settings.chroma_port,
        headers={"Authorization": f"Bearer {settings.chroma_auth_token}"}
    )


###
# Elimina (si existe) y recrea la colección del juego, luego indexa todas sus secciones.
# Devuelve un dict con el resumen de la indexación.
###
def create_index_for_game(game_key: str, game_config: dict, chroma_client):
    """
    Elimina (si existe) y recrea la colección ChromaDB para un juego, indexando todas sus secciones.

    Rol:
        Orquesta el proceso de indexación para un juego concreto, recorriendo sus secciones y almacenando los embeddings en la colección correspondiente de ChromaDB.
    Entradas:
        game_key: Clave identificadora del juego (str).
        game_config: Diccionario de configuración del juego (colección, secciones, rutas, offsets, etc).
        chroma_client: Cliente autenticado de ChromaDB.
    Salidas:
        summary: dict con el resumen de la indexación (colección, secciones indexadas, fallidas y saltadas).
    Notas:
        Elimina la colección previa si existe, para evitar duplicados.
        Indexa solo secciones con datos disponibles.
        Añade metadatos útiles a cada documento (juego, sección, página real).
    """
    collection_name = game_config["collection"]
    base_subdir = game_config.get("base_subdir", game_key)
    sections = game_config.get("sections", {})

    summary = {
        "collection": collection_name,
        "indexed": [],
        "failed": [],
        "skipped": [],
    }

    if not sections:
        logging.info(f"Juego '{game_key}' sin secciones configuradas. Saltando.")
        return summary

    logging.info(f"Recreando colección ChromaDB: '{collection_name}'")
    try:
        chroma_client.delete_collection(collection_name)
    except Exception:
        pass
    chroma_collection = chroma_client.get_or_create_collection(collection_name)

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    for section_key, section_config in sections.items():
        data_subdir = section_config.get("data_subdir", section_key)
        data_path = settings.base_dir / base_subdir / data_subdir

        if not data_path.exists() or not any(data_path.iterdir()):
            logging.warning(f"Directorio vacío o no encontrado para '{section_key}': {data_path}. Saltando.")
            summary["skipped"].append(f"{section_key} (directorio no encontrado o vacío: {data_path})")
            continue

        logging.info(f"  Procesando sección '{section_key}': {data_path}")

        try:
            # solo para PDFs, pero se podrían añadir más tipos si fuera necesario
            reader = SimpleDirectoryReader(input_dir=data_path, file_extractor={".pdf": PDFReader()})
            documents = reader.load_data()

            if not documents:
                logging.warning(f"  Sin documentos en {data_path}. Saltando.")
                summary["skipped"].append(f"{section_key} (sin documentos en {data_path})")
                continue

            # le metemos tb la página real del documento, sumando el offset de la sección para que coincida con el PDF original
            page_offset = section_config.get("page_offset", 0)
            for doc in documents:
                doc.metadata["section"] = section_key
                doc.metadata["game"] = game_key
                if page_offset:
                    raw = doc.metadata.get("page_label", "")
                    try:
                        doc.metadata["page_label"] = str(int(raw) + page_offset)
                    except (ValueError, TypeError):
                        pass

            logging.info(f"  Documentos cargados: {len(documents)}")

            VectorStoreIndex.from_documents(
                documents,
                storage_context=storage_context,
                show_progress=True,
            )
            logging.info(f"  Sección '{section_key}' indexada en colección '{collection_name}'")
            summary["indexed"].append(f"{section_key} ({len(documents)} documentos)")

        except Exception as e:
            logging.error(f"  Error procesando '{section_key}': {e}", exc_info=True)
            summary["failed"].append(f"{section_key} (error: {e})")

    return summary

# ===========================
# Esto se tira como un standalone
# ===========================


if __name__ == "__main__":
    import datetime

    print("--- Iniciando Proceso de Indexación ---")
    setup_llamaindex_settings()

    client = get_chroma_client()

    report_lines = [
        f"Indexación ejecutada: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 60,
    ]

    for game_key, game_config in INDEX_CONFIG.items():
        print(f"\n=== Indexando juego: {game_key} ===")
        summary = create_index_for_game(game_key, game_config, client)

        report_lines.append(f"\nJuego: {game_key}")
        report_lines.append(f"  Colección ChromaDB: {summary['collection']}")
        report_lines.append(f"  Indexados ({len(summary['indexed'])}):")
        for item in summary["indexed"]:
            report_lines.append(f"    [OK] {item}")
        if summary["skipped"]:
            report_lines.append(f"  Saltados ({len(summary['skipped'])}):")
            for item in summary["skipped"]:
                report_lines.append(f"    [SKIP] {item}")
        if summary["failed"]:
            report_lines.append(f"  Fallidos ({len(summary['failed'])}):")
            for item in summary["failed"]:
                report_lines.append(f"    [ERROR] {item}")

    report_path = "indexed.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")

    print(f"\n--- Proceso de Indexación Completado. Resumen guardado en '{report_path}' ---")

