import os
from dotenv import load_dotenv

load_dotenv()

MODEL_PATH = os.getenv("MODEL_PATH")
N_CTX = int(os.getenv("N_CTX", "1024"))
N_GPU_LAYERS = int(os.getenv("N_GPU_LAYERS", "30"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "256"))
LLM_BACKEND = os.getenv("LLM_BACKEND", "local")
VERBOSE = os.getenv("LLM_VERBOSE", "false").lower() == "true"