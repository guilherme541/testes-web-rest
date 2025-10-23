class DashboardPage:
    def __init__(self, driver):
        self.driver = driver

    def esta_logado(self):
        return "Logged In Successfully" in self.driver.page_source

    def obter_mensagem_boas_vindas(self):
        return "Logged In Successfully" if self.esta_logado() else ""