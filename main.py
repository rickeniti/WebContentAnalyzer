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
        try:
            # Load input data from Apify
            result = SEOAnalyzer().analyze(
                html_content=data.get("html", ""),
                url=data.get("url", ""),
                primary_keyword=data.get("primaryKeyword", ""),
                related_keywords=data.get("relatedKeywords", []),
            )
    
            # Save result to Apify output
            await Actor.set_value("OUTPUT", result)
    
        except Exception as e:
            logger.error(f"Error in Apify actor: {str(e)}")
            # Optionally write error to output
            await Actor.set_value("OUTPUT", e)
            raise


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
