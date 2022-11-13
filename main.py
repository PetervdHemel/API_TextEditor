from fastapi import FastAPI, HTTPException
from pathlib import Path

from my_text_processor import MyTextProcessor
from models import PathToText

app = FastAPI()

def load_app(path_to_text: str) -> MyTextProcessor:
    """Calls text processor class and loads the class. Returns class."""
    processor = MyTextProcessor()
    processor.load(Path(path_to_text))
    #processor.load(Path(r".\text.txt"))
    return processor
    
@app.get("/api/v1/{path_to_text}/display")
async def display(path_to_text: str) -> None:
    try:
        processor = load_app(path_to_text)
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"File with path: {path_to_text} does not exist."
        )
    else:
        return processor.display()

def main():
    """
    Reads the text file 'text.txt' and performs various functions.
    """
    
if __name__ == "__main__":
    main()