#!/usr/bin/env python3
"""
u2b - Lightweight YouTube Desktop Command Line App
A simple CLI tool for searching and playing YouTube videos with audio-only support.
"""

import os
import sys
import subprocess
import re
import json
from urllib.parse import urlparse, parse_qs
import requests
from bs4 import BeautifulSoup
import yt_dlp
from colorama import init, Fore, Style
import config

# Initialize colorama for cross-platform colored output
init()

class U2BPlayer:
    def __init__(self):
        self.volume = config.DEFAULT_VOLUME
        self.current_process = None
        self.is_playing = False
        
    def search_youtube(self, query):
        """Search YouTube for videos"""
        try:
            # Use yt-dlp to search for videos
            with yt_dlp.YoutubeDL(config.YOUTUBE_SEARCH_OPTIONS) as ydl:
                results = ydl.extract_info(f"ytsearch{config.MAX_SEARCH_RESULTS}:{query}", download=False)
                
            if 'entries' in results:
                return results['entries']
            return []
        except Exception as e:
            print(f"{Fore.RED}Error searching YouTube: {e}{Style.RESET_ALL}")
            return []
    
    def extract_video_id(self, url):
        """Extract video ID from YouTube URL"""
        if 'youtube.com' in url or 'youtu.be' in url:
            if 'youtu.be' in url:
                return url.split('/')[-1].split('?')[0]
            elif 'youtube.com/watch' in url:
                parsed_url = urlparse(url)
                query_params = parse_qs(parsed_url.query)
                return query_params.get('v', [None])[0]
        return None
    
    def get_video_info(self, video_id_or_url):
        """Get video information"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_id_or_url, download=False)
                return info
        except Exception as e:
            print(f"{Fore.RED}Error getting video info: {e}{Style.RESET_ALL}")
            return None
    
    def play_video(self, video_id_or_url, audio_only=True):
        """Play video with specified options"""
        try:
            # Stop any currently playing video
            self.stop_playback()
            
            # Configure yt-dlp options for streaming
            ydl_opts = {
                'format': 'bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio/best' if audio_only else 'best[height<=720]/best',
                'quiet': True,
                'no_warnings': True,
                'extractaudio': False,  # Don't extract, just get the URL
                'outtmpl': '-',  # Output to stdout for streaming
            }
            
            # Get video info and URL directly
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_id_or_url, download=False)
            
            if not info:
                print(f"{Fore.RED}Could not get video information{Style.RESET_ALL}")
                return False
            
            print(f"{Fore.GREEN}Now playing: {info.get('title', 'Unknown')}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Duration: {info.get('duration', 'Unknown')} seconds{Style.RESET_ALL}")
            
            # Get the direct URL
            video_url = info.get('url')
            if not video_url:
                print(f"{Fore.RED}No stream URL found{Style.RESET_ALL}")
                return False
            
            # Start playback using ffplay
            if audio_only:
                cmd = ['ffplay'] + config.FFMPEG_AUDIO_OPTIONS + ['-volume', str(self.volume), '-i', video_url]
            else:
                cmd = ['ffplay'] + config.FFMPEG_VIDEO_OPTIONS + ['-volume', str(self.volume), '-i', video_url]
            
            self.current_process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.is_playing = True
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}Error playing video: {e}{Style.RESET_ALL}")
            return False
    
    def stop_playback(self):
        """Stop currently playing video"""
        if self.current_process and self.current_process.poll() is None:
            self.current_process.terminate()
            self.current_process.wait()
        self.is_playing = False
    
    def set_volume(self, volume):
        """Set volume level (1-100)"""
        if 1 <= volume <= 100:
            self.volume = volume
            print(f"{Fore.YELLOW}Volume set to: {volume}%{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Volume must be between 1 and 100{Style.RESET_ALL}")
    
    def display_search_results(self, results):
        """Display search results in a formatted way"""
        if not results:
            print(f"{Fore.YELLOW}No results found{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}Search Results:{Style.RESET_ALL}")
        print("-" * 80)
        
        for i, video in enumerate(results[:10], 1):
            title = video.get('title', 'Unknown Title')
            duration = video.get('duration', 'Unknown')
            uploader = video.get('uploader', 'Unknown')
            
            # Truncate long titles
            if len(title) > 70:
                title = title[:67] + "..."
            
            print(f"{Fore.GREEN}{i:2d}.{Style.RESET_ALL} {title}")
            print(f"    Duration: {duration}s | Uploader: {uploader}")
            print()
    
    def show_help(self):
        """Display help information"""
        help_text = f"""
{Fore.CYAN}u2b - YouTube Command Line Player{Style.RESET_ALL}

{Fore.GREEN}Commands:{Style.RESET_ALL}
  <search term>     - Search and play the first result
  <youtube url>     - Play video from YouTube URL
  volume <1-100>    - Set volume level
  stop              - Stop current playback
  help              - Show this help
  quit/exit         - Exit the application

{Fore.YELLOW}Examples:{Style.RESET_ALL}
  never gonna give you up
  https://www.youtube.com/watch?v=dQw4w9WgXcQ
  volume 75
  stop

{Fore.CYAN}Features:{Style.RESET_ALL}
  - Audio-only playback (no ads)
  - Volume control (1-100)
  - Direct URL support
  - Search functionality
"""
        print(help_text)

def main():
    """Main application loop"""
    player = U2BPlayer()
    
    print(f"{Fore.CYAN}Welcome to u2b - YouTube Command Line Player{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Type 'help' for commands or 'quit' to exit{Style.RESET_ALL}")
    print()
    
    while True:
        try:
            # Get user input
            user_input = input(f"{Fore.GREEN}u2b> {Style.RESET_ALL}").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['quit', 'exit']:
                player.stop_playback()
                print(f"{Fore.CYAN}Goodbye!{Style.RESET_ALL}")
                break
            
            elif user_input.lower() == 'help':
                player.show_help()
            
            elif user_input.lower() == 'stop':
                player.stop_playback()
                print(f"{Fore.YELLOW}Playback stopped{Style.RESET_ALL}")
            
            elif user_input.lower().startswith('volume '):
                try:
                    volume = int(user_input.split()[1])
                    player.set_volume(volume)
                except (IndexError, ValueError):
                    print(f"{Fore.RED}Usage: volume <1-100>{Style.RESET_ALL}")
            
            elif user_input.startswith('http'):
                # Direct URL
                video_id = player.extract_video_id(user_input)
                if video_id:
                    player.play_video(user_input)
                else:
                    print(f"{Fore.RED}Invalid YouTube URL{Style.RESET_ALL}")
            
            else:
                # Search query
                print(f"{Fore.YELLOW}Searching for: {user_input}{Style.RESET_ALL}")
                results = player.search_youtube(user_input)
                
                if results:
                    # Play the first result
                    first_video = results[0]
                    video_url = f"https://www.youtube.com/watch?v={first_video['id']}"
                    player.play_video(video_url)
                else:
                    print(f"{Fore.RED}No videos found for: {user_input}{Style.RESET_ALL}")
        
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Interrupted by user{Style.RESET_ALL}")
            player.stop_playback()
            break
        
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main() 