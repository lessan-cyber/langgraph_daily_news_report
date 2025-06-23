# LangGraph Daily AI News Report

## Overview

This project automates the process of fetching, filtering, classifying, summarizing, and reporting daily news articles about Artificial Intelligence (AI) from various RSS feeds. It leverages a modular workflow built with [LangGraph](https://github.com/langchain-ai/langgraph) and integrates LLM-based classification and summarization for high-quality, category-based news digests.

---

## Features

- **Automated RSS Fetching:** Collects articles from multiple AI-related news sources.
- **Date Filtering:** Selects only articles published yesterday (UTC).
- **LLM-based Classification:** Uses a language model to categorize articles into predefined topics.
- **Content Extraction:** Retrieves the main content from each article.
- **Summarization:** Generates concise summaries for each category.
- **Report Generation:** Compiles results into a markdown report, ready for review or publication.
- **Extensible Workflow:** Easily add new agents or modify steps using LangGraph's state graph.

---

## Workflow Structure

The workflow is composed of the following agents (nodes):

1. **RSS Fetcher:** Downloads articles from configured RSS feeds.
2. **Article Filter:** Keeps only articles published yesterday.
3. **Classifier:** Assigns each article to a category using an LLM.
4. **Content Extractor:** Extracts the main text from each article's URL.
5. **Summarizer:** Produces a summary for each category.
6. **Orchestrator:** Manages iterative processing of categories.
7. **Report Generator:** Creates a markdown report of the results.

The workflow is orchestrated as a directed graph, allowing for conditional transitions and iterative category processing.

---

## Project Structure

```
langgraph_daily_news_report/
├── main.py                  # Entry point for running the workflow
├── agents/                  # Contains all agent modules
│   ├── rss_fetcher.py
│   ├── article_filter.py
│   ├── classifier.py
│   ├── content_extractor.py
│   ├── orchestrator.py
│   ├── summarizer.py
│   └── report_generator.py
├── config/                  # Configuration and prompt templates
│   ├── settings.py
│   └── prompts.py
├── workflows/               # Workflow and state definitions
│   ├── daily_ai_news.py
│   └── graph_state.py
├── reports/                 # Generated markdown reports
├── README.md                # This file
├── pyproject.toml           # Project dependencies
└── ...
```

---

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/lessan-cyber/langgraph_daily_news_report
   cd langgraph_daily_news_report
   ```

2. **Install dependencies:**
   ```bash
    uv sync
   ```

3. **Configure API Keys:**
   - Set your Google API key and other settings in `config/settings.py`.

4. **(Optional) Update RSS Feeds or Categories:**
   - Edit `config/settings.py` to add/remove RSS sources or categories.

---

## Usage

Run the workflow from the project root:

```bash
python main.py
```

- The script will fetch, process, and summarize AI news articles from the previous day.
- The final report will be saved in the `reports/` directory as a markdown file (e.g., `report_YYYYMMDD_HHMMSS.md`).
- Console output will show progress and any workflow messages.

---

## Customization

- **Add/Remove RSS Feeds:** Edit the list in `config/settings.py`.
- **Change Categories:** Update the `CATEGORIES` list in `config/settings.py`.
- **Modify Prompts:** Edit prompt templates in `config/prompts.py` for LLM classification and summarization.
- **Extend Workflow:** Add new agents or modify the workflow in `workflows/daily_ai_news.py`.

---

## Dependencies

- Python 3.8+
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [LangChain](https://github.com/langchain-ai/langchain)
- [Feedparser](https://pythonhosted.org/feedparser/)
- [Requests](https://docs.python-requests.org/)
- [python-dateutil](https://dateutil.readthedocs.io/)
- [langchain-google-genai](https://python.langchain.com/docs/integrations/chat/google_genai)

---

## Example Output

A sample report will look like:

```
---
# Daily AI News Report (2025-06-22)

## MACHINE LEARNING
- [Article Title 1](url)
  - Summary: ...

## NLP
- [Article Title 2](url)
  - Summary: ...

...
---
```

---

## Troubleshooting

- **No articles found:**
  - Check your RSS feed URLs and network connection.
- **Date parsing errors:**
  - Ensure articles have a valid `published` date; see logs for details.
- **LLM API errors:**
  - Verify your API key and quota in `config/settings.py`.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Acknowledgements

- Built with [LangGraph](https://github.com/langchain-ai/langgraph) and [LangChain](https://github.com/langchain-ai/langchain).
- Uses Google Generative AI for classification and summarization.
