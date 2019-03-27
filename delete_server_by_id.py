from cbw_api_toolbox.cbw_api import CBWApi

API_KEY = 'VoIGnfE1i292EXJvKbum10CkIsK3q6F4jR7ZirleJoQ='
SECRET_KEY = 'mV6lxKpyPlQ7SmuoWqZapDhrKEXI853pXq1X9wm0pUriOjXNj3rLafL4cwHa1MdyaLZt/xWAsaHcn/krdmByNA=='
API_URL = 'https://10.10.1.109'

SERVER_ID = ''

res = CBWApi(API_URL, API_KEY, SECRET_KEY).delete_server(SERVER_ID)
if res:
    print('OK')
else:
    print('KO')
