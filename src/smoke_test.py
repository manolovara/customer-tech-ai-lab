import anthropic
from config import *
from embeddings import embed

v = embed("hello")
print(f"embeddings ({EMBED_BACKEND}): {len(v)} dims")

msg = anthropic.Anthropic().messages.create(
    model=CLAUDE_MODEL, max_tokens=1000, output_config={"effort": "low"},
    messages=[{"role": "user", "content": "Reply with the word OK"}])
print("claude:", "".join(b.text for b in msg.content if b.type == "text"))