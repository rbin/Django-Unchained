=================
Django Unchained!
=================

Django-Backend support for Couchbase 2.0, utilising CouchbaseKit (Couchbase Python wrapper for Doc Validation)

Because we all know, NoSQL is the future, and some of us want Non-relational data in our Django apps!

Inspired by Django-nonrel, Powered by CouchbaseKit and the Couchbase Python SDK.

UNFINISHED AND FAR FROM PRODUCTION READY! DO NOT USE YET!



Couchbase & CouchbaseKit
========================

You can get detailed information about couchbase itself from
http://www.couchbase.com/ and about its Python driver form
http://www.couchbase.com/develop/python/next.

Documentation: https://couchbasekit.readthedocs.org/en/latest/



Quick Start
===========
UNFINISHED.


    from couchbasekit import Connection

    # you should do this in your base settings.py:
    Connection.auth('myusername', 'p@ssword')


Then define your model document.

**models.py**::

    from django.db import models
    from django.utils.translation import ugettext_lazy as _
    from couchbasekit import Document
    couchbasekit.fields import EmailField, ChoiceField


    class Author(Document):
        __bucket_name__ = 'default'
        __key_field__ = 'slug' # optional
        doc_type = 'user'
        structure = {
            'slug': unicode,
            'first_name': unicode,
            'last_name': unicode,
