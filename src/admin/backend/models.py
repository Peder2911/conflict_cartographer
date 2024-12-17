

from cc_backend_lib import models

class EmailStatusAdminPost(models.user.EmailStatus, models.user.UserPersonIdentification):
    clear_last_emailed: bool
