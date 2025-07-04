import os
import logging
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from seo_analyzer import SEOAnalyzer

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Enable CORS for n8n integration
CORS(app)

# Initialize SEO analyzer
seo_analyzer = SEOAnalyzer()

@app.route('/')
def index():
    """Main web interface for SEO analysis"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_api():
    """API endpoint for n8n workflow integration"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Extract required fields
        html_content = data.get('html')
        url = data.get('url', '')
        primary_keyword = data.get('primaryKeyword', '')
        related_keywords = data.get('relatedKeywords', [])
        
        if not html_content:
            return jsonify({"error": "HTML content is required"}), 400
        
        # Analyze HTML content
        result = seo_analyzer.analyze(
            html_content=html_content,
            url=url,
            primary_keyword=primary_keyword,
            related_keywords=related_keywords
        )
        
        return jsonify(result)
        
    except Exception as e:
        logging.error(f"Error in API analysis: {str(e)}")
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

@app.route('/analyze', methods=['POST'])
def analyze_web():
    """Web interface analysis endpoint"""
    try:
        # Get form data
        html_content = request.form.get('html_content', '')
        url = request.form.get('url', '')
        primary_keyword = request.form.get('primary_keyword', '')
        related_keywords_str = request.form.get('related_keywords', '')
        
        # Parse related keywords
        related_keywords = [kw.strip() for kw in related_keywords_str.split(',') if kw.strip()]
        
        if not html_content:
            return render_template('index.html', error="HTML content is required")
        
        # Analyze HTML content
        result = seo_analyzer.analyze(
            html_content=html_content,
            url=url,
            primary_keyword=primary_keyword,
            related_keywords=related_keywords
        )
        
        return render_template('index.html', result=result)
        
    except Exception as e:
        logging.error(f"Error in web analysis: {str(e)}")
        return render_template('index.html', error=f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
