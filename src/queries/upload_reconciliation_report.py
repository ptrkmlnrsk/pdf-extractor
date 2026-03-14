from pandas import DataFrame
from sqlalchemy import insert
from src.db.session import Session
from src.models.reconciled import Reconciled


def upload_reconciliation_report(report_to_upload: DataFrame):
    report_to_upload = report_to_upload.where(report_to_upload.notnull(), None)
    report_dict = report_to_upload.to_dict(orient="records")  # to robi liste slownikow
    with Session() as session:
        session.execute(insert(Reconciled), report_dict)
        session.commit()
