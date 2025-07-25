#!/usr/bin/env python3
"""
Unit tests for the vid_to_gif module.
"""

import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock
import sys
import subprocess

# Add the project root to sys.path so we can import vid_to_gif
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import vid_to_gif


class TestVidToGif(unittest.TestCase):
    
    def test_seconds_to_hms(self):
        """Test the seconds_to_hms function."""
        self.assertEqual(vid_to_gif.seconds_to_hms(0), "00:00:00.000")
        self.assertEqual(vid_to_gif.seconds_to_hms(61.5), "00:01:01.500")
        self.assertEqual(vid_to_gif.seconds_to_hms(3661.123), "01:01:01.123")
        self.assertEqual(vid_to_gif.seconds_to_hms(7261.999), "02:01:01.999")
    
    def test_check_ffmpeg_installed(self):
        """Test check_ffmpeg when ffmpeg is installed."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock()
            result = vid_to_gif.check_ffmpeg()
            self.assertTrue(result)
            mock_run.assert_called_once_with(
                ['ffmpeg', '-version'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
    
    def test_check_ffmpeg_not_installed(self):
        """Test check_ffmpeg when ffmpeg is not installed."""
        with patch('subprocess.run', side_effect=FileNotFoundError()):
            result = vid_to_gif.check_ffmpeg()
            self.assertFalse(result)
    
    def test_get_video_duration_success(self):
        """Test get_video_duration when it succeeds."""
        with patch('subprocess.run') as mock_run:
            mock_result = MagicMock()
            mock_result.stdout = "120.5\n"
            mock_run.return_value = mock_result
            result = vid_to_gif.get_video_duration("test.mp4")
            self.assertEqual(result, 120.5)
    
    def test_get_video_duration_failure(self):
        """Test get_video_duration when it fails."""
        with patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, 'ffprobe')):
            result = vid_to_gif.get_video_duration("test.mp4")
            self.assertIsNone(result)
    
    def test_convert_video_to_gif_parameter_validation(self):
        """Test parameter validation in convert_video_to_gif."""
        # Create a temporary file for testing
        with tempfile.NamedTemporaryFile(suffix='.mp4') as temp_file:
            temp_path = temp_file.name
            
            # Test invalid FPS
            with self.assertRaises(ValueError) as context:
                vid_to_gif.convert_video_to_gif(temp_path, "output.gif", fps=0)
            self.assertIn("FPS must be between 1 and 60", str(context.exception))
            
            with self.assertRaises(ValueError) as context:
                vid_to_gif.convert_video_to_gif(temp_path, "output.gif", fps=70)
            self.assertIn("FPS must be between 1 and 60", str(context.exception))
            
            # Test invalid scale
            with self.assertRaises(ValueError) as context:
                vid_to_gif.convert_video_to_gif(temp_path, "output.gif", scale=10)
            self.assertIn("Scale must be between 16 and 4096", str(context.exception))
            
            with self.assertRaises(ValueError) as context:
                vid_to_gif.convert_video_to_gif(temp_path, "output.gif", scale=5000)
            self.assertIn("Scale must be between 16 and 4096", str(context.exception))
            
            # Test invalid start_time
            with self.assertRaises(ValueError) as context:
                vid_to_gif.convert_video_to_gif(temp_path, "output.gif", start_time=-5)
            self.assertIn("Start time must be non-negative", str(context.exception))
            
            # Test invalid duration
            with self.assertRaises(ValueError) as context:
                vid_to_gif.convert_video_to_gif(temp_path, "output.gif", duration=0)
            self.assertIn("Duration must be positive", str(context.exception))
            
            with self.assertRaises(ValueError) as context:
                vid_to_gif.convert_video_to_gif(temp_path, "output.gif", duration=-5)
            self.assertIn("Duration must be positive", str(context.exception))


if __name__ == '__main__':
    unittest.main()