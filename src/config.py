import os
from dotenv import load_dotenv

load_dotenv()
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
EMBED_BACKEND = os.environ.get("EMBED_BACKEND", "local")        # "local" | "bedrock"
VECTOR_BACKEND = os.environ.get("VECTOR_BACKEND", "local")      # "local" | "s3vectors"
VECTOR_BUCKET = os.environ.get("VECTOR_BUCKET", "")             # solo para s3vectors
VECTOR_INDEX = os.environ.get("VECTOR_INDEX", "kb-index")
LOCAL_EMBED_MODEL = "BAAI/bge-small-en-v1.5"                    # 384 dimensiones
EMBED_MODEL = "amazon.titan-embed-text-v2:0"                    # solo si EMBED_BACKEND=bedrock
EMBED_DIMS = 384 if EMBED_BACKEND == "local" else 1024
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-haiku-5-5")
# ANTHROPIC_API_KEY lo lee el SDK de Anthropic directamente del entorno