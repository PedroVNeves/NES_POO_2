from PyFinances.finances import *


Paulo = Client("Paulo")
Paulo.add_account('Inter',2000)
Paulo.add_investment('Ações',10000,"09/11/2024",0.01)
generate_report(Paulo)
print(f"Projeção para dezembro de 2025: {future_value(Paulo,"09/12/2025")}")