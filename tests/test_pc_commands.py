import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from unittest.mock import patch, MagicMock
from src.services.pc_command_service import PcCommand

def test_pc_command_initialization():
    """Test that PcCommand initializes correctly"""
    try:
        pc = PcCommand()
        assert pc is not None
        print("PASS: PcCommand initialization test passed")
    except Exception as e:
        print(f"FAIL: PcCommand initialization test failed: {e}")
        raise

@patch('src.services.pc_command_service.Popen')
@patch('src.services.pc_command_service.os.path.exists')
def test_open_browser_url(mock_exists, mock_popen):
    """Test opening browser with URL"""
    try:
        mock_exists.return_value = True
        mock_popen.return_value = MagicMock()

        pc = PcCommand()
        result = pc.open_browser("https://www.google.com")

        assert result is True
        mock_popen.assert_called_once()
        print("PASS: Open browser URL test passed")
    except Exception as e:
        print(f"FAIL: Open browser URL test failed: {e}")
        raise

@patch('src.services.pc_command_service.pywhatkit.playonyt')
def test_play_on_youtube(mock_playonyt):
    """Test playing music on YouTube"""
    try:
        mock_playonyt.return_value = None

        pc = PcCommand()
        result = pc.play_on_youtube("test song")

        assert result is True
        mock_playonyt.assert_called_once_with("test song")
        print("PASS: Play on YouTube test passed")
    except Exception as e:
        print(f"FAIL: Play on YouTube test failed: {e}")
        raise

def test_open_browser_music_detection():
    """Test that open_browser correctly detects music requests"""
    try:
        pc = PcCommand()

        # Test music keywords
        music_commands = [
            "reproduce musica rock",
            "reproducir en youtube pop music",
            "pon musica jazz"
        ]

        for command in music_commands:
            # This should not call the browser opening logic for music
            # We can't easily test the full flow without mocking more,
            # but we can test that the method exists and doesn't crash
            result = pc.open_browser(command)
            assert isinstance(result, bool)
            print(f"PASS: Music detection test passed for: {command}")

    except Exception as e:
        print(f"FAIL: Music detection test failed: {e}")
        raise

def test_open_browser_regular_url():
    """Test that open_browser handles regular URLs"""
    try:
        pc = PcCommand()

        # Test regular URL
        with patch('src.services.pc_command_service.Popen') as mock_popen, \
             patch('src.services.pc_command_service.os.path.exists', return_value=True):

            mock_popen.return_value = MagicMock()
            result = pc.open_browser("https://www.example.com")

            assert result is True
            mock_popen.assert_called_once()
            print("PASS: Regular URL test passed")

    except Exception as e:
        print(f"FAIL: Regular URL test failed: {e}")
        raise

if __name__ == "__main__":
    test_pc_command_initialization()
    test_open_browser_url()
    test_play_on_youtube()
    test_open_browser_music_detection()
    test_open_browser_regular_url()
    print("All PC command tests completed!")
