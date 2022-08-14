from ..thread_class import ThreadCLass


def test_init():
    thread = ThreadCLass()


def test_initialization():
    thread = ThreadCLass()
    thread.initialize(thread_timeout=0.1)


def test_cleanup():
    thread = ThreadCLass()
    thread.initialize(thread_timeout=0.1)
    thread._cleanup
