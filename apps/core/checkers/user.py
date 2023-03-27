from uuid import UUID

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

    @staticmethod
    def check_user_chats(request_user: User, user_id: UUID):
        if request_user.is_superuser:
            return True

        if request_user.pk == user_id:
            return True

        return False

