# vnexpress.py
from fastmcp import FastMCP
import sys
import logging
import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any, List
import webbrowser

logger = logging.getLogger('VNExpress')

# Fix UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stderr.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

# Create an MCP server
mcp = FastMCP("VNExpress")


@mcp.tool()
def get_latest_news(
    category: Optional[str] = "trang-chu",
    limit: Optional[int] = 10
) -> dict:
    """
    Get latest news from VNExpress.net.
    
    Args:
        category: News category. Options:
                 - 'trang-chu': Homepage (default)
                 - 'thoi-su': Politics
                 - 'goc-nhin': Perspectives
                 - 'the-gioi': World
                 - 'kinh-doanh': Business
                 - 'khoa-hoc': Science
                 - 'giai-tri': Entertainment
                 - 'the-thao': Sports
                 - 'phap-luat': Law
                 - 'giao-duc': Education
                 - 'suc-khoe': Health
                 - 'gia-dinh': Family
                 - 'du-lich': Travel
                 - 'so-hoa': Digital
                 - 'xe': Automotive
        limit: Maximum number of articles to return (default: 10)
    
    Returns:
        Dictionary with success status and list of news articles
    """
    try:
        # Build URL
        if category == "trang-chu":
            url = "https://vnexpress.net"
        else:
            url = f"https://vnexpress.net/{category}"
        
        # Set headers to mimic browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Fetch the page
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find news articles
        articles = []
        
        # VNExpress uses different classes for articles
        article_elements = soup.find_all('article', class_='item-news', limit=limit * 2)
        
        for article in article_elements[:limit]:
            try:
                # Extract title and link
                title_tag = article.find('h3', class_='title-news') or article.find('h2', class_='title-news')
                if not title_tag:
                    continue
                    
                link_tag = title_tag.find('a')
                if not link_tag:
                    continue
                
                title = link_tag.get_text(strip=True)
                link = link_tag.get('href', '')
                
                # Make sure link is absolute
                if link and not link.startswith('http'):
                    link = 'https://vnexpress.net' + link
                
                # Extract description
                desc_tag = article.find('p', class_='description')
                description = desc_tag.get_text(strip=True) if desc_tag else ""
                
                # Extract thumbnail
                thumb_tag = article.find('img')
                thumbnail = thumb_tag.get('data-src') or thumb_tag.get('src') if thumb_tag else ""
                
                articles.append({
                    'title': title,
                    'link': link,
                    'description': description,
                    'thumbnail': thumbnail
                })
                
            except Exception as e:
                logger.warning(f"Error parsing article: {str(e)}")
                continue
        
        logger.info(f"Retrieved {len(articles)} articles from category: {category}")
        
        return {
            "success": True,
            "category": category,
            "count": len(articles),
            "articles": articles,
            "source_url": url
        }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch news: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch news: {str(e)}"
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def search_news(
    query: str,
    limit: Optional[int] = 10
) -> dict:
    """
    Search for news articles on VNExpress.net.
    
    Args:
        query: Search keywords
        limit: Maximum number of results to return (default: 10)
    
    Returns:
        Dictionary with success status and search results
    """
    try:
        import urllib.parse
        
        # Build search URL
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://vnexpress.net/tim-kiem?q={encoded_query}"
        
        # Set headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Fetch search results
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find search results
        articles = []
        article_elements = soup.find_all('article', class_='item-news', limit=limit * 2)
        
        for article in article_elements[:limit]:
            try:
                # Extract title and link
                title_tag = article.find('h3', class_='title-news') or article.find('h2', class_='title-news')
                if not title_tag:
                    continue
                    
                link_tag = title_tag.find('a')
                if not link_tag:
                    continue
                
                title = link_tag.get_text(strip=True)
                link = link_tag.get('href', '')
                
                if link and not link.startswith('http'):
                    link = 'https://vnexpress.net' + link
                
                # Extract description
                desc_tag = article.find('p', class_='description')
                description = desc_tag.get_text(strip=True) if desc_tag else ""
                
                articles.append({
                    'title': title,
                    'link': link,
                    'description': description
                })
                
            except Exception as e:
                logger.warning(f"Error parsing search result: {str(e)}")
                continue
        
        logger.info(f"Found {len(articles)} articles for query: {query}")
        
        return {
            "success": True,
            "query": query,
            "count": len(articles),
            "articles": articles,
            "search_url": search_url
        }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Search failed: {str(e)}")
        return {
            "success": False,
            "error": f"Search failed: {str(e)}"
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def get_article_content(
    article_url: str
) -> dict:
    """
    Get full content of a specific article from VNExpress.net.
    
    Args:
        article_url: Full URL of the article
    
    Returns:
        Dictionary with success status and article content
    """
    try:
        if not article_url.startswith('http'):
            return {
                "success": False,
                "error": "Invalid URL. Please provide a complete article URL"
            }
        
        # Set headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Fetch article
        response = requests.get(article_url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract title
        title_tag = soup.find('h1', class_='title-detail')
        title = title_tag.get_text(strip=True) if title_tag else ""
        
        # Extract description/summary
        desc_tag = soup.find('p', class_='description')
        description = desc_tag.get_text(strip=True) if desc_tag else ""
        
        # Extract author and date
        author_tag = soup.find('p', class_='author_mail')
        author = author_tag.get_text(strip=True) if author_tag else ""
        
        # Extract content
        content_div = soup.find('article', class_='fck_detail')
        content_paragraphs = []
        
        if content_div:
            # Get all paragraphs
            paragraphs = content_div.find_all('p', class_='Normal')
            for p in paragraphs:
                text = p.get_text(strip=True)
                if text:
                    content_paragraphs.append(text)
        
        content = '\n\n'.join(content_paragraphs)
        
        logger.info(f"Retrieved article: {title}")
        
        return {
            "success": True,
            "title": title,
            "description": description,
            "author": author,
            "content": content,
            "url": article_url,
            "content_length": len(content)
        }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch article: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch article: {str(e)}"
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def open_article(
    article_url: str
) -> dict:
    """
    Open an article in the default browser.
    
    Args:
        article_url: Full URL of the article
    
    Returns:
        Dictionary with success status
    """
    try:
        if not article_url.startswith('http'):
            return {
                "success": False,
                "error": "Invalid URL. Please provide a complete article URL"
            }
        
        webbrowser.open(article_url)
        
        logger.info(f"Opening article: {article_url}")
        
        return {
            "success": True,
            "message": "Article opened in default browser",
            "url": article_url
        }
        
    except Exception as e:
        logger.error(f"Failed to open article: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def get_trending_news(
    limit: Optional[int] = 10
) -> dict:
    """
    Get trending/most read news from VNExpress.net.
    
    Args:
        limit: Maximum number of articles to return (default: 10)
    
    Returns:
        Dictionary with success status and trending articles
    """
    try:
        url = "https://vnexpress.net"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = []
        
        # Look for most read section
        most_read = soup.find('div', class_='box-category') or soup.find('div', class_='most-read')
        
        if most_read:
            article_elements = most_read.find_all('article', limit=limit)
            
            for article in article_elements:
                try:
                    title_tag = article.find('h3') or article.find('h2')
                    if not title_tag:
                        continue
                    
                    link_tag = title_tag.find('a')
                    if not link_tag:
                        continue
                    
                    title = link_tag.get_text(strip=True)
                    link = link_tag.get('href', '')
                    
                    if link and not link.startswith('http'):
                        link = 'https://vnexpress.net' + link
                    
                    articles.append({
                        'title': title,
                        'link': link
                    })
                    
                except Exception as e:
                    logger.warning(f"Error parsing trending article: {str(e)}")
                    continue
        
        logger.info(f"Retrieved {len(articles)} trending articles")
        
        return {
            "success": True,
            "count": len(articles),
            "articles": articles
        }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch trending news: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch trending news: {str(e)}"
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def list_categories() -> dict:
    """
    List all available news categories on VNExpress.net.
    
    Returns:
        Dictionary with success status and list of categories
    """
    categories = {
        "trang-chu": "Homepage - Latest news",
        "thoi-su": "Politics - National politics and current affairs",
        "goc-nhin": "Perspectives - Opinions and analyses",
        "the-gioi": "World - International news",
        "kinh-doanh": "Business - Economy and business news",
        "khoa-hoc": "Science - Technology and science",
        "giai-tri": "Entertainment - Movies, music, celebrities",
        "the-thao": "Sports - Sports news and updates",
        "phap-luat": "Law - Legal news and crime",
        "giao-duc": "Education - Education and learning",
        "suc-khoe": "Health - Health and wellness",
        "gia-dinh": "Family - Family and relationships",
        "du-lich": "Travel - Tourism and travel guides",
        "so-hoa": "Digital - Technology and gadgets",
        "xe": "Automotive - Cars and motorcycles"
    }
    
    return {
        "success": True,
        "categories": categories,
        "count": len(categories)
    }


# Start the server
if __name__ == "__main__":
    mcp.run(transport="stdio")
