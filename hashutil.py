import hashlib
import random
import string


def make_salt():
    return ''.join([random.choice(string.ascii_letters) for x in range(5)])


def make_hash_with_salt(password, salt=None):
    if not salt:
        salt = make_salt()
    hash = get_hash(password+salt)
    return '{},{}'.format(hash, salt)

def get_hash(text):
    return hashlib.sha256(str.encode(text)).hexdigest()


def verify_hash(password, hash):
    salt = hash.split(',')[1]
    if make_hash_with_salt(password, salt) == hash:
        return True
    return False
