from fastapi import APIRouter

router = APIRouter(
    prefix='/api/v1'
)

@router.get('/hello')
def get_hello():
    data = {
        'msg': 'hello',
        'num': 100
    }
    return data
