from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """
    def has_object_permission(self, request, view, obj):
        # Check if user is participant in conversation
        if hasattr(obj, 'participants'):
            # For Conversation objects
            return request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            # For Message objects
            return request.user in obj.conversation.participants.all()
        return False

    def has_permission(self, request, view):
        # Allow create operations (will be validated in the viewset)
        if request.method == 'POST':
            return True
        return True  # Let has_object_permission handle the filtering