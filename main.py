from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from tools import traducir_texto, generar_audio_openai
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

VOCES_DISPONIBLES = ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']
texto_actual = ""

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "resultado": None,
        "audio": None,
        "voces": VOCES_DISPONIBLES,
        "voz_actual": "nova"
    })

@app.post("/traducir", response_class=HTMLResponse)
async def translate(request: Request, texto: str = Form(...)):
    global texto_actual
    texto_actual = traducir_texto(texto)
    
    voz_por_defecto = "nova"
    audio_path = f"audio_{voz_por_defecto}.mp3"
    generar_audio_openai(texto_actual, audio_path, voz_por_defecto)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "resultado": texto_actual,
        "audio": audio_path,
        "voces": VOCES_DISPONIBLES,
        "voz_actual": voz_por_defecto
    })

@app.get("/audio/{voz}")
async def get_audio_voz(voz: str):
    global texto_actual
    audio_path = f"audio_{voz}.mp3"
    generar_audio_openai(texto_actual, audio_path, voz)
    return FileResponse(audio_path, media_type="audio/mpeg")
