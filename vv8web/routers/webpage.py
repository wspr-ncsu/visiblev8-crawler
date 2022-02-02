from fastapi import APIRouter

router = APIRouter()

@router.get('/')
def get_root():
    return 'hello world'

@router.get('/test')
def get_test():
    return 'this is a test'
