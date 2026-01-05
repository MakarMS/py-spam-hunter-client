from py_spam_hunter_client.exceptions.check_exception import CheckException


def test_check_exception_message():
    message = "failure"
    exc = CheckException(message)
    assert str(exc) == message
