from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, get_db
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Hydro-Logic")

def hitung_prioritas(kelembapan: float, candangan_air: float) -> str:
    """
    Ini adalah inti dari Smart Water Priority (SWP).
    """
    if kelembapan < 30.0 and cadangan_air > 20.0:
        return "🔴 Kritis - Prioritas 1 (Segera Alokasikan Air)"
    elif kelembapan < 50.0:
        return "🟡 Waspada - Prioritas 2 (Jadwalkan Distribusi)"
    else:
        return "🟢 Aman - Tidak Perlu Distribusi Air"

@app.post("/api/sensor_data", response_model=models.DataKeluarResponse)
def terima_data_sensor(data: models.DataMasukIoT, db: Session = Depends(get_db)):
    status_spk = hitung_prioritas(data.kelembapan_tanah, data.level_air_cadangan)

    db_data = models.LahanData(
        sektor_lahan =data.sektor_lahan,
        kelembapan_tanah=data.kelembapan_tanah,
        level_air_cadangan=data.level_air_cadangan,
        status_rekomendasi=status_spk
    )

    db.add(db_data)
    db.commit()
    db.refresh(db_data)

    if "Kritis" in status_spk:
        print(f"\n[TELEGRAM BOT MENGIRIM PESAN] 🚨 PERINGATAN KWT:")
        print(f"Tanah di {data.sektor_lahan} sangat kering ({data.kelembapan_tanah}%). Segera buka katup air ke sektor ini!\n")

    return db_data