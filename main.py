import os
import pandas as pd
import random

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/data", response_class=JSONResponse)
async def data():
    file_path = os.path.join(os.path.dirname(__file__), "data/openTSNE_data.csv")
    df = pd.read_csv(file_path, dtype={"Group": str, "Id": str, "Path": str, "TSNE_1": float, "TSNE_2": float})
    color_by = "Group"
    color_map = groups_to_color_map(df[color_by].unique())
    return [
        {
            "x": row["TSNE_1"],
            "y": row["TSNE_2"],
            "id": row["Id"],
            "group": row["Group"],
            "path": row["Path"],
            "color": color_map[row[color_by]]
        }
        for row in df.to_dict(orient="records")
    ]

@app.get("/image/{filename}")
def image(filename):
    return FileResponse(f"data/{filename}")

def groups_to_color_map(groups: list[str]):
    colors = [f"hsla({random.randint(0, 360)}, 50%, 60%, 1)" for _ in range(len(groups))]
    return {key: value for key, value in zip(groups, colors)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
