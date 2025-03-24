from django.contrib.auth.models import Group
from django.db.utils import OperationalError, ProgrammingError

def create_groups(sender, **kwargs):
    """Ensure 'CarOwners' and 'Drivers' groups exist after migrations."""
    try:
        for group_name in ["CarOwners", "Drivers"]:
            Group.objects.get_or_create(name=group_name)
    except (OperationalError, ProgrammingError):
        # Ignore errors if the database is not fully ready
        pass
"""Your app needs CarOwners and Drivers groups.
Instead of adding this logic in apps.py (which causes database warnings), we move it to signals.py and use post_migrate.Why Use Signals Instead of Calling Functions Directly?
Automatic Execution =Runs when events happen, without modifying views or models.
Decoupled Logic =Keeps your main code clean.
Django Best Practice = Avoids database access during initialization."""