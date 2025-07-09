import re
import logging
from bs4 import BeautifulSoup, Comment
from urllib.parse import urlparse, urljoin
from typing import Dict, List, Any

class SEOAnalyzer:
    """SEO and content marketing metrics analyzer"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Common CTA patterns
        self.cta_patterns = [
            r'\b(buy\s+now|purchase|order\s+now|get\s+started|sign\s+up|subscribe|download|learn\s+more|contact\s+us|call\s+now|book\s+now|try\s+free|free\s+trial|get\s+quote)\b',
            r'\b(click\s+here|read\s+more|view\s+more|see\s+more|shop\s+now|add\s+to\s+cart|checkout|register|join\s+now|apply\s+now)\b'
        ]
        
        # Media element tags
        self.media_tags = ['img', 'video', 'audio', 'iframe', 'embed', 'object']
    
    def analyze(self, html_content: str, url: str = '', primary_keyword: str = '', related_keywords: List[str] = None) -> Dict[str, Any]:
        """
        Analyze HTML content and return SEO metrics
        
        Args:
            html_content: Raw HTML source code
            url: URL of the page (optional)
            primary_keyword: Primary keyword to search for
            related_keywords: List of related keywords to analyze
            
        Returns:
            Dictionary containing SEO analysis results
        """
        if related_keywords is None:
            related_keywords = []
        
        try:
            # Parse HTML with BeautifulSoup
            soup = BeautifulSoup(html_content, 'lxml')
            
            # Extract basic information
            title = self._extract_title(soup)
            content_type = self._determine_content_type(soup, title)
            
            # Clean and extract text content
            clean_text = self._extract_clean_text(soup)
            word_count = self._count_words(clean_text)
            
            # Extract headings
            headings = self._extract_headings(soup)
            
            # Analyze keywords
            primary_kw_freq = self._count_keyword_frequency(clean_text, primary_keyword)
            related_kw_freq = self._count_related_keywords(clean_text, related_keywords)
            
            # Detect media and CTAs
            has_media = self._detect_media(soup)
            has_cta = self._detect_cta(soup, clean_text)
            
            # Generate clean body sample
            clean_body = self._generate_clean_body_sample(clean_text)
            
            # Analyze keyword placement
            keyword_placement = self._analyze_keyword_placement(soup, primary_keyword, title, headings, clean_text)
            
            # Analyze paragraph style
            paragraph_style = self._analyze_paragraph_style(soup)
            
            # Build result
            result = {
                "url": url,
                "title": title,
                "type": content_type,
                "wordCount": word_count,
                "headings": headings,
                "primaryKWfreq": primary_kw_freq,
                "relatedKWfreq": related_kw_freq,
                "hasMedia": has_media,
                "hasCTA": has_cta,
                "cleanBody": clean_body,
                "keywordPlacement": keyword_placement,
                "paragraphStyle": paragraph_style
            }
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error analyzing HTML: {str(e)}")
            raise
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title"""
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text().strip()
        
        # Fallback to h1 if no title tag
        h1_tag = soup.find('h1')
        if h1_tag:
            return h1_tag.get_text().strip()
        
        return "No title found"
    
    def _determine_content_type(self, soup: BeautifulSoup, title: str) -> str:
        """Determine content type based on page structure and title"""
        # Check for common patterns in title and content
        title_lower = title.lower()
        
        # Check for blog/article indicators
        if soup.find('article') or soup.find('time') or soup.find(attrs={'class': re.compile(r'blog|post|article', re.I)}):
            return "blog"
        
        # Check for product page indicators
        if any(keyword in title_lower for keyword in ['buy', 'price', 'product', 'shop', 'store']):
            return "product"
        
        # Check for service page indicators
        if any(keyword in title_lower for keyword in ['service', 'consulting', 'hire', 'expert']):
            return "service"
        
        # Check for landing page indicators
        if soup.find('form') and any(keyword in title_lower for keyword in ['signup', 'register', 'get started']):
            return "landing"
        
        # Default to informational
        return "informational"
    
    def _extract_clean_text(self, soup: BeautifulSoup) -> str:
        """Extract clean text content from HTML body only"""
        # Find the body tag, if it doesn't exist, use the whole document
        body = soup.find('body')
        if not body:
            body = soup
        
        # Remove script and style elements from body
        for script in body(["script", "style", "noscript"]):
            script.decompose()
        
        # Remove comments from body
        for comment in body.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()
        
        # Remove hidden elements from body
        for hidden in body.find_all(attrs={'style': re.compile(r'display\s*:\s*none', re.I)}):
            hidden.decompose()
        
        # Get text content with better spacing from body only
        text = body.get_text(separator=' ', strip=True)
        
        # Clean up whitespace but preserve sentence structure
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    def _count_words(self, text: str) -> int:
        """Count words in text"""
        # Split by whitespace and filter out empty strings
        words = [word for word in text.split() if word.strip()]
        return len(words)
    
    def _extract_headings(self, soup: BeautifulSoup) -> List[str]:
        """Extract all headings from HTML"""
        headings = []
        
        # Find all heading tags (h1-h6)
        for i in range(1, 7):
            heading_tags = soup.find_all(f'h{i}')
            for tag in heading_tags:
                heading_text = tag.get_text().strip()
                if heading_text:
                    headings.append(heading_text)
        
        return headings
    
    def _count_keyword_frequency(self, text: str, keyword: str) -> int:
        """Count frequency of primary keyword (case-insensitive)"""
        if not keyword:
            return 0
        
        keyword = keyword.strip().lower()
        text = text.lower()
        
        # Handle multi-word keywords differently
        if ' ' in keyword:
            # For multi-word keywords, use simple substring matching
            return text.count(keyword)
        else:
            # For single words, use word boundary matching
            pattern = r'\b' + re.escape(keyword) + r'\b'
            matches = re.findall(pattern, text)
            return len(matches)
    
    def _count_related_keywords(self, text: str, keywords: List[str]) -> Dict[str, int]:
        """Count frequency of related keywords"""
        result = {}
        
        for keyword in keywords:
            if keyword:
                frequency = self._count_keyword_frequency(text, keyword)
                result[keyword] = frequency
        
        return result
    
    def _detect_media(self, soup: BeautifulSoup) -> bool:
        """Detect presence of media elements"""
        # Check for media tags
        for tag in self.media_tags:
            if soup.find(tag):
                return True
        
        # Check for common media class names
        media_classes = soup.find_all(attrs={'class': re.compile(r'media|image|video|audio|gallery', re.I)})
        if media_classes:
            return True
        
        return False
    
    def _detect_cta(self, soup: BeautifulSoup, text: str) -> bool:
        """Detect presence of call-to-action elements"""
        # Check for forms
        if soup.find('form'):
            return True
        
        # Check for buttons
        buttons = soup.find_all(['button', 'input'])
        for button in buttons:
            if button.get('type') in ['submit', 'button'] or button.name == 'button':
                return True
        
        # Check for links with CTA-like text
        links = soup.find_all('a')
        for link in links:
            link_text = link.get_text().strip().lower()
            href = link.get('href', '')
            
            # Check for mailto links
            if href.startswith('mailto:'):
                return True
            
            # Check for CTA patterns in link text
            for pattern in self.cta_patterns:
                if re.search(pattern, link_text, re.IGNORECASE):
                    return True
        
        # Check for CTA patterns in general text
        for pattern in self.cta_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False
    
    def _generate_clean_body_sample(self, text: str, max_length: int = 500) -> str:
        """Generate a clean body text sample for analysis"""
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text).strip()
        
        # If text is shorter than max_length, return complete text
        if len(text) <= max_length:
            return text
        
        # For longer text, find a good breaking point
        truncated = text[:max_length]
        
        # Try to break at sentence end
        last_period = truncated.rfind('.')
        last_exclamation = truncated.rfind('!')
        last_question = truncated.rfind('?')
        
        best_break = max(last_period, last_exclamation, last_question)
        
        # If we found a good sentence break point, use it
        if best_break > max_length * 0.7:
            return truncated[:best_break + 1].strip()
        
        # Otherwise, break at last space and add ellipsis
        last_space = truncated.rfind(' ')
        if last_space > 0:
            return truncated[:last_space].strip() + "..."
        
        return truncated + "..."
    
    def _analyze_keyword_placement(self, soup: BeautifulSoup, keyword: str, title: str, headings: List[str], text: str) -> Dict[str, Any]:
        """Analyze keyword placement in different sections"""
        if not keyword:
            return {
                "inTitle": False,
                "inHeadings": False,
                "inIntro": False,
                "inBody": False,
                "placement": []
            }
        
        keyword_lower = keyword.lower()
        placement = []
        
        # Check title
        in_title = keyword_lower in title.lower()
        if in_title:
            placement.append("title")
        
        # Check headings
        in_headings = any(keyword_lower in heading.lower() for heading in headings)
        if in_headings:
            placement.append("headings")
        
        # Check intro (first 200 characters of body text)
        intro_text = text[:200].lower()
        in_intro = keyword_lower in intro_text
        if in_intro:
            placement.append("intro")
        
        # Check body content
        in_body = keyword_lower in text.lower()
        if in_body and not in_intro:
            placement.append("body")
        
        return {
            "inTitle": in_title,
            "inHeadings": in_headings,
            "inIntro": in_intro,
            "inBody": in_body,
            "placement": placement
        }
    
    def _analyze_paragraph_style(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze paragraph style and structure"""
        # Find body tag
        body = soup.find('body')
        if not body:
            body = soup
        
        # Find all paragraphs
        paragraphs = body.find_all('p')
        
        # Calculate paragraph lengths
        paragraph_lengths = []
        for p in paragraphs:
            text = p.get_text().strip()
            if text:  # Only count non-empty paragraphs
                words = len(text.split())
                paragraph_lengths.append(words)
        
        # Calculate average paragraph length
        avg_length = sum(paragraph_lengths) / len(paragraph_lengths) if paragraph_lengths else 0
        
        # Check for bullet points and lists
        bullet_lists = body.find_all(['ul', 'ol'])
        has_bullets = len(bullet_lists) > 0
        
        # Count list items
        list_items = body.find_all('li')
        bullet_count = len(list_items)
        
        # Analyze paragraph distribution
        short_paragraphs = sum(1 for length in paragraph_lengths if length < 20)
        medium_paragraphs = sum(1 for length in paragraph_lengths if 20 <= length < 50)
        long_paragraphs = sum(1 for length in paragraph_lengths if length >= 50)
        
        return {
            "avgParagraphLength": round(avg_length, 1),
            "totalParagraphs": len(paragraph_lengths),
            "shortParagraphs": short_paragraphs,
            "mediumParagraphs": medium_paragraphs,
            "longParagraphs": long_paragraphs,
            "hasBullets": has_bullets,
            "bulletCount": bullet_count,
            "listTypes": len(bullet_lists)
        }
