CLASSIFICATION_PROMPT = """"
You're an expert in classifying technology watch articles, with in-depth knowledge of the fields of Artificial Intelligence, Programming and Startups.
Your objective is to classify the text of an article into one of the following categories: {categories}.
Here are specific guidelines for classification:
- **AI (Artificial Intelligence)**: Articles on generative AI, machine learning, deep learning, neural networks, computer vision, natural language processing (NLP), advanced robotics, AI ethics and AI applications in general.
- Programming**: Articles on programming languages, development frameworks (web, mobile, backend), databases, DevOps, software architecture, development tools, technical cybersecurity, new development technologies. **Include topics related to blockchain, cryptocurrencies from a technical/development point of view (e.g. development of smart contracts, new blockchain architectures).
- **Startup**: Articles on startup financing (fundraising, acquisitions), innovative business models, startup success stories or failures, startup market trends, entrepreneurship, growth hacking, and the non-technical aspects of running a startup.
- **Other**: If the content doesn't clearly fit into any of the main categories above, or if you're not at all sure which category is most appropriate, use this category.
Here's the article title:
"{article_title}"

Here's an excerpt from the article description/summary (if available, otherwise use the title):
"{article_summary}"

Based solely on the title and description and the guidelines provided, assign the article to the most relevant category.

Answer only with the name of the chosen category, without any further explanation or final punctuation.
For example: "Artificial intelligence" or "Programming" or "Startup" or "Other".

"""

SUMMARY_PROMPT = """You're a technology watch expert, able to synthesize complex information in a clear and concise way.
Your objective is to create a detailed and informative summary of a set of articles related to the category “{category_name}”.
Here is the textual content extracted from several articles in the "{category_name}" category. Each article is separated by "--- NEXT ARTICLE ---".

--- START OF ARTICLES ---
{articles_content}
--- END OF ARTICLES ---
The abstract must :
- Be professional and informative in tone.
- Highlight key points, important news, emerging trends and significant developments.
- Avoid repetition and not simply list articles. Synthesize common information and identify recurring topics.
- Include titles of the most relevant original articles or excerpts of their content if necessary to support a point.
- Be concise but detailed enough to give a good overview without having to read all the articles.
- Don't include a preamble like “Here's a summary of the articles...”. Start directly with the content of the summary.
If the articles seem duplicated or don't provide much new information, indicate this.
If the content is insufficient or irrelevant, mention it briefly.

Now generate the summary for category “{category_name}”."""


FINAL_REPORT_PROMPT = """You're a professional writer specializing in technology watch reports.
Your goal is to compile the article summaries provided into a clear, structured and professional Markdown report.

Here are the summaries organized by category for the {report_date} technology watch:

{summaries_content}
Guidelines for the final report :
- Start with a level 1 title: “# Technology Watch Report - {report_date}”.
- Add a brief introduction (1-2 sentences) about the purpose of the report.
- For each category, use a level 2 title: “## [Category Name]”.
- If a category summary is “No items available for this category.” or similar, clearly indicate this under the category title.
- Make sure that the content of the summaries is faithfully reproduced.
- Use standard Markdown formatting (lists, bold, italics) if necessary to improve readability, but do not alter the text of the abstracts themselves.
- The report must be complete and contain no superfluous or repetitive information.

Now generate the complete report."""
