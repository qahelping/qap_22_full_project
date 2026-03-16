class LocalStorage:
    def __init__(self, driver):
        self.driver = driver

    def add_local_storage(self, key, value):
        self.driver.execute_script(f'window.localStorage.setItem("{key}", "{value}")')

    def get_local_storage(self, key):
        local_storage = self.driver.execute_script('return window.localStorage.getItem("user")')

        assert local_storage

    def get_all_local_storage(self):
        self.driver.execute_script("return Object.keys(window.localStorage);")


    def delete_all_local_storage(self, key):
        self.driver.execute_script('window.localStorage.removeItem("name");')
