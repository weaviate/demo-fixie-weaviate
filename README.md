# Introduction

This is a simple demo of building a [Fixie](https://www.fixie.ai/) Agent that can answer questions about documents
stored in Weaviate. 

It takes a query in natural language, uses an LLM to convert it to a Weaviate graphql query, and then sends it to Weaviate for execution.

# Setup

See the data notebook on how to load some data into Weaviate.

# Deployment

## Deploy the natural-to-weaviate-get agent
1. `cd` to `/natural-to-weaviate-get`
2. Run `fixie agent deploy`

## Deploy the search-weaviate agent
1. `cd` to `/search-weaviate`
2. Update the env vars in `.env` with your own Weaviate url and OpenAI api key
3. Run `fixie agent deploy`

# Demo

Talking to the `search-weaviate` agent:

![demo](fixie-demo.gif)
