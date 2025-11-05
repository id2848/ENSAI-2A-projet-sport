from fastapi.responses import RedirectResponse
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from fastapi import FastAPI, UploadFile, File, HTTPException
import io

import logging
from utils.log_init import initialiser_logs

from service.activite_service import ActiviteService

from utils import parse_strava_gpx


app = FastAPI(title="Webservice Sports ENSAI")

initialiser_logs("Webservice")

# ------------- Authentification Basique ------------------

security = HTTPBasic()

USERS = {
    "alice": {"password": "wonderland", "roles": ["admin"]},
    "bob":   {"password": "builder",    "roles": ["user"]},
}

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password

    user = USERS.get(username)
    if not user or not secrets.compare_digest(password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return {"username": username, "roles": user["roles"]}

@app.get("/me")
def me(user = Depends(get_current_user)):
    return {"user": user}

# ----------------------------------------------------------

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirect to the API documentation"""
    return RedirectResponse(url="/docs")

@app.get("/activites/{id_utilisateur}")
def activites_par_utilisateur(id_utilisateur: int, user = Depends(get_current_user)):
    """Afficher activités utilisateur"""
    return ActiviteService().lister_activites(id_utilisateur)

"""
@app.post("users/{user_id}/activities")
def creer_activite(user_id):
    user = UtilisateurDAO().get(user_id)
    activity = user.create_activity()
    AcitivityDAO().save(activity)
    # UtilisateurService().create_activity(user_id)
"""

@app.post("/upload-gpx")
async def upload_gpx(file: UploadFile = File(...)):
    # Lecture du contenu du fichier (texte)
    content = await file.read()
    # Parsing
    return parse_strava_gpx(content)


# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9876)

    logging.info("Arret du Webservice")
