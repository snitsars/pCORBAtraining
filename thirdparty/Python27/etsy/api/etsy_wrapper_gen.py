import storagesqlite
from etsy import Etsy

storage = storagesqlite.Storage('etsy.db')
e = Etsy(storage, '9avabtnm6p26odme939o3o8y', '293yf9k467', permissions=['favorites_rw'])

def endpointfromuri(uri):
  parts = uri.split('/')
  result = ''
  params = []
  for chunk in uri.split('/')[1:]:
    if chunk == '' or chunk[0] != ':':
      result += '/' + chunk
    else:
      result += '/%s'
      params.append(chunk[1:])

  result = '\'' + result + '\''
  if len(params) == 1:
    result += ' % ' + params.pop()
  elif len(params) > 1:
    result += ' % (' + ", ".join(params) + ')'

  return result 


def gen_method(record):
  template = """    def %s(self, %s):
        \"\"\"%s\"\"\"

        endpoint = %s

        self.params = {}
%s
        response = self.execute(endpoint, '%s')
        return json.loads(response.text)

"""
  params = record['params'] if record['params'] else []
  defaults = record['defaults'] if record['defaults'] else []
  mandatory_params = [x for x in params if x not in defaults]
  optional_params = [x for x in params if x in defaults]

  fill_str = "".join(["        self.params['%s'] = %s\n" % (x, x) for x in mandatory_params]) + \
             "".join(["        if %s: self.params['%s'] = %s\n" % (x, x, x) for x in optional_params])


  params_str_list = mandatory_params
  params_str_list.extend([
    x+'=' + ("'" + str(defaults[x]) + "'" if defaults[x] != None else 'None') for x in optional_params
  ])
  params_str = ", ".join(params_str_list)
 
  return template % (record['name'], params_str, record['description'], endpointfromuri(record['uri']), fill_str, record['http_method'].lower())

for record in e.getMethodTable()['results']:
  print gen_method(record)

