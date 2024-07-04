import requests
from KEY import *


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_brand_id():
    # Get Brand_id
    r = requests.get(
        url='https://api.upmind.io/api/admin/brand/settings',
        headers={
            'Authorization': f'Bearer {UP_API_KEY}',
        },
        params={}
    )
    res = r.json()
    brand_id = res['data']['id']
    r.close()
    return brand_id


def create_user_upmind(name_f, name_l, email):
    """
    Create user in UpMind
    :param name_f:
    :param name_l:
    :param email:
    :return:
    """
    brand_id = get_brand_id()

    r = requests.get(
        'https://api.upmind.io/api/admin/clients',
        headers={'Authorization': f'Bearer {UP_API_KEY}'},
        params={
            'brand_id': brand_id,
            'filter[is_guest]': 0,
            'filter[accounts.id|gt]': 0,
            'offset': 0,
            'order': '-created_at',
            'skip_count': 1
        }
    )
    res = r.json()
    r.close()

    flag = False
    if res['total'] == 0:
        flag = True
    else:
        for i in range(len(res['data'])):
            if name_f == res['data'][i]['firstname'] and name_l == res['data'][i]['lastname'] and email == res['data'][i]['email']:
                # User already in upMind
                flag = False
                break
            else:
                flag = True

    if flag:
        # If there is no User in upMind, create it
        params = {
            'brand_id': brand_id,
            'custom_fields': {},
            'email': email,
            'firstname': name_f,
            'has_login': 1,  # true instead of True
            'lastname': name_l,
            'password': '',
            'verified': 0  # false instead of False
        }
        r = requests.post(
            'https://api.upmind.io/api/admin/clients',
            headers={
                'Authorization': f'Bearer {UP_API_KEY}',
                'Content-Type': 'application/json'
            },
            params=params
        )
        res = r.json()
        r.close()
        if res['status'] == 'ok':
            print(bcolors.OKBLUE + 'User CREATED' + bcolors.ENDC)
        else:
            print(bcolors.FAIL + 'User Creation Failed' + bcolors.ENDC)
            print(res)
    else:
        print(bcolors.OKBLUE + 'User EXIST' + bcolors.ENDC)


def get_user_id(name_f, name_l, email):
    """
    Get user_id by name_f, name_l, email
    :param name_f:
    :param name_l:
    :param email:
    :return: user_id
    """
    brand_id = get_brand_id()

    r = requests.get(
        'https://api.upmind.io/api/admin/clients',
        headers={'Authorization': f'Bearer {UP_API_KEY}'},
        params={
            'brand_id': brand_id,
            'filter[is_guest]': 0,
            'filter[accounts.id|gt]': 0,
            'offset': 0,
            'order': '-created_at',
            'skip_count': 1
        }
    )
    res = r.json()
    r.close()
    for i in range(len(res['data'])):
        user = res['data'][i]
        if res['data'][i]['firstname'] == name_f and \
                res['data'][i]['lastname'] == name_l and \
                res['data'][i]['email'] == email:
            return res['data'][i]['id']
    return None


def make_order_(uid, name_f, name_l):
    """
    make free order to user with uid
    """
    r = requests.get(
        'https://api.upmind.io/api/admin/products',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {UP_API_KEY}'
        },
        params={}
    )

    pid = None
    res = r.json()
    for product in res['data']:
        if product['name'] == PRODUCT_NAME:
            pid = product['id']

    r.close()

    print(bcolors.OKBLUE + PRODUCT_NAME + ':' + pid + bcolors.ENDC)

    r = requests.post(
        'https://api.upmind.io/api/admin/orders/quick',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {UP_API_KEY}'
        },
        json={
            "category_slug": "new_contract",
            "client_id": uid,
            "currency_code": "USD",
            "manual_import": "0",
            "products": [
                {
                    "selling_price": 0,
                    "product_id": pid,
                    "quantity": 1,
                    "billing_cycle_months": 1,
                    "provision_field_values": {
                        "domain": name_f+name_l+'.productgen.com',
                        "sld": ''
                    },
                    "attributes": []
                }
            ]
        }
    )
    res = r.json()
    if res['status'] == 'ok':
        print(bcolors.OKBLUE + 'ORDERED SUCCESSFULLY' + bcolors.ENDC)
    else:
        print(res)
        print(bcolors.FAIL + 'ORDERING FAILED' + bcolors.ENDC)

    r.close()


def change_order_(uid):
    r = requests.get(
    'https://api.upmind.io/api/admin/products',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {UP_API_KEY}'
        },
        params={

        }
    )

    pid = None
    tpid = None
    res = r.json()
    for product in res['data']:
        if product['name'] == PRODUCT_NAME:
            pid = product['id']
        if product['name'] == PRODUCT_NAME1:
            tpid = product['id']


    r = requests.get(
        url='https://api.upmind.io/api/admin/contracts_products',
        headers={
            'Authorization': f'Bearer {UP_API_KEY}',
        },
        params={
            'client_id': uid,
            # 'filter[status.code]': 'contract_active',
            'order': '-created_at'
        }
    )
    res = r.json()
    r.close()
    for record in res['data']:
        if record['product_id'] == pid and record['status']['code'] != 'contract_cancelled':
            contract_id = record['contract_id']
            contract_product_id = record['id']
            r = requests.put(
                url=f"https://api.upmind.io/api/admin/contracts/{contract_id}/products/{contract_product_id}/change",
                headers={
                    'Authorization': f'Bearer {UP_API_KEY}',
                    "Content-Type": "application/json"
                },
                json={
                    'pro_rata_amount': 0,
                    'product': {
                        'product_id': tpid,
                        'quantity': 1,
                        'price': '20.00'
                    },
                }
            )
            res = r.json()
            r.close()
            if res['status'] == 'ok':
                print(bcolors.OKBLUE + "CHANGE Success" + bcolors.ENDC)
            else:
                print(bcolors.FAIL + "CHANGE Failed" + bcolors.ENDC)
                print(res)


def make_order(name_f, name_l, email):
    create_user_upmind(name_f, name_l, email)
    uid = get_user_id(name_f, name_l, email)
    make_order_(uid, name_f, name_l)

def change_order(name_f, name_l, email):
    uid = get_user_id(name_f, name_l, email)
    change_order_(uid)

if __name__ == '__main__':
    name_f = 'Ryan'
    name_l = 'Greene'
    email = 'ryantest@greenehome.com'
    # create_user_upmind(name_f, name_l, email)
    # uid = get_user_id(name_f, name_l, email)
    # print(uid)
    change_order(name_f, name_l, email)

