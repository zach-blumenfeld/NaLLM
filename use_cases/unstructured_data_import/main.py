import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel
import uvicorn


current_file = Path(__file__).resolve()
project_root = current_file.parents[2]
sys.path.append(str(project_root))
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from use_cases.shared.llm.openai import OpenAIChat
from use_cases.shared.driver.neo4j import Neo4jDatabase
from use_cases.shared.components.unstructured_data_extractor import (
    DataExtractor,
    DataExtractorWithSchema,
)
from use_cases.shared.components.data_disambiguation import DataDisambiguation
from use_cases.shared.components.data_to_csv import DataToCSV

openai_api_key = os.environ.get("OPENAI_API_KEY", "")

llm = OpenAIChat(openai_api_key=openai_api_key, model_name="gpt-3.5-turbo")

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Payload(BaseModel):
    input: str
    neo4j_schema: str


@app.post("/data2cypher")
async def root(payload: Payload):
    """
    Takes an input and created a Cypher query
    """
    if not payload:
        return "missing request body"
    try:
        result = ""

        if payload.neo4j_schema == "" or payload.neo4j_schema == None:
            extractor = DataExtractor(llm=llm)
            result = extractor.run(data=payload.input)
        else:
            extractor = DataExtractorWithSchema(llm=llm)
            result = extractor.run(schema=payload.neo4j_schema, data=payload.input)

        print("Extracted result: " + str(result))

        disambiguation = DataDisambiguation(llm=llm)
        disambiguation_result = disambiguation.run(result)

        print("Disambiguation result " + str(disambiguation_result))

        return {"data": disambiguation_result}

    except Exception as e:
        print(e)
        return f"Error: {e}"


if __name__ == "__main__":
    load_dotenv()
    uvicorn.run(
        "use_cases.unstructured_data_import.main:app",
        host="0.0.0.0",
        port=7860,
        reload=True,
    )
