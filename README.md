# Better Web Search Agent Skill

This agent skill enhances web searches by providing more comprehensive and relevant results through a multi-step process. It utilizes Google Search and LLM capabilities to deliver high-quality, summarized information from multiple sources.

## How it Works

The agent follows these steps to process your search query:

1. **Query Optimization** (0-25%)
   - Takes the user's input query
   - Uses LLM to generate multiple optimized search variations
   - Creates alternative phrasings to capture different aspects of the search

2. **Web Search** (25-30%)
   - Performs Google searches using all optimized queries
   - Collects unique URLs, titles, and descriptions
   - Removes duplicate results

3. **Source Quality Assessment** (30-65%)
   - Evaluates each source's relevance and quality
   - Uses LLM to determine which sources are most valuable for the query
   - Filters out low-quality or irrelevant sources

4. **Content Extraction** (65-80%)
   - Retrieves content from approved high-quality sources
   - Processes and cleans the text content
   - Shows progress for each source being processed

5. **Token Management** (80-85%)
   - Checks total token count of collected content
   - If exceeds 120,000 tokens, removes entire sources (starting with longest)
   - Ensures content stays within LLM processing limits

6. **Summary Generation** (85-100%)
   - Summarizes all collected information
   - Creates a comprehensive response to the original query
   - Returns results in a structured format

## Features

- Smart query optimization for better search results
- Automatic duplicate removal
- Quality-based source filtering
- Progressive loading with status updates
- Token limit management
- Efficient content summarization

## Debug Mode

The skill includes a debug mode that can save intermediate results to avoid reprocessing the same queries during development:
- Saves results to `debug_results.json`
- Can load previous results to skip time-consuming processing steps
- Useful for development and testing

## Input Parameters

The skill accepts a single input parameter:
- `input`: The search query or question from the user (string)

## Output

Returns a structured response containing:
- Original input query
- Summarized information from all processed sources
- Progress updates throughout the process