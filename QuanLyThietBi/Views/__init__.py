from .phongban import (
    get_phongban_list,
    create_phongban,
    get_phongban_by_id,
    update_phongban,
    delete_phongban,
    search_phongban
)

__all__ = [
    'get_phongban_list',
    'create_phongban', 
    'get_phongban_by_id',
    'update_phongban',
    'delete_phongban',
    'search_phongban'
]

from . import admin_views
from . import staff_views