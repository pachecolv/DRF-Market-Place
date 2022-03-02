from rest_framework import permissions

class isProductSeller(permissions.BasePermission):
    """
    Object-level permission to allow only sellers of a
    product to sell it.
    """
    message = 'You must be the owner of the object'

    def has_object_permission(self, request, views, obj):
        seller = request.user.seller.get()
        if not seller:
            return False

        return obj.seller == seller
