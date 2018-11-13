import requests
from requests_toolbelt.utils import dump

API_TOKEN = 'm3MLGHi8SgbJOFQkC3-h-S2mpoajCRtO'
API_URL = 'https://api.findface.pro/v1/'
GALLERY = 'my_gallery'


# ServiceException = requests.exceptions.RequestException
class ServiceException(IOError):
    pass


# -------------------------------------------

def _service(url, method='GET', data=None, files=None):
    r = requests.request(
        method,
        API_URL + url,
        headers={'Authorization': 'Token {}'.format(API_TOKEN)},
        data=data,
        files=files
    )

    # def printable(s):
    #     def isprint(c): return (32 <= c <= 126) or (c == 13) or (c == 10)
    #
    #     return ''.join(chr(char) if isprint(char) else ' ' for char in s)
    # print '===================================='
    # print printable(dump.dump_all(r))
    # print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'

    if r.status_code != 200:

        try:
            code = r.json()['code']
            reason = r.json()['reason']
            try:
                r.raise_for_status()
            except requests.exceptions.RequestException as e:
                raise ServiceException("{}: {}".format(code, reason))
        except ValueError:
            r.raise_for_status()

    return r


def create_gallery(name):
    return _service('galleries/{}/'.format(name), 'POST')

def delete_gallery(name=GALLERY):
    return _service('galleries/{}/'.format(name), 'DELETE')

def get_gallery_list():
    return _service('galleries/').json()['results']


def _touch_GALLERY():
    if not GALLERY in get_gallery_list():
        create_gallery(GALLERY)


def list_faces():
    _touch_GALLERY()
    return _service('faces/gallery/{}/'.format(GALLERY)).json()['results']


def get_face(_id):
    return _service('faces/id/{}/'.format(_id)).json()


def delete_face(_id):
    return _service('faces/id/{}/'.format(_id), 'DELETE')


def create_face(photo, meta):
    _touch_GALLERY()
    return _service('face/', 'POST', {'meta': meta, 'galleries': GALLERY}, {'photo': photo}).json()['results'][0]


def identify_face(photo, n, threshold):
    data, files = ({'photo': photo}, None) if isinstance(photo, (str, unicode)) else ({}, {'photo': photo})

    data.update({
        'n': n,
        'threshold': threshold
    })

    r = _service(
        'identify/', 'POST', data, files
    ).json()['results'].values()[0]

    for f in r:
        f['face']['confidence'] = f['confidence']
        # print '==============================', f['confidence']

    return [f['face'] for f in r]
