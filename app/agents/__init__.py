from app.agents.base import BaseAgent

from app.core.config import settings

def get_agent() -> BaseAgent:
    provider = settings.ai_provider.lower()

    if provider == "anthropic":
        from app.agents.anthropic import AnthropicAgent
        
        return AnthropicAgent()

    if provider == "gemini":
        from app.agents.gemini import GeminiAgent
        
        return GeminiAgent()

    raise ValueError(f"Unknown AI provider: '{provider}'. Valid options: anthropic, gemini")
