from .metrics import router as metrics_router
from .alerts import router as alerts_router
from .predictions import router as predictions_router

__all__ = ["metrics_router", "alerts_router", "predictions_router"]
