from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string

class Trader:
    
    def run(self, state: TradingState):
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))

				# Orders to be placed on exchange matching engine
        result = {}

        products = ["STARFRUIT", "AMETHYSTS"]
        limits = {p:20 for p in products}
        means = {products[0]:5058.63895, products[1]:9999.99975} #Using data from day0
        stdevs = {products[0]:11.717389, products[1]:1.496228} #Using data from day0
        
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []
            acceptable_price_max : float = means[product] + 2 * stdevs[product]
            acceptable_price_min : float = means[product] - 2 * stdevs[product]

            if len(order_depth.sell_orders) != 0:
                best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                if int(best_ask) < acceptable_price_min:
                    print("BUY", str(-best_ask_amount) + "x", best_ask)
                    orders.append(Order(product, best_ask, -best_ask_amount))
    
            if len(order_depth.buy_orders) != 0:
                best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                if int(best_bid) > acceptable_price_max:
                    print("SELL", str(best_bid_amount) + "x", best_bid)
                    orders.append(Order(product, best_bid, -best_bid_amount))
            
            result[product] = orders
    
		    # String value holding Trader state data required. 
				# It will be delivered as TradingState.traderData on next execution.
        traderData = "SAMPLE" 
        
				# Sample conversion request. Check more details below. 
        conversions = 1
        return result, conversions, traderData