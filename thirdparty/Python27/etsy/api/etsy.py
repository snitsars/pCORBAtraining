import urllib
from urlparse import unquote, parse_qs
import json
import logging
import requests
#from oauth_hook import OAuthHook
from requests_oauthlib import OAuth1Session
import webbrowser

log = logging.getLogger(__name__)

class Etsy(object):
    """
    Represents the etsy API
    """
    url_base = "https://openapi.etsy.com/v2"
    
    class EtsyError(Exception):
        pass
    
    def __init__(self, storage, consumer_key, consumer_secret, permissions):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.storage = storage
        self.oauth_token = self.storage.get('oauth_token', self.consumer_key)
        self.oauth_token_secret = self.storage.get('oauth_token_secret', self.consumer_key)

        if not self.oauth_token or not self.oauth_token_secret:
          (self.oauth_token, self.oauth_token_secret) = self.authorize(permissions)
          self.storage.put('oauth_token', self.consumer_key, self.oauth_token)
          self.storage.put('oauth_token_secret', self.consumer_key, self.oauth_token_secret)
          self.storage.put('permissions', self.consumer_key, " ".join(permissions))

        self.session = OAuth1Session(self.consumer_key, self.consumer_secret, self.oauth_token, self.oauth_token_secret)
        self.params = {}


    def authorize(self, permissions):
        """OAuth autorization"""

        url = self.url_base + "/oauth/request_token"

        querystring = urllib.urlencode({'scope' : " ".join(permissions)})
        if querystring:
            url = "%s?%s" % (url, querystring)
        
        session1 = OAuth1Session(self.consumer_key, self.consumer_secret)
        token = session1.fetch_request_token(url)

        webbrowser.open(token['login_url'])
        verifier = raw_input('Please type verification code here: ')

        session2 = OAuth1Session(self.consumer_key, self.consumer_secret, token['oauth_token'], token['oauth_token_secret'], verifier=verifier)
        access_token = session2.fetch_access_token(self.url_base + "/oauth/access_token")

        return (access_token['oauth_token'], access_token['oauth_token_secret'])

    
    def execute(self, endpoint, method='get', oauth=None):
        """
        Actually do the request, and raise exception if an error comes back.
        """
        querystring = urllib.urlencode(self.params)
        url = "%s%s" % (self.url_base, endpoint)
        if querystring:
            url = "%s?%s" % (url, querystring)
        
        response = getattr(self.session, method)(url)
                
        if response.status_code > 201:
            e = response.text
            code = response.status_code
            raise self.EtsyError('API returned %s response: %s' % (code, e))
        return response


    def getMethodTable(self, ):
        """Get a list of all methods available."""

        endpoint = '/'

        self.params = {}

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def getPublicBaseline(self, ):
        """Pings a public v2 uri to get a performance baseline"""

        endpoint = '/baseline'

        self.params = {}

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def getCategory(self, tag):
        """Retrieves a top-level Category by tag."""

        endpoint = '/categories/%s' % tag

        self.params = {}
        self.params['tag'] = tag

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def getSubCategory(self, subtag, tag):
        """Retrieves a second-level Category by tag and subtag."""

        endpoint = '/categories/%s/%s' % (tag, subtag)

        self.params = {}
        self.params['subtag'] = subtag
        self.params['tag'] = tag

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def getSubSubCategory(self, subtag, subsubtag, tag):
        """Retrieves a third-level Category by tag, subtag and subsubtag."""

        endpoint = '/categories/%s/%s/%s' % (tag, subtag, subsubtag)

        self.params = {}
        self.params['subtag'] = subtag
        self.params['subsubtag'] = subsubtag
        self.params['tag'] = tag

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllCountry(self, ):
        """Finds all Country."""

        endpoint = '/countries'

        self.params = {}

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def getCountry(self, country_id):
        """Retrieves a Country by id."""

        endpoint = '/countries/%s' % country_id

        self.params = {}
        self.params['country_id'] = country_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findByIsoCode(self, iso_code, limit='25', page=None, offset='0'):
        """Get the country info for the given ISO code."""

        endpoint = '/countries/iso/%s' % iso_code

        self.params = {}
        self.params['iso_code'] = iso_code
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllFeaturedTreasuries(self, region='__ALL_REGIONS__', limit='25', page=None, offset='0'):
        """Finds all FeaturedTreasuries."""

        endpoint = '/featured_treasuries'

        self.params = {}
        if region: self.params['region'] = region
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def getFeaturedTreasuryById(self, featured_treasury_id):
        """Finds FeaturedTreasury by numeric ID."""

        endpoint = '/featured_treasuries/%s' % featured_treasury_id

        self.params = {}
        self.params['featured_treasury_id'] = featured_treasury_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllListingsForFeaturedTreasuryId(self, featured_treasury_id):
        """Finds all listings for a certain FeaturedTreasury."""

        endpoint = '/featured_treasuries/%s/listings' % featured_treasury_id

        self.params = {}
        self.params['featured_treasury_id'] = featured_treasury_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllActiveListingsForFeaturedTreasuryId(self, featured_treasury_id):
        """Finds all active listings for a certain FeaturedTreasury."""

        endpoint = '/featured_treasuries/%s/listings/active' % featured_treasury_id

        self.params = {}
        self.params['featured_treasury_id'] = featured_treasury_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllFeaturedListings(self, region='__ALL_REGIONS__', limit='25', page=None, offset='0'):
        """Finds all FeaturedTreasury listings."""

        endpoint = '/featured_treasuries/listings'

        self.params = {}
        if region: self.params['region'] = region
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllCurrentFeaturedListings(self, region='US'):
        """Finds FeaturedTreasury listings that are currently displayed on a regional homepage."""

        endpoint = '/featured_treasuries/listings/homepage_current'

        self.params = {}
        if region: self.params['region'] = region

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllFeaturedTreasuriesByOwner(self, owner_id, limit='25', page=None, offset='0'):
        """Finds all FeaturedTreasury by numeric owner_id."""

        endpoint = '/featured_treasuries/owner/%s' % owner_id

        self.params = {}
        self.params['owner_id'] = owner_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def getGuest(self, guest_id):
        """Get a guest by ID."""

        endpoint = '/guests/%s' % guest_id

        self.params = {}
        self.params['guest_id'] = guest_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllGuestCarts(self, guest_id):
        """Get all guest's carts"""

        endpoint = '/guests/%s/carts' % guest_id

        self.params = {}
        self.params['guest_id'] = guest_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def addToGuestCart(self, guest_id, listing_id, selected_variations=None, quantity='1'):
        """Add a listing to guest's cart"""

        endpoint = '/guests/%s/carts' % guest_id

        self.params = {}
        self.params['guest_id'] = guest_id
        self.params['listing_id'] = listing_id
        if selected_variations: self.params['selected_variations'] = selected_variations
        if quantity: self.params['quantity'] = quantity

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def updateGuestCartListingQuantity(self, guest_id, listing_id, quantity, listing_customization_id='0'):
        """Update a guest's cart listing purchase quantity"""

        endpoint = '/guests/%s/carts' % guest_id

        self.params = {}
        self.params['guest_id'] = guest_id
        self.params['listing_id'] = listing_id
        self.params['quantity'] = quantity
        if listing_customization_id: self.params['listing_customization_id'] = listing_customization_id

        response = self.execute(endpoint, 'put')
        return json.loads(response.text)


    def removeGuestCartListing(self, guest_id, listing_id, listing_customization_id='0'):
        """Remove a listing from a guest's cart"""

        endpoint = '/guests/%s/carts' % guest_id

        self.params = {}
        self.params['guest_id'] = guest_id
        self.params['listing_id'] = listing_id
        if listing_customization_id: self.params['listing_customization_id'] = listing_customization_id

        response = self.execute(endpoint, 'delete')
        return json.loads(response.text)


    def findGuestCart(self, guest_id, cart_id):
        """Get a guest's cart"""

        endpoint = '/guests/%s/carts/%s' % (guest_id, cart_id)

        self.params = {}
        self.params['guest_id'] = guest_id
        self.params['cart_id'] = cart_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def updateGuestCart(self, guest_id, cart_id, destination_zip=None, shipping_option_id=None, message_to_seller=None, coupon_code=None, destination_country_id=None):
        """Update a guest's cart"""

        endpoint = '/guests/%s/carts/%s' % (guest_id, cart_id)

        self.params = {}
        self.params['guest_id'] = guest_id
        self.params['cart_id'] = cart_id
        if destination_zip: self.params['destination_zip'] = destination_zip
        if shipping_option_id: self.params['shipping_option_id'] = shipping_option_id
        if message_to_seller: self.params['message_to_seller'] = message_to_seller
        if coupon_code: self.params['coupon_code'] = coupon_code
        if destination_country_id: self.params['destination_country_id'] = destination_country_id

        response = self.execute(endpoint, 'put')
        return json.loads(response.text)


    def deleteGuestCart(self, guest_id, cart_id):
        """Delete a guest's cart"""

        endpoint = '/guests/%s/carts/%s' % (guest_id, cart_id)

        self.params = {}
        self.params['guest_id'] = guest_id
        self.params['cart_id'] = cart_id

        response = self.execute(endpoint, 'delete')
        return json.loads(response.text)


    def claimGuest(self, guest_id):
        """Claim this guest to the associated user. Merges the GuestCart's associated with this GuestId into the logged in User's Carts. Returns the number of listings merged in meta['listings_merged']."""

        endpoint = '/guests/%s/claim' % guest_id

        self.params = {}
        self.params['guest_id'] = guest_id

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def mergeGuest(self, guest_id, target_guest_id):
        """Merge this guest to a different guest. Merges the GuestCart's associated with this GuestId into the target guest's cart. Returns the number of listings merged in meta['listings_merged']."""

        endpoint = '/guests/%s/merge' % guest_id

        self.params = {}
        self.params['guest_id'] = guest_id
        self.params['target_guest_id'] = target_guest_id

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def generateGuest(self, ):
        """A helper method that generates a Guest ID to associate to this anonymous session. This method is not strictly necessary, as any sufficiently random guest ID that is 13 characters in length will suffice and automatically create a guest account on use if it does not yet exist."""

        endpoint = '/guests/generator'

        self.params = {}

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def listImageTypes(self, ):
        """Lists available image types along with their supported sizes."""

        endpoint = '/image_types'

        self.params = {}

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def createListing(self, title, description, price, who_made, is_supply, when_made, quantity, image=None, taxonomy_id=None, shop_section_id=None, style=None, processing_min=None, processing_max=None, image_ids=None, state='active', is_customizable=None, tags=None, recipient=None, non_taxable=None, materials=None, shipping_template_id=None, occasion=None, category_id=None):
        """Creates a new Listing. NOTE: A shipping_template_id is required when creating a listing. <strong>NOTE: All listings created on www.etsy.com must be actual items for sale. Please see our <a href='/developers/documentation/getting_started/testing'>guidelines for testing</a> with live listings.</strong>"""

        endpoint = '/listings'

        self.params = {}
        self.params['title'] = title
        self.params['description'] = description
        self.params['price'] = price
        self.params['who_made'] = who_made
        self.params['is_supply'] = is_supply
        self.params['when_made'] = when_made
        self.params['quantity'] = quantity
        if image: self.params['image'] = image
        if taxonomy_id: self.params['taxonomy_id'] = taxonomy_id
        if shop_section_id: self.params['shop_section_id'] = shop_section_id
        if style: self.params['style'] = style
        if processing_min: self.params['processing_min'] = processing_min
        if processing_max: self.params['processing_max'] = processing_max
        if image_ids: self.params['image_ids'] = image_ids
        if state: self.params['state'] = state
        if is_customizable: self.params['is_customizable'] = is_customizable
        if tags: self.params['tags'] = tags
        if recipient: self.params['recipient'] = recipient
        if non_taxable: self.params['non_taxable'] = non_taxable
        if materials: self.params['materials'] = materials
        if shipping_template_id: self.params['shipping_template_id'] = shipping_template_id
        if occasion: self.params['occasion'] = occasion
        if category_id: self.params['category_id'] = category_id

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def getListing(self, listing_id):
        """Retrieves a Listing by id."""

        endpoint = '/listings/%s' % listing_id

        self.params = {}
        self.params['listing_id'] = listing_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def updateListing(self, listing_id, featured_rank=None, wholesale_price=None, taxonomy_id=None, shop_section_id=None, processing_min=None, title=None, processing_max=None, image_ids=None, state='active', item_length=None, is_customizable=None, item_height=None, description=None, tags=None, price=None, item_weight=None, style=None, who_made=None, recipient=None, non_taxable=None, is_supply=None, item_weight_unit=None, when_made=None, renew=None, materials=None, item_dimensions_unit=None, shipping_template_id=None, occasion=None, category_id=None, item_width=None, quantity=None):
        """Updates a Listing"""

        endpoint = '/listings/%s' % listing_id

        self.params = {}
        self.params['listing_id'] = listing_id
        if featured_rank: self.params['featured_rank'] = featured_rank
        if wholesale_price: self.params['wholesale_price'] = wholesale_price
        if taxonomy_id: self.params['taxonomy_id'] = taxonomy_id
        if shop_section_id: self.params['shop_section_id'] = shop_section_id
        if processing_min: self.params['processing_min'] = processing_min
        if title: self.params['title'] = title
        if processing_max: self.params['processing_max'] = processing_max
        if image_ids: self.params['image_ids'] = image_ids
        if state: self.params['state'] = state
        if item_length: self.params['item_length'] = item_length
        if is_customizable: self.params['is_customizable'] = is_customizable
        if item_height: self.params['item_height'] = item_height
        if description: self.params['description'] = description
        if tags: self.params['tags'] = tags
        if price: self.params['price'] = price
        if item_weight: self.params['item_weight'] = item_weight
        if style: self.params['style'] = style
        if who_made: self.params['who_made'] = who_made
        if recipient: self.params['recipient'] = recipient
        if non_taxable: self.params['non_taxable'] = non_taxable
        if is_supply: self.params['is_supply'] = is_supply
        if item_weight_unit: self.params['item_weight_unit'] = item_weight_unit
        if when_made: self.params['when_made'] = when_made
        if renew: self.params['renew'] = renew
        if materials: self.params['materials'] = materials
        if item_dimensions_unit: self.params['item_dimensions_unit'] = item_dimensions_unit
        if shipping_template_id: self.params['shipping_template_id'] = shipping_template_id
        if occasion: self.params['occasion'] = occasion
        if category_id: self.params['category_id'] = category_id
        if item_width: self.params['item_width'] = item_width
        if quantity: self.params['quantity'] = quantity

        response = self.execute(endpoint, 'put')
        return json.loads(response.text)


    def deleteListing(self, listing_id):
        """Deletes a Listing"""

        endpoint = '/listings/%s' % listing_id

        self.params = {}
        self.params['listing_id'] = listing_id

        response = self.execute(endpoint, 'delete')
        return json.loads(response.text)


    def findAllListingFavoredBy(self, listing_id, limit='25', page=None, offset='0'):
        """Retrieves a set of FavoriteListing objects associated to a Listing."""

        endpoint = '/listings/%s/favored-by' % listing_id

        self.params = {}
        self.params['listing_id'] = listing_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllListingFiles(self, listing_id):
        """Finds all ListingFiles on a Listing"""

        endpoint = '/listings/%s/files' % listing_id

        self.params = {}
        self.params['listing_id'] = listing_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def uploadListingFile(self, listing_id, rank='1', listing_file_id=None, name=None, file=None):
        """Upload a new listing file, or attach an existing file to this listing.  You must either provide the listing_file_id
of an existing listing file, or the name and file data of a new file that you are uploading.  If you are attaching
a file to a listing that is currently not digital, the listing will be converted to a digital listing.  This will
cause the listing to have free shipping and will remove any variations."""

        endpoint = '/listings/%s/files' % listing_id

        self.params = {}
        self.params['listing_id'] = listing_id
        if rank: self.params['rank'] = rank
        if listing_file_id: self.params['listing_file_id'] = listing_file_id
        if name: self.params['name'] = name
        if file: self.params['file'] = file

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def findListingFile(self, listing_id, listing_file_id):
        """Finds a ListingFile by ID"""

        endpoint = '/listings/%s/files/%s' % (listing_id, listing_file_id)

        self.params = {}
        self.params['listing_id'] = listing_id
        self.params['listing_file_id'] = listing_file_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def deleteListingFile(self, listing_id, listing_file_id):
        """Removes the listing file from this listing.  If this is the last file on a listing, the listing will no longer
be considered a digital listing."""

        endpoint = '/listings/%s/files/%s' % (listing_id, listing_file_id)

        self.params = {}
        self.params['listing_id'] = listing_id
        self.params['listing_file_id'] = listing_file_id

        response = self.execute(endpoint, 'delete')
        return json.loads(response.text)


    def findAllListingFundOnEtsyCampaign(self, listing_id):
        """Retrieves a set of FundOnEtsyCampaign objects associated to a Listing."""

        endpoint = '/listings/%s/fundonetsycampaign' % listing_id

        self.params = {}
        self.params['listing_id'] = listing_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllListingImages(self, listing_id):
        """Retrieves a set of ListingImage objects associated to a Listing."""

        endpoint = '/listings/%s/images' % listing_id

        self.params = {}
        self.params['listing_id'] = listing_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def uploadListingImage(self, listing_id, is_watermarked='0', image=None, rank='1', overwrite='0', listing_image_id=None):
        """Upload a new listing image, or re-associate a previously deleted one. You may associate an image
                                      to any listing within the same shop that the image's original listing belongs to.
                                      You MUST pass either a listing_image_id OR an image to this method.
                                      Passing a listing_image_id serves to re-associate an image that was previously deleted.
                                      If you wish to re-associate an image, we strongly recommend using the listing_image_id
                                      argument as opposed to re-uploading a new image each time, to save bandwidth for you as well as us.
                                      Pass overwrite=1 to replace the existing image at a given rank.
                                      When uploading a new listing image with a watermark, pass is_watermarked=1; existing listing images
                                      will not be affected by this parameter."""

        endpoint = '/listings/%s/images' % listing_id

        self.params = {}
        self.params['listing_id'] = listing_id
        if is_watermarked: self.params['is_watermarked'] = is_watermarked
        if image: self.params['image'] = image
        if rank: self.params['rank'] = rank
        if overwrite: self.params['overwrite'] = overwrite
        if listing_image_id: self.params['listing_image_id'] = listing_image_id

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def getImage_Listing(self, listing_id, listing_image_id):
        """Retrieves a Image_Listing by id."""

        endpoint = '/listings/%s/images/%s' % (listing_id, listing_image_id)

        self.params = {}
        self.params['listing_id'] = listing_id
        self.params['listing_image_id'] = listing_image_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def deleteListingImage(self, listing_id, listing_image_id):
        """Deletes a listing image. A copy of the file remains on our servers,
                                       and so a deleted image may be re-associated with the listing without
                                       re-uploading the original image; see uploadListingImage"""

        endpoint = '/listings/%s/images/%s' % (listing_id, listing_image_id)

        self.params = {}
        self.params['listing_id'] = listing_id
        self.params['listing_image_id'] = listing_image_id

        response = self.execute(endpoint, 'delete')
        return json.loads(response.text)


    def findAllListingShippingProfileEntries(self, ):
        """Retrieves a set of ShippingProfileEntries objects associated to a Listing."""

        endpoint = '/listings/%s/shipping/info' % listing_id

        self.params = {}

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def createShippingInfo(self, primary_cost, secondary_cost, listing_id, destination_country_id=None, region_id=None):
        """Creates a new ShippingInfo."""

        endpoint = '/listings/%s/shipping/info' % listing_id

        self.params = {}
        self.params['primary_cost'] = primary_cost
        self.params['secondary_cost'] = secondary_cost
        self.params['listing_id'] = listing_id
        if destination_country_id: self.params['destination_country_id'] = destination_country_id
        if region_id: self.params['region_id'] = region_id

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def getListingShippingUpgrades(self, listing_id):
        """Get the shipping upgrades available for a listing."""

        endpoint = '/listings/%s/shipping/upgrades' % listing_id

        self.params = {}
        self.params['listing_id'] = listing_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def createListingShippingUpgrade(self, listing_id, type, price, value, secondary_price):
        """Creates a new ShippingUpgrade for the listing. Will unlink the listing if linked to a ShippingTemplate."""

        endpoint = '/listings/%s/shipping/upgrades' % listing_id

        self.params = {}
        self.params['listing_id'] = listing_id
        self.params['type'] = type
        self.params['price'] = price
        self.params['value'] = value
        self.params['secondary_price'] = secondary_price

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def updateListingShippingUpgrade(self, price, listing_id, type, value_id, secondary_price):
        """Updates a ShippingUpgrade on a listing. Will unlink the listing if linked to a ShippingTemplate."""

        endpoint = '/listings/%s/shipping/upgrades' % listing_id

        self.params = {}
        self.params['price'] = price
        self.params['listing_id'] = listing_id
        self.params['type'] = type
        self.params['value_id'] = value_id
        self.params['secondary_price'] = secondary_price

        response = self.execute(endpoint, 'put')
        return json.loads(response.text)


    def deleteListingShippingUpgrade(self, listing_id, type, value_id):
        """Deletes the ShippingUpgrade from the listing. Will unlink the listing if linked to a ShippingTemplate."""

        endpoint = '/listings/%s/shipping/upgrades' % listing_id

        self.params = {}
        self.params['listing_id'] = listing_id
        self.params['type'] = type
        self.params['value_id'] = value_id

        response = self.execute(endpoint, 'delete')
        return json.loads(response.text)


    def findAllListingTransactions(self, listing_id, limit='25', page=None, offset='0'):
        """Retrieves a set of Transaction objects associated to a Listing."""

        endpoint = '/listings/%s/transactions' % listing_id

        self.params = {}
        self.params['listing_id'] = listing_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def getListingTranslation(self, listing_id, language):
        """Retrieves a ListingTranslation by listing_id and language"""

        endpoint = '/listings/%s/translations/%s' % (listing_id, language)

        self.params = {}
        self.params['listing_id'] = listing_id
        self.params['language'] = language

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def createListingTranslation(self, listing_id, language, tags='False', description='False', title='False'):
        """Creates a ListingTranslation by listing_id and language"""

        endpoint = '/listings/%s/translations/%s' % (listing_id, language)

        self.params = {}
        self.params['listing_id'] = listing_id
        self.params['language'] = language
        if tags: self.params['tags'] = tags
        if description: self.params['description'] = description
        if title: self.params['title'] = title

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def updateListingTranslation(self, listing_id, language, tags='False', description='False', title='False'):
        """Updates a ListingTranslation by listing_id and language"""

        endpoint = '/listings/%s/translations/%s' % (listing_id, language)

        self.params = {}
        self.params['listing_id'] = listing_id
        self.params['language'] = language
        if tags: self.params['tags'] = tags
        if description: self.params['description'] = description
        if title: self.params['title'] = title

        response = self.execute(endpoint, 'put')
        return json.loads(response.text)


    def deleteListingTranslation(self, listing_id, language):
        """Deletes a ListingTranslation by listing_id and language"""

        endpoint = '/listings/%s/translations/%s' % (listing_id, language)

        self.params = {}
        self.params['listing_id'] = listing_id
        self.params['language'] = language

        response = self.execute(endpoint, 'delete')
        return json.loads(response.text)


    def getListingVariations(self, listing_id):
        """Get the listing variations available for a listing."""

        endpoint = '/listings/%s/variations' % listing_id

        self.params = {}
        self.params['listing_id'] = listing_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def createListingVariations(self, listing_id, variations, sizing_scale=None, dimensions_scale=None, length_scale=None, weight_scale=None, custom_property_names=None, width_scale=None, recipient_id=None, diameter_scale=None, height_scale=None):
        """Update all of the listing variations available for a listing; optionally set custom property names and property qualifiers. Expects a JSON array with a collection of objects of the form: <code>[{"property_id":200, "value":"Black"}, {"property_id":200, "value":"White"}]</code>"""

        endpoint = '/listings/%s/variations' % listing_id

        self.params = {}
        self.params['listing_id'] = listing_id
        self.params['variations'] = variations
        if sizing_scale: self.params['sizing_scale'] = sizing_scale
        if dimensions_scale: self.params['dimensions_scale'] = dimensions_scale
        if length_scale: self.params['length_scale'] = length_scale
        if weight_scale: self.params['weight_scale'] = weight_scale
        if custom_property_names: self.params['custom_property_names'] = custom_property_names
        if width_scale: self.params['width_scale'] = width_scale
        if recipient_id: self.params['recipient_id'] = recipient_id
        if diameter_scale: self.params['diameter_scale'] = diameter_scale
        if height_scale: self.params['height_scale'] = height_scale

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def updateListingVariations(self, listing_id, variations, sizing_scale=None, dimensions_scale=None, length_scale=None, weight_scale=None, custom_property_names=None, width_scale=None, recipient_id=None, diameter_scale=None, height_scale=None):
        """Update all of the listing variations available for a listing. Expects a JSON array with a collection of objects of the form: <code>[{"property_id":200, "value":"Black"}, {"property_id":200, "value":"White"}]</code>"""

        endpoint = '/listings/%s/variations' % listing_id

        self.params = {}
        self.params['listing_id'] = listing_id
        self.params['variations'] = variations
        if sizing_scale: self.params['sizing_scale'] = sizing_scale
        if dimensions_scale: self.params['dimensions_scale'] = dimensions_scale
        if length_scale: self.params['length_scale'] = length_scale
        if weight_scale: self.params['weight_scale'] = weight_scale
        if custom_property_names: self.params['custom_property_names'] = custom_property_names
        if width_scale: self.params['width_scale'] = width_scale
        if recipient_id: self.params['recipient_id'] = recipient_id
        if diameter_scale: self.params['diameter_scale'] = diameter_scale
        if height_scale: self.params['height_scale'] = height_scale

        response = self.execute(endpoint, 'put')
        return json.loads(response.text)


    def createListingVariation(self, listing_id, value, property_id, price=None, is_available='True'):
        """Add a new listing variation for a listing."""

        endpoint = '/listings/%s/variations/%s' % (listing_id, property_id)

        self.params = {}
        self.params['listing_id'] = listing_id
        self.params['value'] = value
        self.params['property_id'] = property_id
        if price: self.params['price'] = price
        if is_available: self.params['is_available'] = is_available

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def updateListingVariation(self, listing_id, is_available, value, property_id, price=None):
        """Update a listing variation for a listing."""

        endpoint = '/listings/%s/variations/%s' % (listing_id, property_id)

        self.params = {}
        self.params['listing_id'] = listing_id
        self.params['is_available'] = is_available
        self.params['value'] = value
        self.params['property_id'] = property_id
        if price: self.params['price'] = price

        response = self.execute(endpoint, 'put')
        return json.loads(response.text)


    def deleteListingVariation(self, listing_id, value, property_id):
        """Remove a listing variation for a listing."""

        endpoint = '/listings/%s/variations/%s' % (listing_id, property_id)

        self.params = {}
        self.params['listing_id'] = listing_id
        self.params['value'] = value
        self.params['property_id'] = property_id

        response = self.execute(endpoint, 'delete')
        return json.loads(response.text)


    def findAllListingActive(self, category=None, min_price=None, lat=None, translate_keywords='false', accepts_gift_cards='false', tags=None, color=None, region=None, sort_on='created', lon=None, max_price=None, color_accuracy='0', sort_order='down', limit='25', location=None, offset='0', keywords=None, page=None, geo_level='city'):
        """Finds all active Listings. (Note: the sort_on and sort_order options only work when combined with one of the search options: keywords, color, tags, location, etc.)"""

        endpoint = '/listings/active'

        self.params = {}
        if category: self.params['category'] = category
        if min_price: self.params['min_price'] = min_price
        if lat: self.params['lat'] = lat
        if translate_keywords: self.params['translate_keywords'] = translate_keywords
        if accepts_gift_cards: self.params['accepts_gift_cards'] = accepts_gift_cards
        if tags: self.params['tags'] = tags
        if color: self.params['color'] = color
        if region: self.params['region'] = region
        if sort_on: self.params['sort_on'] = sort_on
        if lon: self.params['lon'] = lon
        if max_price: self.params['max_price'] = max_price
        if color_accuracy: self.params['color_accuracy'] = color_accuracy
        if sort_order: self.params['sort_order'] = sort_order
        if limit: self.params['limit'] = limit
        if location: self.params['location'] = location
        if offset: self.params['offset'] = offset
        if keywords: self.params['keywords'] = keywords
        if page: self.params['page'] = page
        if geo_level: self.params['geo_level'] = geo_level

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def getInterestingListings(self, limit='25', page=None, offset='0'):
        """Collects the list of interesting listings"""

        endpoint = '/listings/interesting'

        self.params = {}
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def getTrendingListings(self, limit='25', page=None, offset='0'):
        """Collects the list of listings used to generate the trending listing page"""

        endpoint = '/listings/trending'

        self.params = {}
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def pagesSignup(self, email, title, brand_url, brand_name, name):
        """Sign up for Pages"""

        endpoint = '/pages-signup'

        self.params = {}
        self.params['email'] = email
        self.params['title'] = title
        self.params['brand_url'] = brand_url
        self.params['brand_name'] = brand_name
        self.params['name'] = name

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def findPage(self, page_id):
        """Find a single page."""

        endpoint = '/pages/%s' % page_id

        self.params = {}
        self.params['page_id'] = page_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def updatePageData(self, page_id, link=None, page_name=None, byline=None, avatar=None):
        """Update a Page's data."""

        endpoint = '/pages/%s' % page_id

        self.params = {}
        self.params['page_id'] = page_id
        if link: self.params['link'] = link
        if page_name: self.params['page_name'] = page_name
        if byline: self.params['byline'] = byline
        if avatar: self.params['avatar'] = avatar

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def uploadAvatar(self, page_id, avatar):
        """Upload a new avatar"""

        endpoint = '/pages/%s/avatar' % page_id

        self.params = {}
        self.params['page_id'] = page_id
        self.params['avatar'] = avatar

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def findAllPageCollections(self, page_id, limit='25', page=None, offset='0'):
        """See all of a page's public collections."""

        endpoint = '/pages/%s/collections' % page_id

        self.params = {}
        self.params['page_id'] = page_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def createPageCollection(self, page_id, name, privacy_level='public'):
        """Create a page collection for the given page."""

        endpoint = '/pages/%s/collections' % page_id

        self.params = {}
        self.params['page_id'] = page_id
        self.params['name'] = name
        if privacy_level: self.params['privacy_level'] = privacy_level

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def getPageCollection(self, collection_id, page_id):
        """Retrieve a single page collection."""

        endpoint = '/pages/%s/collections/%s' % (page_id, collection_id)

        self.params = {}
        self.params['collection_id'] = collection_id
        self.params['page_id'] = page_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def updatePageCollection(self, collection_id, page_id, privacy_level='public', name=None):
        """Update a page collection."""

        endpoint = '/pages/%s/collections/%s' % (page_id, collection_id)

        self.params = {}
        self.params['collection_id'] = collection_id
        self.params['page_id'] = page_id
        if privacy_level: self.params['privacy_level'] = privacy_level
        if name: self.params['name'] = name

        response = self.execute(endpoint, 'put')
        return json.loads(response.text)


    def deletePageCollection(self, collection_id, page_id):
        """Delete a page collection."""

        endpoint = '/pages/%s/collections/%s' % (page_id, collection_id)

        self.params = {}
        self.params['collection_id'] = collection_id
        self.params['page_id'] = page_id

        response = self.execute(endpoint, 'delete')
        return json.loads(response.text)


    def getCollectionListings(self, page_id, collection_id, limit='25', page=None, offset='0'):
        """Retrieve the listings for a single page collection."""

        endpoint = '/pages/%s/collections/%s/listings' % (page_id, collection_id)

        self.params = {}
        self.params['page_id'] = page_id
        self.params['collection_id'] = collection_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def addListingToCollection(self, collection_id, listing_id, page_id):
        """Add a listing to a page collection"""

        endpoint = '/pages/%s/collections/%s/listings/%s' % (page_id, collection_id, listing_id)

        self.params = {}
        self.params['collection_id'] = collection_id
        self.params['listing_id'] = listing_id
        self.params['page_id'] = page_id

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def removeListingFromCollection(self, collection_id, listing_id, page_id):
        """Remove a listing from a collection"""

        endpoint = '/pages/%s/collections/%s/listings/%s' % (page_id, collection_id, listing_id)

        self.params = {}
        self.params['collection_id'] = collection_id
        self.params['listing_id'] = listing_id
        self.params['page_id'] = page_id

        response = self.execute(endpoint, 'delete')
        return json.loads(response.text)


    def findPageCollectionsForListings(self, listing_ids, page_id):
        """Find the collection ids for the authorized page and listing ids"""

        endpoint = '/pages/%s/collections/listings_map' % page_id

        self.params = {}
        self.params['listing_ids'] = listing_ids
        self.params['page_id'] = page_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def addCurator(self, curator_id, page_id):
        """Add a user as curator for a page."""

        endpoint = '/pages/%s/curators/%s' % (page_id, curator_id)

        self.params = {}
        self.params['curator_id'] = curator_id
        self.params['page_id'] = page_id

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def removeCurator(self, curator_id, page_id):
        """Remove a user from curating page."""

        endpoint = '/pages/%s/curators/%s' % (page_id, curator_id)

        self.params = {}
        self.params['curator_id'] = curator_id
        self.params['page_id'] = page_id

        response = self.execute(endpoint, 'delete')
        return json.loads(response.text)


    def curatorPeopleSearch(self, query):
        """Search for people to add as curators."""

        endpoint = '/pages/find-curators'

        self.params = {}
        self.params['query'] = query

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findPayment(self, payment_id):
        """Get a Direct Checkout Payment"""

        endpoint = '/payments/%s' % payment_id

        self.params = {}
        self.params['payment_id'] = payment_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findPaymentAdjustments(self, payment_id, limit='25', page=None, offset='0'):
        """Get a Payment Adjustments from a Payment Id"""

        endpoint = '/payments/%s/adjustments' % payment_id

        self.params = {}
        self.params['payment_id'] = payment_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findPaymentAdjustment(self, payment_id, payment_adjustment_id):
        """Get a Direct Checkout Payment Adjustment"""

        endpoint = '/payments/%s/adjustments/%s' % (payment_id, payment_adjustment_id)

        self.params = {}
        self.params['payment_id'] = payment_id
        self.params['payment_adjustment_id'] = payment_adjustment_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findPaymentAdjustmentItem(self, payment_id, payment_adjustment_id, page=None, limit='25', offset='0'):
        """Get Direct Checkout Payment Adjustment Items"""

        endpoint = '/payments/%s/adjustments/%s/items' % (payment_id, payment_adjustment_id)

        self.params = {}
        self.params['payment_id'] = payment_id
        self.params['payment_adjustment_id'] = payment_adjustment_id
        if page: self.params['page'] = page
        if limit: self.params['limit'] = limit
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findPaymentAdjustmentItem(self, payment_id, payment_adjustment_item_id, payment_adjustment_id):
        """Get a Direct Checkout Payment Adjustment Item"""

        endpoint = '/payments/%s/adjustments/%s/items/%s' % (payment_id, payment_adjustment_id, payment_adjustment_item_id)

        self.params = {}
        self.params['payment_id'] = payment_id
        self.params['payment_adjustment_item_id'] = payment_adjustment_item_id
        self.params['payment_adjustment_id'] = payment_adjustment_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def getPrivateBaseline(self, ):
        """Pings a private v2 uri to get a performance baseline"""

        endpoint = '/private-baseline'

        self.params = {}

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def getPropertyOptionModifier(self, property_id, sizing_scale=None, length_scale=None, dimensions_scale=None, weight_scale=None, recipient_id=None, width_scale=None, category_id=None, diameter_scale=None, height_scale=None):
        """Add a value for a given property."""

        endpoint = '/property_options/modifiers'

        self.params = {}
        self.params['property_id'] = property_id
        if sizing_scale: self.params['sizing_scale'] = sizing_scale
        if length_scale: self.params['length_scale'] = length_scale
        if dimensions_scale: self.params['dimensions_scale'] = dimensions_scale
        if weight_scale: self.params['weight_scale'] = weight_scale
        if recipient_id: self.params['recipient_id'] = recipient_id
        if width_scale: self.params['width_scale'] = width_scale
        if category_id: self.params['category_id'] = category_id
        if diameter_scale: self.params['diameter_scale'] = diameter_scale
        if height_scale: self.params['height_scale'] = height_scale

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllSuggestedPropertyOptions(self, property_id, sizing_scale=None, length_scale=None, dimensions_scale=None, weight_scale=None, recipient_id=None, width_scale=None, category_id=None, diameter_scale=None, height_scale=None):
        """Finds all suggested property options for a given property."""

        endpoint = '/property_options/suggested'

        self.params = {}
        self.params['property_id'] = property_id
        if sizing_scale: self.params['sizing_scale'] = sizing_scale
        if length_scale: self.params['length_scale'] = length_scale
        if dimensions_scale: self.params['dimensions_scale'] = dimensions_scale
        if weight_scale: self.params['weight_scale'] = weight_scale
        if recipient_id: self.params['recipient_id'] = recipient_id
        if width_scale: self.params['width_scale'] = width_scale
        if category_id: self.params['category_id'] = category_id
        if diameter_scale: self.params['diameter_scale'] = diameter_scale
        if height_scale: self.params['height_scale'] = height_scale

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findPropertySet(self, taxonomy_id=None, recipient_id=None, category_id=None):
        """Find the property set for the category id"""

        endpoint = '/property_sets'

        self.params = {}
        if taxonomy_id: self.params['taxonomy_id'] = taxonomy_id
        if recipient_id: self.params['recipient_id'] = recipient_id
        if category_id: self.params['category_id'] = category_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def getReceipt(self, receipt_id):
        """Retrieves a Receipt by id."""

        endpoint = '/receipts/%s' % receipt_id

        self.params = {}
        self.params['receipt_id'] = receipt_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def updateReceipt(self, receipt_id, was_shipped=None, was_paid=None):
        """Updates a Receipt"""

        endpoint = '/receipts/%s' % receipt_id

        self.params = {}
        self.params['receipt_id'] = receipt_id
        if was_shipped: self.params['was_shipped'] = was_shipped
        if was_paid: self.params['was_paid'] = was_paid

        response = self.execute(endpoint, 'put')
        return json.loads(response.text)


    def findAllReceiptListings(self, receipt_id, limit='25', page=None, offset='0'):
        """Finds all listings in a receipt"""

        endpoint = '/receipts/%s/listings' % receipt_id

        self.params = {}
        self.params['receipt_id'] = receipt_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllReceiptTransactions(self, receipt_id, limit='25', page=None, offset='0'):
        """Retrieves a set of Transaction objects associated to a Receipt."""

        endpoint = '/receipts/%s/transactions' % receipt_id

        self.params = {}
        self.params['receipt_id'] = receipt_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllRegion(self, ):
        """Finds all Region."""

        endpoint = '/regions'

        self.params = {}

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def getRegion(self, region_id):
        """Retrieves a Region by id."""

        endpoint = '/regions/%s' % region_id

        self.params = {}
        self.params['region_id'] = region_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findEligibleRegions(self, ):
        """"""

        endpoint = '/regions/eligible'

        self.params = {}

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findBrowseSegments(self, path='', region='US'):
        """Find all Browse Segments"""

        endpoint = '/segments'

        self.params = {}
        if path: self.params['path'] = path
        if region: self.params['region'] = region

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findBrowseSegmentListings(self, path, min_price=None, lat=None, accepts_gift_cards='false', sort_on='created', lon=None, max_price=None, ship_to=None, sort_order='down', limit='25', location=None, offset='0', keywords=None, page=None, geo_level='city'):
        """Find Listings for a Segment by Segment path. NOTE: Offset must be an integer multiple of limit."""

        endpoint = '/segments/listings'

        self.params = {}
        self.params['path'] = path
        if min_price: self.params['min_price'] = min_price
        if lat: self.params['lat'] = lat
        if accepts_gift_cards: self.params['accepts_gift_cards'] = accepts_gift_cards
        if sort_on: self.params['sort_on'] = sort_on
        if lon: self.params['lon'] = lon
        if max_price: self.params['max_price'] = max_price
        if ship_to: self.params['ship_to'] = ship_to
        if sort_order: self.params['sort_order'] = sort_order
        if limit: self.params['limit'] = limit
        if location: self.params['location'] = location
        if offset: self.params['offset'] = offset
        if keywords: self.params['keywords'] = keywords
        if page: self.params['page'] = page
        if geo_level: self.params['geo_level'] = geo_level

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findBrowseSegmentPosters(self, path=''):
        """Find Browse SegmentPosters by Segment slug"""

        endpoint = '/segments/posters'

        self.params = {}
        if path: self.params['path'] = path

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def getServerEpoch(self, ):
        """Get server time, in epoch seconds notation."""

        endpoint = '/server/epoch'

        self.params = {}

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def ping(self, ):
        """Check that the server is alive."""

        endpoint = '/server/ping'

        self.params = {}

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def getShippingCosts(self, origin_postal_code, destination_postal_code, shipping_provider_id, mail_class, weight, destination_country_id, origin_country_id, weight_units='oz', ships_on_date='0', package_type='parcel', height=None, signature_confirmation=None, width=None, length=None, origin_state=None, destination_state=None, insurance_value='0', dimension_units='in'):
        """Returns postage costs for the shipping carrier based on the supplied package"""

        endpoint = '/shipping/%s/postage-costs' % shipping_provider_id

        self.params = {}
        self.params['origin_postal_code'] = origin_postal_code
        self.params['destination_postal_code'] = destination_postal_code
        self.params['shipping_provider_id'] = shipping_provider_id
        self.params['mail_class'] = mail_class
        self.params['weight'] = weight
        self.params['destination_country_id'] = destination_country_id
        self.params['origin_country_id'] = origin_country_id
        if weight_units: self.params['weight_units'] = weight_units
        if ships_on_date: self.params['ships_on_date'] = ships_on_date
        if package_type: self.params['package_type'] = package_type
        if height: self.params['height'] = height
        if signature_confirmation: self.params['signature_confirmation'] = signature_confirmation
        if width: self.params['width'] = width
        if length: self.params['length'] = length
        if origin_state: self.params['origin_state'] = origin_state
        if destination_state: self.params['destination_state'] = destination_state
        if insurance_value: self.params['insurance_value'] = insurance_value
        if dimension_units: self.params['dimension_units'] = dimension_units

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def getShippingInfo(self, shipping_info_id):
        """Retrieves a ShippingInfo by id."""

        endpoint = '/shipping/info/%s' % shipping_info_id

        self.params = {}
        self.params['shipping_info_id'] = shipping_info_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def updateShippingInfo(self, shipping_info_id, listing_id=None, destination_country_id=None, secondary_cost=None, region_id=None, primary_cost=None):
        """Updates a ShippingInfo with the given id."""

        endpoint = '/shipping/info/%s' % shipping_info_id

        self.params = {}
        self.params['shipping_info_id'] = shipping_info_id
        if listing_id: self.params['listing_id'] = listing_id
        if destination_country_id: self.params['destination_country_id'] = destination_country_id
        if secondary_cost: self.params['secondary_cost'] = secondary_cost
        if region_id: self.params['region_id'] = region_id
        if primary_cost: self.params['primary_cost'] = primary_cost

        response = self.execute(endpoint, 'put')
        return json.loads(response.text)


    def deleteShippingInfo(self, shipping_info_id):
        """Deletes the ShippingInfo with the given id."""

        endpoint = '/shipping/info/%s' % shipping_info_id

        self.params = {}
        self.params['shipping_info_id'] = shipping_info_id

        response = self.execute(endpoint, 'delete')
        return json.loads(response.text)


    def getPostageRates(self, origin_postal_code, shipping_provider_id, weight, destination_country_id, origin_country_id, weight_units='oz', ships_on_date='0', destination_postal_code=None, height=None, width=None, length=None, destination_state=None, dimension_units='in'):
        """Returns postage costs for all mail classes for a shipping carrier based on the supplied package"""

        endpoint = '/shipping/providers/%s/mail-class-rates' % shipping_provider_id

        self.params = {}
        self.params['origin_postal_code'] = origin_postal_code
        self.params['shipping_provider_id'] = shipping_provider_id
        self.params['weight'] = weight
        self.params['destination_country_id'] = destination_country_id
        self.params['origin_country_id'] = origin_country_id
        if weight_units: self.params['weight_units'] = weight_units
        if ships_on_date: self.params['ships_on_date'] = ships_on_date
        if destination_postal_code: self.params['destination_postal_code'] = destination_postal_code
        if height: self.params['height'] = height
        if width: self.params['width'] = width
        if length: self.params['length'] = length
        if destination_state: self.params['destination_state'] = destination_state
        if dimension_units: self.params['dimension_units'] = dimension_units

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def createShippingTemplate(self, primary_cost, title, origin_country_id, secondary_cost, destination_region_id=None, max_processing_days=None, destination_country_id=None, min_processing_days=None):
        """Creates a new ShippingTemplate"""

        endpoint = '/shipping/templates'

        self.params = {}
        self.params['primary_cost'] = primary_cost
        self.params['title'] = title
        self.params['origin_country_id'] = origin_country_id
        self.params['secondary_cost'] = secondary_cost
        if destination_region_id: self.params['destination_region_id'] = destination_region_id
        if max_processing_days: self.params['max_processing_days'] = max_processing_days
        if destination_country_id: self.params['destination_country_id'] = destination_country_id
        if min_processing_days: self.params['min_processing_days'] = min_processing_days

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def getShippingTemplate(self, shipping_template_id):
        """Retrieves a ShippingTemplate by id."""

        endpoint = '/shipping/templates/%s' % shipping_template_id

        self.params = {}
        self.params['shipping_template_id'] = shipping_template_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def updateShippingTemplate(self, shipping_template_id, max_processing_days=None, min_processing_days=None, origin_country_id=None, title=None):
        """Updates a ShippingTemplate"""

        endpoint = '/shipping/templates/%s' % shipping_template_id

        self.params = {}
        self.params['shipping_template_id'] = shipping_template_id
        if max_processing_days: self.params['max_processing_days'] = max_processing_days
        if min_processing_days: self.params['min_processing_days'] = min_processing_days
        if origin_country_id: self.params['origin_country_id'] = origin_country_id
        if title: self.params['title'] = title

        response = self.execute(endpoint, 'put')
        return json.loads(response.text)


    def deleteShippingTemplate(self, shipping_template_id):
        """Deletes the ShippingTemplate with the given id."""

        endpoint = '/shipping/templates/%s' % shipping_template_id

        self.params = {}
        self.params['shipping_template_id'] = shipping_template_id

        response = self.execute(endpoint, 'delete')
        return json.loads(response.text)


    def findAllShippingTemplateEntries(self, shipping_template_id, page=None, limit='25', offset='0'):
        """Retrieves a set of ShippingTemplateEntry objects associated to a ShippingTemplate."""

        endpoint = '/shipping/templates/%s/entries' % shipping_template_id

        self.params = {}
        self.params['shipping_template_id'] = shipping_template_id
        if page: self.params['page'] = page
        if limit: self.params['limit'] = limit
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllShippingTemplateUpgrades(self, shipping_template_id):
        """Retrieves a list of shipping upgrades for the parent ShippingTemplate"""

        endpoint = '/shipping/templates/%s/upgrades' % shipping_template_id

        self.params = {}
        self.params['shipping_template_id'] = shipping_template_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def createShippingTemplateUpgrade(self, price, type, shipping_template_id, value, secondary_price):
        """Creates a new ShippingUpgrade for the parent ShippingTemplate. Updates any listings linked to the ShippingTemplate."""

        endpoint = '/shipping/templates/%s/upgrades' % shipping_template_id

        self.params = {}
        self.params['price'] = price
        self.params['type'] = type
        self.params['shipping_template_id'] = shipping_template_id
        self.params['value'] = value
        self.params['secondary_price'] = secondary_price

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def updateShippingTemplateUpgrade(self, price, secondary_price, type, shipping_template_id, value_id):
        """Updates a ShippingUpgrade of the parent ShippingTemplate. Updates any listings linked to the ShippingTemplate."""

        endpoint = '/shipping/templates/%s/upgrades' % shipping_template_id

        self.params = {}
        self.params['price'] = price
        self.params['secondary_price'] = secondary_price
        self.params['type'] = type
        self.params['shipping_template_id'] = shipping_template_id
        self.params['value_id'] = value_id

        response = self.execute(endpoint, 'put')
        return json.loads(response.text)


    def deleteShippingTemplateUpgrade(self, type, shipping_template_id, value_id):
        """Deletes the ShippingUpgrade from the parent ShippingTemplate. Updates any listings linked to the ShippingTemplate."""

        endpoint = '/shipping/templates/%s/upgrades' % shipping_template_id

        self.params = {}
        self.params['type'] = type
        self.params['shipping_template_id'] = shipping_template_id
        self.params['value_id'] = value_id

        response = self.execute(endpoint, 'delete')
        return json.loads(response.text)


    def createShippingTemplateEntry(self, primary_cost, secondary_cost, shipping_template_id, destination_region_id=None, destination_country_id=None):
        """Creates a new ShippingTemplateEntry"""

        endpoint = '/shipping/templates/entries'

        self.params = {}
        self.params['primary_cost'] = primary_cost
        self.params['secondary_cost'] = secondary_cost
        self.params['shipping_template_id'] = shipping_template_id
        if destination_region_id: self.params['destination_region_id'] = destination_region_id
        if destination_country_id: self.params['destination_country_id'] = destination_country_id

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def getShippingTemplateEntry(self, shipping_template_entry_id):
        """Retrieves a ShippingTemplateEntry by id."""

        endpoint = '/shipping/templates/entries/%s' % shipping_template_entry_id

        self.params = {}
        self.params['shipping_template_entry_id'] = shipping_template_entry_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def updateShippingTemplateEntry(self, shipping_template_entry_id, primary_cost=None, destination_country_id=None, secondary_cost=None):
        """Updates a ShippingTemplateEntry"""

        endpoint = '/shipping/templates/entries/%s' % shipping_template_entry_id

        self.params = {}
        self.params['shipping_template_entry_id'] = shipping_template_entry_id
        if primary_cost: self.params['primary_cost'] = primary_cost
        if destination_country_id: self.params['destination_country_id'] = destination_country_id
        if secondary_cost: self.params['secondary_cost'] = secondary_cost

        response = self.execute(endpoint, 'put')
        return json.loads(response.text)


    def deleteShippingTemplateEntry(self, shipping_template_entry_id):
        """Deletes the ShippingTemplateEntry"""

        endpoint = '/shipping/templates/entries/%s' % shipping_template_entry_id

        self.params = {}
        self.params['shipping_template_entry_id'] = shipping_template_entry_id

        response = self.execute(endpoint, 'delete')
        return json.loads(response.text)


    def findAllShops(self, lon=None, shop_name=None, distance_max='35', limit='25', offset='0', lat=None, page=None):
        """Finds all Shops.  If there is a keywords parameter, finds shops with shop_name starting with keywords."""

        endpoint = '/shops'

        self.params = {}
        if lon: self.params['lon'] = lon
        if shop_name: self.params['shop_name'] = shop_name
        if distance_max: self.params['distance_max'] = distance_max
        if limit: self.params['limit'] = limit
        if offset: self.params['offset'] = offset
        if lat: self.params['lat'] = lat
        if page: self.params['page'] = page

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def getShop(self, shop_id):
        """Retrieves a Shop by id."""

        endpoint = '/shops/%s' % shop_id

        self.params = {}
        self.params['shop_id'] = shop_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def updateShop(self, shop_id, announcement=None, policy_additional=None, policy_payment=None, policy_refunds=None, policy_welcome=None, title=None, digital_sale_message=None, sale_message=None, policy_shipping=None, policy_seller_info=None):
        """Updates a Shop"""

        endpoint = '/shops/%s' % shop_id

        self.params = {}
        self.params['shop_id'] = shop_id
        if announcement: self.params['announcement'] = announcement
        if policy_additional: self.params['policy_additional'] = policy_additional
        if policy_payment: self.params['policy_payment'] = policy_payment
        if policy_refunds: self.params['policy_refunds'] = policy_refunds
        if policy_welcome: self.params['policy_welcome'] = policy_welcome
        if title: self.params['title'] = title
        if digital_sale_message: self.params['digital_sale_message'] = digital_sale_message
        if sale_message: self.params['sale_message'] = sale_message
        if policy_shipping: self.params['policy_shipping'] = policy_shipping
        if policy_seller_info: self.params['policy_seller_info'] = policy_seller_info

        response = self.execute(endpoint, 'put')
        return json.loads(response.text)


    def getShopAbout(self, shop_id):
        """Retrieves a ShopAbout object associated to a Shop."""

        endpoint = '/shops/%s/about' % shop_id

        self.params = {}
        self.params['shop_id'] = shop_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def uploadShopBanner(self, image, shop_id):
        """Upload a new shop banner image"""

        endpoint = '/shops/%s/appearance/banner' % shop_id

        self.params = {}
        self.params['image'] = image
        self.params['shop_id'] = shop_id

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def deleteShopBanner(self, shop_id):
        """Deletes a shop banner image"""

        endpoint = '/shops/%s/appearance/banner' % shop_id

        self.params = {}
        self.params['shop_id'] = shop_id

        response = self.execute(endpoint, 'delete')
        return json.loads(response.text)


    def findAllShopCoupons(self, shop_id):
        """Retrieves all Shop_Coupons by shop_id"""

        endpoint = '/shops/%s/coupons' % shop_id

        self.params = {}
        self.params['shop_id'] = shop_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def createCoupon(self, coupon_code, shop_id, free_shipping='false', expiration_date=None, domestic_only='false', pct_discount=None, fixed_discount=None, seller_active='false', minimum_purchase_price=None, currency_code='USD'):
        """Creates a new Coupon. May only have one of <code>free_shipping</code>, <code>pct_discount</code> or <code>fixed_discount</code>"""

        endpoint = '/shops/%s/coupons' % shop_id

        self.params = {}
        self.params['coupon_code'] = coupon_code
        self.params['shop_id'] = shop_id
        if free_shipping: self.params['free_shipping'] = free_shipping
        if expiration_date: self.params['expiration_date'] = expiration_date
        if domestic_only: self.params['domestic_only'] = domestic_only
        if pct_discount: self.params['pct_discount'] = pct_discount
        if fixed_discount: self.params['fixed_discount'] = fixed_discount
        if seller_active: self.params['seller_active'] = seller_active
        if minimum_purchase_price: self.params['minimum_purchase_price'] = minimum_purchase_price
        if currency_code: self.params['currency_code'] = currency_code

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def findCoupon(self, shop_id, coupon_id):
        """Retrieves a Shop_Coupon by id and shop_id"""

        endpoint = '/shops/%s/coupons/%s' % (shop_id, coupon_id)

        self.params = {}
        self.params['shop_id'] = shop_id
        self.params['coupon_id'] = coupon_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def updateCoupon(self, shop_id, coupon_id, seller_active='false'):
        """Updates a coupon"""

        endpoint = '/shops/%s/coupons/%s' % (shop_id, coupon_id)

        self.params = {}
        self.params['shop_id'] = shop_id
        self.params['coupon_id'] = coupon_id
        if seller_active: self.params['seller_active'] = seller_active

        response = self.execute(endpoint, 'put')
        return json.loads(response.text)


    def deleteCoupon(self, shop_id, coupon_id):
        """Deletes a coupon"""

        endpoint = '/shops/%s/coupons/%s' % (shop_id, coupon_id)

        self.params = {}
        self.params['shop_id'] = shop_id
        self.params['coupon_id'] = coupon_id

        response = self.execute(endpoint, 'delete')
        return json.loads(response.text)


    def findLedger(self, shop_id):
        """Get a Shop Payment Account Ledger"""

        endpoint = '/shops/%s/ledger/' % shop_id

        self.params = {}
        self.params['shop_id'] = shop_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findLedgerEntries(self, shop_id, min_created=None, limit='25', offset='0', max_created=None, page=None):
        """Get a Shop Payment Account Ledger's Entries"""

        endpoint = '/shops/%s/ledger/entries' % shop_id

        self.params = {}
        self.params['shop_id'] = shop_id
        if min_created: self.params['min_created'] = min_created
        if limit: self.params['limit'] = limit
        if offset: self.params['offset'] = offset
        if max_created: self.params['max_created'] = max_created
        if page: self.params['page'] = page

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllShopListingsActive(self, shop_id, category=None, min_price=None, translate_keywords='false', tags=None, color=None, sort_on='created', max_price=None, color_accuracy='0', limit='25', offset='0', keywords=None, sort_order='down', page=None, include_private='0'):
        """Finds all active Listings associated with a Shop.<br /><br />(<strong>NOTE:</strong> If calling on behalf of a shop owner in the context of listing management, be sure to include the parameter <strong>include_private = true</strong>.  This will return private listings that are not publicly visible in the shop, but which can be managed.  This is an experimental feature and may change.)"""

        endpoint = '/shops/%s/listings/active' % shop_id

        self.params = {}
        self.params['shop_id'] = shop_id
        if category: self.params['category'] = category
        if min_price: self.params['min_price'] = min_price
        if translate_keywords: self.params['translate_keywords'] = translate_keywords
        if tags: self.params['tags'] = tags
        if color: self.params['color'] = color
        if sort_on: self.params['sort_on'] = sort_on
        if max_price: self.params['max_price'] = max_price
        if color_accuracy: self.params['color_accuracy'] = color_accuracy
        if limit: self.params['limit'] = limit
        if offset: self.params['offset'] = offset
        if keywords: self.params['keywords'] = keywords
        if sort_order: self.params['sort_order'] = sort_order
        if page: self.params['page'] = page
        if include_private: self.params['include_private'] = include_private

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllShopListingsDraft(self, shop_id, limit='25', page=None, offset='0'):
        """Finds all of a Shop's draft listings"""

        endpoint = '/shops/%s/listings/draft' % shop_id

        self.params = {}
        self.params['shop_id'] = shop_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllShopListingsExpired(self, shop_id, limit='25', page=None, offset='0'):
        """Retrieves Listings associated to a Shop that are expired"""

        endpoint = '/shops/%s/listings/expired' % shop_id

        self.params = {}
        self.params['shop_id'] = shop_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def getShopListingExpired(self, listing_id, shop_id):
        """Retrieves a Listing associated to a Shop that is inactive"""

        endpoint = '/shops/%s/listings/expired/%s' % (shop_id, listing_id)

        self.params = {}
        self.params['listing_id'] = listing_id
        self.params['shop_id'] = shop_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllShopListingsFeatured(self, shop_id, limit='25', page=None, offset='0'):
        """Retrieves Listings associated to a Shop that are featured"""

        endpoint = '/shops/%s/listings/featured' % shop_id

        self.params = {}
        self.params['shop_id'] = shop_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllShopListingsInactive(self, shop_id, limit='25', page=None, offset='0'):
        """Retrieves Listings associated to a Shop that are inactive"""

        endpoint = '/shops/%s/listings/inactive' % shop_id

        self.params = {}
        self.params['shop_id'] = shop_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def getShopListingInactive(self, listing_id, shop_id):
        """Retrieves a Listing associated to a Shop that is inactive"""

        endpoint = '/shops/%s/listings/inactive/%s' % (shop_id, listing_id)

        self.params = {}
        self.params['listing_id'] = listing_id
        self.params['shop_id'] = shop_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findShopPaymentTemplates(self, shop_id):
        """Retrieves the PaymentTemplate associated with the Shop"""

        endpoint = '/shops/%s/payment_templates' % shop_id

        self.params = {}
        self.params['shop_id'] = shop_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def createShopPaymentTemplate(self, shop_id, city=None, name=None, zip=None, allow_other=None, country_id=None, second_line=None, state=None, allow_paypal=None, allow_cc=None, first_line=None, allow_mo=None, paypal_email=None, allow_check=None):
        """Creates a new PaymentTemplate"""

        endpoint = '/shops/%s/payment_templates' % shop_id

        self.params = {}
        self.params['shop_id'] = shop_id
        if city: self.params['city'] = city
        if name: self.params['name'] = name
        if zip: self.params['zip'] = zip
        if allow_other: self.params['allow_other'] = allow_other
        if country_id: self.params['country_id'] = country_id
        if second_line: self.params['second_line'] = second_line
        if state: self.params['state'] = state
        if allow_paypal: self.params['allow_paypal'] = allow_paypal
        if allow_cc: self.params['allow_cc'] = allow_cc
        if first_line: self.params['first_line'] = first_line
        if allow_mo: self.params['allow_mo'] = allow_mo
        if paypal_email: self.params['paypal_email'] = paypal_email
        if allow_check: self.params['allow_check'] = allow_check

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def updateShopPaymentTemplate(self, shop_id, payment_template_id, city=None, name=None, zip=None, allow_other=None, country_id=None, second_line=None, state=None, allow_paypal=None, allow_cc=None, first_line=None, allow_mo=None, paypal_email=None, allow_check=None):
        """Updates a PaymentTemplate"""

        endpoint = '/shops/%s/payment_templates/%s' % (shop_id, payment_template_id)

        self.params = {}
        self.params['shop_id'] = shop_id
        self.params['payment_template_id'] = payment_template_id
        if city: self.params['city'] = city
        if name: self.params['name'] = name
        if zip: self.params['zip'] = zip
        if allow_other: self.params['allow_other'] = allow_other
        if country_id: self.params['country_id'] = country_id
        if second_line: self.params['second_line'] = second_line
        if state: self.params['state'] = state
        if allow_paypal: self.params['allow_paypal'] = allow_paypal
        if allow_cc: self.params['allow_cc'] = allow_cc
        if first_line: self.params['first_line'] = first_line
        if allow_mo: self.params['allow_mo'] = allow_mo
        if paypal_email: self.params['paypal_email'] = paypal_email
        if allow_check: self.params['allow_check'] = allow_check

        response = self.execute(endpoint, 'put')
        return json.loads(response.text)


    def findAllShopReceipts(self, shop_id, min_created=None, was_shipped=None, was_paid=None, max_last_modified=None, limit='25', offset='0', max_created=None, page=None, min_last_modified=None):
        """Retrieves a set of Receipt objects associated to a Shop."""

        endpoint = '/shops/%s/receipts' % shop_id

        self.params = {}
        self.params['shop_id'] = shop_id
        if min_created: self.params['min_created'] = min_created
        if was_shipped: self.params['was_shipped'] = was_shipped
        if was_paid: self.params['was_paid'] = was_paid
        if max_last_modified: self.params['max_last_modified'] = max_last_modified
        if limit: self.params['limit'] = limit
        if offset: self.params['offset'] = offset
        if max_created: self.params['max_created'] = max_created
        if page: self.params['page'] = page
        if min_last_modified: self.params['min_last_modified'] = min_last_modified

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findShopPaymentByReceipt(self, shop_id, receipt_id):
        """Get a Payment by Shop Receipt ID"""

        endpoint = '/shops/%s/receipts/%s/payments' % (shop_id, receipt_id)

        self.params = {}
        self.params['shop_id'] = shop_id
        self.params['receipt_id'] = receipt_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def submitTracking(self, tracking_code, carrier_name, send_bcc='False'):
        """Submits tracking information and sends a shipping notification email to the buyer. If <code>send_bcc</code> is <code>true</code>, the shipping notification will be sent to the seller as well. Refer to <a href="/developers/documentation/getting_started/seller_tools#section_tracking_codes">additional documentation</a>."""

        endpoint = '/shops/%s/receipts/%s/tracking' % (shop_id, receipt_id)

        self.params = {}
        self.params['tracking_code'] = tracking_code
        self.params['carrier_name'] = carrier_name
        if send_bcc: self.params['send_bcc'] = send_bcc

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def findAllShopReceiptsByStatus(self, status, shop_id, limit='25', page=None, offset='0'):
        """Retrieves a set of Receipt objects associated to a Shop based on the status."""

        endpoint = '/shops/%s/receipts/%s' % (shop_id, status)

        self.params = {}
        self.params['status'] = status
        self.params['shop_id'] = shop_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def searchAllShopReceipts(self, search_query, shop_id, limit='25', page=None, offset='0'):
        """Searches the set of Receipt objects associated to a Shop by a query"""

        endpoint = '/shops/%s/receipts/search' % shop_id

        self.params = {}
        self.params['search_query'] = search_query
        self.params['shop_id'] = shop_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def getShopReviews(self, shop_id, limit='30', page=None, offset='0'):
        """Retrieves a list of reviews left for listings purchased from a shop"""

        endpoint = '/shops/%s/reviews' % shop_id

        self.params = {}
        self.params['shop_id'] = shop_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllShopSections(self, shop_id):
        """Retrieves a set of ShopSection objects associated to a Shop."""

        endpoint = '/shops/%s/sections' % shop_id

        self.params = {}
        self.params['shop_id'] = shop_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def createShopSection(self, shop_id, user_id=None, title=None):
        """Creates a new ShopSection."""

        endpoint = '/shops/%s/sections' % shop_id

        self.params = {}
        self.params['shop_id'] = shop_id
        if user_id: self.params['user_id'] = user_id
        if title: self.params['title'] = title

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def getShopSection(self, shop_id, shop_section_id):
        """Retrieves a ShopSection by id and shop_id"""

        endpoint = '/shops/%s/sections/%s' % (shop_id, shop_section_id)

        self.params = {}
        self.params['shop_id'] = shop_id
        self.params['shop_section_id'] = shop_section_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def updateShopSection(self, shop_id, shop_section_id, title=None, user_id=None):
        """Updates a ShopSection with the given id."""

        endpoint = '/shops/%s/sections/%s' % (shop_id, shop_section_id)

        self.params = {}
        self.params['shop_id'] = shop_id
        self.params['shop_section_id'] = shop_section_id
        if title: self.params['title'] = title
        if user_id: self.params['user_id'] = user_id

        response = self.execute(endpoint, 'put')
        return json.loads(response.text)


    def deleteShopSection(self, shop_id, shop_section_id):
        """Deletes the ShopSection with the given id."""

        endpoint = '/shops/%s/sections/%s' % (shop_id, shop_section_id)

        self.params = {}
        self.params['shop_id'] = shop_id
        self.params['shop_section_id'] = shop_section_id

        response = self.execute(endpoint, 'delete')
        return json.loads(response.text)


    def findAllShopSectionListings(self, shop_section_id, shop_id, limit='25', page=None, offset='0'):
        """Finds all listings within a shop section"""

        endpoint = '/shops/%s/sections/%s/listings' % (shop_id, shop_section_id)

        self.params = {}
        self.params['shop_section_id'] = shop_section_id
        self.params['shop_id'] = shop_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllShopSectionListingsActive(self, shop_id, shop_section_id, sort_on='created', limit='25', offset='0', sort_order='down', page=None):
        """Finds all listings within a shop section"""

        endpoint = '/shops/%s/sections/%s/listings/active' % (shop_id, shop_section_id)

        self.params = {}
        self.params['shop_id'] = shop_id
        self.params['shop_section_id'] = shop_section_id
        if sort_on: self.params['sort_on'] = sort_on
        if limit: self.params['limit'] = limit
        if offset: self.params['offset'] = offset
        if sort_order: self.params['sort_order'] = sort_order
        if page: self.params['page'] = page

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def getShopSectionTranslation(self, shop_id, language, shop_section_id):
        """Retrieves a ShopSectionTranslation by shop_id, shop_section_id and language"""

        endpoint = '/shops/%s/sections/%s/translations/%s' % (shop_id, shop_section_id, language)

        self.params = {}
        self.params['shop_id'] = shop_id
        self.params['language'] = language
        self.params['shop_section_id'] = shop_section_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def createShopSectionTranslation(self, shop_id, language, shop_section_id, title='False'):
        """Creates a ShopSectionTranslation by shop_id, shop_section_id and language"""

        endpoint = '/shops/%s/sections/%s/translations/%s' % (shop_id, shop_section_id, language)

        self.params = {}
        self.params['shop_id'] = shop_id
        self.params['language'] = language
        self.params['shop_section_id'] = shop_section_id
        if title: self.params['title'] = title

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def updateShopSectionTranslation(self, shop_id, language, shop_section_id, title='False'):
        """Updates a ShopSectionTranslation by shop_id, shop_section_id and language"""

        endpoint = '/shops/%s/sections/%s/translations/%s' % (shop_id, shop_section_id, language)

        self.params = {}
        self.params['shop_id'] = shop_id
        self.params['language'] = language
        self.params['shop_section_id'] = shop_section_id
        if title: self.params['title'] = title

        response = self.execute(endpoint, 'put')
        return json.loads(response.text)


    def deleteShopSectionTranslation(self, shop_id, language, shop_section_id):
        """Deletes a ShopSectionTranslation by shop_id, shop_section_id and language"""

        endpoint = '/shops/%s/sections/%s/translations/%s' % (shop_id, shop_section_id, language)

        self.params = {}
        self.params['shop_id'] = shop_id
        self.params['language'] = language
        self.params['shop_section_id'] = shop_section_id

        response = self.execute(endpoint, 'delete')
        return json.loads(response.text)


    def findAllShopTransactions(self, shop_id, limit='25', page=None, offset='0'):
        """Retrieves a set of Transaction objects associated to a Shop."""

        endpoint = '/shops/%s/transactions' % shop_id

        self.params = {}
        self.params['shop_id'] = shop_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def getShopTranslation(self, shop_id, language):
        """Retrieves a ShopTranslation by shop_id and language"""

        endpoint = '/shops/%s/translations/%s' % (shop_id, language)

        self.params = {}
        self.params['shop_id'] = shop_id
        self.params['language'] = language

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def createShopTranslation(self, language, shop_id, announcement='False', policy_additional='False', title='False', policy_refunds='False', policy_welcome='False', policy_payment='False', vacation_message='False', sale_message='False', vacation_autoreply='False', policy_shipping='False', policy_seller_info='False'):
        """Creates a ShopTranslation by shop_id and language"""

        endpoint = '/shops/%s/translations/%s' % (shop_id, language)

        self.params = {}
        self.params['language'] = language
        self.params['shop_id'] = shop_id
        if announcement: self.params['announcement'] = announcement
        if policy_additional: self.params['policy_additional'] = policy_additional
        if title: self.params['title'] = title
        if policy_refunds: self.params['policy_refunds'] = policy_refunds
        if policy_welcome: self.params['policy_welcome'] = policy_welcome
        if policy_payment: self.params['policy_payment'] = policy_payment
        if vacation_message: self.params['vacation_message'] = vacation_message
        if sale_message: self.params['sale_message'] = sale_message
        if vacation_autoreply: self.params['vacation_autoreply'] = vacation_autoreply
        if policy_shipping: self.params['policy_shipping'] = policy_shipping
        if policy_seller_info: self.params['policy_seller_info'] = policy_seller_info

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def updateShopTranslation(self, language, shop_id, announcement='False', policy_additional='False', title='False', policy_refunds='False', policy_welcome='False', policy_payment='False', vacation_message='False', sale_message='False', vacation_autoreply='False', policy_shipping='False', policy_seller_info='False'):
        """Updates a ShopTranslation by shop_id and language"""

        endpoint = '/shops/%s/translations/%s' % (shop_id, language)

        self.params = {}
        self.params['language'] = language
        self.params['shop_id'] = shop_id
        if announcement: self.params['announcement'] = announcement
        if policy_additional: self.params['policy_additional'] = policy_additional
        if title: self.params['title'] = title
        if policy_refunds: self.params['policy_refunds'] = policy_refunds
        if policy_welcome: self.params['policy_welcome'] = policy_welcome
        if policy_payment: self.params['policy_payment'] = policy_payment
        if vacation_message: self.params['vacation_message'] = vacation_message
        if sale_message: self.params['sale_message'] = sale_message
        if vacation_autoreply: self.params['vacation_autoreply'] = vacation_autoreply
        if policy_shipping: self.params['policy_shipping'] = policy_shipping
        if policy_seller_info: self.params['policy_seller_info'] = policy_seller_info

        response = self.execute(endpoint, 'put')
        return json.loads(response.text)


    def deleteShopTranslation(self, shop_id, language):
        """Deletes a ShopTranslation by shop_id and language"""

        endpoint = '/shops/%s/translations/%s' % (shop_id, language)

        self.params = {}
        self.params['shop_id'] = shop_id
        self.params['language'] = language

        response = self.execute(endpoint, 'delete')
        return json.loads(response.text)


    def getListingShop(self, listing_id):
        """Retrieves a shop by a listing id."""

        endpoint = '/shops/listing/%s' % listing_id

        self.params = {}
        self.params['listing_id'] = listing_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def getBuyerTaxonomy(self, ):
        """Retrieve the entire taxonomy as seen by buyers in search."""

        endpoint = '/taxonomy/buyer/get'

        self.params = {}

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllTopCategory(self, ):
        """Retrieves all top-level Categories."""

        endpoint = '/taxonomy/categories'

        self.params = {}

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllTopCategoryChildren(self, tag):
        """Retrieves children of a top-level Category by tag."""

        endpoint = '/taxonomy/categories/%s' % tag

        self.params = {}
        self.params['tag'] = tag

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllSubCategoryChildren(self, subtag, tag):
        """Retrieves children of a second-level Category by tag and subtag."""

        endpoint = '/taxonomy/categories/%s/%s' % (tag, subtag)

        self.params = {}
        self.params['subtag'] = subtag
        self.params['tag'] = tag

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def getSellerTaxonomy(self, ):
        """Retrieve the entire taxonomy as used by sellers in the listing process."""

        endpoint = '/taxonomy/seller/get'

        self.params = {}

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findSuggestedStyles(self, ):
        """Retrieve all suggested styles."""

        endpoint = '/taxonomy/styles'

        self.params = {}

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllTeams(self, limit='25', page=None, offset='0'):
        """Returns all Teams"""

        endpoint = '/teams'

        self.params = {}
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllUsersForTeam(self, team_id, status='active', limit='25', page=None, offset='0'):
        """Returns a list of users for a specific team"""

        endpoint = '/teams/%s/users/' % team_id

        self.params = {}
        self.params['team_id'] = team_id
        if status: self.params['status'] = status
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findTeams(self, team_ids):
        """Returns specified team by ID or team name"""

        endpoint = '/teams/%s/' % team_ids

        self.params = {}
        self.params['team_ids'] = team_ids

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def getTransaction(self, transaction_id):
        """Retrieves a Transaction by id."""

        endpoint = '/transactions/%s' % transaction_id

        self.params = {}
        self.params['transaction_id'] = transaction_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllTreasuries(self, sort_on='hotness', sort_order='down', limit='25', offset='0', keywords=None, page=None):
        """Search Treasuries or else List all Treasuries"""

        endpoint = '/treasuries'

        self.params = {}
        if sort_on: self.params['sort_on'] = sort_on
        if sort_order: self.params['sort_order'] = sort_order
        if limit: self.params['limit'] = limit
        if offset: self.params['offset'] = offset
        if keywords: self.params['keywords'] = keywords
        if page: self.params['page'] = page

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def createTreasury(self, listing_ids, title, tags='', description=None, private='0'):
        """Create a Treasury"""

        endpoint = '/treasuries'

        self.params = {}
        self.params['listing_ids'] = listing_ids
        self.params['title'] = title
        if tags: self.params['tags'] = tags
        if description: self.params['description'] = description
        if private: self.params['private'] = private

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def getTreasury(self, treasury_key):
        """Get a Treasury"""

        endpoint = '/treasuries/%s' % treasury_key

        self.params = {}
        self.params['treasury_key'] = treasury_key

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def deleteTreasury(self, ):
        """Delete a Treasury"""

        endpoint = '/treasuries/%s' % treasury_key

        self.params = {}

        response = self.execute(endpoint, 'delete')
        return json.loads(response.text)


    def findTreasuryComments(self, treasury_key, limit='25', page=None, offset='0'):
        """Get a Treasury's Comments"""

        endpoint = '/treasuries/%s/comments' % treasury_key

        self.params = {}
        self.params['treasury_key'] = treasury_key
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def postTreasuryComment(self, message):
        """Leave a comment on a Treasury List"""

        endpoint = '/treasuries/%s/comments' % treasury_key

        self.params = {}
        self.params['message'] = message

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def deleteTreasuryComment(self, ):
        """Delete a given comment on a Treasury List"""

        endpoint = '/treasuries/%s/comments/%s' % (treasury_key, comment_id)

        self.params = {}

        response = self.execute(endpoint, 'delete')
        return json.loads(response.text)


    def addTreasuryListing(self, listing_id, treasury_key):
        """Add listing to a Treasury"""

        endpoint = '/treasuries/%s/listings' % treasury_key

        self.params = {}
        self.params['listing_id'] = listing_id
        self.params['treasury_key'] = treasury_key

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def removeTreasuryListing(self, listing_id, treasury_key):
        """Remove listing from a Treasury"""

        endpoint = '/treasuries/%s/listings/%s' % (treasury_key, listing_id)

        self.params = {}
        self.params['listing_id'] = listing_id
        self.params['treasury_key'] = treasury_key

        response = self.execute(endpoint, 'delete')
        return json.loads(response.text)


    def describeOccasionEnum(self, ):
        """Describes the legal values for Listing.occasion."""

        endpoint = '/types/enum/occasion'

        self.params = {}

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def describeRecipientEnum(self, ):
        """Describes the legal values for Listing.recipient."""

        endpoint = '/types/enum/recipient'

        self.params = {}

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def describeWhenMadeEnum(self, include_formatted=None):
        """Describes the legal values for Listing.when_made."""

        endpoint = '/types/enum/when_made'

        self.params = {}
        if include_formatted: self.params['include_formatted'] = include_formatted

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def describeWhoMadeEnum(self, ):
        """Describes the legal values for Listing.who_made."""

        endpoint = '/types/enum/who_made'

        self.params = {}

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllUsers(self, keywords=None, limit='25', page=None, offset='0'):
        """Finds all Users whose name or username match the keywords parameter."""

        endpoint = '/users'

        self.params = {}
        if keywords: self.params['keywords'] = keywords
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def getUser(self, user_id):
        """Retrieves a User by id."""

        endpoint = '/users/%s' % user_id

        self.params = {}
        self.params['user_id'] = user_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllUserAddresses(self, user_id, limit='25', page=None, offset='0'):
        """Retrieves a set of UserAddress objects associated to a User."""

        endpoint = '/users/%s/addresses' % user_id

        self.params = {}
        self.params['user_id'] = user_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def createUserAddress(self, city, user_id, name, zip, country_id, first_line, state=None, second_line=None):
        """Creates a new UserAddress. Note: state is required when the country is US, Canada, or Australia. See section above about valid codes."""

        endpoint = '/users/%s/addresses/' % user_id

        self.params = {}
        self.params['city'] = city
        self.params['user_id'] = user_id
        self.params['name'] = name
        self.params['zip'] = zip
        self.params['country_id'] = country_id
        self.params['first_line'] = first_line
        if state: self.params['state'] = state
        if second_line: self.params['second_line'] = second_line

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def getUserAddress(self, user_address_id):
        """Retrieves a UserAddress by id."""

        endpoint = '/users/%s/addresses/%s' % (user_id, user_address_id)

        self.params = {}
        self.params['user_address_id'] = user_address_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def deleteUserAddress(self, user_address_id):
        """Deletes the UserAddress with the given id."""

        endpoint = '/users/%s/addresses/%s' % (user_id, user_address_id)

        self.params = {}
        self.params['user_address_id'] = user_address_id

        response = self.execute(endpoint, 'delete')
        return json.loads(response.text)


    def uploadAvatar(self, user_id, src=None, image=None):
        """Upload a new user avatar image"""

        endpoint = '/users/%s/avatar' % user_id

        self.params = {}
        self.params['user_id'] = user_id
        if src: self.params['src'] = src
        if image: self.params['image'] = image

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def getAvatarImgSrc(self, user_id):
        """Get avatar image source"""

        endpoint = '/users/%s/avatar/src' % user_id

        self.params = {}
        self.params['user_id'] = user_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def getUserBillingOverview(self, user_id):
        """Retrieves the user's current balance."""

        endpoint = '/users/%s/billing/overview' % user_id

        self.params = {}
        self.params['user_id'] = user_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def getAllUserCarts(self, user_id, limit='100', page=None, offset='0'):
        """Get a user's Carts"""

        endpoint = '/users/%s/carts' % user_id

        self.params = {}
        self.params['user_id'] = user_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def addToCart(self, listing_id, user_id, selected_variations=None, quantity='1'):
        """Add a listing to a cart"""

        endpoint = '/users/%s/carts' % user_id

        self.params = {}
        self.params['listing_id'] = listing_id
        self.params['user_id'] = user_id
        if selected_variations: self.params['selected_variations'] = selected_variations
        if quantity: self.params['quantity'] = quantity

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def updateCartListingQuantity(self, listing_id, user_id, quantity, listing_customization_id='0'):
        """Update a cart listing purchase quantity"""

        endpoint = '/users/%s/carts' % user_id

        self.params = {}
        self.params['listing_id'] = listing_id
        self.params['user_id'] = user_id
        self.params['quantity'] = quantity
        if listing_customization_id: self.params['listing_customization_id'] = listing_customization_id

        response = self.execute(endpoint, 'put')
        return json.loads(response.text)


    def removeCartListing(self, listing_id, user_id, listing_customization_id='0'):
        """Remove a listing from a cart"""

        endpoint = '/users/%s/carts' % user_id

        self.params = {}
        self.params['listing_id'] = listing_id
        self.params['user_id'] = user_id
        if listing_customization_id: self.params['listing_customization_id'] = listing_customization_id

        response = self.execute(endpoint, 'delete')
        return json.loads(response.text)


    def getUserCart(self, user_id, cart_id):
        """Get a cart"""

        endpoint = '/users/%s/carts/%s' % (user_id, cart_id)

        self.params = {}
        self.params['user_id'] = user_id
        self.params['cart_id'] = cart_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def updateCart(self, user_id, cart_id, destination_zip=None, shipping_option_id=None, message_to_seller=None, coupon_code=None, destination_country_id=None):
        """Update a cart"""

        endpoint = '/users/%s/carts/%s' % (user_id, cart_id)

        self.params = {}
        self.params['user_id'] = user_id
        self.params['cart_id'] = cart_id
        if destination_zip: self.params['destination_zip'] = destination_zip
        if shipping_option_id: self.params['shipping_option_id'] = shipping_option_id
        if message_to_seller: self.params['message_to_seller'] = message_to_seller
        if coupon_code: self.params['coupon_code'] = coupon_code
        if destination_country_id: self.params['destination_country_id'] = destination_country_id

        response = self.execute(endpoint, 'put')
        return json.loads(response.text)


    def deleteCart(self, user_id, cart_id):
        """Delete a cart"""

        endpoint = '/users/%s/carts/%s' % (user_id, cart_id)

        self.params = {}
        self.params['user_id'] = user_id
        self.params['cart_id'] = cart_id

        response = self.execute(endpoint, 'delete')
        return json.loads(response.text)


    def addAndSelectShippingForApplePay(self, city, user_id, zip, country_id, cart_id, state=None, second_line=None):
        """Saves and selects a shipping address for apple pay"""

        endpoint = '/users/%s/carts/%s/add_and_select_shipping_for_apple' % (user_id, cart_id)

        self.params = {}
        self.params['city'] = city
        self.params['user_id'] = user_id
        self.params['zip'] = zip
        self.params['country_id'] = country_id
        self.params['cart_id'] = cart_id
        if state: self.params['state'] = state
        if second_line: self.params['second_line'] = second_line

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def findAllCartListings(self, user_id, cart_id):
        """Finds all listings in a given Cart"""

        endpoint = '/users/%s/carts/%s/listings' % (user_id, cart_id)

        self.params = {}
        self.params['user_id'] = user_id
        self.params['cart_id'] = cart_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def getUserCartForShop(self, shop_id, user_id):
        """Get a cart from a shop ID"""

        endpoint = '/users/%s/carts/shop/%s' % (user_id, shop_id)

        self.params = {}
        self.params['shop_id'] = shop_id
        self.params['user_id'] = user_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllUserCharges(self, user_id, min_created=None, sort_order='up', limit='25', offset='0', max_created=None, page=None):
        """Retrieves a set of BillCharge objects associated to a User. NOTE: from 8/8/12 the min_created and max_created arguments will be mandatory and can be no more than 31 days apart."""

        endpoint = '/users/%s/charges' % user_id

        self.params = {}
        self.params['user_id'] = user_id
        if min_created: self.params['min_created'] = min_created
        if sort_order: self.params['sort_order'] = sort_order
        if limit: self.params['limit'] = limit
        if offset: self.params['offset'] = offset
        if max_created: self.params['max_created'] = max_created
        if page: self.params['page'] = page

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def getUserChargesMetadata(self, user_id):
        """Metadata for the set of BillCharges objects associated to a User"""

        endpoint = '/users/%s/charges/meta' % user_id

        self.params = {}
        self.params['user_id'] = user_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def getCirclesContainingUser(self, user_id, limit='25', page=None, offset='0'):
        """Returns a list of users who have circled this user"""

        endpoint = '/users/%s/circles' % user_id

        self.params = {}
        self.params['user_id'] = user_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def getConnectedUser(self, to_user_id, user_id, limit='25', page=None, offset='0'):
        """Returns details about a connection between users"""

        endpoint = '/users/%s/circles/%s' % (user_id, to_user_id)

        self.params = {}
        self.params['to_user_id'] = to_user_id
        self.params['user_id'] = user_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def unconnectUsers(self, to_user_id, user_id):
        """Removes a user (to_user_id) from the logged in user's (user_id) circle"""

        endpoint = '/users/%s/circles/%s' % (user_id, to_user_id)

        self.params = {}
        self.params['to_user_id'] = to_user_id
        self.params['user_id'] = user_id

        response = self.execute(endpoint, 'delete')
        return json.loads(response.text)


    def listFollowingPages(self, limit='25', page=None, offset='0'):
        """Lists the pages that the current user is following"""

        endpoint = '/users/%s/connected_pages' % user_id

        self.params = {}
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def followPage(self, page_id, user_id):
        """Follow a page."""

        endpoint = '/users/%s/connected_pages' % user_id

        self.params = {}
        self.params['page_id'] = page_id
        self.params['user_id'] = user_id

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def unfollowPage(self, page_id, user_id):
        """Unfollow a page."""

        endpoint = '/users/%s/connected_pages/%s' % (user_id, page_id)

        self.params = {}
        self.params['page_id'] = page_id
        self.params['user_id'] = user_id

        response = self.execute(endpoint, 'delete')
        return json.loads(response.text)


    def getConnectedUsers(self, user_id, limit='25', page=None, offset='0'):
        """Returns a list of users that are in this user's cricle"""

        endpoint = '/users/%s/connected_users' % user_id

        self.params = {}
        self.params['user_id'] = user_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def connectUsers(self, to_user_id, user_id):
        """Adds user (to_user_id) to the user's (user_id) circle"""

        endpoint = '/users/%s/connected_users' % user_id

        self.params = {}
        self.params['to_user_id'] = to_user_id
        self.params['user_id'] = user_id

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def findAllUserFavoredBy(self, user_id, limit='25', page=None, offset='0'):
        """Retrieves a set of FavoriteUser objects associated to a User."""

        endpoint = '/users/%s/favored-by' % user_id

        self.params = {}
        self.params['user_id'] = user_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllUserFavoriteListings(self, user_id, limit='25', page=None, offset='0'):
        """Finds all favorite listings for a user"""

        endpoint = '/users/%s/favorites/listings' % user_id

        self.params = {}
        self.params['user_id'] = user_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findUserFavoriteListings(self, listing_id, user_id):
        """Finds a favorite listing for a user"""

        endpoint = '/users/%s/favorites/listings/%s' % (user_id, listing_id)

        self.params = {}
        self.params['listing_id'] = listing_id
        self.params['user_id'] = user_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def createUserFavoriteListings(self, listing_id, user_id):
        """Creates a new favorite listing for a user"""

        endpoint = '/users/%s/favorites/listings/%s' % (user_id, listing_id)

        self.params = {}
        self.params['listing_id'] = listing_id
        self.params['user_id'] = user_id

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def deleteUserFavoriteListings(self, listing_id, user_id):
        """Delete a favorite listing for a user"""

        endpoint = '/users/%s/favorites/listings/%s' % (user_id, listing_id)

        self.params = {}
        self.params['listing_id'] = listing_id
        self.params['user_id'] = user_id

        response = self.execute(endpoint, 'delete')
        return json.loads(response.text)


    def findAllUserFavoriteUsers(self, user_id, limit='25', page=None, offset='0'):
        """Finds all favorite users for a user"""

        endpoint = '/users/%s/favorites/users' % user_id

        self.params = {}
        self.params['user_id'] = user_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findUserFavoriteUsers(self, user_id, target_user_id):
        """Finds a favorite user for a user"""

        endpoint = '/users/%s/favorites/users/%s' % (user_id, target_user_id)

        self.params = {}
        self.params['user_id'] = user_id
        self.params['target_user_id'] = target_user_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def createUserFavoriteUsers(self, user_id, target_user_id):
        """Creates a new favorite listing for a user"""

        endpoint = '/users/%s/favorites/users/%s' % (user_id, target_user_id)

        self.params = {}
        self.params['user_id'] = user_id
        self.params['target_user_id'] = target_user_id

        response = self.execute(endpoint, 'post')
        return json.loads(response.text)


    def deleteUserFavoriteUsers(self, user_id, target_user_id):
        """Delete a favorite listing for a user"""

        endpoint = '/users/%s/favorites/users/%s' % (user_id, target_user_id)

        self.params = {}
        self.params['user_id'] = user_id
        self.params['target_user_id'] = target_user_id

        response = self.execute(endpoint, 'delete')
        return json.loads(response.text)


    def findAllUserFeedbackAsAuthor(self, user_id, limit='25', page=None, offset='0'):
        """Retrieves a set of Feedback objects associated to a User."""

        endpoint = '/users/%s/feedback/as-author' % user_id

        self.params = {}
        self.params['user_id'] = user_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllUserFeedbackAsBuyer(self, user_id, limit='25', page=None, offset='0'):
        """Retrieves a set of Feedback objects associated to a User."""

        endpoint = '/users/%s/feedback/as-buyer' % user_id

        self.params = {}
        self.params['user_id'] = user_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllUserFeedbackAsSeller(self, user_id, limit='25', page=None, offset='0'):
        """Retrieves a set of Feedback objects associated to a User."""

        endpoint = '/users/%s/feedback/as-seller' % user_id

        self.params = {}
        self.params['user_id'] = user_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllUserFeedbackAsSubject(self, user_id, limit='25', page=None, offset='0'):
        """Retrieves a set of Feedback objects associated to a User."""

        endpoint = '/users/%s/feedback/as-subject' % user_id

        self.params = {}
        self.params['user_id'] = user_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllFeedbackFromBuyers(self, limit='25', user_id=None, page=None, offset='0'):
        """
                    Returns a set of FeedBack objects associated to a User.
                    This is essentially the union between the findAllUserFeedbackAsBuyer
                    and findAllUserFeedbackAsSubject methods."""

        endpoint = '/users/%s/feedback/from-buyers' % user_id

        self.params = {}
        if limit: self.params['limit'] = limit
        if user_id: self.params['user_id'] = user_id
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllFeedbackFromSellers(self, limit='25', user_id=None, page=None, offset='0'):
        """
                    Returns a set of FeedBack objects associated to a User.
                    This is essentially the union between
                    the findAllUserFeedbackAsBuyer and findAllUserFeedbackAsSubject methods."""

        endpoint = '/users/%s/feedback/from-sellers' % user_id

        self.params = {}
        if limit: self.params['limit'] = limit
        if user_id: self.params['user_id'] = user_id
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllUserPayments(self, user_id, min_created=None, sort_order='up', limit='25', offset='0', max_created=None, page=None):
        """Retrieves a set of BillPayment objects associated to a User."""

        endpoint = '/users/%s/payments' % user_id

        self.params = {}
        self.params['user_id'] = user_id
        if min_created: self.params['min_created'] = min_created
        if sort_order: self.params['sort_order'] = sort_order
        if limit: self.params['limit'] = limit
        if offset: self.params['offset'] = offset
        if max_created: self.params['max_created'] = max_created
        if page: self.params['page'] = page

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllUserPaymentTemplates(self, user_id):
        """Retrieves a set of PaymentTemplate objects associated to a User."""

        endpoint = '/users/%s/payments/templates' % user_id

        self.params = {}
        self.params['user_id'] = user_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findUserProfile(self, user_id):
        """Returns the UserProfile object associated with a User."""

        endpoint = '/users/%s/profile' % user_id

        self.params = {}
        self.params['user_id'] = user_id

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def updateUserProfile(self, user_id, bio=None, city=None, gender=None, region=None, country_id=None, materials=None, birth_month=None, birth_day=None, birth_year=None):
        """Updates the UserProfile object associated with a User. <br /><b>Notes:</b><ul><li>Name changes are subject to admin review and therefore unavailable via the API.</li><li>Materials must be provided as a <i>period-separated</i> list of ASCII words.</ul>"""

        endpoint = '/users/%s/profile' % user_id

        self.params = {}
        self.params['user_id'] = user_id
        if bio: self.params['bio'] = bio
        if city: self.params['city'] = city
        if gender: self.params['gender'] = gender
        if region: self.params['region'] = region
        if country_id: self.params['country_id'] = country_id
        if materials: self.params['materials'] = materials
        if birth_month: self.params['birth_month'] = birth_month
        if birth_day: self.params['birth_day'] = birth_day
        if birth_year: self.params['birth_year'] = birth_year

        response = self.execute(endpoint, 'put')
        return json.loads(response.text)


    def findAllUserBuyerReceipts(self, user_id, limit='25', page=None, offset='0'):
        """Retrieves a set of Receipt objects associated to a User."""

        endpoint = '/users/%s/receipts' % user_id

        self.params = {}
        self.params['user_id'] = user_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllUserShippingProfiles(self, user_id, limit='25', page=None, offset='0'):
        """Retrieves a set of ShippingTemplate objects associated to a User."""

        endpoint = '/users/%s/shipping/templates' % user_id

        self.params = {}
        self.params['user_id'] = user_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllUserShops(self, user_id, limit='25', page=None, offset='0'):
        """Retrieves a set of Shop objects associated to a User."""

        endpoint = '/users/%s/shops' % user_id

        self.params = {}
        self.params['user_id'] = user_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllTeamsForUser(self, user_id, limit='25', page=None, offset='0'):
        """Returns a list of teams for a specific user"""

        endpoint = '/users/%s/teams' % user_id

        self.params = {}
        self.params['user_id'] = user_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllUserBuyerTransactions(self, user_id, limit='25', page=None, offset='0'):
        """Retrieves a set of Transaction objects associated to a User."""

        endpoint = '/users/%s/transactions' % user_id

        self.params = {}
        self.params['user_id'] = user_id
        if limit: self.params['limit'] = limit
        if page: self.params['page'] = page
        if offset: self.params['offset'] = offset

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)


    def findAllUserTreasuries(self, user_id, sort_on='hotness', include_private='0', sort_order='down', limit='25', offset='0', page=None):
        """Get a user's Treasuries. <strong>Note:</strong> The <code>treasury_r</code> permission scope is required in order to display private Treasuries for a user when the boolean parameter <code>include_private</code> is <code>true</code>."""

        endpoint = '/users/%s/treasuries' % user_id

        self.params = {}
        self.params['user_id'] = user_id
        if sort_on: self.params['sort_on'] = sort_on
        if include_private: self.params['include_private'] = include_private
        if sort_order: self.params['sort_order'] = sort_order
        if limit: self.params['limit'] = limit
        if offset: self.params['offset'] = offset
        if page: self.params['page'] = page

        response = self.execute(endpoint, 'get')
        return json.loads(response.text)

       