from object_checker.base_object_checker import AbacChecker

from apps.core.models import User, OfferChatUser


class ChatChecker(AbacChecker):
    @staticmethod
    def check_chat(request_user: User, offer_chat_id):
        if request_user.is_superuser:
            return True

        if OfferChatUser.objects.filter(offer_chat_id=offer_chat_id, user=request_user).exists():
            return True

        return False
