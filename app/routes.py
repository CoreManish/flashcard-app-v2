from app import api
from app.apis import *

# Add Resources to API route
api.add_resource(HomeResource, '/')
api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(DeckResource, '/deck')
api.add_resource(CardResource, '/card/<int:deck_id>')
api.add_resource(OneCardResource, "/onecard/<int:deck_id>")
api.add_resource(IEDeckResource, "/iedeck")
api.add_resource(IECardResource, "/iecard")