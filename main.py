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
import threading
import time
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
        self.queue = []
        self.current_track = None
        self.queue_lock = threading.Lock()
        self.player_thread = None
        
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
    
    def play_video(self, video_id_or_url, audio_only=True, add_to_queue=False):
        """Play video with specified options"""
        try:
            # Get video info first
            ydl_opts = {
                'format': 'bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio/best' if audio_only else 'best[height<=720]/best',
                'quiet': True,
                'no_warnings': True,
                'extractaudio': False,
                'outtmpl': '-',
            }
            
            # Get video info
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_id_or_url, download=False)
            
            if not info:
                print(f"{Fore.RED}Could not get video information{Style.RESET_ALL}")
                return False
            
            # If something is already playing and we're not explicitly adding to queue
            if self.is_playing and not add_to_queue:
                # Add to queue instead of stopping current track
                self.add_to_queue(info)
                return True
            
            # If nothing is playing, start playing immediately
            if not self.is_playing:
                self.current_track = info
                self._play_track(info)
                return True
            
            # If we're explicitly adding to queue
            if add_to_queue:
                self.add_to_queue(info)
                return True
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}Error playing video: {e}{Style.RESET_ALL}")
            return False
    
    def stop_playback(self):
        """Stop currently playing video"""
        self.is_playing = False  # Set this first to prevent auto-play next
        if self.current_process and self.current_process.poll() is None:
            self.current_process.terminate()
            try:
                self.current_process.wait(timeout=2)  # Wait up to 2 seconds
            except subprocess.TimeoutExpired:
                self.current_process.kill()  # Force kill if it doesn't terminate
        self.current_process = None
        self.current_track = None
    
    def set_volume(self, volume):
        """Set volume level (1-100)"""
        if 1 <= volume <= 100:
            self.volume = volume
            print(f"{Fore.YELLOW}Volume set to: {volume}%{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Volume must be between 1 and 100{Style.RESET_ALL}")
    
    def add_to_queue(self, video_info):
        """Add a video to the queue"""
        with self.queue_lock:
            self.queue.append(video_info)
            print(f"{Fore.CYAN}Added to queue: {video_info.get('title', 'Unknown')}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Queue length: {len(self.queue)}{Style.RESET_ALL}")
    
    def get_queue_info(self):
        """Get current queue information"""
        with self.queue_lock:
            return {
                'current': self.current_track,
                'queue': self.queue.copy(),
                'length': len(self.queue)
            }
    
    def show_queue(self):
        """Display current queue"""
        queue_info = self.get_queue_info()
        
        print(f"\n{Fore.CYAN}=== Current Queue ==={Style.RESET_ALL}")
        
        if queue_info['current']:
            print(f"{Fore.GREEN}▶ Now Playing: {queue_info['current'].get('title', 'Unknown')}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⏸ Nothing currently playing{Style.RESET_ALL}")
        
        if queue_info['queue']:
            print(f"\n{Fore.CYAN}Up Next:{Style.RESET_ALL}")
            for i, track in enumerate(queue_info['queue'], 1):
                duration = track.get('duration', 'Unknown')
                print(f"  {i}. {track.get('title', 'Unknown')} ({duration}s)")
        else:
            print(f"{Fore.YELLOW}  Queue is empty{Style.RESET_ALL}")
    
    def clear_queue(self):
        """Clear the queue"""
        with self.queue_lock:
            self.queue.clear()
            print(f"{Fore.YELLOW}Queue cleared{Style.RESET_ALL}")
    
    def skip_current(self):
        """Skip current track and play next in queue"""
        if self.current_process and self.current_process.poll() is None:
            # Temporarily disable auto-play next to prevent double-triggering
            was_playing = self.is_playing
            self.is_playing = False
            
            self.current_process.terminate()
            try:
                self.current_process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.current_process.kill()
            
            print(f"{Fore.YELLOW}Skipped current track{Style.RESET_ALL}")
            
            # Small delay to ensure process is fully terminated
            time.sleep(0.5)
            
            # Manually trigger next song
            if was_playing:
                self.play_next_in_queue()
    
    def play_next_in_queue(self):
        """Play the next track in the queue"""
        with self.queue_lock:
            if self.queue:
                next_track = self.queue.pop(0)
                self.current_track = next_track
                self._play_track(next_track)
            else:
                self.current_track = None
                self.is_playing = False
                print(f"{Fore.YELLOW}Queue finished{Style.RESET_ALL}")
    
    def _play_track(self, video_info):
        """Internal method to play a track"""
        try:
            print(f"{Fore.GREEN}Now playing: {video_info.get('title', 'Unknown')}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Duration: {video_info.get('duration', 'Unknown')} seconds{Style.RESET_ALL}")
            
            # Configure yt-dlp options for streaming
            ydl_opts = {
                'format': 'bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio/best[acodec!=none]',
                'quiet': True,
                'no_warnings': True,
                'extractaudio': False,
                'outtmpl': '-',
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            }
            
            # Get the direct URL
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_info['webpage_url'], download=False)
            
            if not info:
                print(f"{Fore.RED}Could not get video information{Style.RESET_ALL}")
                self.play_next_in_queue()
                return
            
            video_url = info.get('url')
            if not video_url:
                print(f"{Fore.RED}No stream URL found{Style.RESET_ALL}")
                self.play_next_in_queue()
                return
            
            # Use ffplay with better stream handling
            cmd = [
                'ffplay',
                '-nodisp',
                '-autoexit',
                '-hide_banner',
                '-loglevel', 'error',
                '-nostats',
                '-volume', str(self.volume),
                '-protocol_whitelist', 'file,http,https,tcp,tls,crypto',
                '-i', video_url
            ]
            
            # Start ffplay process
            self.current_process = subprocess.Popen(
                cmd, 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.PIPE,
                text=True
            )
            self.is_playing = True
            
            # Start a thread to monitor the process
            def monitor_playback():
                try:
                    # Check if process is valid before monitoring
                    if not self.current_process:
                        return
                    
                    # Wait for the process to complete naturally
                    return_code = self.current_process.wait()
                    
                    # Get any error output for debugging
                    stderr_output = self.current_process.stderr.read() if self.current_process and self.current_process.stderr else ""
                    
                    # Only play next if we're still supposed to be playing
                    if self.is_playing and return_code == 0:
                        self.play_next_in_queue()
                    elif return_code != 0:
                        print(f"{Fore.YELLOW}Track ended unexpectedly (code: {return_code}){Style.RESET_ALL}")
                        if stderr_output:
                            print(f"{Fore.YELLOW}Error: {stderr_output.strip()}{Style.RESET_ALL}")
                        if self.is_playing:
                            self.play_next_in_queue()
                            
                except Exception as e:
                    if self.is_playing:
                        print(f"{Fore.YELLOW}Playback interrupted: {e}{Style.RESET_ALL}")
                        self.play_next_in_queue()
            
            self.player_thread = threading.Thread(target=monitor_playback, daemon=True)
            self.player_thread.start()
            
        except Exception as e:
            print(f"{Fore.RED}Error playing track: {e}{Style.RESET_ALL}")
            self.play_next_in_queue()
    
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
  <search term>     - Search and add to queue (or play if nothing is playing)
  <youtube url>     - Add YouTube URL to queue (or play if nothing is playing)
  volume <1-100>    - Set volume level
  stop              - Stop current playback
  queue             - Show current queue
  clear             - Clear the queue
  skip              - Skip current track
  help              - Show this help
  quit/exit         - Exit the application

{Fore.YELLOW}Examples:{Style.RESET_ALL}
  never gonna give you up
  https://www.youtube.com/watch?v=dQw4w9WgXcQ
  volume 75
  queue
  skip
  clear

{Fore.CYAN}Features:{Style.RESET_ALL}
  - Audio-only playback (no ads)
  - Smart queue system
  - Volume control (1-100)
  - Direct URL support
  - Search functionality
  - Continuous playback
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
            
            elif user_input.lower() == 'queue':
                player.show_queue()
            
            elif user_input.lower() == 'clear':
                player.clear_queue()
            
            elif user_input.lower() == 'skip':
                player.skip_current()
            
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
                    # Add the first result to queue or play if nothing is playing
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