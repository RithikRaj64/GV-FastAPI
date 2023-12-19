from langchain.agents import AgentExecutor, AgentType, initialize_agent, load_tools 
from langchain.llms import OpenAI
from langchain.tools import BaseTool

from typing import List
import json
import requests

def get_top_google_results(query: str, count: int = 5):
    URL = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {
        "X-API-KEY": "GOOGLE SERPER API KEY",
        "Content-Type": "application/json",
    }

    response = requests.request("POST", URL, data=payload, headers=headers).json()
    print(response)

    result_links = []
    for i in response["organic"]:
        result_links.append(i["link"])
    return result_links

async def chat(data: str):
    llm = OpenAI(
        max_tokens=200,
        temperature=0,
        client=None,
        model="text-davinci-003",
        frequency_penalty=1,
        presence_penalty=0,
        top_p=1,
        openai_api_key="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",
    )
    tools: List[BaseTool] = load_tools(["google-serper"], llm=llm)
    agent: AgentExecutor = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )
    template = """I have following doubts in waste management. """

    response: str = agent.run(data.content + template)

    references = get_top_google_results(data)

    reply = {"content" : response, "references" : references}

    return reply