from object_checker.base_object_checker import AbacChecker

from apps.core.models import User, Message


class MessageChecker(AbacChecker):
    @staticmethod
    def check_message(request_user: User, message: Message):
        if request_user.is_superuser:
            return True

        if request_user == message.user:
            return True

        return False
