# Tools

## Black

Code formatter.

Format `back-end/src` code using [`scripts/format.sh`](../scripts/format.sh). 
Pass `-c | --check` flag to check for code style conformance.

If you use `PyCharm`, be sure to turn off auto formatter:
1. Navigate to `Settings / Preferences` > `Appearance & Behavior` > `Scopes`.
1. Add new scope with name `python` and pattern `file:*.py`.
1. Navigate to `Settings / Preferences` > `Editor` > `Code Style` > `Formatter Control`.
1. Add created `python` scope.

## Pylint

Code linter.

Lint code for the entire `back-end` using [`scripts/lint.sh`](../scripts/lint.sh)
or manually specify directories and modules/files:
```shell script
pylint conf dms/models.py
```

In order to display a help message for the given message id, pass it to `--help-msg` option:
```shell script
pylint --help-msg=<id>
```

For example:
```shell script
$ scripts/lint.sh
dms/admin.py:3:0: E5142: User model imported from django.contrib.auth.models (imported-auth-user)

$ pylint --help-msg=E5142
:imported-auth-user (E5142): *User model imported from django.contrib.auth.models*
  Don't import django.contrib.auth.models.User model. Use
  django.contrib.auth.get_user_model() instead! This message belongs to the
  auth-user-checker checker.
```

Lint settings can be found in [`.pylintrc`](../.pylintrc).

## PyTest

Test framework.

Run tests for the entire `back-end` using [`scripts/test.sh`](../scripts/test.sh).

We use default [`pytest`](https://docs.pytest.org/en/stable/) 
and Django-specific addon [`pytest-django`](https://pytest-django.readthedocs.io/en/latest/).
