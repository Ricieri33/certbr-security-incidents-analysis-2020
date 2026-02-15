# Análise de Incidentes de Segurança - CERT.br (Jan–Jun 2020)

## Objetivo
Analisar o comportamento dos incidentes de segurança no primeiro semestre de 2020, identificando:
- Crescimento mensal
- Concentração por categoria
- Principais responsáveis pelas variações

## Tecnologias Utilizadas
- Python
- Pandas
- Matplotlib

## Principais Insights
- Houve aumento significativo em março de 2020.
- O crescimento foi impulsionado principalmente por Scan e DoS.
- Scan foi o tipo mais frequente no período.
- Junho apresentou o maior volume absoluto de incidentes.

## Estrutura do Projeto
```
certbr-security-incidents-analysis-2020/
├── data/
│   └── Dados.csv
├── images/
│   └── (gráficos gerados)
├── notebooks/
│   └── analise_certbr_2020.py
├── requirements.txt
└── README.md
```

## Como Executar

1. Clone o repositório:
git clone https://github.com/Ricieri33/certbr-security-incidents-analysis-2020.git

2. Instale as dependências:
pip install -r requirements.txt

3. Execute o script:
python notebooks/analise_certbr_2020.py

## Autor
Marcelo Ricieri  
2026