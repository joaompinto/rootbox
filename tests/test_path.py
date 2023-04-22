from rootbox.mount_checker import is_path_contained


def test_path_contained():
    assert is_path_contained("/test/path", "/test") is True
    assert is_path_contained("/test/path", "/test1") is False
