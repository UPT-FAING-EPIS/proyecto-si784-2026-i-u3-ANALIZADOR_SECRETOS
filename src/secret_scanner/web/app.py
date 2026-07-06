import os
import math
import re
import string
import secrets
import zipfile
import tempfile
import shutil
import urllib.request
from pathlib import Path
from typing import List, Dict, Any
from collections import Counter

from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel

from secret_scanner.scanner.file_scanner import scan_path, _mask_secret
from secret_scanner.scanner.patterns import PATTERNS

# Define paths
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="SecretScanner API",
    description="Multipurpose Web API for scanning secrets, checking password strength, and generating secure keys.",
    version="1.0.0"
)

# Models
class ScanPathRequest(BaseModel):
    path: str

class ScanGitRequest(BaseModel):
    clone_url: str

class ScanCodeRequest(BaseModel):
    code: str

class CustomPatternRequest(BaseModel):
    pattern: str
    text: str

class EntropyRequest(BaseModel):
    secret: str

class GenerateSecretRequest(BaseModel):
    length: int = 32
    use_upper: bool = True
    use_lower: bool = True
    use_digits: bool = True
    use_symbols: bool = True

# Helper: local text scanner
def scan_raw_text(text: str) -> List[Dict[str, Any]]:
    findings = []
    lines = text.splitlines()
    for lineno, line in enumerate(lines, start=1):
        for pat in PATTERNS:
            if pat["pattern"].search(line):
                findings.append({
                    "type": pat["name"],
                    "severity": pat["severity"],
                    "file": "Pasted Code",
                    "line": lineno,
                    "content": _mask_secret(line.rstrip())
                })
    return findings

# Helper: Shannon & Pool Entropy
def calculate_entropy_metrics(secret: str) -> Dict[str, Any]:
    if not secret:
        return {
            "shannon_entropy": 0.0,
            "pool_entropy_bits": 0.0,
            "strength": "Vacio",
            "crack_time_seconds": 0,
            "crack_time_formatted": "Inmediato",
            "recommendations": ["El secreto está vacío."]
        }
    
    # Shannon Entropy
    len_s = len(secret)
    counts = Counter(secret)
    shannon = 0.0
    for count in counts.values():
        p = count / len_s
        shannon -= p * math.log2(p)
    
    # Pool size estimation
    pool_size = 0
    recommendations = []
    
    has_lower = any(c.islower() for c in secret)
    has_upper = any(c.isupper() for c in secret)
    has_digit = any(c.isdigit() for c in secret)
    has_special = any(c in string.punctuation for c in secret)
    
    if has_lower:
        pool_size += 26
    else:
        recommendations.append("Agrega letras minúsculas (a-z) para ampliar el espacio de búsqueda.")
        
    if has_upper:
        pool_size += 26
    else:
        recommendations.append("Agrega letras mayúsculas (A-Z) para aumentar la complejidad.")
        
    if has_digit:
        pool_size += 10
    else:
        recommendations.append("Incluye números (0-9) para mayor resistencia a ataques de diccionario.")
        
    if has_special:
        pool_size += len(string.punctuation)
    else:
        recommendations.append("Utiliza caracteres especiales y símbolos (e.g. @, #, $, %) para robustecer la clave.")
        
    if pool_size == 0:
        pool_size = 256  # fallback for other unicode chars
        
    # Key space entropy (bits of security)
    pool_entropy = len_s * math.log2(pool_size)
    
    # Strength level
    if pool_entropy < 40:
        strength = "Muy Débil"
    elif pool_entropy < 60:
        strength = "Débil"
    elif pool_entropy < 80:
        strength = "Medio"
    elif pool_entropy < 100:
        strength = "Fuerte"
    else:
        strength = "Muy Fuerte"
        
    if len_s < 12:
        recommendations.append("El secreto es corto. Aumenta la longitud a mínimo 16 caracteres para claves de API o 12 para contraseñas.")
        
    # Estimated crack time at 10 billion guesses/sec
    guesses = 2 ** pool_entropy
    hash_rate = 1e10  # 10 billion attempts/sec (high-end GPU cluster)
    seconds_to_crack = (guesses / 2) / hash_rate
    
    # Format crack time
    if seconds_to_crack < 1:
        crack_time_str = "Menos de un segundo"
    elif seconds_to_crack < 60:
        crack_time_str = f"{seconds_to_crack:.2f} segundos"
    elif seconds_to_crack < 3600:
        crack_time_str = f"{seconds_to_crack / 60:.1f} minutos"
    elif seconds_to_crack < 86400:
        crack_time_str = f"{seconds_to_crack / 3600:.1f} horas"
    elif seconds_to_crack < 31536000:
        crack_time_str = f"{seconds_to_crack / 86400:.1f} días"
    elif seconds_to_crack < 31536000000:
        crack_time_str = f"{seconds_to_crack / 31536000:.1f} años"
    else:
        crack_time_str = "Siglos (Prácticamente indescifrable)"
        
    return {
        "shannon_entropy": round(shannon, 2),
        "pool_entropy_bits": round(pool_entropy, 1),
        "strength": strength,
        "crack_time_seconds": seconds_to_crack,
        "crack_time_formatted": crack_time_str,
        "recommendations": recommendations if recommendations else ["¡El secreto cumple con excelentes prácticas de complejidad!"]
    }

# API Endpoints
@app.post("/api/scan")
def scan_directory(req: ScanPathRequest):
    target = Path(req.path)
    if not target.exists():
        raise HTTPException(status_code=400, detail=f"La ruta '{req.path}' no existe.")
    
    try:
        findings = scan_path(str(target), verbose=False)
        
        # Count files
        ignored_dirs = {".git", "__pycache__", "node_modules", "output",
                        ".venv", "venv", ".tox", "dist", "build", ".mypy_cache"}
        total_files = 0
        if target.is_file():
            total_files = 1
        else:
            for dirpath, dirnames, filenames in os.walk(target):
                dirnames[:] = [d for d in dirnames if d not in ignored_dirs]
                total_files += len(filenames)
                
        return {
            "path": str(target.resolve()),
            "total_files": total_files,
            "findings": findings
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error durante el escaneo: {str(e)}")

@app.post("/api/scan-code")
def scan_code(req: ScanCodeRequest):
    try:
        findings = scan_raw_text(req.code)
        return {
            "total_lines": len(req.code.splitlines()),
            "findings": findings
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al analizar el código: {str(e)}")

@app.get("/api/patterns")
def get_patterns():
    # Return serializable pattern details
    serializable = []
    for pat in PATTERNS:
        serializable.append({
            "name": pat["name"],
            "severity": pat["severity"],
            "regex": pat["pattern"].pattern
        })
    return serializable

@app.post("/api/patterns/test")
def check_custom_pattern(req: CustomPatternRequest):
    try:
        compiled = re.compile(req.pattern)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Expresión regular inválida: {str(e)}")
    
    matches = []
    lines = req.text.splitlines()
    for lineno, line in enumerate(lines, start=1):
        for m in compiled.finditer(line):
            matches.append({
                "line": lineno,
                "match": m.group(0),
                "start": m.start(),
                "end": m.end(),
                "content": line.rstrip()
            })
    return {"matches": matches}

@app.post("/api/entropy")
def check_entropy(req: EntropyRequest):
    return calculate_entropy_metrics(req.secret)

@app.post("/api/generate-secret")
def generate_secret(req: GenerateSecretRequest):
    pool = ""
    if req.use_upper:
        pool += string.ascii_uppercase
    if req.use_lower:
        pool += string.ascii_lowercase
    if req.use_digits:
        pool += string.digits
    if req.use_symbols:
        pool += string.punctuation
        
    if not pool:
        pool = string.ascii_letters + string.digits
        
    secret = "".join(secrets.choice(pool) for _ in range(req.length))
    metrics = calculate_entropy_metrics(secret)
    
    return {
        "secret": secret,
        "metrics": metrics
    }

@app.post("/api/scan-git")
def scan_github_repository(req: ScanGitRequest):
    # Parse Owner and Repo from URL
    match = re.search(r"https?://(?:www\.)?github\.com/([^/]+)/([^/.]+)", req.clone_url)
    if not match:
        raise HTTPException(
            status_code=400,
            detail="URL de GitHub no válida. Debe tener formato: https://github.com/usuario/repositorio"
        )
    owner, repo = match.group(1), match.group(2)
    
    # Create temp directory
    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, "repo.zip")
    
    try:
        # Try downloading refs/heads/main.zip
        zip_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/main.zip"
        download_req = urllib.request.Request(
            zip_url,
            headers={'User-Agent': 'SecretScanner/1.0.0'}
        )
        
        try:
            with urllib.request.urlopen(download_req) as response, open(zip_path, "wb") as out_file:
                shutil.copyfileobj(response, out_file)
        except Exception:
            # Fallback to master.zip
            fallback_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/master.zip"
            fallback_req = urllib.request.Request(
                fallback_url,
                headers={'User-Agent': 'SecretScanner/1.0.0'}
            )
            with urllib.request.urlopen(fallback_req) as response, open(zip_path, "wb") as out_file:
                shutil.copyfileobj(response, out_file)
                
        # Extract ZIP
        extract_dir = os.path.join(temp_dir, "extracted")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
            
        # Scan extracted files
        findings = scan_path(extract_dir, verbose=False)
        
        # Count files
        total_files = 0
        for _, _, filenames in os.walk(extract_dir):
            total_files += len(filenames)
            
        # Normalise file paths to be relative to the extracted repo
        for f in findings:
            f["file"] = os.path.relpath(f["file"], extract_dir)
            parts = Path(f["file"]).parts
            if len(parts) > 1:
                # Remove the top-level repo directory name extracted from zip
                f["file"] = str(Path(*parts[1:]))
                
        return {
            "path": req.clone_url,
            "total_files": total_files,
            "findings": findings
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al descargar o escanear el repositorio: {str(e)}"
        )
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


@app.post("/api/scan-upload")
def scan_zip_upload(file: UploadFile = File(...)):
    if not file.filename.endswith(".zip"):
        raise HTTPException(
            status_code=400,
            detail="Tipo de archivo no permitido. Solo se aceptan archivos comprimidos en formato .zip"
        )
        
    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, "upload.zip")
    
    try:
        # Save ZIP upload to temp file
        with open(zip_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Extract ZIP
        extract_dir = os.path.join(temp_dir, "extracted")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
            
        # Scan extracted files
        findings = scan_path(extract_dir, verbose=False)
        
        # Count files
        total_files = 0
        for _, _, filenames in os.walk(extract_dir):
            total_files += len(filenames)
            
        # Normalise file paths
        for f in findings:
            f["file"] = os.path.relpath(f["file"], extract_dir)
            parts = Path(f["file"]).parts
            if len(parts) > 1:
                f["file"] = str(Path(*parts[1:]))
                
        return {
            "path": file.filename,
            "total_files": total_files,
            "findings": findings
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al descomprimir o escanear el archivo: {str(e)}"
        )
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# Fallback serving index.html
@app.get("/")
def read_index():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return HTMLResponse("<h1>SecretScanner Web Interface</h1><p>Static files are missing. Please build the frontend static files.</p>")

# Mount static files (must be mounted last to not override specific API routes)
app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")
