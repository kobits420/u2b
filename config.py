"""
Configuration file for u2b - YouTube Command Line Player
"""

# Default settings
DEFAULT_VOLUME = 50
DEFAULT_AUDIO_ONLY = True
MAX_SEARCH_RESULTS = 10

# FFmpeg settings
FFMPEG_AUDIO_OPTIONS = [
    '-nodisp',      # No video display for audio-only
    '-autoexit',    # Exit when playback ends
    '-hide_banner', # Hide FFmpeg banner
    '-loglevel', 'error',  # Only show errors
    '-nostats',     # Don't show statistics
    '-sync', 'ext'  # External clock sync for better timing
]

FFMPEG_VIDEO_OPTIONS = [
    '-autoexit',    # Exit when playback ends
    '-hide_banner', # Hide FFmpeg banner
    '-loglevel', 'error'  # Only show errors
]

# YouTube search settings
YOUTUBE_SEARCH_OPTIONS = {
    'quiet': True,
    'no_warnings': True,
    'extract_flat': True,
    'default_search': 'ytsearch',
    'max_downloads': MAX_SEARCH_RESULTS,
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-us,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    },
}

# Supported video formats (priority order)
AUDIO_FORMATS = [
    'bestaudio[ext=m4a]',
    'bestaudio[ext=mp3]',
    'bestaudio[ext=webm]',
    'bestaudio'
]

VIDEO_FORMATS = [
    'best[height<=720]',
    'best[height<=480]',
    'best'
]

# Color settings for terminal output
COLORS = {
    'success': 'green',
    'error': 'red',
    'warning': 'yellow',
    'info': 'cyan',
    'prompt': 'green'
} 