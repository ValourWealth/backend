# # ----------------------------------------------------------------------------------------------------------------


# # ===========================================================================================================================================
# # ----------------------------------------------- For market
# import os
# from exa_py import Exa
# from dotenv import load_dotenv

# # Load API Key from .env
# load_dotenv()
# EXA_API_KEY = os.getenv("EXA_API_KEY")

# # Initialize Exa Client
# exa = Exa(api_key=EXA_API_KEY)

# def search_stock_news(query="US Stock Market", num_results=300):
#     """
#     Fetch latest stock market news using Exa API and get images.
#     """
#     if not EXA_API_KEY:
#         return {"error": "Missing Exa API Key"}

#     try:
#         # Step 1: Fetch News Articles
#         result = exa.search(
#             query,
#             type="auto",
#             category="business",
#             num_results=num_results
#         )

#         articles = []
#         urls = []

#         if hasattr(result, "results"):
#             for res in result.results:
#                 articles.append({
#                     "title": "Market",  # ✅ Static title
#                     "url": getattr(res, "url", ""),
#                     "published_date": getattr(res, "published_date", "Unknown"),
#                     "description": getattr(res, "title", ""),  # ✅ Title moved to description
#                     "score": getattr(res, "score", 0),
#                     "image_url": ""  # Placeholder for image
#                 })
#                 if res.url:
#                     urls.append(res.url)

#         # Step 2: Fetch Images using Exa's get_contents()
#         if urls:
#             content_result = exa.get_contents(urls=urls, extras={"extractImages": True})
#             for i, content in enumerate(content_result.results):
#                 if i < len(articles):
#                     articles[i]["image_url"] = getattr(content, "image", "")

#         return {"results": articles}

#     except Exception as e:
#         return {"error": str(e)}




# # ===========================================================================================================================================
# # For Technology
# # Initialize Exa Client
# exa = Exa(api_key=EXA_API_KEY)

# def search_technology_news(query="Technology", num_results=50):
#     """
#     Fetch latest technology news using Exa API and get images.
#     """
#     if not EXA_API_KEY:
#         return {"error": "Missing Exa API Key"}

#     try:
#         # Step 1: Fetch Technology News Articles
#         result = exa.search(
#             query,
#             type="auto",
#             category="technology",  # ✅ Fetch only technology-related news
#             num_results=num_results
#         )

#         articles = []
#         urls = []

#         if hasattr(result, "results"):
#             for res in result.results:
#                 articles.append({
#                     "title": "Tech News",  # ✅ Static title
#                     "url": getattr(res, "url", ""),
#                     "published_date": getattr(res, "published_date", "Unknown"),
#                     "description": getattr(res, "title", ""),  # ✅ Title moved to description
#                     "score": getattr(res, "score", 0),
#                     "image_url": ""  # Placeholder for image
#                 })
#                 if res.url:
#                     urls.append(res.url)

#         # Step 2: Fetch Images using Exa's get_contents()
#         if urls:
#             content_result = exa.get_contents(urls=urls, extras={"extractImages": True})
#             for i, content in enumerate(content_result.results):
#                 if i < len(articles):
#                     articles[i]["image_url"] = getattr(content, "image", "")

#         return {"results": articles}

#     except Exception as e:
#         return {"error": str(e)}



# # ===========================================================================================================================================


# # Stock news exa api----

# # Initialize Exa Client
# exa = Exa(api_key=EXA_API_KEY)

# def search_stock_news(query="Stock Market", num_results=50):
#     """
#     Fetch latest stock news using Exa API and get images.
#     """
#     if not EXA_API_KEY:
#         return {"error": "Missing Exa API Key"}

#     try:
#         # Step 1: Fetch Stock News Articles
#         result = exa.search(
#             query,
#             type="auto",
#             category="stocks",  # ✅ Fetch only stock-related news
#             num_results=num_results
#         )

#         articles = []
#         urls = []

#         if hasattr(result, "results"):
#             for res in result.results:
#                 articles.append({
#                     "title": "Stock News",  # ✅ Static title
#                     "url": getattr(res, "url", ""),
#                     "published_date": getattr(res, "published_date", "Unknown"),
#                     "description": getattr(res, "title", ""),  # ✅ Title moved to description
#                     "score": getattr(res, "score", 0),
#                     "image_url": ""  # Placeholder for image
#                 })
#                 if res.url:
#                     urls.append(res.url)

#         # Step 2: Fetch Images using Exa's get_contents()
#         if urls:
#             content_result = exa.get_contents(urls=urls, extras={"extractImages": True})
#             for i, content in enumerate(content_result.results):
#                 if i < len(articles):
#                     articles[i]["image_url"] = getattr(content, "image", "")

#         return {"results": articles}

#     except Exception as e:
#         return {"error": str(e)}



# # ========================================================================================================================

# #  For Recent Post


# # Initialize Exa Client
# exa = Exa(api_key=EXA_API_KEY)

# def search_recent_news(query="London OR United States", num_results=50):
#     """
#     Fetch recent news articles related to London and the US.
#     """
#     if not EXA_API_KEY:
#         return {"error": "Missing Exa API Key"}

#     try:
#         # Step 1: Fetch Recent News
#         result = exa.search(
#             query,
#             type="auto",
#             category="news",
#             num_results=num_results
#         )

#         articles = []
#         urls = []

#         if hasattr(result, "results"):
#             for res in result.results:
#                 if hasattr(res, "url") and res.url:  # Ensure URL exists
#                     articles.append({
#                         "title": "Recent News",  # Static title
#                         "url": res.url,
#                         "published_date": getattr(res, "published_date", "Unknown"),
#                         "description": getattr(res, "title", ""),
#                         "score": getattr(res, "score", 0),
#                         "image_url": ""  # Placeholder for image
#                     })
#                     urls.append(res.url)

#         # Step 2: Fetch Images
#         if urls:
#             content_result = exa.get_contents(urls=urls, extras={"extractImages": True})
#             for i, content in enumerate(content_result.results):
#                 if i < len(articles):
#                     articles[i]["image_url"] = getattr(content, "image", "")

#         # Filter out articles without images
#         articles = [article for article in articles if article["image_url"]]

#         return {"results": articles}

#     except Exception as e:
#         return {"error": str(e)}


# # ==========================================================================================================================
# # For Crypto's 

# # Initialize Exa Client
# exa = Exa(api_key=EXA_API_KEY)

# def search_crypto_news(query="Cryptocurrency", num_results=50):
#     """
#     Fetch latest cryptocurrency news using Exa API and get images.
#     """
#     if not EXA_API_KEY:
#         return {"error": "Missing Exa API Key"}

#     try:
#         # Step 1: Fetch Crypto News Articles
#         result = exa.search(
#             query,
#             type="auto",
#             category="cryptocurrency",
#             num_results=num_results
#         )

#         articles = []
#         urls = []

#         if hasattr(result, "results"):
#             for res in result.results:
#                 articles.append({
#                     "title": "Crypto",  # ✅ Static title
#                     "url": getattr(res, "url", ""),
#                     "published_date": getattr(res, "published_date", "Unknown"),
#                     "description": getattr(res, "title", ""),  # ✅ Title moved to description
#                     "score": getattr(res, "score", 0),
#                     "image_url": ""  # Placeholder for image
#                 })
#                 if res.url:
#                     urls.append(res.url)

#         # Step 2: Fetch Images using Exa's get_contents()
#         if urls:
#             content_result = exa.get_contents(urls=urls, extras={"extractImages": True})
#             for i, content in enumerate(content_result.results):
#                 if i < len(articles):
#                     articles[i]["image_url"] = getattr(content, "image", "")

#         return {"results": articles}

#     except Exception as e:
#         return {"error": str(e)}



# # =========================================================================================================
# # For Editor Choice:


# # Initialize Exa Client
# exa = Exa(api_key=EXA_API_KEY)

# def fetch_stock_data(category="trending", num_results=50):
#     """
#     Fetch stock market data from Exa API based on category.
#     Categories: 'trending', 'insights', 'algo_picks', 'gainers_losers'
#     """
#     if not EXA_API_KEY:
#         return {"error": "Missing Exa API Key"}

#     category_queries = {
#         "trending": "Most Active Stocks Today",
#         "insights": "Stock Market Expert Opinions",
#         "algo_picks": "AI Recommended Stocks",
#         "gainers_losers": "Biggest Stock Gainers and Losers Today",
#     }

#     query = category_queries.get(category, "Stock Market")

#     try:
#         # Fetch news articles
#         result = exa.search(
#             query,
#             type="auto",
#             category="business",
#             num_results=num_results
#         )

#         articles = []
#         urls = []

#         if hasattr(result, "results"):
#             for res in result.results:
#                 articles.append({
#                     "title": res.title or "Stock News",
#                     "url": getattr(res, "url", ""),
#                     "published_date": getattr(res, "published_date", "Unknown"),
#                     "description": getattr(res, "title", ""),
#                     "score": getattr(res, "score", 0),
#                     "image_url": ""  # Placeholder for image
#                 })
#                 if res.url:
#                     urls.append(res.url)

#         # Fetch images
#         if urls:
#             content_result = exa.get_contents(urls=urls, extras={"extractImages": True})
#             for i, content in enumerate(content_result.results):
#                 if i < len(articles):
#                     articles[i]["image_url"] = getattr(content, "image", "")

#         return {"results": articles}

#     except Exception as e:
#         return {"error": str(e)}
