NEW_MODEL_INFO = "SELECT * FROM model_info ORDER BY id DESC LIMIT 1"

VALID_DATE = "SELECT COUNT(*) AS records FROM station_date where station = %s and date = %s"

