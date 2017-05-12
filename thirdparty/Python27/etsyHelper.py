from etsy import Etsy
e = Etsy('9avabtnm6p26odme939o3o8y', '293yf9k467')
#print e.find_user('kakmedvedrbv')
#print e.findAllUserFavoriteUsers('kakmedvedrbv')
e.authorize(permissions=['favorites_rw'])
#e.get_user_info('__SELF__')