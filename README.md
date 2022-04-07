# CATS
CATS: Coin Automated Trading System

## Environments
	python 3.8
  	pyupbit
	numpy 1.19.5
  	pandas 1.35
  	prophet
  	neuralprophet
  
## Usage

Example:  

	python run.py

Arguments:  

    parser.add_argument('--access_key', default=None, type=str)
    parser.add_argument('--secret_key', default=None, type=str)
    
    parser.add_argument('--buy_ticker', default='KRW-ETH', type=str)
    parser.add_argument('--sell_ticker', default='ETH', type=str)
    
    parser.add_argument('--target_interval', default="minute240", type=str)
    parser.add_argument('--ma_interval', default="minute60", type=str)
    parser.add_argument('--ma_count', default=24, type=int)
    parser.add_argument('--model_name', default='np', type=str)
    
    parser.add_argument('--p_yield', default=1.02, type=float)
    parser.add_argument('--loss_cut', default=0.98, type=float)
