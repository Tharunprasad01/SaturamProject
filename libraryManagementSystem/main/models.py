class Book:
    def __init__(self,id,title,author,genre,availablity):
        self.id = id
        self.title = title
        self.author = author
        self.genre = genre
        self.availablity = availablity

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return{
            'id':self.id,
            'title':self.title,
            'author':self.author,
            'genre':self.genre,
            'availablity':self.availablity
        }
