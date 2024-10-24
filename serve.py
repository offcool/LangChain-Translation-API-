from fastapi import FastAPI,Request,HTTPException
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from langserve import add_routes
from dotenv import load_dotenv
load_dotenv()

groq_api_key=os.getenv("GROQ_API_KEY")
model=ChatGroq(model="Gemma2-9b-It",groq_api_key=groq_api_key)

# 1. Create prompt template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

parser=StrOutputParser()

##create chain
chain=prompt_template|model|parser



## App definition
app=FastAPI(title="Langchain Server",
            version="1.0",
            description="A simple API server using Langchain runnable interfaces")

@app.post("/chain/invoke")
async def invoke_chain(request: Request):
    try:
        request_data = await request.json()  # Get JSON data from request
        text = request_data.get("text")  # Extract 'text'
        language = request_data.get("language")  # Extract 'language'

        if not text or not language:
            raise HTTPException(status_code=400, detail="Text and language are required")

        # Invoke the chain with provided text and language
        result = chain.invoke({"text": text, "language": language})
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## Adding chain routes
add_routes(
    app,
    chain,
    path="/chain"
)

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)

