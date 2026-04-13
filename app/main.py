from fastapi import FastAPI, HTTPException

from app.config import MODEL_PATH, N_CTX, N_GPU_LAYERS, MAX_TOKENS, VERBOSE
from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.local_llm_service import LocalLLMService

app = FastAPI(title="Local LLM Service")

llm_service = LocalLLMService(
    model_path=MODEL_PATH,
    n_ctx=N_CTX,
    n_gpu_layers=N_GPU_LAYERS,
    verbose=VERBOSE,
)


@app.get("/health")
def health() -> dict:
    return llm_service.health()


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest) -> AnalyzeResponse:
    try:
        content = llm_service.analyze(req.text, max_tokens=MAX_TOKENS)
        return AnalyzeResponse(
            content=content,
            backend="llama_cpp_local",
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc