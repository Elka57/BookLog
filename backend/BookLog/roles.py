from rest_framework_roles.roles import is_anon, is_user, is_admin, is_staff
from users.models import UserTypes

def is_journalist(request, view, obj=None):
    return is_user(request, view) and request.user.user_type == UserTypes.JOURNALIST.value

def is_reader(request, view, obj=None):
    return is_user(request, view) and request.user.user_type == UserTypes.READER.value

ROLES = {
  'ANON':       lambda req, vw, obj=None: is_anon(req, vw),
  'USER':       lambda req, vw, obj=None: is_user(req, vw),
  'ADMIN':      lambda req, vw, obj=None: is_admin(req, vw),
  'STAFF':      lambda req, vw, obj=None: is_staff(req, vw),
  'JOURNALIST': is_journalist,
  'READER':     is_reader,
}
