import numpy
import pygad
from sqlalchemy.engine.row import LegacyRow
class Item():
    def __init__(self, itemId, location, quantity):
        self.itemId = itemId
        self.location = location
        self.quantity = quantity
    def getAisle(self):
        return int(self.location[0:2])
    def getRack(self):
        return self.location[3:4]
    def getBay(self):
        return int(self.location[5:6])
    def getLocation(self):
        return self.location

class Order():
    def __init__(self, orderId, items):
        self.orderId = orderId
        self.items = items
    
    def getItems(self):
        return self.items

# functions to process orders
def sortItems(pickItems):
    for i in range(1,len(pickItems)):
        point = pickItems[i].getBay() + (pickItems[i].getAisle()*10)
        pointItem = pickItems[i]
        j= i-1
        while j>=0 and point < (pickItems[j].getBay() + (pickItems[j].getAisle()*10)): 
            pickItems[j+1] = pickItems[j]                   
            j-=1
        pickItems[j+1] = pointItem 
    return pickItems
def changeAisle(fro, to ):
    return (to - fro) * 3
#moving 1 bay = 1 unit moving accross 1 aisle = 3 units
def calculateDist(pickItems):
    rackLength = 8
    distance = 0
    currentAisle = pickItems[0].getAisle()
    lastAisle = pickItems[len(pickItems)-1].getAisle()
    aisleStartIndex = 0
    #variable to check if the picker starts from the top or bottom of the racks (to achieve the combined routing strategy)
    fromBottom = True
    i =1
    end = len(pickItems) 
    while(i<end ):
        #print("compare curr" +str(currentAisle) +" last" + str(lastAisle))
        
        if currentAisle != pickItems[i].getAisle() or currentAisle == lastAisle:
            if currentAisle == lastAisle:
                i = len(pickItems)
                end = -1
            #The first Bay location of the first item and the last Bay location of the last item respectively
            startBay = pickItems[aisleStartIndex].getBay()
            endBay =pickItems[i-1].getBay()
            #check if the picker is entering the top or bottom of the aisle
            # adds the distance from the top/bottom to the last item in the aisle
            if fromBottom:
                #the last bay the picker will travel to in the aisle
                destBay = endBay
                distance += destBay
            else :
                destBay = startBay
                distance += rackLength - destBay
            #when picker's last item is >4 start on the top when entering the next aisle
            #adds the distance the picker walks to reach the top/bottom of the ailse
            if(destBay >4):
                distance += rackLength - destBay
                fromBottom = False
            else:
                distance += destBay
                fromBottom = True
            #move aisles
            if currentAisle != lastAisle:
                distance +=changeAisle (currentAisle, pickItems[i].getAisle())
                currentAisle = pickItems[i].getAisle()
                aisleStartIndex = i
        i+=1
    return distance

#!!!!!!!!!!!!!!!should check if the order can be fulfilled based on available items before getting to this part
#convert query data into objects for fitness function to calculate fitness
def createOrderObjects(orders, inventory): # orders = orders to be fulfilled (list of all rows from query), inventory =  item location and quantity in each location
    #inventory should be dictionary {"item_id": {"i":{"location":location, "quantity": quantity}}} i=1,2,3 i.e first second and third instance of item from query
    orderIdIndex=[]
    orderList=[]
    print(orders)
    for orderItem in orders: #order item should be 1 row from query
        ord_id = orderItem.order_id
        if ord_id not in orderIdIndex: #!!!!!!!
            orderIdIndex.append(ord_id)
            orderList.append(Order(ord_id,[]))
        x=True
        ind = 1
        quantityNeeded = orderItem.quantity
        #create item location based on the quantity/location available in inventory 
        while (x):
            inventoryQuantity = inventory[str(orderItem.item_id)][str(ind)]["quantity"]
            if  inventoryQuantity >= quantityNeeded:
                inventory[str(orderItem.item_id)][str(ind)]["quantity"] -= quantityNeeded
                index = orderIdIndex.index(ord_id)
                orderList[index].items.append(Item(orderItem.item_id, inventory[str(orderItem.item_id)][str(ind)]["location"], quantityNeeded))
                x=False    
            else:
                index = orderIdIndex.index(ord_id)
                orderList[index].items.append(Item(orderItem.item_id, inventory[str(orderItem.item_id)][str(ind)]["location"], inventoryQuantity))
                quantityNeeded -= inventoryQuantity
                inventory[str(orderItem.item_id)][str(ind)]["quantity"] = 0
                ind+=1
    return orderList

                                

def generatePickList(orders):

    #variables for fitness function
    
    



    function_inputs = [4,-2,3,5,-11,-4] # Function inputs.
    desired_output = 44 # Function output.
    def fitness_func(solution, solution_idx):
        fitness =0
        for i in range (0, len(orderList)):
            itemList=[]
            itemList.append(orderList[solution[i]])
            return fitness


    #variables to tweak to optimise Genetic Algo
    num_generations = 50
    num_parents_mating = 10
    sol_per_pop = 20
    num_genes = len(orderList)
    ga_instance = pygad.GA(num_generations=num_generations,
                        num_parents_mating=num_parents_mating,
                        fitness_func=fitness_func,
                        sol_per_pop=sol_per_pop,
                        num_genes=num_genes,
                        gene_type=int,
                        allow_duplicate_genes=False,
                        gene_space={'low':0,'high':len(orderList)}
                        )
    ga_instance.run()
    print(ga_instance.best_solution())
    print(len(orderList)-1)
    #ga_instance.plot_fitness()

