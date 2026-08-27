from sqlalchemy import Column, Integer, String, Float, DateTime
from pydantic import BaseModel, Field
from datetime import datetime
from database import Base

# ==========================================
# 1. SQLALCHEMY MODELS (Tabel Database)
# ==========================================
class LahanData(Base):
    __tablename__ = "data_lahan"

    id = Column(Integer, primary_key=True, index=True)
    sektor_lahan = Column(String, index=True) # Contoh: Sektor A, Sektor B
    kelembapan_tanah = Column(Float) # Persentase 0-100%
    level_air_cadangan = Column(Float) # Persentase 0-100% dari tangki/sumber
    status_rekomendasi = Column(String) # Output SPK
    waktu_pencatatan = Column(DateTime, default=datetime.utcnow)

# ==========================================
# 2. PYDANTIC SCHEMAS (Validasi Data Masuk/Keluar)
# ==========================================

class DataMasukIoT(BaseModel):
    sektor_lahan: str = Field(..., example="Sektor A")
    kelembapan_tanah: float = Field(..., ge=0, le=100, description="Kelembapan 0-100%")
    level_air_cadangan: float = Field(..., ge=0, le=100, description="Kapasitas air 0-100%")

class DataKeluarResponse(DataMasukIoT):
    id: int
    status_rekomendasi: str
    waktu_pencatatan: datetime

    class Config:
        from_attributes = True