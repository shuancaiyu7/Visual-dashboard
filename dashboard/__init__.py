# dashboard/__init__.py


def run_dashboard(*args, **kwargs):
    from .app import run_dashboard as _run_dashboard

    return _run_dashboard(*args, **kwargs)


__all__ = ["run_dashboard"]
