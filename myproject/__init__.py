# Monkey patch Django to ignore MySQL version checks since Django 4.2+ drops support for MySQL 5.7
try:
    from django.db.backends.mysql.base import DatabaseWrapper
    DatabaseWrapper.check_database_version_supported = lambda self: None
except ImportError:
    pass
