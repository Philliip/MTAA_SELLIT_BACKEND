from object_checker.base_object_checker import AbacChecker

from apps.core.models import User, Image


class ImageChecker(AbacChecker):
    @staticmethod
    def check_delete(request_user: User, image: Image):
        if request_user.is_superuser:
            return True

        if request_user == image.offer.user:
            return True

        return False
