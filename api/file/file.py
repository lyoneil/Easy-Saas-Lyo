# _*_ coding: utf-8 _*_

"""
file api
"""

from .utils import RespFile, RespFileList, check_file_permission, get_filetag_id_list
from ..base import *
from ..utils import get_current_user

# define router
router = APIRouter()


@router.get("/", response_model=RespFileList)
def _get_file_schema_list(skip: int = Query(0, description="skip count"),
                          limit: int = Query(100, description="limit count"),
                          current_user: User = Depends(get_current_user),
                          session: Session = Depends(get_session)):
    """
    get file schema list and filetag_id list list of current_user
    """
    user_id = current_user.id
    _filter = File.user_id == user_id

    # get file model list and schema list
    file_model_list = session.query(File).filter(_filter).offset(skip).limit(limit).all()
    file_schema_list = [FileSchema(**fm.dict()) for fm in file_model_list]

    # return file schema list and filetag_id list list
    filetag_id_list_list = [get_filetag_id_list(fm.id, session) for fm in file_model_list]
    return RespFileList(data_file_list=file_schema_list, data_filetag_id_list_list=filetag_id_list_list)


@router.patch("/{file_id}", response_model=RespFile)
def _update_file_model(file_id: str = Path(..., description="file id"),
                       file_schema: FileUpdate = Body(..., description="update schema"),
                       current_user: User = Depends(get_current_user),
                       session: Session = Depends(get_session)):
    """
    update file model based on update schema, return file schema
    - **status_code=403**: no permission to access file
    """
    # check file_id and get file model
    file_model = check_file_permission(file_id, current_user.id, session)

    # update file model based on update schema
    for field in file_schema.model_dump(exclude_unset=True):
        setattr(file_model, field, getattr(file_schema, field))
    session.merge(file_model)
    session.commit()

    # return file schema and filetag_id list
    file_schema = FileSchema(**file_model.dict())
    return RespFile(data_file=file_schema, data_filetag_id_list=[])


@router.post("/trash/", response_model=Resp)
def _trash_file_model_list(file_id_list: List[str] = Body(..., description="list of file id"),
                           current_user: User = Depends(get_current_user),
                           session: Session = Depends(get_session)):
    """
    trash file model list by file_id list
    """
    _filter = File.user_id == current_user.id

    # trash file model list by file_id list
    _filter1 = File.id.in_(file_id_list)
    _update = {File.is_trash: True, File.trash_time: datetime.utcnow()}
    session.query(File).filter(_filter, _filter1).update(_update, synchronize_session=False)
    session.commit()

    # return result
    return Resp(msg="trash success")


@router.post("/untrash/", response_model=Resp)
def _untrash_file_model_list(file_id_list: List[str] = Body(..., description="list of file id"),
                             current_user: User = Depends(get_current_user),
                             session: Session = Depends(get_session)):
    """
    untrash file model by file_id list
    """
    _filter = File.user_id == current_user.id

    # untrash file model list by file_id list
    _filter1 = File.id.in_(file_id_list)
    _update = {File.is_trash: False, File.trash_time: None}
    session.query(File).filter(_filter, _filter1).update(_update, synchronize_session=False)
    session.commit()

    # return result
    return Resp(msg="untrash success")


@router.delete("/", response_model=Resp)
def _delete_file_model_list(file_id_list: List[str] = Body(..., description="list of file id"),
                            current_user: User = Depends(get_current_user),
                            session: Session = Depends(get_session)):
    """
    delete file model list by file_id list
    """
    _filter = File.user_id == current_user.id

    # delete file model list by file_id list
    _filter1 = File.id.in_(file_id_list)
    _filter2 = File.is_trash == True
    session.query(File).filter(_filter, _filter1, _filter2).delete()
    session.commit()

    # return result
    return Resp(msg="delete success")
