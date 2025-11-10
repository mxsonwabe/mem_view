import os
from pathlib import Path
from typing import Union
from typing_extensions import TypedDict

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root() -> dict[str, str]:
    return {"Hello": "World"}

class Data(TypedDict):
    item_id: int
    q: Union[int, str, None]

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None) -> Data:
    item_data: Data = {"item_id": item_id, "q": q}
    return item_data

data = []

def get_stats(dir: str = ".") -> None:
    global data
    if not dir:
        return
    path = Path(dir).resolve()
    for p in path.iterdir():
        if p.is_symlink():
            continue
        if not p.is_dir():
            data.append([p, os.path.getsize(p), p.suffix])
            # print(str(p.suffix))
            # print(str(p.lstat()))

@app.get("/read_stats")
def read_stats():
    global data
    get_stats()
    return {"data": data}


def main() -> None:
    global data
    print("Hello from memory-app!")
    get_stats()
    for d in data:
        print(d)


if __name__ == "__main__":
    main()
