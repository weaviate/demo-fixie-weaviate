from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain

llm = OpenAI(temperature=0.0)

TEMPLATE = """
    
    You are a parser that can convert natural language query into a valid graphql query based on this schema:
    {{
    "class": "Article",
    "properties": [
        {{"name": "author", "dataType": ["text"]}},
        {{"name": "title", "dataType": ["text"]}},
        {{"name": "summary", "dataType": ["text"]}},
        {{"name": "genre", "dataType": ["text"]}},
    ],
    }}

    For example, the natural language query:

    Find technology articles by Michael Brown whose title is about exploring AI in transportation, specifically focusing on bicycles. Return the summary only

    is this graphql query:

    {{
     Get {{
      Article(
       where: {{operator: And, operands: [
        {{path: ["author"], operator: Equal, valueText: "Michael Brown"}}, 
        {{path: ["genre"], operator: Equal, valueText: "Technology"}}]}}
       hybrid: {{query: "AI in transportation bicycles", alpha: 0.5, properties: ["title"]}}
       ){{
         summary
         _additional {{score }}
        }}
       }}
    }}

    only the following genres are valid: Environmental Science, Technology, Wellness
    unless specified otherwise, do the search in both the "title" and "summary" field
    unless specified otherwise, return both the "title" and "summary" field

    translate this natural language query:

    {natural_language_query}
    """

prompt = PromptTemplate(
    input_variables=["natural_language_query"],
    template=TEMPLATE,
)

chain = LLMChain(llm=llm, prompt=prompt)


def invoke_chain(query):
    """
    Convert a natural language query into a valid weaviate graphql query
    """
    return chain.run(query)
