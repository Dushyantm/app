# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .intent_detection import IntentDetection
import sqlite3
from typing import List, Dict
from .sql_agent import execute_sql_query

app = FastAPI()

class Query(BaseModel):
    text: str

def get_db_connection():
    conn = sqlite3.connect('./database/travel_database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.post("/detect_intent")
async def detect_intent(query: Query):
    intent_detector = IntentDetection(query.text)
    intent = intent_detector.detect_intent()
    return {"intent": intent}

@app.post("/query_database")
async def query_database(query: Query):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query.text)
        results = cursor.fetchall()
        return {"results": [dict(row) for row in results]}
    except sqlite3.Error as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

@app.post("/process_query")
async def process_query(query: Query):
    intent_detector = IntentDetection(query.text)
    intent = intent_detector.detect_intent()
    
    if intent.strip().upper() == "SQL":
        try:
            result = execute_sql_query(query.text)
            # print(result)
            return {"type": "database", "results": result}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    elif intent.strip().upper() == "LLM":
        # Here you would typically call your LLM to process the query
        # For now, we'll just return a placeholder response
        return {"type": "llm", "response": "This query would be processed by the LLM."}
    else:
        raise HTTPException(status_code=400, detail="Unknown intent")