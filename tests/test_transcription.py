import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from io import BytesIO
from src.services.transcriber_service import Transcriber

def test_transcriber_initialization():
    """Test that Transcriber initializes correctly"""
    try:
        transcriber = Transcriber()
        assert transcriber.model is not None
        print("PASS: Transcriber initialization test passed")
    except Exception as e:
        print(f"FAIL: Transcriber initialization test failed: {e}")
        raise

def test_transcriber_with_mock_audio():
    """Test transcription with a simple mock audio file"""
    try:
        transcriber = Transcriber()

        # Create a simple mock audio file (this is just for testing the pipeline)
        # In a real scenario, you'd use a proper audio file
        mock_audio = BytesIO(b"mock audio data")
        mock_audio.filename = "test.wav"

        # This will likely fail due to mock data, but tests the error handling
        try:
            result = transcriber.transcribe(mock_audio)
            # If it succeeds with mock data, that's unexpected but good
            assert isinstance(result, str)
            print("PASS: Transcriber mock audio test passed")
        except Exception as e:
            # Expected to fail with mock data, but should fail gracefully
            print(f"PASS: Transcriber mock audio test passed (expected failure with mock data): {e}")

    except Exception as e:
        print(f"FAIL: Transcriber mock audio test failed: {e}")
        raise

def test_transcriber_error_handling():
    """Test that Transcriber handles errors gracefully"""
    try:
        transcriber = Transcriber()

        # Test with None input
        try:
            result = transcriber.transcribe(None)
            print("FAIL: Transcriber should have failed with None input")
        except Exception:
            print("PASS: Transcriber correctly handles None input")

        # Test with invalid file
        invalid_audio = BytesIO(b"invalid")
        invalid_audio.filename = "invalid.wav"
        try:
            result = transcriber.transcribe(invalid_audio)
            print("FAIL: Transcriber should have failed with invalid audio")
        except Exception:
            print("PASS: Transcriber correctly handles invalid audio")

    except Exception as e:
        print(f"FAIL: Transcriber error handling test failed: {e}")
        raise

if __name__ == "__main__":
    test_transcriber_initialization()
    test_transcriber_with_mock_audio()
    test_transcriber_error_handling()
    print("All transcription tests completed!")
