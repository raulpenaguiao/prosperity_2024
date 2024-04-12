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
            curr_position : int = state.position[product]
            num_sell_orders : int = len(order_depth.sell_orders)
            num_buy_orders : int = len(order_depth.buy_orders)

            print("Acceptable price min : " + str(acceptable_price_min))
            print("Acceptable price max : " + str(acceptable_price_max))
            print("Current position : " + str(curr_position))
            print("Buy Order depth : " + str(num_sell_orders) + ", Sell order depth : " + str(num_buy_orders))



            index : int = 0
            ordered_sell_orders = [[ask, order_depth.sell_orders[ask]] for ask in order_depth.sell_orders]
            ordered_sell_orders.sort()
            while index < num_sell_orders:
                ask, ask_amount = ordered_sell_orders[index]
                if int(ask) > acceptable_price_min:
                    break
                
                amount_bought = max(-ask_amount, limits[product] - curr_position)
                print("BUY", str(amount_bought) + "x", ask)
                orders.append(Order(product, ask, ask_amount))

                curr_position += amount_bought
                if curr_position == limits[product]:
                    break
                index += 1

            
            index : int = 0
            ordered_buy_orders = [[ask, order_depth.buy_orders[ask]] for ask in order_depth.buy_orders]
            ordered_buy_orders.sort(reverse=True)
            while index < num_buy_orders:
                bid, bid_amount = ordered_buy_orders[index]
                if int(bid) < acceptable_price_max:
                    break
                
                amount_sold = max(bid_amount, limits[product] + curr_position)
                print("SELL", str(amount_sold) + "x", bid)
                orders.append(Order(product, bid, bid_amount))

                curr_position -= amount_sold
                if curr_position == -limits[product]:
                    break
                index += 1

            result[product] = orders
    
		    # String value holding Trader state data required. 
				# It will be delivered as TradingState.traderData on next execution.
        traderData = "SAMPLE" 
        
				# Sample conversion request. Check more details below. 
        conversions = 1
        return result, conversions, traderData