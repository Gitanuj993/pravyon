from fastapi import APIRouter, HTTPException
import httpx

from app.services.ml_service import get_prediction

router = APIRouter(
    prefix="/api/v1",
    tags=["Prediction"]
)


@router.post("/predict")
async def predict(project: dict):

    print("Project data received")

    try:

        prediction = await get_prediction(project)

        return {
            "status": "success",
            "data": prediction
        }

    except httpx.HTTPStatusError as error:

        raise HTTPException(
            status_code=error.response.status_code,
            detail="ML service returned an error"
        )

    except httpx.RequestError:

        raise HTTPException(
            status_code=503,
            detail="ML service is unavailable"
        )