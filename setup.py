from setuptools import setup, find_packages

setup(
    name='PyFinances',  # Nome do pacote
    version='0.1',  # Versão do pacote
    description='''Este módulo Python oferece
        uma solução abrangente para gestão financeira
        pessoal, incluindo funcionalidades para converter
        e manipular datas, calcular períodos de meses fechados
        entre datas, e calcular valores futuros de investimentoS
        com base em juros compostos. Além disso, o módulo inclui
        classes para representar transações financeiras, contas 
        bancárias e investimentos, permitindo aos usuários acompanhar
        suas finanças de maneira organizada e precisa.''',
    long_description=open('README.md').read(),  # Descrição detalhada, pode ser o conteúdo de um README
    url='https://github.com/PedroVNeves/NES_POO_2',
    packages=find_packages(),
    install_requires=[ 
        'pytest',
    ],
)