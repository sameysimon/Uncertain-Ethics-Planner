from Raspberry.Environment.MultiMoralMDP import MM_MDP
from copy import deepcopy
import random
class CarCatProblem(MM_MDP):
    def __init__(self, num_lanes=5, p_car=0.16, p_cat=0.09, total_time=10, rand_car_lanes=None, rand_cat_lanes=None) -> None:
        self.rules=[]
        self.TheoryClasses = [[CarCatProblem.Progress, CarCatProblem.MoveAndCollide, CarCatProblem.NewCats, CarCatProblem.NewCars]]
        self.num_lanes=num_lanes
        self.p_car=p_car
        self.car_speed = 1
        self.p_cat=p_cat
        self.cat_speed = 3
        self.total_time = total_time
        self.road_length=8

        if rand_car_lanes is None:
            rand_car_lanes = self.randLanes()
        if rand_cat_lanes is None:
            rand_cat_lanes = self.randLanes()
        self.rand_cat_lanes = rand_cat_lanes
        self.rand_car_lanes = rand_car_lanes

        self.stateFactory(self.default())

    def randLanes(self):
        r=[]
        for i in range(self.total_time):
            r.append(random.randint(0,self.num_lanes))
        return r

    def getActions(self, state):
        a = []
        if state.props['time']==self.total_time:
            return a
        a.append('N')
        if 0<state.props['lane']:
            a.append('W')
        if state.props['lane']<self.num_lanes-1:
            a.append('E')
        return a


    def default(self):
        p = {
            'time':0,
            'lane':2,
            'cars':{},
            'cats':{},
            'num_collisions':0,
            'num_cat_hits':0
        }
        for lane in range(self.num_lanes):
            p['cars'][lane]=[]
            p['cats'][lane]=[]
        return p

    def Progress(self, props, prob, action):
        for lane in range(self.num_lanes):
            props['cats'] = [pos - self.cat_speed for pos in self.props['cats'][lane]]
            props['cars'] = [pos - self.car_speed for pos in self.props['cars'][lane]]
        return (props, prob)

    def MoveAndCollide(self, props, prob, action):
        # Find next lane
        lane = props['lane']
        next_lane = lane
        if action=='W':
            next_lane-=1
        elif action=='E':
            next_lane+=1

        # Check for collision with cats and cars
        # Checking for cats/cars in this lane and the lane we're moving into.
        oncoming_cats, oncoming_cars = props['cats'][lane], props['cars'][lane]
        if lane != next_lane:
            oncoming_cats += props['cats'][next_lane]
            oncoming_cars += props['cars'][next_lane]

        cat_hit, car_hit = 0, 0

        for cat in oncoming_cats:
            if cat <= 0:
                cat_hit += 1
        for car in oncoming_cars:
            if car <= 0:
                car_hit += 1
        
        props['lane'] = next_lane
        props['num_collisions'] += car_hit
        props['num_cat_hits'] += cat_hit

        return (props, prob)

    def NewCats(self, props, prob, action):
        o=[(props, prob*(1-self.p_cat))]
        props_ = deepcopy(props)
        props_['cats'][self.rand_cat_lanes[props['time']]].append(self.road_length)
        o.append((props_, prob*self.p_cat))
        return o

    def NewCars(self, props, prob, action):
        o=[(props, prob*(1-self.p_car))]
        props_ = deepcopy(props)
        props_['cars'][self.rand_car_lanes[props['time']]].append(self.road_length)
        o.append((props_, prob*self.p_car))
        return o

    