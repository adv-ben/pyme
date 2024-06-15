class order():
    def __init__(self, user_id, order_id, side, price, volume):
        self.user_id = user_id
        self.order_id = order_id
        self.side = side # buy or sell side limit order
        self.price = price
        self.volume = volume

    def output(self):
        print(self.user_id, self.order_id, self.side, self.price, self.volume)

class State():
    def __init__(self, buy_state=[], sell_state=[]):
        self.buy = buy_state
        self.sell = sell_state

    def buy(self):
        return self.buy
    
    def sell(self):
        return self.sell

class MatchingEngine():
    # Matching Engine
    # Calls all other relavant functions
    def __init__(self):
        self.state = State()

    def getBestBid(self):
        # get highest price, oldest bid
        # if no offers, returns None
        currentOrder = None
        for order in self.state.buy:
            if currentOrder is None:
                currentOrder = order
            else:
                if order.price > currentOrder.price:
                    currentOrder = order
                if order.price == currentOrder.price and order.id < currentOrder.id:
                    currentOrder = order
        return currentOrder
    
    def getBestAsk(self):
        # get lowest price, oldest ask
        # if no offers, returns None
        currentOrder = None
        for order in self.state.sell:
            if currentOrder is None:
                currentOrder = order
            else:
                if order.price < currentOrder.price:
                    currentOrder = order
                if order.price == currentOrder.price and order.id < currentOrder.id:
                    currentOrder = order
        return currentOrder

    def ordersCross(order1, order2):
        # returns wether 2 orders would execute if both existed
        if order1.side == order2.side:
            return False
        else:
            if order1.size == "buy":
                if order1.price >= order2.price:
                    return True
            elif order1.size == "sell":
                if order1.price <= order2.price:
                    return True
            return False

    def crossMarket(self, order):
        # returns wether the market is crossed
        bestBid = self.getBestBid()
        bestAsk = self.getBestAsk()
        return self.ordersCross(bestBid, order) or self.ordersCross(bestAsk, order)
        
    def placeOrder(self, order):
        # places an order in its corresponding order list
        # assumes that the order does not cross the market
        if order.side == "buy":
            if self.state.buy[0].price >= order.price:
                self.state.buy.insert(0, order)
            elif self.state.buy[-1].price <= order.price:
                self.state.buy.insert(len(self.state.buy), order)
            else:
                for idx, o in enumerate(self.state.buy):
                    if o.price >= order.price:
                        self.state.buy.insert(idx, order)
                        break
        elif order.side == "sell":
            if self.state.sell[0].price <= order.price:
                self.state.sell.insert(0, order)
            elif self.state.sell[-1].price >= order.price:
                self.state.sell.insert(len(self.state.sell), order)
            else:
                for idx, o in enumerate(self.state.sell):
                    if o.price <= order.price:
                        self.state.sell.insert(idx, order)
                        break
  
    def getBestCounterOrder(self, order):
        pass

    def executeOrders(self, counter_order, order):
        # update can be 0 1 or 2
        pass

    def returnState(self):
        return self.state.buy, self.state.sell

    def processOrder(self, order):
        if not self.crossMarket(order):
            # does not cross market, place order
            placeOrder(self, order)
        else:
            counter_order = getBestCounterOrder(self, order)
            update, counter_order, order = executeOrders(self, counter_order, order)
            if update == 0: # counter order exists, market no longer crossed, need to update
                placeOrder(self, counter_order)
            if update == 1: # order exists
                if not crossMarket(self, order):
                    placeOrder(self, order)
                    return None
                else:
                    # order exists, market crossed
                    processOrder(self, order)
        return None


