from fastapi import APIRouter
from vv8db_sidecar.models.parsed_log_model import ParsedLogModel

router = APIRouter(
    prefix='/api/v1'
)

@router.put('parsedlog')
def put_parsed_log(parsed_log: ParsedLogModel):
    print(type(parsed_log))
