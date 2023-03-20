from object_checker.base_object_checker import AbacChecker

from apps.core.models import User


class UserChecker(AbacChecker):
    @staticmethod
    def check_user(request_user: User, user: User):
        if request_user.is_superuser:
            return True

        if request_user == user:
            return True

        return False
