from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string

class Trader:
    
    def run(self, state: TradingState):
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))

        # Orders to be placed on exchange matching engine
        result = {}

        products = ["STARFRUIT", "AMETHYSTS", "ORCHIDS", "GIFT_BASKET", "CHOCOLATE", "STRAWBERRIES", "ROSES"]
        limits = {
            products[0]:20,
            products[1]:20,
            products[2]:100,
            products[3]:60,
            products[4]:250,
            products[5]:350,
            products[6]:60,
        }
        means = {
            products[0]:5058.63895, 
            products[1]:9999.99975, 
            products[2]:1208.8047445255474, 
            products[3]:69953.65645, 
            products[4]:7797.2716, 
            products[5]:4007.6894, 
            products[6]:14332.1346
        } #Using data from day0
        stdevs = {
            products[0]:11.717389, 
            products[1]:1.496228, 
            products[2]:22.073794479817607, 
            products[3]:372.61117925726313, 
            products[4]:54.757879578902596, 
            products[5]:21.95996133034307, 
            products[6]:60.560166662738155
        } #Using data from day0
        
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []
            acceptable_price_max : float = means[product] + 2 * stdevs[product]
            acceptable_price_min : float = means[product] - 2 * stdevs[product]
            if product in state.position:
                curr_position : int = state.position[product]
                print("Current position on " + product + "is : " + str(curr_position))
            else:
                curr_position = 0
                print("Current position on " + product + "is : " + str(0))
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