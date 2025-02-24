# Charts Skill Documentation

## Overview
Charts Skill is a Streamlit-based web application that integrates with AnythingLLM as an agent skill. It processes natural language queries and creates visualizations based on data retrieved from the backend server.

## Features
- Integration with AnythingLLM agent system
- Dynamic data visualization
- Natural language query processing
- Multiple chart types
- Automatic chart selection
- Interactive visualization options

## Technical Stack
- Python/Streamlit
- Plotly for visualizations
- Pandas for data processing
- Docker containerization

## Installation and Setup

### Requirements
- Python 3.8+
- Streamlit
- Docker and Docker Compose
- AnythingLLM agent system

### Local Development Setup

1. Clone the repository:
\`\`\`bash
git clone [charts-skill-repo-url]
cd charts_skill
\`\`\`

2. Create virtual environment:
\`\`\`bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate  # Windows
\`\`\`

3. Install dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

4. Set up environment variables:
\`\`\`bash
cp .env.example .env
# Edit .env with your settings
\`\`\`

5. Run Streamlit:
\`\`\`bash
streamlit run app.py
\`\`\`

### Docker Deployment

1. Build the container:
\`\`\`bash
docker-compose build charts-skill
\`\`\`

2. Start the service:
\`\`\`bash
docker-compose up -d charts-skill
\`\`\`

### Production Deployment

1. Transfer files to server:
\`\`\`bash
scp -r charts_skill/ user@server:/path/to/deployment
\`\`\`

2. On the server:
\`\`\`bash
cd /path/to/deployment
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
\`\`\`

## Configuration

### Environment Variables
\`\`\`env
BACKEND_URL=http://backend:8000
ANYTHING_LLM_TOKEN=your-token
DEBUG=False
PORT=8501
\`\`\`

## Usage Guide

### Query Processing
The application accepts queries in natural language format:
- "Show me sales data for last month"
- "Create a pie chart of product categories"
- "Compare revenue across regions"

### Chart Types
Available visualizations include:
- Line charts
- Bar charts
- Pie charts
- Scatter plots
- Area charts
- Heat maps

### Data Processing
1. Query interpretation
2. Data retrieval from backend
3. Data transformation
4. Chart generation
5. Interactive display

## Integration with AnythingLLM

### Agent Communication
- Receives queries from AnythingLLM
- Processes natural language
- Returns visualization URLs

### Response Format
\`\`\`python
{
    "chart_url": "http://charts-skill:8501/chart/123",
    "chart_type": "line",
    "data_description": "Sales data visualization"
}
\`\`\`

## Security

### Authentication
- Token-based authentication with AnythingLLM
- Backend API authentication
- Session management

### Data Protection
- Secure data transmission
- Temporary data storage
- Access control

## Monitoring and Maintenance

### Logging
\`\`\`bash
# View application logs
docker-compose logs charts-skill

# Monitor streamlit
streamlit logs
\`\`\`

### Health Checks
- Backend connectivity
- AnythingLLM agent status
- System resource usage

## Troubleshooting

### Common Issues

1. Connection Problems
- Check backend availability
- Verify AnythingLLM token
- Check network settings

2. Visualization Errors
- Validate data format
- Check memory usage
- Review query syntax

3. Performance Issues
- Monitor resource usage
- Check data size
- Optimize query processing

## Development Guidelines

### Code Structure
\`\`\`
charts_skill/
├── app.py              # Main Streamlit application
├── utils/
│   ├── data_processing.py
│   ├── chart_generator.py
│   └── query_parser.py
├── config/
│   └── settings.py
└── tests/
\`\`\`

### Testing
\`\`\`bash
# Run tests
pytest

# Run with coverage
coverage run -m pytest
coverage report
\`\`\`

### Adding New Features
1. Create feature branch
2. Implement functionality
3. Add tests
4. Update documentation
5. Submit pull request

## Performance Optimization

### Data Handling
- Efficient data processing
- Caching mechanisms
- Query optimization

### Visualization
- Lazy loading
- Data sampling for large datasets
- Progressive loading

## Future Improvements
- Additional chart types
- Enhanced query understanding
- Better error handling
- Performance optimizations
- Extended customization options

## Backend Integration

### API Endpoints Used
\`\`\`
GET /api/data - Retrieve datasets
POST /api/process - Process data
GET /api/chart-types - Available visualizations
\`\`\`

### Data Flow
1. Receive query from AnythingLLM
2. Parse and process query
3. Request data from backend
4. Generate visualization
5. Return result to agent

## User Interface

### Main Components
- Query input
- Chart display
- Configuration options
- Interactive controls

### Customization Options
- Chart colors
- Data ranges
- Axis labels
- Legend position

## Error Handling

### Query Errors
- Invalid syntax
- Unsupported chart types
- Missing data

### System Errors
- Backend connection issues
- Processing failures
- Resource limitations