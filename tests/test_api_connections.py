import sys
import os
sys.path.append("src")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from src.services.llm_service import LLM
from src.services.tts_service import TTS
from src.models.weather import Weather

def test_llm_api_connection():
    """Test that LLM service can connect to Novita API"""
    try:
        llm = LLM()
        # Test a simple completion
        response = llm.client.chat.completions.create(
            model=llm.model,
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        assert response is not None
        assert len(response.choices) > 0
        assert response.choices[0].message.content is not None
        print("PASS: LLM API connection test passed")
    except Exception as e:
        print(f"FAIL: LLM API connection test failed: {e}")
        raise

def test_tts_api_connection():
    """Test that TTS service can connect to ElevenLabs API"""
    try:
        tts = TTS()
        # Test TTS generation with a short text
        test_text = "Hello world"
        result = tts.process(test_text)
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0
        print("PASS: TTS API connection test passed")
    except Exception as e:
        print(f"FAIL: TTS API connection test failed: {e}")
        raise

def test_weather_api_connection():
    """Test that Weather service can fetch data"""
    try:
        weather = Weather()
        # Test with a known city
        result = weather.get("London")
        assert result is not None
        assert isinstance(result, dict)
        assert "temperature" in result or "temp" in result
        print("PASS: Weather API connection test passed")
    except Exception as e:
        print(f"FAIL: Weather API connection test failed: {e}")
        raise

if __name__ == "__main__":
    test_llm_api_connection()
    test_tts_api_connection()
    test_weather_api_connection()
    print("All API connection tests passed!")
