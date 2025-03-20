from config.Translation_config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TIMEOUT

def test_openai_config():
    """Verifica que la configuración de OpenAI sea válida"""
    assert OPENAI_API_KEY and OPENAI_API_KEY != "your_openai_api_key_here", \
        "La clave de API de OpenAI no está configurada"
    assert OPENAI_API_KEY.startswith("sk-"), \
        "La clave de API de OpenAI debe comenzar con 'sk-'"
    assert len(OPENAI_API_KEY) > 20, \
        "La clave de API de OpenAI parece ser demasiado corta"
    
    print("✅ Configuración de OpenAI verificada correctamente")

if __name__ == "__main__":
    test_openai_config() 