class ClientException(Exception): pass
class OtherException(Exception): pass

def raise_exception(status_code: int):
	if (str(status_code) == 401):
		raise ClientException()
	else:
		raise OtherException()
