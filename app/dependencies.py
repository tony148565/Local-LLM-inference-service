from app.config import MODEL_PATH, N_CTX, N_GPU_LAYERS, VERBOSE
from app.services.llm.local_backend import LocalBackend
from app.services.llm.router import LLMRouter
from app.services.llm.analyze_service import AnalyzeService
from app.services.llm.classify_service import ClassifyService
from app.services.track2event_service import Track2EventService
from app.tools.Track2EventTool import Track2EventTool
from app.services.llm.event_decision_service import EventDecisionService
from app.services.track2event_analysis_service import Track2EventAnalysisService


LLM_BACKEND = "local"

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

track2event_tool = Track2EventTool(
    python_bin="/home/tony/.venv_track/bin/python",
    cli_path="/home/tony/Track2Event/cli.py",
    workdir="/home/tony/Track2Event",
)

track2event_service = Track2EventService(track2event_tool)

event_decision_service = EventDecisionService(router)

track2event_analysis_service = Track2EventAnalysisService(
    track2event_service=track2event_service,
    event_decision_service=event_decision_service,
)