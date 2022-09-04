class ListContact:
    def __init__(self, first_name, last_name, address):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address

    def __eq__(self, other):
        if not isinstance(other, ListContact):
            return False

        return self.first_name == other.first_name and self.last_name == other.last_name and self.address == other.address


class FullContact(ListContact):
    def __init__(self, first_name, last_name, category, birthday, address):
        super().__init__(first_name, last_name, address)
        self.category = category
        self.birthday = birthday

    def __eq__(self, other):
        if not isinstance(other, FullContact):
            if isinstance(other, ListContact):
                return super.__eq__(self, other)
            return False

        return self.first_name == other.first_name and \
            self.last_name == other.last_name and \
            self.address == other.address and \
            self.birthday == other.birthday and \
            self.category == other.category
