"""Analytics & Raporlama endpoint'leri.

Görüntüleme: tüm aktif ekip. Mock veri üretimi: admin/manager.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.deps import ActiveUser, DbSession, require_roles
from app.models.user import UserRole
from app.schemas.analytics import AnalyticsSummary, ReportCreate, ReportRead
from app.services import analytics_service, client_service

router = APIRouter()

ManagerUser = Annotated[object, Depends(require_roles(UserRole.admin, UserRole.manager))]


def _get_client_or_404(db: DbSession, client_id: int):
    client = client_service.get_client(db, client_id)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Müşteri bulunamadı")
    return client


@router.get(
    "/summary", response_model=AnalyticsSummary, summary="Müşteri metrik özeti + zaman serisi"
)
def summary(
    db: DbSession,
    _: ActiveUser,
    client_id: int,
    days: Annotated[int, Query(ge=1, le=365)] = 30,
) -> AnalyticsSummary:
    _get_client_or_404(db, client_id)
    return analytics_service.get_summary(db, client_id, days)


@router.post(
    "/generate", summary="Müşteri için MOCK metrik üret (admin/manager)"
)
def generate(
    db: DbSession,
    _: ManagerUser,
    client_id: int,
    days: Annotated[int, Query(ge=1, le=365)] = 30,
) -> dict:
    client = _get_client_or_404(db, client_id)
    created = analytics_service.generate_snapshots_for_client(db, client, days=days)
    return {"created": created}


# ---- Raporlar ----


@router.get("/reports", response_model=list[ReportRead], summary="Raporları listele")
def list_reports(
    db: DbSession, _: ActiveUser, client_id: int | None = None
) -> list[ReportRead]:
    return analytics_service.list_reports(db, client_id=client_id)


@router.post(
    "/reports",
    response_model=ReportRead,
    status_code=status.HTTP_201_CREATED,
    summary="Rapor oluştur",
)
def create_report(
    db: DbSession, current_user: ActiveUser, data: ReportCreate, _: ManagerUser
) -> ReportRead:
    client = _get_client_or_404(db, data.client_id)
    return analytics_service.create_report(
        db, client, days=data.period_days, generated_by=current_user, title=data.title
    )


@router.get("/reports/{report_id}", response_model=ReportRead, summary="Tek rapor")
def get_report(db: DbSession, _: ActiveUser, report_id: int) -> ReportRead:
    report = analytics_service.get_report(db, report_id)
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rapor bulunamadı")
    return report
