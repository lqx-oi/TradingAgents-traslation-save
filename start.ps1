#cd F:\TradingAgents
conda activate tradingagents
pip install -r requirements.txt
$env:FINNHUB_API_KEY = 
$env:OPENAI_API_KEY = 
$env:OPENAI_API_BASE = 
python -m cli.main