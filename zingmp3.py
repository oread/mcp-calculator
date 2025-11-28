# zingmp3.py
from fastmcp import FastMCP
import sys
import logging
import requests
import webbrowser
from typing import Optional, Dict, Any
import urllib.parse

logger = logging.getLogger('ZingMP3')

# Fix UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stderr.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

# Create an MCP server
mcp = FastMCP("ZingMP3")


@mcp.tool()
def search_song(
    query: str,
    limit: Optional[int] = 5
) -> dict:
    """
    Search for songs on Zing MP3.
    
    Args:
        query: Search query (song name, artist name, or keywords)
        limit: Maximum number of results to return (default: 5)
    
    Returns:
        Dictionary with success status and search results
    """
    try:
        # Zing MP3 search URL
        search_url = f"https://zingmp3.vn/tim-kiem/tat-ca?q={urllib.parse.quote(query)}"
        
        logger.info(f"Searching for: {query}")
        
        return {
            "success": True,
            "query": query,
            "search_url": search_url,
            "message": f"Search URL generated for: {query}",
            "instructions": "Open the search_url in your browser to see results"
        }
        
    except Exception as e:
        logger.error(f"Search failed: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def play_song(
    song_url: str
) -> dict:
    """
    Play a song from Zing MP3 by opening it in the default browser.
    
    Args:
        song_url: Direct URL to the song on Zing MP3 (e.g., 'https://zingmp3.vn/bai-hat/...')
    
    Returns:
        Dictionary with success status
    """
    try:
        if not song_url.startswith('http'):
            return {
                "success": False,
                "error": "Invalid URL. Please provide a complete Zing MP3 URL starting with http:// or https://"
            }
        
        # Open the URL in default browser
        webbrowser.open(song_url)
        
        logger.info(f"Opening song: {song_url}")
        
        return {
            "success": True,
            "message": "Song opened in default browser",
            "url": song_url
        }
        
    except Exception as e:
        logger.error(f"Failed to play song: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def play_artist(
    artist_name: str
) -> dict:
    """
    Open an artist page on Zing MP3.
    
    Args:
        artist_name: Name of the artist
    
    Returns:
        Dictionary with success status and artist URL
    """
    try:
        # Create artist search URL
        artist_url = f"https://zingmp3.vn/tim-kiem/tat-ca?q={urllib.parse.quote(artist_name)}"
        
        # Open in browser
        webbrowser.open(artist_url)
        
        logger.info(f"Opening artist page for: {artist_name}")
        
        return {
            "success": True,
            "artist": artist_name,
            "url": artist_url,
            "message": f"Artist page for '{artist_name}' opened in browser"
        }
        
    except Exception as e:
        logger.error(f"Failed to open artist page: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def play_playlist(
    playlist_url: str
) -> dict:
    """
    Play a playlist from Zing MP3.
    
    Args:
        playlist_url: Direct URL to the playlist on Zing MP3 (e.g., 'https://zingmp3.vn/playlist/...')
    
    Returns:
        Dictionary with success status
    """
    try:
        if not playlist_url.startswith('http'):
            return {
                "success": False,
                "error": "Invalid URL. Please provide a complete Zing MP3 playlist URL"
            }
        
        # Open the playlist in browser
        webbrowser.open(playlist_url)
        
        logger.info(f"Opening playlist: {playlist_url}")
        
        return {
            "success": True,
            "message": "Playlist opened in default browser",
            "url": playlist_url
        }
        
    except Exception as e:
        logger.error(f"Failed to play playlist: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def browse_chart(
    chart_type: Optional[str] = "realtime"
) -> dict:
    """
    Open Zing MP3 music charts.
    
    Args:
        chart_type: Type of chart to browse. Options:
                   - 'realtime': Real-time trending chart (default)
                   - 'week': Weekly top chart
                   - 'vpop': Vietnamese pop chart
                   - 'usuk': US-UK pop chart
                   - 'kpop': K-pop chart
    
    Returns:
        Dictionary with success status and chart URL
    """
    try:
        chart_urls = {
            "realtime": "https://zingmp3.vn/zing-chart",
            "week": "https://zingmp3.vn/zing-chart-tuan",
            "vpop": "https://zingmp3.vn/zing-chart/bai-hat-Viet-Nam",
            "usuk": "https://zingmp3.vn/zing-chart/bai-hat-US-UK",
            "kpop": "https://zingmp3.vn/zing-chart/bai-hat-KPop"
        }
        
        chart_url = chart_urls.get(chart_type.lower(), chart_urls["realtime"])
        
        # Open chart in browser
        webbrowser.open(chart_url)
        
        logger.info(f"Opening chart: {chart_type}")
        
        return {
            "success": True,
            "chart_type": chart_type,
            "url": chart_url,
            "message": f"Chart '{chart_type}' opened in browser"
        }
        
    except Exception as e:
        logger.error(f"Failed to open chart: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def browse_genre(
    genre: str
) -> dict:
    """
    Browse songs by genre on Zing MP3.
    
    Args:
        genre: Music genre to browse. Examples:
              - 'pop', 'rock', 'rap', 'edm', 'ballad', 'jazz', 'classical', etc.
    
    Returns:
        Dictionary with success status and genre URL
    """
    try:
        # Create genre search URL
        genre_url = f"https://zingmp3.vn/tim-kiem/tat-ca?q={urllib.parse.quote(genre)}"
        
        # Open in browser
        webbrowser.open(genre_url)
        
        logger.info(f"Browsing genre: {genre}")
        
        return {
            "success": True,
            "genre": genre,
            "url": genre_url,
            "message": f"Genre '{genre}' opened in browser"
        }
        
    except Exception as e:
        logger.error(f"Failed to browse genre: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def get_song_info(
    song_name: str,
    artist_name: Optional[str] = None
) -> dict:
    """
    Get information about a specific song.
    
    Args:
        song_name: Name of the song
        artist_name: Name of the artist (optional, helps narrow search)
    
    Returns:
        Dictionary with success status and search URL
    """
    try:
        # Build search query
        if artist_name:
            query = f"{song_name} {artist_name}"
        else:
            query = song_name
        
        search_url = f"https://zingmp3.vn/tim-kiem/tat-ca?q={urllib.parse.quote(query)}"
        
        logger.info(f"Getting info for: {query}")
        
        return {
            "success": True,
            "song_name": song_name,
            "artist_name": artist_name,
            "search_url": search_url,
            "message": f"Search results for '{query}'",
            "instructions": "Open the search_url to see song details, lyrics, and play options"
        }
        
    except Exception as e:
        logger.error(f"Failed to get song info: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def open_zingmp3_home() -> dict:
    """
    Open Zing MP3 homepage.
    
    Returns:
        Dictionary with success status
    """
    try:
        home_url = "https://zingmp3.vn"
        
        webbrowser.open(home_url)
        
        logger.info("Opening Zing MP3 homepage")
        
        return {
            "success": True,
            "url": home_url,
            "message": "Zing MP3 homepage opened in browser"
        }
        
    except Exception as e:
        logger.error(f"Failed to open homepage: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


# Start the server
if __name__ == "__main__":
    mcp.run(transport="stdio")
