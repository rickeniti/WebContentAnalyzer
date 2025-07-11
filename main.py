import json
import os
import logging
from seo_analyzer import SEOAnalyzer
from apify import Actor
from seo_analyzer import SEOAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    async with Actor:
        # Get input
        data = await Actor.get_input() or {}

        # Extract fields
        html_content = data.get("html", "")
        url = data.get("url", "")
        primary_keyword = data.get("primaryKeyword", "")
        related_keywords = data.get("relatedKeywords", [])

        # Run analysis
        analyzer = SEOAnalyzer()
        result = analyzer.analyze(
            html_content=html_content,
            url=url,
            primary_keyword=primary_keyword,
            related_keywords=related_keywords,
        )

        # Save result
        await Actor.set_value("OUTPUT", result)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
