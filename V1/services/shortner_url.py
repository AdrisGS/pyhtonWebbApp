import random

class id_generator:
    # short = id_generator()
    # numero de supuestos registros existentes
    # id = 10000000000000000000000
    id = random.randrange(100000000000, 10000000000000)
    # id = random.choice([123123123, 98234816294, 9821391726301826, 12312978643, 347263495345, 12412419759754124, 975192460514346, 97539134086234])
    # Almacena el order_id en como identificador para no tener una url_id duplicado
    order2id = {}
    
    def url_id(self, order_id):
        if order_id in self.order2id:
            id = self.order2id[order_id]
            url_id = self.encode(id)
        else:
            # Almacena order_id
            self.order2id[order_id] = self.id
            url_id = self.encode(self.id)
            # increase cnt for next url
            self.id += 1
        
        return url_id
    
    def encode(self, id):
        # base 62 characters
        characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        base = len(characters)
        ret = []
        # convert base10 id into base62 id for having alphanumeric shorten url
        while id > 0:
            val = id % base
            ret.append(characters[val])
            id = id // base
        # since ret has reversed order of base62 id, reverse ret before return it
        return "".join(ret[::-1])


# print(short.url_id("sd.com"))
