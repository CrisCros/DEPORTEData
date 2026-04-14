from fastapi import APIRouter, Depends

from app.services.data_service import DataService, get_data_service

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/kpis")
def get_dashboard_kpis(data_service: DataService = Depends(get_data_service)):
    return data_service.dashboard_kpis()


@router.get("/series")
def get_dashboard_series(data_service: DataService = Depends(get_data_service)):
    return data_service.dashboard_series()
