"""Optional Ollama or OpenAI-compatible LLM. Python stdlib only."""
import json
import os
import urllib.request
import urllib.error

class LLMError(RuntimeError):
    pass

class LLMClient:
    def __init__(self, provider=None, model=None, timeout=65):
        self.provider=(provider or os.getenv("LLM_PROVIDER","ollama")).lower()
        if self.provider not in ("ollama","openai"):
            raise ValueError("LLM_PROVIDER must be ollama or openai")
        default="qwen3:4b-instruct" if self.provider=="ollama" else "gpt-4o-mini"
        self.model=model or (os.getenv("OLLAMA_MODEL") if self.provider=="ollama" else os.getenv("OPENAI_MODEL")) or default
        self.timeout=timeout

    def chat(self, system, user, *, structured=False):
        messages=[{"role":"system","content":system},{"role":"user","content":user}]
        if self.provider=="ollama":
            base=os.getenv("OLLAMA_BASE_URL","http://127.0.0.1:11434").rstrip("/")
            url=base+"/api/chat"
            payload={"model":self.model,"messages":messages,"stream":False,"options":{"temperature":0}}
            if structured: payload["format"]="json"
            headers={"Content-Type":"application/json"}
        else:
            key=os.getenv("OPENAI_API_KEY")
            if not key: raise LLMError("OPENAI_API_KEY is required for hosted model mode")
            url="https://api.openai.com/v1/chat/completions"
            payload={"model":self.model,"messages":messages,"temperature":0}
            if structured: payload["response_format"]={"type":"json_object"}
            headers={"Content-Type":"application/json","Authorization":"Bearer "+key}
        req=urllib.request.Request(url,data=json.dumps(payload).encode(),headers=headers,method="POST")
        try:
            with urllib.request.urlopen(req,timeout=self.timeout) as resp:
                data=json.load(resp)
            return data["message"]["content"] if self.provider=="ollama" else data["choices"][0]["message"]["content"]
        except (urllib.error.URLError,TimeoutError,ValueError,KeyError,IndexError,TypeError) as exc:
            raise LLMError("Model request failed. Check provider, model, and connectivity.") from exc
