from sys import argv
import copy
def main():
    smallest_costs=float('inf')    #I will keep the costs for each recursion.
    mycosts=0       #The cost of the cell the person walked.
    current_position=[0,0]     #The current position of the person who tries to reach the opposite side.
    map_data=[]      #I will keep the map in a list.
    cost_list=[]     #My first row is about costs.I need a list to keeep them :)
    with open(argv[1].strip(),"r") as input:
        input_lines=input.readlines()
    
    for line in input_lines:
        for cost in line.strip().split():
            cost_list.append(cost)
        break
    cost1,cost2,cost3=map(int,cost_list)

    for line in input_lines[1:]:
        map_data.append(line.strip().split())
    
    while [] in map_data:
        map_data.remove([])
    
    count=1
    for mylist in map_data:
        if int(mylist[0])==1:
            current_position[0]=count
            current_position[1]=1
            break
        else:    
            count+=1

    cost_data_map = copy.deepcopy(map_data)      #I need a copy list to determine the costs.In recursion part,I am replacing some values with "X".It is getting problem unless I create a copy list.
    
    
    def get_current_value(cost_data_map, current_position):
        if type(current_position)==list:
            return int(cost_data_map[current_position[0] - 1][current_position[1] - 1])

    def right_trial(current_position):       #in recursion part,I am using this function in if statement. 
        mycopy=current_position.copy()
        if mycopy[1]!=len(map_data[0]):
            mycopy[1]+=1
            return mycopy
        
    def right(current_position):
        if current_position[1]!=len(map_data[0]):
            current_position[1]+=1
            return current_position
    
    def up_trial(current_position):
        mycopy=current_position.copy()
        if mycopy[0]!=1:
            mycopy[0]-=1
            return mycopy 
        
    def up(current_position):
        if current_position[0]!=1:
            current_position[0]-=1
            return current_position
    
    def down_trial(current_position):
        mycopy=current_position.copy()
        if mycopy[0]!=len(map_data):
            mycopy[0]+=1
            return mycopy
        
    def down(current_position):
        if current_position[0]!=len(map_data):
            current_position[0]+=1
            return current_position
    
    def left_trial(current_position):
        mycopy=current_position.copy()
        if mycopy[1]!=1:
            mycopy[1]-=1
            return mycopy

    def left(current_position):
        if current_position[1]!=1:
            current_position[1]-=1
            return current_position
    
    def cost(current_position):      #Each cost of the cell
        right_one_coordinate=[current_position[0],current_position[1]+1]
        upper_one_coordinate=[current_position[0]-1,current_position[1]]
        left_one_coordinate=[current_position[0],current_position[1]-1]
        down_one_coordinate=[current_position[0]+1,current_position[1]]
        right_up_coordinate=[current_position[0]-1,current_position[1]+1]
        left_up_coordinate=[current_position[0]-1,current_position[1]-1]
        left_down_coordinate=[current_position[0]+1,current_position[1]-1]
        right_down_coordinate=[current_position[0]+1,current_position[1]+1]

        cost3_check=[right_one_coordinate,upper_one_coordinate,left_one_coordinate,down_one_coordinate]
        cost2_check=[right_up_coordinate,left_up_coordinate,left_down_coordinate,right_down_coordinate]
    
        check_list=[right_one_coordinate,upper_one_coordinate,left_one_coordinate,down_one_coordinate,right_up_coordinate,left_up_coordinate,left_down_coordinate,right_down_coordinate]
        counter=0
        for location in check_list:
            if not 0 in location and location[1]!=len(cost_data_map[0])+1 and location[0]!=len(cost_data_map[0])+1:
                if get_current_value(cost_data_map,location)==0:
                    if location in cost3_check:
                        return cost3
                    if location in cost2_check:
                        return cost2
            counter+=1
        if counter==len(check_list):
            return cost1
    
    mycost_list=[]
    x_locations_list=[]
    mypath=[]
    path_dict={}
    x_locations=[]    #There will be some points to be marked as "X"
    visited=[]       #The cells I have ever visited.
    right_end_list=[]
    left_end_list=[]
    
    for i,right_end in enumerate(cost_data_map):
        if right_end[-1]=="1":
            right_end_list.append([i+1,len(right_end)])
    
    for i,left_end in enumerate(cost_data_map):
        if left_end[0]=="1":
            left_end_list.append([i+1,1])
    
    def total_cost(x_locations):
        mycost=0
        for position in x_locations:
            mycost+=cost(position)
        return mycost
    
    
    
    def route_finder(current_position):
        nonlocal x_locations
        nonlocal x_locations_list
        nonlocal smallest_costs
        nonlocal mycost_list
        
        motions_trial=[right_trial,up_trial,down_trial,left_trial]
        motions=[right,up,down,left]

        x_locations.append(current_position.copy())


        if current_position[1]==len(map_data[0]):
            if total_cost(x_locations)<smallest_costs:
                smallest_costs=total_cost(x_locations)
            mycost_list.append(smallest_costs)
            x_locations_list.append(x_locations.copy())
            return x_locations,smallest_costs,x_locations_list
        
        for move in motions_trial:  
            next_position = move(current_position)  
            if get_current_value(cost_data_map, next_position) == 1:
                if not next_position in x_locations:
                    if total_cost(x_locations)+cost(next_position)<smallest_costs:
                        motions[motions_trial.index(move)](current_position)
                        route_finder(current_position)
                        x_locations.pop()
                        current_position=x_locations[-1].copy()
        
        return x_locations_list
    
    def cheapest_list():
        mylist=[]    
        for left_edge in left_end_list:
            print(left_edge)
            for i in route_finder(left_edge):
                print(i)
                mylist.append((i,total_cost(i)))
            x_locations.clear()
            x_locations_list.clear()
            smallest_costs=float('inf')
            mycost_list.clear()
        return mylist

    # for i in route_finder([1,1]):
    #     print(i,total_cost(i))
    # x_locations.clear()
    # x_locations_list.clear()
    # smallest_costs=float('inf')
    # mycost_list.clear()
    # for i in route_finder([2,1]):
    #     print(i,total_cost(i))
    # x_locations.clear()
    # x_locations_list.clear()
    # smallest_costs=float('inf')
    # mycost_list.clear()
    # for i in route_finder([3,1]):
    #     print(i,total_cost(i))
    
    # print(cheapest_list())
    
    cheapest_list()
    
    
    
    # if cheapest_list():
    #     min_list = min(cheapest_list(), key=lambda x: x[1])
    # else:
    #     min_list=[]

    # def myfunc():
    #     if min_list:
    #         for position in min_list[0]:
    #             map_data[position[0]-1][position[1]-1]="X"
    #         print(f"Cost of the route: {min_list[1]}")
    #         for mylist in map_data:
    #             for i in mylist:
    #                 print(f"{i} ",end="")
    #             print()
    #     else:
    #         print("There is no possible route!")

    # myfunc()
    
    return current_position,right,up,down,left,cost
main()










    # def route_finder(current_position):
    #     nonlocal x_locations
    #     nonlocal mycosts
    #     nonlocal smallest_costs
    #     nonlocal visited
    #     nonlocal mypath

    #     motions_trial=[right_trial,up_trial,down_trial,left_trial]
    #     motions=[right,up,down,left]
    #     possible_route=False
    
    #     for move in motions_trial:  
    #         next_position = move()
    #         if get_current_value(cost_data_map, next_position) == 1:
    #             if next_position not in visited:
    #                 mid_path=False
    #                 if mycosts + cost(next_position) < smallest_costs:
    #                     mid_path=True
    #                     if not current_position in x_locations:    
    #                         x_locations.append(current_position.copy())
    #                     mycosts += cost(current_position)
    #                     motions[motions_trial.index(move)]()  
    #                     possible_route=True
    #                     break
    #                 else:                     
    #                     continue
    #     if current_position[1]==len(map_data[0]):
    #         x_locations.append(current_position.copy())
    #         mycosts+=cost(current_position)
    #         if mycosts<smallest_costs:
    #             smallest_costs=mycosts
    #             mypath=copy.deepcopy(x_locations)
    #             visited=copy.deepcopy(x_locations)
    #             mycosts=mycosts-cost(x_locations.pop())
    #             mycosts=mycosts-cost(x_locations[-1])
    #             current_position=x_locations[-1]
    #             x_locations.pop()
    #             route_finder()
    #         else:
    #             visited=copy.deepcopy(x_locations)
    #             mycosts=mycosts-cost(x_locations.pop())
    #             mycosts=mycosts-cost(x_locations[-1])
    #             current_position=x_locations[-1]
    #             x_locations.pop()
    #             route_finder()
    #     else:
    #         if not mid_path:
    #             print("buraya uğradım")
    #             visited.append(current_position.copy())
    #             mycosts=mycosts-cost(x_locations[-1])
    #             current_position=x_locations.pop()
    #         if not possible_route:
    #             return "There is no possible route!"
    #         route_finder()
            

    # for current_position in left_end_list:
    #     x_locations.clear()
    #     mycosts=0
    #     smallest_costs=0
    #     visited.clear()
    #     route_finder(current_position)
    #     path_dict.append({mypath:smallest_costs})
    # print("loop end") 