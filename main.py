import json
import os
import logging
from seo_analyzer import SEOAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        # Load input data from Apify
        with open(os.environ['APIFY_INPUT_PATH'], 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Extract required fields
        html_content = data.get('html')
        url = data.get('url', '')
        primary_keyword = data.get('primaryKeyword', '')
        related_keywords = data.get('relatedKeywords', [])

        if not html_content:
            raise ValueError("HTML content is required")

        # Run analysis
        analyzer = SEOAnalyzer()
        result = analyzer.analyze(
            html_content=html_content,
            url=url,
            primary_keyword=primary_keyword,
            related_keywords=related_keywords
        )

        # Save result to Apify output
        with open(os.environ['APIFY_OUTPUT_PATH'], 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Error in Apify actor: {str(e)}")
        # Optionally write error to output
        with open(os.environ['APIFY_OUTPUT_PATH'], 'w', encoding='utf-8') as f:
            json.dump({"error": str(e)}, f, ensure_ascii=False, indent=2)
        raise

if __name__ == "__main__":
    main()
