import ollama
import tempfile
import os
import pypandoc
from .rag_database import SupportFiles, postgres_engine
from sqlalchemy.orm import Session
from langchain_text_splitters import RecursiveCharacterTextSplitter



async def postgress_store_support_file(username: str, filename: str, file_content: bytes):

    try:
        # get text from the bytes of the file

        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{filename.split('.')[-1]}") as temp:
            temp.write(file_content)
            temp_path = temp.name

        text = pypandoc.convert_file(temp_path, 'plain')
        os.remove(temp_path)

        # split text up uding langchain text splitter into mnanagable chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1800, chunk_overlap=50)
        chunks = text_splitter.split_text(text)

        # create vector embeddings for each chunk
        client = ollama.AsyncClient()

        embedding_response = await client.embed(
            model='nomic-embed-text',
            input=chunks
        )

        embeddings = embedding_response['embeddings']

        with Session(postgres_engine) as session:

            for embedding, chunk in zip(embeddings, chunks):

                new_chunk = SupportFiles( username=username, filename=filename, content=chunk, embedding=embedding)
                session.add(new_chunk)
        
            session.commit()

        return True

    except:
        return False
        

async def postgress_delete_support_file(username: str, filename: str):

    try:
    
        # creates sqlalchemy session and deletes account from table
        with Session(postgres_engine) as session:
            chunks = session.query(SupportFiles).filter(SupportFiles.username == username, SupportFiles.filename == filename).all()

            for chunk in chunks:
                session.delete(chunk)
            session.commit()
            

    except Exception as e:
        print(f'error removing from rag: {e}')
 

async def perform_rag(username: str, prompt: str, return_ammount: int):
        
    try:
        client = ollama.AsyncClient()

        response = await client.embed(
            model='nomic-embed-text',
            input=prompt
        )
        query_embedding = response['embeddings'][0]

        with Session(postgres_engine) as session:
            results = (session.query(SupportFiles).filter(SupportFiles.username == username)
                       .order_by(SupportFiles.embedding.cosine_distance(query_embedding)).limit(return_ammount).all())
            
            return_list = []

            for chunk in results:
                return_list.append(chunk.content)

        return return_list
    
    except Exception as e:
        print(f'rag error: {e}')
        return []
