from flask_app.config.mysqlconnection import connectToMySQL

class Trip():
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.price = data['price']
        self.discount = data['discount']
        self.date = data['date']
        self.time = data['time']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.order_id = data['order_id']

    @classmethod
    def create_trip(cls,data):
        query = 'INSERT INTO trips (name, description, price, date, time,order_id) VALUES (%(name)s,%(description)s,%(price)s,%(date)s,%(time)s,%(order_id)s);'
        return connectToMySQL('tennessee_trekker_schema').query_db(query,data)

    @classmethod
    def show_all_trips(data):
        query = 'SELECT * FROM trips'
        results = connectToMySQL('tennessee_trekker_schema').query_db(query)

        trips = []
        for row in results:
            trips.append(Trip(row))
        return trips
