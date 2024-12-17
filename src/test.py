from config.settings import LLMConfig, OllamaConfig, OpenAIConfig

config = LLMConfig()
print(config.openai.api_key)
print(config.ollama.host)
