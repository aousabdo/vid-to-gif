# vid-to-gif

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/downloads/)
[![CI](https://github.com/aousabdo/vid-to-gif/actions/workflows/ci.yml/badge.svg)](https://github.com/aousabdo/vid-to-gif/actions/workflows/ci.yml)

A command-line tool to convert any video file into a high-quality GIF using ffmpeg.

## Features

- Converts any video format supported by ffmpeg to GIF
- High-quality output using optimized color palette
- Customizable FPS and output size
- Create GIFs from specific segments of videos
- Batch processing for multiple videos
- Simple command-line interface
- Cross-platform compatibility (Windows, macOS, Linux)
- Verbose mode for detailed output

## Requirements

- Python 3.6 or higher
- ffmpeg installed and available in PATH

### Installing ffmpeg

#### macOS (using Homebrew)
```bash
brew install ffmpeg
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install ffmpeg
```

#### Windows
1. Download from the [official ffmpeg website](https://ffmpeg.org/download.html)
2. Add to your system PATH

## Installation

### From source
1. Clone or download this repository
2. Navigate to the project directory
3. Install the package:

```bash
pip install .
```

Or for development:

```bash
pip install -e .
```

Alternatively, you can install directly from GitHub:

```bash
pip install git+https://github.com/aousabdo/vid-to-gif.git
```

## Usage

```bash
vid-to-gif input.mp4 output.gif
```

### Options

- `--fps`: Frames per second for the GIF (default: 15, range: 1-60)
- `--scale`: Height to scale the GIF to (default: 480, range: 16-4096)
- `--start SECONDS`: Start time in seconds (default: 0)
- `--duration SECONDS`: Duration in seconds (default: entire video)
- `--verbose`, `-v`: Print detailed output

### Examples

```bash
# Basic conversion
vid-to-gif input.mp4 output.gif

# Higher quality with more frames
vid-to-gif input.mp4 output.gif --fps 20 --scale 600

# For smaller file size
vid-to-gif input.mp4 output.gif --fps 10 --scale 320

# Create a GIF from a specific segment
vid-to-gif input.mp4 output.gif --start 10 --duration 5

# With detailed output
vid-to-gif input.mp4 output.gif --verbose

# Combine multiple options
vid-to-gif input.mp4 output.gif --start 30 --duration 10 --fps 24 --scale 480

# Batch processing (multiple inputs, multiple outputs)
vid-to-gif video1.mp4 video2.mp4 video3.mp4 output1.gif output2.gif output3.gif

# Batch processing with shared options
vid-to-gif video1.mp4 video2.mp4 video3.mp4 output1.gif output2.gif output3.gif --fps 20 --scale 480
```

### Auto-generated output names

If you don't specify an output file for a single input, the tool will automatically generate one:

```bash
# This will create input.gif
vid-to-gif input.mp4
```

## Running Tests

To run the unit tests:

```bash
python run_tests.py
```

## How it works

The tool uses ffmpeg with a two-pass process:
1. First, it generates an optimized color palette from the video
2. Then it converts the video to GIF using that palette for better color quality

This approach produces higher quality GIFs compared to direct conversion.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This tool is built on top of the amazing [ffmpeg](https://ffmpeg.org/) project