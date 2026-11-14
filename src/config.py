import os
from dotenv import load_dotenv

load_dotenv()
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
VECTOR_BUCKET = os.environ["VECTOR_BUCKET"]          # 3-63 chars, minusculas
VECTOR_INDEX = os.environ.get("VECTOR_INDEX", "kb-index")
EMBED_MODEL = "amazon.titan-embed-text-v2:0"
EMBED_DIMS = 1024
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-haiku-5-5")
# ANTHROPIC_API_KEY lo lee el SDK de Anthropic directamente del entorno
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY") 