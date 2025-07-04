# SEO Content Analyzer

## Overview

This is a Flask-based web application designed to analyze HTML content for SEO metrics and content marketing insights. The application provides both a web interface for manual analysis and an API endpoint for integration with automation tools like n8n workflows.

## System Architecture

### Frontend Architecture
- **Framework**: HTML/CSS/JavaScript with Bootstrap for UI components
- **Theme**: Dark theme Bootstrap with custom styling
- **Interactivity**: Vanilla JavaScript for clipboard functionality and form handling
- **Structure**: Single-page application with form-based input and JSON output display

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Structure**: Modular design with separate analyzer logic
- **Entry Point**: `main.py` serves as the application runner
- **Core Logic**: `seo_analyzer.py` contains the SEO analysis engine

### API Design
- **REST API**: Single endpoint `/api/analyze` for POST requests
- **CORS Enabled**: Configured for cross-origin requests to support n8n integration
- **Input Format**: JSON payload with HTML content, URL, and keyword parameters
- **Output Format**: Structured JSON response with SEO metrics

## Key Components

### 1. Flask Application (`app.py`)
- **Purpose**: Main application setup and routing
- **Key Features**:
  - Web interface route (`/`)
  - API endpoint for analysis (`/api/analyze`)
  - CORS configuration for external integrations
  - Environment-based configuration

### 2. SEO Analyzer (`seo_analyzer.py`)
- **Purpose**: Core SEO analysis functionality
- **Key Features**:
  - HTML parsing with BeautifulSoup
  - Content type detection
  - Keyword analysis capabilities
  - CTA (Call-to-Action) pattern recognition
  - Media element detection
  - Text extraction and word counting

### 3. Web Interface (`templates/index.html`)
- **Purpose**: User-friendly web interface for SEO analysis
- **Key Features**:
  - Bootstrap-based responsive design
  - Form inputs for HTML content and keywords
  - JSON output display
  - Dark theme styling

### 4. Frontend JavaScript (`static/js/app.js`)
- **Purpose**: Client-side functionality
- **Key Features**:
  - Clipboard copy functionality
  - Toast notifications
  - Cross-browser compatibility

## Data Flow

1. **Web Interface Flow**:
   - User inputs HTML content and optional keywords via web form
   - Form submission triggers analysis
   - Results displayed as formatted JSON

2. **API Integration Flow**:
   - External system (n8n) sends POST request to `/api/analyze`
   - JSON payload includes HTML content, URL, and keywords
   - SEO analyzer processes content
   - Structured response returned as JSON

3. **Analysis Process**:
   - HTML content parsed using BeautifulSoup
   - Text extraction and cleaning
   - Keyword density analysis
   - SEO element detection (title, headings, meta tags)
   - Content marketing metrics calculation

## External Dependencies

### Python Libraries
- **Flask**: Web framework for application structure
- **Flask-CORS**: Cross-origin resource sharing support
- **BeautifulSoup4**: HTML parsing and manipulation
- **lxml**: XML/HTML parser backend

### Frontend Dependencies
- **Bootstrap**: CSS framework for responsive design
- **Bootstrap Icons**: Icon library for UI elements
- **Custom CSS**: Additional styling for dark theme

## Deployment Strategy

### Current Setup
- **Development Server**: Flask development server on port 5000
- **Host Configuration**: Binds to 0.0.0.0 for external access
- **Debug Mode**: Enabled for development environment

### Environment Configuration
- **Session Secret**: Configurable via environment variable
- **Logging**: Debug level logging enabled
- **CORS**: Configured for n8n integration requirements

### Production Considerations
- Replace Flask development server with production WSGI server
- Configure proper environment variables
- Implement proper error handling and logging
- Add rate limiting for API endpoints

## Changelog

- July 04, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.