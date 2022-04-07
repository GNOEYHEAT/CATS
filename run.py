import wandb
import pyupbit
import time
import argparse
from model import *
from utils import *


def run(args):
    
    upbit = pyupbit.Upbit(args.access_key, args.secret_key)
    print("")
    print("autotrade run")
    print("")

    while True:
        
        try:
            
            temp = []
            krw = get_balance("KRW", upbit)
            btc = get_balance(args.sell_ticker, upbit)
            
            current_price = get_current_price(args.buy_ticker)
            
            if krw >= 5000:
                
                target_price = get_target_price(args.buy_ticker,
                                                args.target_interval,
                                                get_k(args.buy_ticker))
                
                ma_price = get_ma(args.buy_ticker,
                                  args.ma_interval,
                                  args.ma_count)
                
                predicted_price = get_predict_price(args.buy_ticker,
                                                    args.model_name)
                
                print("")
                print("current_price : ", current_price)
                print("target_price : ", target_price)
                print("ma_price : ", ma_price)
                print("predicted_price : ", predicted_price)
                print("")
                
                if target_price < current_price \
                and ma_price < current_price \
                and predicted_price > current_price:
                    upbit.buy_market_order(args.buy_ticker, krw*0.9995)
                    print("***autotrade buy***")
                    wandb.log({"buy_price" : current_price,
                               "ma_price" : ma_price,
                               "good_predicted_price" : predicted_price,
                               "yield_target_price" : target_price*args.p_yield,
                               "loss_cut_target_price" : target_price*args.loss_cut})
                    
            elif krw < 5000 and btc > 0:
                
                predicted_price = get_predict_price(args.buy_ticker,
                                                    args.model_name)
                    
                print("")
                print("current_price : ", current_price)
                print("yield_target_price : ", target_price*args.p_yield)
                print("loss_cut_target_price : ", target_price*args.loss_cut)
                print("predicted_price : ", predicted_price)
                print("")
                
                if target_price*args.p_yield < current_price \
                and predicted_price < current_price:
                    upbit.sell_market_order(args.buy_ticker, btc*0.9995)
                    print("***autotrade good sell***")
                    wandb.log({"good_price" : current_price,
                               "predict_price" : predict_price})
                    
                elif target_price*args.loss_cut > current_price \
                and predicted_price > current_price:
                    upbit.sell_market_order(args.buy_ticker, btc*0.9995)
                    print("***autotrade bad sell***")
                    wandb.log({"bad_price" : current_price,
                               "predict_price" : predict_price})
                        
                else:                
                    print("")
                    print("current_price : ", current_price)
                    print("yield_target_price : ", target_price*args.p_yield)
                    print("loss_cut_target_price : ", target_price*args.loss_cut)
                    print("")
                    wandb.log({"current_price" : current_price})
                    
            time.sleep(1)
            
        except:
            
            print("")
            print("autotrade error")
            print("")
            time.sleep(1)
    
    
if __name__ == '__main__':
    
    wandb.init(project="Coin")
    
    parser = argparse.ArgumentParser(description='CATS')
    
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
    
    args = parser.parse_args()
    wandb.config.update(args)
    run(args)