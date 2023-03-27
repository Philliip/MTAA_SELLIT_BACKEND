from object_checker.base_object_checker import AbacChecker

from apps.core.models import User, Offer


class OfferChecker(AbacChecker):
    @staticmethod
    def check_offer(request_user: User, offer: Offer):
        if request_user.is_superuser:
            return True

        if request_user == offer.user:
            return True

        return False
