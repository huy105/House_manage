
def get_valid_input(input_string, valid_options):
    input_string += " ({}) ".format(", ".join(valid_options))
    response = input(input_string)
    while response.lower() not in valid_options:
        response = input(input_string)
    return response

class Property:
    def __init__(self, square_feet='', beds='',
        baths='', **kwargs):
            super().__init__(**kwargs)
            self.square_feet = square_feet
            self.num_bedrooms = beds
            self.num_baths = baths
    
    def display(self):
        print("PROPERTY DETAILS")
        print("================")
        print("square footage: {}".format(self.square_feet))
        print("bedrooms: {}".format(self.num_bedrooms))
        print("bathrooms: {}".format(self.num_baths))
        print()
    
    def prompt_init():
        return dict(square_feet=input("Enter the square feet: "),
                beds=input("Enter number of bedrooms: "),
                baths=input("Enter number of baths: "))
    
    prompt_init = staticmethod(prompt_init)


class Apartment(Property):
    valid_laundries = ("coin", "ensuite", "none")
    valid_balconies = ("yes", "no", "solarium")
    
    def __init__(self, balcony='', laundry='', **kwargs):
        super().__init__(**kwargs)
        self.balcony = balcony
        self.laundry = laundry
    
    def display(self):
        super().display()
        print("APARTMENT DETAILS")
        print("laundry: %s" % self.laundry)
        print("has balcony: %s" % self.balcony)
    
    def prompt_init():
        parent_init = Property.prompt_init()
        
        laundry = get_valid_input(
            "What laundry facilities does "
            "the property have? ", 
            Apartment.valid_laundries)
        
        balcony = get_valid_input(
            "Does the property have a balcony? ",
            Apartment.valid_balconies)
        
        parent_init.update({ "laundry": laundry, "balcony": balcony})
        
        return parent_init
    
    prompt_init = staticmethod(prompt_init)

class House(Property):
    valid_garage = ("attached", "detached", "none")
    valid_fenced = ("yes", "no")
    def __init__(self, num_stories='',
        garage='', fenced='', **kwargs):
        super().__init__(**kwargs)
        self.garage = garage
        self.fenced = fenced
        self.num_stories = num_stories
    
    def display(self):
        super().display()
        print("HOUSE DETAILS")
        print("# of stories: {}".format(self.num_stories))
        print("garage: {}".format(self.garage))
        print("fenced yard: {}".format(self.fenced))
    
    def prompt_init():
        parent_init = Property.prompt_init()
        
        fenced = get_valid_input("Is the yard fenced? ", House.valid_fenced)
        
        garage = get_valid_input("Is there a garage? ", House.valid_garage)
        
        num_stories = input("How many stories? ")
        
        parent_init.update({
            "fenced": fenced,
            "garage": garage,
            "num_stories": num_stories
        })
        
        return parent_init
    
    prompt_init = staticmethod(prompt_init)


class Purchase:
    def __init__(self, price='', taxes='', **kwargs):
        super().__init__(**kwargs)
        self.price = price
        self.taxes = taxes
    
    def display(self):
        super().display()
        print("PURCHASE DETAILS")
        print("selling price: {}".format(self.price))
        print("estimated taxes: {}".format(self.taxes))
    
    def prompt_init():
        return dict(
        price=input("What is the selling price? "),
        taxes=input("What are the estimated taxes? "))
    
    prompt_init = staticmethod(prompt_init)
    
class Rental:
    def __init__(self, furnished='', utilities='',
        rent='', **kwargs):
        super().__init__(**kwargs)
        self.furnished = furnished
        self.rent = rent
        self.utilities = utilities
    
    def display(self):
        super().diplay()
        print("RENTAL DETAILS")
        print("rent: {}".format(self.rent))
        print("estimated utilities: {}".format(self.utilities))
        print("furnished: {}".format(self.furnished))
    
    def prompt_init():
        return dict(
        rent = input("What is the monthly rent? "),
        utilities = input("What are the estimated utilities? "),
        furnished = get_valid_input("Is the property furnished? ", ("yes", "no")))
 
    prompt_init = staticmethod(prompt_init)


class HouseRental(Rental, House):
    
    def prompt_init():
        init = House.prompt_init()
        init.update(Rental.prompt_init())
        return init
    
    prompt_init = staticmethod(prompt_init)


class ApartmentRental(Rental, Apartment):
    def prompt_init():
        init = Apartment.prompt_init()
        init.update(Rental.prompt_init())
        return init
 
    prompt_init = staticmethod(prompt_init)


class ApartmentPurchase(Purchase, Apartment):
    def prompt_init():
        init = Apartment.prompt_init()
        init.update(Purchase.prompt_init())
        return init
    
    prompt_init = staticmethod(prompt_init)


class HousePurchase(Purchase, House):
    def prompt_init():
        init = House.prompt_init()
        init.update(Purchase.prompt_init())
        return init
    
    prompt_init = staticmethod(prompt_init)

class Agent:
    def __init__(self):
        self.property_list = []
    
    def display_properties(self):
        for property in self.property_list:
            property.display()

    type_map = {
        ("house", "rental"): HouseRental,
        ("house", "purchase"): HousePurchase,
        ("apartment", "rental"): ApartmentRental,
        ("apartment", "purchase"): ApartmentPurchase
    }

    def add_property(self):
        property_type = get_valid_input("What type of property? ",("house", "apartment")).lower()
        payment_type = get_valid_input("What payment type? ",("purchase", "rental")).lower()
    
        PropertyClass = self.type_map[(property_type, payment_type)]
        init_args = PropertyClass.prompt_init()
        self.property_list.append(PropertyClass(**init_args))

#Chỉ cần kế thừa là có thể gọi được phương thức từ superclass, cụ thể ở đây là đối tượng được tạo \
# ra từ class HouseRental hoàn toàn có thể sử dụng phương thức display

#Static method để gọi phương thức trực tiếp từ class mà không cần tạo ra một đối tượng \
# trong trường hợp trên đây nó dùng để gọi tới method prompt_init để nhập thông tin người dùng

#Khi gọi obj.display() ở class HouseRental nó sẽ gọi tới display ở class Rental trước \ 
# mà ở trong phương thức display() của class Rental gọi tới super().display() mặc dù nó \
# không kế thừa bất kỳ class nào nhưng nó sẽ gọi tới display csủa lớp thứ 2 mà HouseRental \
# kế thừa đó là class House và tiếp tục nó lại gọi tới display của class mà class House \
# kế thừa đó là Property.

#Trong class Agent type dùng để lựa chọn class, các class ở đây là 1 đối tượng có thể sử dụng \
# và gọi tới như một đối tượng bình thường hoặc là 1 kiểu dữ liệu nguyên thủy  \
# (int, float, string, boolean). Vì nó được gọi như bình thường nên biến PropertyClass chứa giá trị\ 
# là 1 class và vì vậy PropertyClass.prompt_init() có thể gọi tới method prompt_init.

#Với biến dict type_map trong class Agent ta có thể gọi tới self.type_map và indexing một cách như bt