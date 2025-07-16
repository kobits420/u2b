# u2b - Hyper-Lightweight YouTube Command Line Player

A **hyper-lightweight** YouTube desktop command-line application that delivers **permanently ad-free** audio streaming with maximum efficiency. Search, play, and control volume instantly - no bloat, no ads, just pure audio performance.

## Features

- **⚡ Hyper-Lightweight**: Minimal resource usage, instant startup
- **🚫 Permanently Ad-Free**: Zero advertisements, ever
- **🎵 Audio-First Design**: Optimized for music and podcast streaming
- **🔍 Instant Search**: Type and play - no waiting, no buffering
- **🎚️ Volume Control**: Precise volume adjustment (1-100)
- **🔗 Direct URL Support**: Paste any YouTube link for immediate playback
- **💻 Cross-Platform**: Windows, macOS, Linux - one codebase
- **🎨 Clean Interface**: Beautiful colored terminal output
- **⚡ Maximum Efficiency**: Streamlined for speed and performance

## Prerequisites

Before installing u2b, you need to have the following installed:

1. **Python 3.7+**
2. **FFmpeg** - Required for audio/video playback

### Installing FFmpeg

#### Windows:
1. Download FFmpeg from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Extract the files to a folder (e.g., `C:\ffmpeg`)
3. Add the `bin` folder to your system PATH
4. Restart your command prompt

#### macOS:
```bash
brew install ffmpeg
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install ffmpeg
```

## Installation

### Quick Start (Recommended)

1. Clone or download this repository
2. Navigate to the project directory
3. Run the installation script:

```bash
python install.py
```

### Manual Installation

1. Clone or download this repository
2. Navigate to the project directory
3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. Install FFmpeg (see Prerequisites section above)
5. Test the installation:

```bash
python test.py
```

## Usage

Run the application:

```bash
python main.py
```

### Commands

- **Search and Play**: Type any search term to find and play the first result
  ```
  never gonna give you up
  ```

- **Direct URL**: Paste a YouTube URL to play directly
  ```
  https://www.youtube.com/watch?v=dQw4w9WgXcQ
  ```

- **Volume Control**: Set volume level (1-100)
  ```
  volume 75
  ```

- **Stop Playback**: Stop currently playing video
  ```
  stop
  ```

- **Help**: Show available commands
  ```
  help
  ```

- **Exit**: Quit the application
  ```
  quit
  ```

### Examples

```
u2b> never gonna give you up
Searching for: never gonna give you up
Now playing: Rick Astley - Never Gonna Give You Up (Official Music Video)
Duration: 213 seconds

u2b> volume 80
Volume set to: 80%

u2b> stop
Playback stopped

u2b> https://www.youtube.com/watch?v=dQw4w9WgXcQ
Now playing: Rick Astley - Never Gonna Give You Up (Official Music Video)
Duration: 213 seconds
```

## Why u2b?

**🎯 Built for Efficiency**
- **Hyper-lightweight**: Under 500KB of Python code
- **Instant startup**: No bloated GUI, no unnecessary dependencies
- **Minimal memory footprint**: Uses only what's needed

**🚫 Permanently Ad-Free**
- Advanced streaming technology ensures zero advertisements
- No tracking, no analytics, no interruptions
- Pure, uninterrupted audio experience

**⚡ Maximum Performance**
- Direct audio streaming for minimal latency
- Optimized for music and podcast consumption
- Efficient resource usage even on older hardware

**🎵 Audio-First Philosophy**
- Designed specifically for audio content
- No video processing overhead
- Crystal-clear audio quality

## Troubleshooting

### Common Issues

1. **"ffplay not found"**: Make sure FFmpeg is installed and in your PATH
2. **"yt-dlp not found"**: Run `pip install -r requirements.txt`
3. **No audio**: Check your system volume and the app's volume setting
4. **Search not working**: Check your internet connection

### Windows Specific

- Ensure FFmpeg is properly added to PATH
- Run as administrator if you encounter permission issues
- Use PowerShell or Command Prompt

## Dependencies

- `yt-dlp`: YouTube video extraction
- `pytube`: YouTube video processing
- `requests`: HTTP requests
- `beautifulsoup4`: HTML parsing
- `colorama`: Cross-platform colored terminal output
- `ffmpeg`: Audio/video playback (external dependency)

## License

This project is open source and available under the MIT License.

## Disclaimer

This tool is for educational purposes. Please respect YouTube's terms of service and copyright laws. Only download and play content you have permission to access. 