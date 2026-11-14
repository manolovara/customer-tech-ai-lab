import json
import anthropic, boto3
from config import *

br = boto3.client("bedrock-runtime", region_name=AWS_REGION)
r = br.invoke_model(modelId=EMBED_MODEL, body=json.dumps(
    {"inputText": "hello", "dimensions": EMBED_DIMS, "normalize": True}))
print("embedding dims:", len(json.loads(r["body"].read())["embedding"]))

msg = anthropic.Anthropic().messages.create(
    model=CLAUDE_MODEL, max_tokens=20,
    messages=[{"role": "user", "content": "Reply with the word OK"}])
print("claude:", msg.content[0].text)