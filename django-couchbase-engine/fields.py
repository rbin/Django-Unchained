#! /usr/bin/env python
"""
couchbasekit.fields
~~~~~~~~~~~~~~~~~~~

:website: http://github.com/kirpit/couchbasekit
:copyright: Copyright 2012, Roy Enjoy <kirpit *at* gmail.com>, see AUTHORS.txt.
:license: MIT, see LICENSE.txt for details.

* :class:`couchbasekit.fields.CustomField`
* :class:`couchbasekit.fields.ChoiceField`
* :class:`couchbasekit.fields.EmailField`
* :class:`couchbasekit.fields.PasswordField`
"""
from abc import ABCMeta


class CustomField(object):
    """The abstract custom field to be extended by all other field classes.

    .. note::
        You can also create your own custom field types by implementing this
        class. All you have to do is to assign your final (that is calculated
        and ready to be saved) value to the :attr:`value` property. Please
        note that it should also accept unicode raw values, which are fetched
        and returned from couchbase server. See :class:`PasswordField` source
        code as an example.

        Please contribute back if you create a generic and useful custom field.
    """
    __metaclass__ = ABCMeta
    _value = None
    def __init__(self):
        raise NotImplementedError()

    def __repr__(self):
        return repr(self.value)

    def __eq__(self, other):
        if type(self) is type(other) and self.value==other.value:
            return True
        return False

    @property
    def value(self):
        """Property to be used when saving a custom field into
        :class:`couchbasekit.document.Document` instance.

        :returns: The value to be saved for the field within
            :class:`couchbasekit.document.Document` instances.
        :rtype: unicode
        """
        if not isinstance(self._value, basestring):
            raise ValueError("%s's 'value' is not set." % type(self).__name__)
        return self._value

    @value.setter
    def value(self, value):
        """Propery setter that should be used to assign final (calculated)
        value.
        """
        self._value = value


class ChoiceField(CustomField):
    """The custom field to be used for multi choice options such as gender,
    static category list etc. This class can't be used directly that has to be
    extended by your choice list class. Thankfully, it's just easy::

        class Gender(ChoiceField):
            CHOICES = {
                'M': 'Male',
                'F': 'Female',
            }

    and all you have to do is to pass the current value to create your choice
    object:

    >>> choice = Gender('F')
    >>> choice.value
    'F'
    >>> choice.text
    'Female'

    :param choice: The choice value.
    :type choice: basestring
    """
    __metaclass__ = ABCMeta
    CHOICES = {}
    def __eq__(self, other):
        if super(ChoiceField, self).__eq__(other) and \
           self.CHOICES==other.CHOICES:
            return True
        return False

    def __init__(self, choice):
        if not isinstance(self.CHOICES, dict) or not len(self.CHOICES):
            raise AttributeError("ChoiceFields must have dictionary 'CHOICES' "
                                 "attribute and cannot be empty.")
        if choice not in self.CHOICES:
            raise ValueError("Default choice for %s must be "
                             "within the 'CHOICES' attribute."
                             % type(self).__name__)
        self.value = choice

    @property
    def text(self):
        """Returns the text of the current choice, object property.

        :rtype: unicode
        """
        return self.CHOICES.get(self.value)

    def iteritems(self):
        return self.CHOICES.iteritems()


class EmailField(CustomField):
    """The custom field to be used for email addresses and intended to validate
    them as well.

    .. warning::
        Email address validation is NOT implemented yet. A best practice
        validation that doesn't depend on any other package is much appreciated.

    :param email: Email address to be saved.
    :type email: basestring
    """
    def __init__(self, email):
        if not self.is_valid(email):
            raise ValueError("Email address is invalid.")
        self.value = email

    @staticmethod
    def is_valid(email):
        """Email address validation method.

        :param email: Email address to be saved.
        :type email: basestring
        :returns: Always True, as it's not implemented yet.
        :rtype: bool
        """
        # TODO: validate email address
        RuntimeWarning('EmailField.is_valid() method is not implemented yet.')
        return True


class PasswordField(CustomField):
    """The custom field to be used for password types.

    It encrypts the raw passwords on-the-fly and depends on
    `py-bcrypt` library for such encryption.

    :param password: Raw or encrypted password value.
    :type password: unicode
    :raises: :exc:`ImportError` if `py-bcrypt` was not found.
    """
    LOG_ROUNDS = 12
    def __init__(self, password):
        if not isinstance(password, basestring):
            raise ValueError("Password must be a string or unicode.")
        # do the encryption if raw password provided
        if not password.startswith(('$2a$', '$2y$')):
            bcrypt = self.get_bcrypt()
            password = bcrypt.hashpw(password, bcrypt.gensalt(self.LOG_ROUNDS))
        self.value = password

    @staticmethod
    def get_bcrypt():
        """Returns the `py-bcrypt` library for internal usage.

        :returns: `py-bcrypt` package.
        :raises: :exc:`ImportError` if `py-bcrypt` was not found.
        """
        try: import bcrypt
        except ImportError:
            raise ImportError("PasswordField requires 'py-bcrypt' "
                              "library to hash the passwords.")
        else: return bcrypt

    def check_password(self, raw_password):
        """Validates the given raw password against the intance's encrypted one.

        :param raw_password: Raw password to be checked against.
        :type raw_password: unicode
        :returns: True if comparison was successful, False otherwise.
        :rtype: bool
        :raises: :exc:`ImportError` if `py-bcrypt` was not found.
        """
        bcrypt = self.get_bcrypt()
        return bcrypt.hashpw(raw_password, self.value)==self.value