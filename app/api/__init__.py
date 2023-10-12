from fastapi import APIRouter
from app.api.endpoints import user, certificate, project, community, discrepancy, contact, index, images

router = APIRouter()
router.include_router(index.router)
router.include_router(user.router, prefix="/users", tags=["User Management"])
router.include_router(certificate.router, prefix="/certificates", tags=["Certificate Management"])
router.include_router(project.router, prefix="/projects", tags=["Project Management"])
router.include_router(community.router, prefix="/community", tags=["Community Engagement"])
# router.include_router(discrepancy.router, prefix="/discrepancy", tags=["Discrepancy Detection"])
router.include_router(contact.router, prefix="/contact", tags=["Contact Information"])
router.include_router(images.router, prefix="/images", tags=["Manage mages"])

# Include other routers here for other entities