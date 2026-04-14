from fastapi import FastAPI, HTTPException

from app.config import MODEL_PATH, N_CTX, N_GPU_LAYERS, MAX_TOKENS, VERBOSE
from app.schemas import AnalyzeRequest, AnalyzeResponse, TextAnalysisResult
from app.services.llm.local_backend import LocalBackend
from app.services.llm.router import LLMRouter
from app.services.llm.analyze_service import AnalyzeService
from app.services.llm.classify_service import ClassifyService

app = FastAPI(title="Local LLM Service")
LLM_BACKEND = 'local'

local_backend = LocalBackend(
    model_path=MODEL_PATH,
    n_ctx=N_CTX,
    n_gpu_layers=N_GPU_LAYERS,
    verbose=VERBOSE,
)

router = LLMRouter(
    local_backend=local_backend,
    openai_backend=None,
    mode=LLM_BACKEND,
)

analyze_service = AnalyzeService(router)
classify_service = ClassifyService(router)

@app.get("/health")
def health() -> dict:
    return local_backend.health()


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    try:
        content = analyze_service.analyze(req.text, max_tokens=MAX_TOKENS)
        return AnalyzeResponse(
            content=content,
            backend=router.mode,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

@app.post("/classify", response_model=TextAnalysisResult)
def classify(req: AnalyzeRequest):
    try:
        return classify_service.classify(req.text, max_tokens=MAX_TOKENS)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

