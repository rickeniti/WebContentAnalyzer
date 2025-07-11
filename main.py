from apify import Actor
from seo_analyzer import SEOAnalyzer
import logging

async def main():
    async with Actor:
        data = await Actor.get_input() or {}

        logging.info(f"Received input: {data}")

        html_content = data.get("html", "")
        url = data.get("url", "")
        primary_keyword = data.get("primaryKeyword", "")
        related_keywords = data.get("relatedKeywords", [])

        if not html_content:
            logging.warning("No HTML content provided. Skipping analysis.")
            await Actor.set_value("OUTPUT", {"error": "No HTML content provided"})
            return

        analyzer = SEOAnalyzer()
        result = analyzer.analyze(
            html_content=html_content,
            url=url,
            primary_keyword=primary_keyword,
            related_keywords=related_keywords,
        )

        logging.info(f"Analysis result: {result}")
        await Actor.set_value("OUTPUT", result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
