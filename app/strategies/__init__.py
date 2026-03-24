from app.strategies.base import BaseStrategy
from app.strategies.implement import ImplementTaskStrategy
from app.strategies.review import CodeReviewStrategy

_STRATEGIES: dict[str, type[BaseStrategy]] = {
    "To-do": ImplementTaskStrategy,
    "Under analysis": CodeReviewStrategy,
}

def get_strategy(column: str) -> BaseStrategy | None:
    cls = _STRATEGIES.get(column)
    
    return cls() if cls else None
