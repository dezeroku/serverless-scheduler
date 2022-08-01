def get_username(event):
    # This can be probably handled much better and cleaner?
    # At least let's put some error handling
    return event["requestContext"]["authorizer"]["jwt"]["claims"]["username"]
