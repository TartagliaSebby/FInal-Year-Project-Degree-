import numpy
import random
import pygad
#from sqlalchemy.engine.row import LegacyRow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text,select,delete, update
from database import db, orders, pick_list,assigned_orders
from sqlalchemy.orm import sessionmaker, Session
import json

#database connection
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="Sebas",
    password="FypDatabase",
    hostname="Sebas.mysql.pythonanywhere-services.com",
    databasename="Sebas$FYP",
)
engine = db.create_engine(SQLALCHEMY_DATABASE_URI,{"pool_recycle": 299})

session = sessionmaker(bind=engine)
Session =session()


#daily maintenance of the tables (deleting temporary tables)
with engine.connect() as connection:
    connection.execute(text("delete from assigned_orders where 1=1"))
    connection.execute(text("delete from instruction where 1=1"))
    connection.execute(text("delete from received_items where 1=1"))
    connection.execute(text("delete from pick_list where 1=1"))

# genetic algorithm part
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


def createOrderObjects(orders, inventory): # orders = orders to be fulfilled (list of all rows from query), inventory =  item location and quantity in each location
    #inventory should be dictionary {"item_id": {"i":{"location":location, "quantity": quantity}}} i=1,2,3 i.e first second and third instance of item from query
    orderIdIndex=[]
    orderList=[]
    for orderItem in orders: #order item should be 1 row from query
        ord_id = orderItem.order_id
        if ord_id not in orderIdIndex:
            orderIdIndex.append(ord_id)
            orderList.append(Order(ord_id,[]))
        x=True
        ind = 1
        quantityNeeded = orderItem.quantity
        #create item location based on the quantity/location available in inventory
        while (x):
            inventoryQuantity = int(inventory[str(orderItem.item_id)][str(ind)]["quantity"])
            if  inventoryQuantity >= quantityNeeded:
                newQuant = int(inventory[str(orderItem.item_id)][str(ind)]["quantity"]) - quantityNeeded
                inventory[str(orderItem.item_id)][str(ind)]["quantity"] = newQuant
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

def splitOrders(orderList,numOfEmp):
    splitedOrders = []
    numOfOrd = len(orderList)
    ordPerEmp = int(numOfOrd/numOfEmp)
    extraOrds = numOfOrd%numOfEmp
    #assign orders to employees evenly
    for i in range (0, numOfEmp):
        splitedOrders.append(orderList[ordPerEmp*i:ordPerEmp*(i+1)])
    #assign left over orders to some employees
    indLeftOrd = ordPerEmp * numOfEmp
    for i in range (0,extraOrds):
        splitedOrders[i].append(orderList[indLeftOrd+i])
    return splitedOrders

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
    midPoint = rackLength/2
    distance = 0
    currentAisle = pickItems[0].getAisle()
    lastAisle = pickItems[len(pickItems)-1].getAisle()
    aisleStartIndex = 0
    #variable to check if the picker starts from the top or bottom of the racks (to achieve the combined routing strategy)
    fromBottom = True
    i =1
    end = len(pickItems)
    while(i<end ):
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
            #when picker's last item is past the midpoint start on the top when entering the next aisle
            #adds the distance the picker walks to reach the top/bottom of the ailse
            if(destBay >midPoint):
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




#start of program/script
with engine.connect() as connection:
    orderRows = connection.execute(text("SELECT order_ids FROM picking_parameters")).fetchall()
    employeeRows =connection.execute(text("SELECT employee_ids FROM picking_parameters")).fetchall()
    ordersJson = json.loads(orderRows[0].order_ids)
    employeesJson = json.loads(employeeRows[0].employee_ids)
    inventoryLoc = connection.execute(text("""
            SELECT il.item_id, il.quantity, location
            FROM item_location il
            WHERE item_id IN(
                SELECT item_id
                FROM order_item
                WHERE order_id IN ({})
            )
            ORDER BY il.item_id
    """.format(ordersJson["order_id"]))).fetchall()
    order_itemRow = connection.execute(text("SELECT order_id, item_id, quantity from order_item WHERE order_id IN ( {} )".format(ordersJson["order_id"]))).fetchall()
# create orderlist and inventory list
order = order_itemRow
employee= employeesJson["employee_id"]


inventory ={}
for location in inventoryLoc:
    if location.item_id not in inventory:
        inventory[str(location.item_id)] = {"1":{"location" :str(location.location), "quantity":str(location.quantity)}}
    else:
        size = len(inventory[str(location.item_id)])
        inventory[str(location.item_id)][str(size+1)] = {"location" :str(location.location), "quantity":str(location.quantity)}

#variables for fitness functipm
orderList = createOrderObjects(order, inventory)
employeeList = employee.split(",")

numOfEmp = len(employeeList)
numOfOrd = len(orderList)
def fitness_func(solution, solution_idx):
    distance = 0
    tempOrdList = []
    for i in range (0, len(solution)):
        tempOrdList.append(orderList[solution[i]])
    random.shuffle(tempOrdList)
    splitedOrd = splitOrders(tempOrdList, numOfEmp)

    #calculate distance for each pickList and sum up distance
    for pickList in splitedOrd:
        itemsList =[]
        for order in pickList:
            itemsList.extend(order.items)
        sortItems(itemsList)
        distance += calculateDist(itemsList)
    fitness = -distance
    return fitness

#variables to tweak to optimise Genetic Algo
num_generations = 100
num_parents_mating = 10
sol_per_pop = 60
num_genes = len(orderList)
ga_instance = pygad.GA(num_generations=num_generations,
                    num_parents_mating=num_parents_mating,
                    fitness_func=fitness_func,
                    sol_per_pop=sol_per_pop,
                    num_genes=num_genes,
                    gene_type=int,
                    allow_duplicate_genes=False,
                    crossover_type="uniform",
                    crossover_probability= 0.1,
                    mutation_type="adaptive",
                    mutation_probability=[0.4,0.01],
                    #mutation_num_genes = [int(num_genes/4),2],
                    parent_selection_type="sss",
                    gene_space={'low':0,'high':len(orderList)},
                    keep_elitism=int(sol_per_pop/4),
                    #stop_criteria=["saturate_20"],
                    suppress_warnings=True,
                    save_best_solutions=True
                    )
ga_instance.run()
#clear old pickList and store new pick_list
with engine.connect() as conn:
    conn.execute(("delete from pick_list where 1=1"))
ind_sol =ga_instance.best_solutions[ga_instance.best_solution_generation]
splitedAssigned = splitOrders(orderList, numOfEmp)
x=0
y=0
for pickList in splitedAssigned:

    itemsinList =[]
    for order in pickList:
        Session.add(assigned_orders(order_id = order.orderId, emp_id = employeeList[x]))
        Session.commit()
        itemsinList+= order.items
    x+=1
    sortItems(itemsinList)
    FPickList={}
    i=0
    for item in itemsinList:
        FPickList[str(i)] ={"item_id":item.itemId, "location":item.location, "quantity": item.quantity}
        i+=1
        #picklists contain item_id quantity and location and //order id  
    pl = pick_list(emp_id = employeeList[y], pick_list = FPickList)
    y+=1
    Session.add(pl)
    Session.commit()
    Session.close
# update assigned order status to "picking"
with engine.connect() as connection:
    connection.execute(text("update orders set order_status = 'picking' where order_id in({})".format(ordersJson["order_id"])))