# ================================================
# Getting the URL of an object:
# It needs to be serialized!

def getUrl(object, serializer, request):
    representation = serializer(object ,context = {"request":request})
    return representation.data["url"]
