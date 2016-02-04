import storagesqlite
from etsy import Etsy

storage = storagesqlite.Storage('etsy.db')
e = Etsy(storage, 0.2, '9avabtnm6p26odme939o3o8y', '293yf9k467', permissions=['favorites_rw'])

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

#print cur_offset, raw_listings['count'], raw_listings['pagination']['next_offset']
def gen_ext_method(mandatory_params, optional_params, defaults):
  template_ext = """    def %sExt(self, %s):
      \"\"\"%s\"\"\"

      if offset<0: raise Exception('Invalid \\\'offset\\\' parameter: %%s. offset shound not be less than 0.' %% offset)
      if limit<0: raise Exception('Invalid \\\'limit\\\' parameter: %%s. limit shound not be less than 0.' %% limit)

      result = []
      cur_offset = offset
      while True:
        raw_listings = self.%s(%s)

        filtered = [x for x in raw_listings['results'] if filterfunc(x)] if filterfunc else raw_listings['results']
        if limit>0:
          result.extend(filtered[:limit-len(result)])
          if len(result) == limit: return result
        else:
          result.extend(filtered)

        if raw_listings['pagination']['next_offset'] == None: return result

        cur_offset += raw_listings['pagination']['effective_limit']

      return result

"""

  params_str_list = list(mandatory_params)
  params_str_list.extend(['offset=0', 'limit=0', 'filterfunc=None'])
  params_str_list.extend([
    x+'=' + ("'" + str(defaults[x]) + "'" if defaults[x] != None else 'None') for x in optional_params if x not in ['limit', 'page', 'offset']
  ])
  params_str = ", ".join(params_str_list)

  params_str2_list = list(mandatory_params)
  params_str2_list.extend(['offset=cur_offset', 'limit=100'])
  params_str2_list.extend([x+'='+x for x in optional_params if x not in ['limit', 'page', 'offset']])

  params_str2 = ", ".join(params_str2_list)

  return template_ext % (record['name'], params_str, 'Wrapper for: ' + record['name'], record['name'], params_str2)

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


  params_str_list = list(mandatory_params)
  params_str_list.extend([
    x+'=' + ("'" + str(defaults[x]) + "'" if defaults[x] != None else 'None') for x in optional_params
  ])
  params_str = ", ".join(params_str_list)


  fill_str = "".join(["        self.params['%s'] = %s\n" % (x, x) for x in mandatory_params]) + \
             "".join(["        if %s: self.params['%s'] = %s\n" % (x, x, x) for x in optional_params])

  result = template % (record['name'], params_str, record['description'], endpointfromuri(record['uri']), fill_str, record['http_method'].lower())

  if (('limit' in params) or ('page' in params) or ('offset' in params)):
    result += '\n' + gen_ext_method(mandatory_params, optional_params, defaults)

  return result


for record in e.getMethodTable()['results']:
  print gen_method(record)

