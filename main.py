from fastapi import FastAPI, HTTPException
from pathlib import Path

from my_text_processor import MyTextProcessor
from models import Replace

app = FastAPI()

# .\venv\Scripts\activate
# uvicorn main:app --reload

def load_app(path_to_text: str) -> MyTextProcessor:
    """Calls text processor class and loads the class. Returns class."""
    processor = MyTextProcessor()
    processor.load(Path(path_to_text))
    # processor.load(Path(r".\text.txt"))
    return processor

def try_path(path) -> MyTextProcessor:
    try:
        processor = load_app(path)
    except FileNotFoundError:
        raise HTTPException(
            status_code = 404,
            detail = f"File with path: {path} does not exist."
        )
    else:
        return processor
    
@app.get("/api/v1/{path_to_text}/display")
async def display(path_to_text: str) -> None:
    processor = try_path(path_to_text)
    return processor.display()

@app.post("/api/v1/{path_to_text}/search/")
async def search(path_to_text: str, search_string: str) -> list[tuple[int, int]]:
    """Returns search result"""
    processor = try_path(path_to_text)
    
    return processor.search(search_string)

@app.post("/api/v1/{path_to_text}/replace/")
async def replace(path_to_text: str, replace: Replace) -> str:
    """Returns replaced search result"""
    processor = try_path(path_to_text)
    
    processor.replace(replace.search_string, replace.replace_string)
    
    if replace.save and replace.save_path:
        try:
            processor.save(replace.save_path)
        except ValueError:
            raise HTTPException(
                status_code = 400,
                detail = f"Path: {replace.save_path} is an incorrect path."
            )
        
    return processor.display()

@app.post("/api/v1/{path_to_text}/common/")
async def common(path_to_text: str, limit: int = 10) -> list[tuple[str, int]]:
    """Returns most common words"""
    processor = try_path(path_to_text)
    
    return processor.get_common_words(limit)

@app.get("/api/v1/{path_to_text}/palindromes/")
async def palindromes(path_to_text: str) -> list[str]:
    """Returns a list of all palindromes in text"""
    processor = try_path(path_to_text)
    
    return processor.get_palindrome_words()

@app.get("/api/v1/{path_to_text}/emails/")
async def emails(path_to_text: str):
    """Returns a list of all emails found in text"""
    processor = try_path(path_to_text)
    
    return processor.get_emails()

@app.get("/api/v1/{path_to_text}/secret/")
async def emails(path_to_text: str) -> tuple:
    """Returns a tuple containing the encrypted and decrypted strings"""
    processor = try_path(path_to_text)
    
    return processor.find_secret()
    

def main():
    """
    Reads the text file 'text.txt' and performs various functions.
    """
    
if __name__ == "__main__":
    main()