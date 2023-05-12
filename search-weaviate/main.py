import fixieai
import os
import weaviate
import logging

logging.basicConfig(level=logging.INFO)


BASE_PROMPT = """I am an agent to help users retrieve information from a weaviate. I will
translate a user's natural langauge query into a weaviate graphql query and return the results.
"""

FEW_SHOTS = """
Q: Show me articles about environmental science, written by Jane Smith, that mention the benefits of a plant-based diet.
Thought: I need to translate this natural language query into a weaviate graphql query.
Ask Agent[shukri/natural-to-weaviate-get]: Show me articles about environmental science, written by Jane Smith, that mention the benefits of a plant-based diet.
Agent[shukri/natural-to-weaviate-get] says: X
Thought: I need to run the following query on weaviate: X
Ask Func[query]: X
Func[query] says: Y
Thought: I need to display the results to the user
A: Here are the results:
Y
"""
agent = fixieai.CodeShotAgent(
    BASE_PROMPT,
    FEW_SHOTS,
    llm_settings=fixieai.LlmSettings(temperature=0.0, model="openai/text-davinci-003"),
)
weaviate_client = weaviate.Client(
    os.environ["WEAVIATE_URL"],
    additional_headers={"X-OPENAI-API-KEY": os.environ["WEAVIATE_OPENAI_API_KEY"]},
)


@agent.register_func
def query(query: fixieai.Message) -> str:
    graphql_query = query.text
    logging.info(f"Received query: {graphql_query}")

    try:
        results = weaviate_client.query.raw(graphql_query)
    except Exception as e:
        traceback.print_exc()
        results = str(e)

    return display_results(results)


def display_results(data):
    articles = data.get("data", {}).get("Get", {}).get("Article", [])

    formatted_output = []
    for idx, article in enumerate(articles, start=1):
        score = article.get("_additional", {}).get("score", "")
        article_output = [f"{idx}. Score: {score}"]
        for key, value in article.items():
            if key != "_additional":
                article_output.append(f"   {key}: {value}")
        formatted_output.append("\n".join(article_output))

    logging.info(f"Formatted output: {formatted_output}")

    if not formatted_output:
        return "No results found."

    return "\n".join(formatted_output)
