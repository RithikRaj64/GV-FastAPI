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
        "X-API-KEY": "e352ce658cbb5bcdfa1c9806ef17a3b0018abd9f ",
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
    tools: List[BaseTool] = load_tools(["google-serper"], llm=llm, serper_api_key="e352ce658cbb5bcdfa1c9806ef17a3b0018abd9f")
    agent: AgentExecutor = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )
    template = """Answer only if query is related to waste management. Or just say NO. The query is """

    response: str = agent.run(data + template)

    references = get_top_google_results(data)

    reply = {"content" : response, "references" : references}

    return reply