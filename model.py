import random
import copy
from math import sin, cos, sqrt, atan2, radians

class ABC():
    def __init__(self, bee=10, limit=10, iterasi = 100):
        self.bee_count = bee
        self.max_limit = limit
        self.limit = [0 for i in range(bee)]
        self.iterasi = iterasi
        self.temp_fx = []
        self.temp_fit = []
        self.temp_bee = []

    def distance(self,city1, city2):
        # approximate radius of earth in km
        R = 6373.0
        # ubah float latitude longitute menjadi radians
        lat1 = radians(float(city1[0]))
        lon1 = radians(float(city1[1]))
        lat2 = radians(float(city2[0]))
        lon2 = radians(float(city2[1]))
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        return round(distance,4)

    # membuat cost matrix atau distance matrix
    def cost_matrix(self, coordinate):
        _coordinate = [x.split(",") for x in coordinate.split(";")]
        self.cities = [x[0] for x in _coordinate]
        self.cost_matrix = {}
        for i in range(len(self.cities)):
            self.cost_matrix[self.cities[i]] = {}
            for j in range(len(self.cities)):
                self.cost_matrix[self.cities[i]][self.cities[j]] = self.distance(_coordinate[i][1:],_coordinate[j][1:])

    def total_distance(self,route):
        res = 0
        for i in range(len(route)-1):
            res += self.cost_matrix[route[i]][route[i+1]]
        return res

    # menghitung object function -> f(x)
    def f(self, bee_routes):
        f = []
        for bee_route in bee_routes:
            f.append(self.total_distance(bee_route))
        return f

    # menghitung fitness fit
    def all_fitness(self, fx):
        fitness = []
        for f in fx:
            fitness.append(self.count_fit(f))
        return fitness
    
    def count_fit(self, fx):
        if(fx>0):
            return 1/(1+fx)
        else:
            return 1+abs(fx)
        return 0


    def prob(self, fitness,sum_fitness):
        return fitness/sum_fitness

    def all_prob(self, fitness):
        sum_fitness = sum(fitness)
        p = []
        for fitnes in fitness:
            p.append(self.prob(fitnes,sum_fitness))
        return p

    def best_route(self, bee_route, f, fit):
        index = 0
        min_fit = max(fit)
        for i in range(len(fit)):
            if(fit[i] == min_fit):
                index = i
        return [bee_route[index], f[index], fit[index]]

    def get_random_r(self):
        for i in range(len(self.bee[0])):
            r1 = random.randint(1,len(self.bee[0])-1)
            for j in range(len(self.bee[0])):
                while(True):
                    r2 = random.randint(1,len(self.bee[0])-1)
                    if(r2 != r1):
                        break
        return r1,r2

    def swap_destination(self,arr,p1,p2):
        arr[p1], arr[p2] = arr[p2], arr[p1]
        return arr

    def greedy_solution_eBee(self):
        for i in range(len(self.bee)):
            if (self.fit[i] < self.temp_fit[i]):
                self.limit[i] = 0
                self.bee[i] = self.temp_bee[i]
                self.fx[i] = self.temp_fx[i]
                self.fit[i] = self.temp_fit[i]
            else:
                self.limit[i] +=1

    def eBee(self):
        self.temp_bee.clear()
        self.temp_fx.clear()
        self.temp_fit.clear()
        self.temp_bee = copy.deepcopy(self.bee)
        for i in range(len(self.temp_bee)):
            r1,r2 = self.get_random_r()
            self.temp_bee[i] = self.swap_destination(self.temp_bee[i],r1,r2)
        self.temp_fx = self.f(self.temp_bee)
        self.temp_fit = self.all_fitness(self.temp_fx)
        self.greedy_solution_eBee()

    def oBee(self):
        self.temp_bee.clear()
        self.temp_fx.clear()
        self.temp_fit.clear()
        self.temp_bee = copy.deepcopy(self.bee)
        bee_index = 0
        index = 0
        proba = self.all_prob(self.fit)
        while(bee_index<len(self.bee)):
            #cek kalo index sourcenya habis, bakal ngulang dia ke index ke 0
            if(index == len(self.bee)-1):
                index = 0
            r = random.uniform(0,1)
            #kalo nilai r nya lebih kecil, di cek lagi rutenya
            if(r<proba[index]):
                #swap destination pada bee ke index
                for i in range(len(self.temp_bee)):
                    r1,r2 = self.get_random_r()
                    self.temp_bee[index] = self.swap_destination(self.temp_bee[index],r1,r2)
                #cek f(x)
                o_f = self.total_distance(self.temp_bee[index])
                #cek fitness
                o_fit = self.count_fit(o_f)
                #greedy solution
                if(self.fit[index]< o_fit):
                    self.limit[index] = 0
                    self.bee[index] = self.temp_bee[index]
                    self.fx[index] = o_f
                    self.fit[index] = o_fit
                else:
                    self.limit[index] += 1
                index +=1
                bee_index +=1
            else:
                index +=1

    def main(self, coordinate, start_destination):
        self.bee = []
        self.cost_matrix(coordinate)
        cities2 =copy.deepcopy(self.cities)
        for i in range(self.bee_count):
            mylist = copy.deepcopy(cities2)
            random.shuffle(mylist)
            mylist.remove(start_destination)
            mylist.insert(0,start_destination)
            self.bee.append(mylist)
        for i in range(self.iterasi):
            self.fx = list(self.f(self.bee))
            self.fit = list(self.all_fitness(self.fx))
            self.eBee()
            self.oBee()
        result =  self.best_route(self.bee,self.fx,self.fit)
        result[0].append(start_destination)
        result[1] = round(result[1] + self.cost_matrix[result[0][-2]][result[0][0]],2)
        return {
            "path" : result[0],
            "distance": result[1],
            "fitness": result[2]
        }