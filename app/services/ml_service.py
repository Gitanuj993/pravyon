import httpx

ML_SERVICE_URL = (
    "https://model-service-dev-6h80.onrender.com/predict"
)


async def get_prediction(project_data: dict):

    async with httpx.AsyncClient(timeout=60.0) as client:

        response = await client.post(
            ML_SERVICE_URL,
            json=project_data
        )

        response.raise_for_status()

        return response.json()