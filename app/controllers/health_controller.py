from fastapi import APIRouter

from app.dtos.health_dto import HealthResponseDTO

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponseDTO)
def health() -> HealthResponseDTO:
    return HealthResponseDTO(status="ok")
