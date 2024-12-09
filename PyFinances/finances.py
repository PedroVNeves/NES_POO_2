from datetime import datetime
from typing import List, Union

def converter_para_datetime(date: Union[str, datetime]) -> datetime:
    """
    Converte uma data para o formato datetime.
    
    Args:
        date (str | datetime): Data a ser convertida, podendo ser uma string no formato "dd/mm/yyyy"
                              ou um objeto datetime.
    
    Returns:
        datetime: Objeto datetime correspondente à data fornecida.
    
    Raises:
        ValueError: Se o valor fornecido não for uma string válida ou um objeto datetime.
    """
    if isinstance(date, str):
        try:
            # Caso a data seja passada como string, converter para datetime
            return datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            raise ValueError("A string da data deve estar no formato 'dd/mm/yyyy'.")
    elif isinstance(date, datetime):
        # Caso seja um objeto datetime, retornar diretamente
        return date
    else:
        raise ValueError("O argumento deve ser uma string no formato 'dd/mm/yyyy' ou um objeto datetime.")

def calcular_meses_fechados(data_inicial: Union[str, datetime], data_final: Union[str, datetime] = None) -> int:
    """
    Calcula a quantidade de meses fechados entre a data inicial e a data atual.
    
    Args:
        data_inicial (str | datetime): Data inicial no formato "dd/mm/yyyy" ou um objeto datetime.
    
    Returns:
        int: Quantidade de meses fechados.
    """
    # Converte a data inicial para datetime, reutilizando a função de conversão
    data_inicial = converter_para_datetime(data_inicial)
    data_final = converter_para_datetime(data_final)
    
    # Calcula a diferença em anos e meses
    anos = data_final.year - data_inicial.year
    meses = data_final.month - data_inicial.month
    
    # Total de meses
    meses_fechados = anos * 12 + meses
    
    # Garantir que só conte meses fechados
    if data_final.day < data_inicial.day:
        meses_fechados -= 1
    
    return meses_fechados

def calcular_juros_compostos(principal: float, taxa: float, data_inicio: Union[str, datetime], data_final: Union[str, datetime]) -> float:
    """
    Calcula o montante final com juros compostos.
    
    Args:
        principal (float): Capital inicial investido.
        taxa (float): Taxa de juros por período (em decimal, por exemplo, 5% = 0.05).
        data_inicio (str | datetime): Data de início do investimento.
        data_final (str | datetime): Data de término do investimento.
    
    Returns:
        float: Montante final após o período especificado.
    """
    tempo = calcular_meses_fechados(data_inicio, data_final)
    montante = principal * (1 + taxa) ** tempo
    return round(montante, 2)

class Transaction:
    def __init__(self, amount: float, date: Union[str, datetime], category: str, description: str):
        """
        Classe para representar uma transação financeira.
        
        Args:
            amount (float): Quantia da transação.
            date (str | datetime): Data da transação, no formato "dd/mm/yyyy" ou um objeto datetime.
            category (str): Categoria da transação.
            description (str): Descrição detalhada da transação.
        """
        self.amount = amount
        self.date = converter_para_datetime(date)
        self.category = category
        self.description = description

    def __str__(self) -> str:
        """
        Retorna uma representação em string da transação.
        
        Returns:
            str: Descrição da transação, incluindo descrição, quantia e categoria.
        """
        return f"{self.description}.R${self.amount}.{self.category} "
    
    def update(self, attribute: str, content: Union[str, float, datetime]):
        """
        Atualiza um atributo da transação.
        
        Args:
            attribute (str): Nome do atributo a ser atualizado ("amount", "date", "category" ou "description").
            content (str | float | datetime): Novo valor do atributo.
        """
        if attribute == 'amount':
            self.amount = content
        elif attribute == 'date':
            self.date = content
        elif attribute == 'category':
            self.category = content
        elif attribute == 'description':
            self.description = content

class Client:
    def __init__(self, name: str):
        """
        Classe para representar um cliente.
        
        Args:
            name (str): Nome do cliente.
        """
        self.name = name
        self.accounts: List[Account] = []
        self.investments: List[Investment] = []
    
    def add_account(self, account_name: str, balance: float):
        """
        Adiciona uma nova conta para o cliente.
        
        Args:
            account_name (str): Nome da conta.
            balance (float): Saldo inicial da conta.
        """
        self.accounts.append(Account(account_name, balance, self))
        

    def add_investment(self, investment_type: str, initial_amount: float, date_purchased: Union[str, datetime], rate_of_return: float):
        """
        Adiciona um novo investimento para o cliente.
        
        Args:
            investment_type (str): Tipo do investimento (ex.: "ações", "imobiliário").
            initial_amount (float): Quantia inicial investida.
            date_purchased (str | datetime): Data de compra do investimento no formato "dd/mm/yyyy" ou um objeto datetime.
            rate_of_return (float): Taxa de retorno esperada por período.
        """
        self.investments.append(Investment(investment_type, initial_amount, date_purchased, rate_of_return, self))
    
    def get_investments_by_type(self, investment_type: str):
        """
        Obtém um investimento pelo seu tipo.
        
        Args:
            investment_type (str): Tipo do investimento.
        
        Returns:
            Investment | None: Instância de Investment que corresponde ao tipo especificado, ou None se não encontrado.
        """
        for investment in self.investments:
            if investment.type == investment_type:
                return investment

    def get_account_by_name(self, name: str):
        """
        Obtém uma conta pelo seu nome.
        
        Args:
            name (str): Nome da conta.
        
        Returns:
            Account | None: Instância de Account que corresponde ao nome especificado, ou None se não encontrado.
        """
        for account in self.accounts:
            if account.name == name:
                return account   

    def get_net_worth(self) -> float:
        """
        Calcula o patrimônio líquido do cliente, somando o saldo das contas e o valor dos investimentos.
        
        Returns:
            float: Patrimônio líquido do cliente.
        """
        net_worth = 0
        for account in self.accounts:
            net_worth += account.balance
        for investment in self.investments:
            net_worth += investment.calculate_value()
        return net_worth

class Account:
    def __init__(self, name: str, balance: float, client: Client):
        """
        Classe para representar uma conta bancária de um cliente.
        
        Args:
            name (str): Nome da conta.
            balance (float): Saldo inicial da conta.
            client (Client): Instância da classe Client ao qual esta conta pertence.
        """
        self.name = name
        self.balance = balance
        self.transactions: List[Transaction] = []
        self.client: Client = client
    
    def add_transaction(self, amount: float, date: Union[str, datetime], category: str, description: str):
        """
        Adiciona uma nova transação à conta.
        
        Args:
            amount (float): Quantia da transação.
            date (str | datetime): Data da transação, no formato "dd/mm/yyyy" ou um objeto datetime.
            category (str): Categoria da transação.
            description (str): Descrição detalhada da transação.
        """
        self.transactions.append(Transaction(amount, date, category, description))
        self.balance += amount
    
    def get_transactions(self, start_date: Union[str, datetime] = None, end_date: Union[str, datetime] = None, category: str = None) -> List[Transaction]:
        """
        Obtém as transações da conta com base nos filtros de data e categoria.
        
        Args:
            start_date (str | datetime, optional): Data inicial para filtrar as transações.
            end_date (str | datetime, optional): Data final para filtrar as transações.
            category (str, optional): Categoria para filtrar as transações.
        
        Returns:
            List[Transaction]: Lista de transações que atendem aos filtros.
        """
        filtered_transactions = self.transactions
        
        # Filtrar por data de início
        start_date = converter_para_datetime(start_date)
        end_date = converter_para_datetime(end_date)
        if start_date:
            filtered_transactions = [t for t in filtered_transactions if t.date >= start_date]
        
        # Filtrar por data de término
        if end_date:
            filtered_transactions = [t for t in filtered_transactions if t.date <= end_date]
        
        # Filtrar por categoria
        if category != None:
            filtered_transactions = [t for t in filtered_transactions if t.category == category]
        
        return filtered_transactions

class Investment:
    def __init__(self, investment_type: str, initial_amount: float, date_purchased: Union[str, datetime], rate_of_return: float, client: Client):
        """
        Classe para representar um investimento de um cliente.
        
        Args:
            investment_type (str): Tipo do investimento (ex.: "ações", "imobiliário").
            initial_amount (float): Quantia inicial investida.
            date_purchased (str | datetime): Data de compra do investimento no formato "dd/mm/yyyy" ou um objeto datetime.
            rate_of_return (float): Taxa de retorno esperada por período.
            client (Client): Instância da classe Client ao qual este investimento pertence.
        """
        self.type = investment_type
        self.initial_amount = initial_amount
        self.date_purchased = converter_para_datetime(date_purchased)
        self.rate_of_return = rate_of_return
        self.client = client

    def calculate_value(self, date: Union[str, datetime] = None) -> float:
        """
        Calcula o valor atual do investimento com base na data fornecida.
        
        Args:
            date (str | datetime, optional): Data para calcular o valor atual do investimento.
                                            Se não fornecido, o cálculo será realizado com a data atual.
        
        Returns:
            float: Valor atual do investimento.
        """
        if date == None:
            date = datetime.now()
        current_value = calcular_juros_compostos(self.initial_amount, self.rate_of_return, self.date_purchased, date)
        return current_value

    def sell_investment(self, account_name: str) -> str:
        """
        Realiza a venda de um investimento e deposita o valor em uma conta do cliente.
        
        Args:
            account_name (str): Nome da conta para onde o valor do investimento será depositado.
        
        Returns:
            str: Mensagem indicando sucesso ou erro na venda do investimento.
        """
        investments = self.client.investments
        value = self.calculate_value()
        date = self.date_purchased
        accounts: List[Account] = self.client.accounts
        for account in accounts:
            if account.name == account_name:
                destination_account: Account = account
            else:
                return "Account not found"
        destination_account.add_transaction(
            value,
            date,
            "Investment Sale",
            f"Investment Sale. Value: R${value} deposited in account {destination_account.name} on day: {datetime.now()}")
        self.client.investments.remove(self)
        return "Investment sold successfully"

def generate_report(client: Client):
    """
    Gera um relatório do cliente, incluindo patrimônio líquido, contas e investimentos.
    
    Args:
        client (Client): Instância da classe Client para gerar o relatório.
    """
    print(f'''
    Nome: {client.name}

    Patrimônio líquido: {client.get_net_worth()}
    ''')
    print("Contas:")
    for account in client.accounts:
        print(f'''
            Nome da conta: {account.name}
            Valor da conta: {account.balance}
        ''')
    print("Investimentos:")
    for investment in client.investments:
        print(f'''
            Tipo de investimento: {investment.type}
            Valor atual do investimento: {investment.calculate_value()}
        ''')

def future_value(client: Client, date: Union[str, datetime]) -> float:
    """
    Calcula o valor futuro do patrimônio líquido do cliente em uma data específica.
    
    Args:
        client (Client): Instância da classe Client para calcular o valor futuro.
        date (str | datetime): Data futura para calcular o valor.
        
    Returns:
        float: Patrimônio líquido futuro do cliente na data especificada.
    """
    net_worth = 0
    for account in client.accounts:
        net_worth += account.balance
    for investment in client.investments:
        net_worth += investment.calculate_value(date)
    return net_worth