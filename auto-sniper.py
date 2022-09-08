import csv
import time
from datetime import datetime
from modules import MagicEden
from utils.solana import lamports_to_sol


max_fp = 3
min_fp = 0.2
collections_amount = 8
under_floor = 40
auto_list_floor = 0
delay = 20

def order_collections(popular_collections: list):
    
    def get_sales(collection: dict):
        
        return collection["txns"]
    
    ordered = sorted(popular_collections, key=get_sales, reverse=True)
    
    matching_collections = []
    
    for collection in ordered:
        
        fp = collection.get("fp")
        
        if fp:
            
            fp = lamports_to_sol(fp)
            
            if min_fp <= fp <= max_fp:
                
                matching_collections.append(collection)

            if len(matching_collections) == collections_amount:
                
                break
            
    return matching_collections


while True:
        
    popular_collections = MagicEden.get_popular_collections(limit=50, window="1h")

    if popular_collections:
        
        try:
                
            orderer_collections = order_collections(popular_collections)

            with open('me-sniper.csv', 'w') as f:
                
                csv_writer = csv.writer(f)
                
                csv_writer.writerow(
                    [
                        "Collection","MinPrice","MaxPrice","UnderFloor(%)","MinRank","MaxRank","Attributes","AutoListByPrice(%)","AutoListByFloor(%)"
                    ]
                )
                
                for collection in orderer_collections:
                        
                    csv_writer.writerow(
                        [
                            collection["collectionSymbol"], "", "", under_floor, "", "", "", "", auto_list_floor
                        ]
                    )
                    
        except Exception as e:
            
            print(datetime.now(), e)
            
            open('me-sniper.csv', 'w').close()
              
    else:
        
        print(datetime.now(), "unable to fetch popular collections")
        
        open('me-sniper.csv', 'w').close()

    time.sleep(delay)