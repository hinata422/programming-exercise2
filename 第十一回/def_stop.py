class Stop:
    def __init__(self, id, name, lat, lng, routes):
        self.id = id
        self.name = name
        self.lat = lat
        self.lng = lng
        self.routes = routes

    def countRoutes(self):
        return len(self.routes)
