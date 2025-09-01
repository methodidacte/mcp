import os
import asyncio
from lxml import html as lxml_html
from mcp.server.fastmcp import FastMCP
from playwright.async_api import async_playwright

# SOURCE
# https://brightdata.fr/blog/ai/web-scraping-with-mcp

# Define a temporary file path for the HTML content
HTML_FILE = os.path.join(os.getenv("TMPDIR", os.path.expanduser("~\\tmp")), "methodidacte_blog_page.html")

# Initialize the MCP server with a descriptive name
mcp = FastMCP("Methodidacte Blog Scraper")

print("MCP Server Initialized: Methodidacte Blog Scraper")

@mcp.tool()
async def fetch_page(url: str) -> str:
    """
    Fetches the HTML content of the given Methodidacte Blog URL using Playwright
    and saves it to a temporary file. Returns a status message.
    """
    print(f"Executing fetch_page for URL: {url}")
    try:
        async with async_playwright() as p:
            # Launch headless Chromium browser
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            # Navigate to the URL with a generous timeout
            await page.goto(url, timeout=90000, wait_until="domcontentloaded")
            # Wait for a key element (e.g., body) to ensure basic loading
            await page.wait_for_selector("body", timeout=30000)
            # Add a small delay for any dynamic content rendering via JavaScript
            await asyncio.sleep(5)

            html_content = await page.content()
            with open(HTML_FILE, "w", encoding="utf-8") as f:
                f.write(html_content)

            await browser.close()
            print(f"Successfully fetched and saved HTML to {HTML_FILE}")
            return f"HTML content for {url} downloaded and saved successfully to {HTML_FILE}."
    except Exception as e:
        error_message = f"Error fetching page {url}: {str(e)}"
        print(error_message)
        return error_message

def _extract_xpath(tree, xpath, default="N/A"):
    """Helper function to extract text using XPath, returning default if not found."""
    try:
        # Use text_content() to get text from node and children, strip whitespace
        result = tree.xpath(xpath)
        if result:
            return result[0].text_content().strip()
        return default
    except Exception:
        return default

    
@mcp.tool()
async def summarize_page(url: str) -> str:
    """
    Uses the saved HTML file (downloaded by fetch_page) to summary the blog post.
    """
    print(f"Executing extract_info from file: {HTML_FILE}")
    if not os.path.exists(HTML_FILE):
        return {
            "error": f"HTML file not found at {HTML_FILE}. Please run fetch_page first."
        }

    try:
        with open(HTML_FILE, "r", encoding="utf-8") as f:
            page_html = f.read()

        tree = lxml_html.fromstring(page_html)

        article = tree.xpath('//article')
        article = article[0].text_content().strip()
        h1 = tree.xpath('//article//h1')[0].text_content().strip()

        print(f"Successfully summaried the blog post: {h1}")
        return article

    except Exception as e:
        error_message = f"Error parsing HTML: {str(e)}"
        print(error_message)  # Added for logging
        return {"error": error_message}


if __name__ == "__main__":
    print("Starting MCP Server with stdio transport...")
    # Run the server, listening via standard input/output
    mcp.run(transport="stdio")
