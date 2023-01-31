# agent behaviors for buying, selling and holding based on the probability of trading p
def buy_sell_hold(p, amount_times):
    assert p <= 0.5, "p should be smaller than 0.5"
    psis = np.zeros(amount_times)
    dice_rolls = np.random.uniform(0, 1, amount_times)
    indices = np.nonzero(dice_rolls <= 2*p)

    for index in indices[0]:
        if np.random.randint(0,2) == 0:
            psis[index] = 1
        else:
            psis[index] = -1
    return psis

# model w noise
class Agent:
    def __init__(self, size) -> None:
        self.size = size

class Model:
    def __init__(self, p: float, n: int, size: int, k: int, omega: int, b: int) -> None:
        self.n = n
        self.p = p
        self.daily_return = 0
        self.trading_volume = 0
        self.k = k
        self.omega = omega
        self.daily_returns = []
        self.count = 0
        self.b = b

        self.daily_trading_volumes = []

        
    def distribute_opinion_groups(self) -> int:
        if self.b == 0:
            # number of opinion groups
            if self.daily_return == 0:
                c = self.n
            elif abs(self.daily_return) > self.n:
                c = 1
            else:    
                c = (self.n / abs(self.daily_return)) ** self.omega
                

        else:
            if self.daily_return != 0:
                mean = (self.n / abs(self.daily_return)) ** self.omega
                
            elif abs(self.daily_return) >= n:
                mean = 1
            else:
                mean = self.n
            
            c = np.random.normal(loc = mean, scale = math.sqrt(mean * self.b))  
                
        return int(c)

    def step(self):
        self.count += 1
        c = self.distribute_opinion_groups()
        print('C:', c)
        psis = buy_sell_hold(self.p, c)
        #print('psis:', psis)
        return_matrix = psis * int(self.n/c)
        #print('return_matrix:', return_matrix)
        trading_volume = np.sum(np.abs(return_matrix))
        self.daily_return = np.sum(return_matrix) #* k
        print('daily_return:', self.daily_return)
        self.daily_returns.append(self.daily_return)
        self.daily_trading_volumes.append(trading_volume)
        return self.count

def get_binheights(data_list, bin):
    list_of_bin_heights = []
    for dataset in data_list:
        binheights, bin_edges, _ = plt.hist(dataset, bins=bin)#, alpha=0.5, cumulative=-1, density=True, log = True, histtype='step')
        list_of_bin_heights.append(binheights)
    
    mean = np.mean(list_of_bin_heights, axis = 0)
    std = np.std(list_of_bin_heights, axis = 0)

    return mean, std

def normalise(returns):
    """
    Normalises an array
    """
    array = np.array(returns)
    return np.abs((array - array.mean())/array.std())

def run_ABM(p, n, size, k, omega, b, t, runs):
    ''' Runs the ABM model for a given number of runs and time steps. Returns a list of lists of daily returns and a list of lists of trading volume.'''
    ABM_sim_results_returns = []
    ABM_sim_results_volume = []
    for run in range(runs):
        model = Model(p, n, size, k, omega, b)
        for i in range(t):
            model.step()
        ABM_sim_results_returns.append(normalise(model.daily_returns))
        ABM_sim_results_volume.append(normalise(model.trading_volume))    
    ABM_sim_results_returns_array = np.array(ABM_sim_results_returns)
    ABM_sim_results_volume_array = np.array(ABM_sim_results_volume)
    return ABM_sim_results_returns, ABM_sim_results_volume

bin=np.logspace(start=0, stop=np.log(5), num=1000)
mean_bins, std_bins = get_binheights(ABM_sim_results_returns, bin)
plt.hist(mean_bins, bin, cumulative=-1, density=True, log = True, histtype='step')
plt.gca().set_xscale("log")
plt.show()