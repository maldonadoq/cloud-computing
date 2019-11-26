from scipy.optimize import fsolve, linprog
import matplotlib.pyplot as plt
import numpy as np

## basic parameter settings
k = 1e-28               # effective switched capacitance
tau = 0.002             # lentgh of slot time
phi = 0.002             # dropping task cost
omega = 1e6             # the bw of MEC in Hz
sigma = 1e-13           # the noise power of the receiver (in W)
p_tx_max = 1            # the maximum transmit power of mobile device (in W)
f_max = 1.5e9           # the maximum CPU-cycle frequency of mobile device (in Hz)
E_max = 0.002           # the maximum amout of battery output energy (in J)
L = 100                # the input size of the computation task (in bit)
X = 737.5               # the number of CPU cycles needed on processing one bit of task
W = L * X               # the number of CPU cycles needed on processing one task
E_H_max = 48e-6         # the upper bound of the energy arrive at the mobile device (in J)
p_H = E_H_max/(2*tau)   # the average Energy Harvesting (EH) power (in W)
g0 = pow(10, -4)        # the path-loss constant
d0 = 1                  # the relative distance between each mobile device and each MEC server
rho = 1                 # the probability that the computation task is requested

## parameter control
N = 5                   # the number of mobile devices
M = 3                   # the number of MEC servers
T = 1000                 # the number of time slot
tau_d = 0.002           # execution deadline (in second)
d = 50                  # the distance between the mobile device and the MEC server (in meter)
E_min = 0.02e-3         # the minimum amout of battery output energy
V = 1e-5                # the weight of penalty (the control parameter introduced by Lyapunov Optimization)
max_connects = 4        # the maximum number of processible mobile devices for each MEC server
min_distance = 10       # the minimum distance from mobile device to MEC server
max_distance = 50       # the maximum distance from mobile device to MEC server

E_max_hat = min(max(k * W * np.power(f_max,2), p_tx_max * tau), E_max)
theta = E_max_hat + V*phi/E_min

## storage
B = np.zeros((T,N))             # the battery energy level
B_hat = np.zeros((T,N))         # the virtual battery energy level
e = np.zeros((T,N))             # the amout of the harvested and stored energy
chosen_mode = np.zeros((T,N))   # {0: local, 1: remote, 2: drop, 3: no task request}
chosen_server = np.zeros((T,N)) # record the index of chosen server for each mobile device if its choice is MEC server execution
f = np.zeros((T,N))             # the CPU-cycle frequency of local execution
p = np.zeros((T,N))             # the transmit power of computation offloading

mobile_exe_cost = np.zeros((T,N))       # the mobile execution cost (delay)
server_exe_cost = np.zeros((T,N))       # the MEC server execution cost (delay)
final_chosen_cost = np.zeros((T,N))     # the final execution delay under currently chosen modes

mobile_exe_E = np.zeros((T,N))          # the energy consumption for mobile execution
server_exe_E = np.zeros((T,N))          # the energy consumption for MEC server execution
final_chosen_E = np.zeros((T,N))        # the energy consumption of the final chosen modes

if __name__ == "__main__":
    
    t = 0
    while(t < T-1):
        print('Time slot: ', t)
        # allocate storage for mode-chosen
        J_m = np.zeros(N)                       # the matrices for J_m values
        J_s = np.zeros((N,M))                   # the matrices for J_s values
        J_d = V * phi                           # the value of J_d
        p_mat = np.zeros((N,M))                 # the matrix for transmit power
        server_cost_mat = np.zeros((N,M))       # the matrix for MEC server execution cost
        server_E_mat = np.zeros((N,M))         # the matrix for energy consumption of MEC server
        int_goal = np.zeros(N * (M+2))          # the vector of optimization goal for intlinprog
        intcon = np.arange(N * (M + 2))         # the vector of optimization variable for intlinprog

        #initialization
        # generate the virtual battery energy level
        B_hat[t:] = B[t:] - theta
        # generate the channel power gain (from each mobile device to each MEC sever)
        E_H_t = np.random.uniform(0, E_H_max)
        distances = np.random.uniform(min_distance, max_distance, (N, M))
        gamma = np.random.exponential(1, (N,M))
        h_mat = g0 * gamma * np.power(d0/distances, 4)
        
        # step 1: for each mobile device, choose the initial mode
        for i in range(N):
            # step 1.1: get the optimal energy harvesting no matter whether task is requested
            E_H_t = np.random.uniform(0, E_H_max)
            if(B_hat[t,i] <= 0):
                e[t,i] = E_H_t

            # step 1.2: get the (initial) optimal computation offloading strategy generate the task request
            zeta = np.random.binomial(1, rho)
            if(zeta == 0):
                # chosen mode has to be 3
                chosen_mode[t, i] = 3
            else:
                # step 1.2.1: solve the optimization problem $\mathcal{P}_{ME}$ (f(t, i) > 0)
                # calculate f_L and f_U

                f_L = max(np.sqrt(E_min / (k * W)), W / tau_d)
                f_U = min(np.sqrt(E_max / (k * W)), f_max)

                if(f_L <= f_U):
                    # the sub-problem is feasible
                    if(B_hat[t,i] < 0):
                        f_0 = np.power(V / (-2 * B_hat[t, i] * k) ,1/3)
                    else:
                        # complex number may exist, which may lead to error
                        f_0 = np.power(V / (2 * B_hat[t, i] * k) ,1/3)

                    if((B_hat[t,i] >= 0) or ((B_hat[t,i] < 0) and (f_0 > f_U))):
                        f[t,i] = f_U
                    elif((B_hat[t,i] < 0) and (f_L <= f_0) and (f_0 <= f_U)):
                        f[t,i] = f_0
                    elif((B_hat[t,i] < 0) and (f_0 < f_L)):
                        f[t,i] = f_L

                    # check if f[t.i] is zero
                    if(f[t,i] == 0):
                        print('   something wrong! f is 0  [ME]')

                    # calculate the delay of mobile exec
                    mobile_exe_cost[t,i] = W / f[t,i]
                    # calculate the energy consumption of mobile exec
                    mobile_exe_E[t,i] = k * W * np.power(f[t,i], 2)
                    # calculate the value of optimization goal          |   
                    J_m[i] = -B_hat[t,i] * k * W * (np.power(f[t,i], 2) + V * W / f[t,i])
                else:
                    # the sub-problem is not fasible
                    #print('Mobile: Nt fasible')
                    f[t,i] = 0
                    mobile_exe_cost[t,i] = 0
                    mobile_exe_E[t,i] = 0
                    J_m[i] = 100

                # step 1.2.2: solve the optimization problem p[t, i] > 0
                # calculate J_s(i, j) from mobile device i to each MEC server j

                for j in range(M):
                    h = h_mat[i,j]

                    E_tmp = sigma * L * np.log(2) / (omega * h)
                    p_L_taud = (np.power(2, L/(omega * tau_d)) - 1) * sigma / h

                    # calculate p_L
                    if(E_tmp >= E_min):
                        p_L = p_L_taud
                    else:
                        # calculate p_E_min
                        y = lambda x: x * L - omega * np.log2(1 + (h * x) / sigma) * E_min
                        p_E_min = fsolve(y, 0.2)
                        p_L = max(p_L_taud, p_E_min)
                    
                    if(E_tmp >= E_max):
                        p_U = 0
                    else:
                        # calculate p_E max
                        y = lambda x: x * L - omega * np.log2(1 + (h * x) / sigma) * E_max
                        p_E_max = fsolve(y,100)
                        p_U = min(p_tx_max, p_E_max)
                    
                    #print('p_L: ',p_L)
                    #print('p_U: ',p_U)
                    if(p_L <= p_U):
                        # the sub-problem is feasible
                        # calculate p_0
                        vir_bat = B_hat[t,i]
                        
                        y = lambda x: vir_bat * np.log2(1 + h*x/sigma) + h*(V - vir_bat*x) /(np.log(2) * (sigma + h*x))
                        p_0 = fsolve(y, 0.5)

                        if((B_hat[t,i] >= 0) or ((B_hat[t,i] < 0) and (p_U < p_0))):
                            p_mat[i,j] = p_U
                        elif((B_hat[t,i] < 0) and (p_L > p_0)):
                            p_mat[i,j] = p_L
                        elif((B_hat[t,i] <0) and (p_L <= p_0) and (p_0 <= p_U)):
                            p_mat[i,j] = p_0

                        # check wheter p_mat[i,j] is zero
                        if(p_mat[i,j] == 0):
                            print('   something wrong! p is 0  [SE]')
                        
                        # calculate the delay of MEC server exec
                        server_cost_mat[i,j] = L / (omega * np.log2(1 + (h * p_mat[i,j] / sigma)))
                        # calculate the energy consumption of MEC server exec
                        server_E_mat[i,j] = p_mat[i,j] * server_cost_mat[i,j]
                        # calculate the value of optimization goal
                        J_s[i,j] = (-B_hat[t,i] * p_mat[i,j] + V) * server_cost_mat[i,j]
                    else:
                        # the sub-problem is not feasible
                        #print('MEC: Not fasible')
                        p_mat[i,j] = 0
                        server_cost_mat[i,j] = 0
                        server_E_mat[i,j] = 0
                        J_s[i,j] = 100

                # prepare the optimization goal
                #int_goal[i*(M+2): (i+1)*(M+2)] = [J_m[i], J_d, J_s[i,0], J_s[i,1], J_s[i,2], J_s[i,3], J_s[i,4], J_s[i,5], J_s[i,6], J_s[i,7]]
                int_goal[i*(M+2): (i+1)*(M+2)] = [J_m[i], J_d, J_s[i,0], J_s[i,1], J_s[i,2]]

        # step 2: choose the optimal execution mode with intlinprog (bug exists!!!)
        # prepare A, a matrix with size (N+M, N*(M+2))

        A_up = np.zeros((N, N*(M+2)))
        for m in range(N):
            for n in range(m*(M+2), (m+1)*(M+2)):
                A_up[m,n] = 1
        
        tmp1 = np.identity(M)
        tmp2 = np.zeros((M,2))
        tmp3 = np.concatenate((tmp2,tmp1), axis=1)
        A_down = tmp3
        for m in range(N-1):
            A_down = np.concatenate((A_down,tmp3), axis=1)
        
        int_A = np.concatenate((A_up,A_down), axis=0)

        # prepare b, a vector with length N+M
        int_b = np.concatenate((np.ones(N), np.ones(M)*max_connects), axis=0)
        
        # obtain the computation result
        int_res = linprog(int_goal, int_A, int_b, None, None, (0,1))
        #int_res = linprog(intcon, int_A, int_b, None, None, (0,1))

        #print(int_res, '\n')        
        #print(int_res.x.shape)
        #print(int_res.x, '\n')
        #print(int_res.success)

        for m in range(N):
            minit = m*(M+2)
            for n in range(minit, (m+1)*(M+2)):
                if(int_res.success):
                    if(n == minit):
                        chosen_mode[t, m] = 0
                        final_chosen_cost[t, m] = mobile_exe_cost[t, m]
                        final_chosen_E[t, m] = mobile_exe_E[t, m]
                    elif(n == minit + 1):
                        chosen_mode[t, m] = 2
                        final_chosen_cost[t, m] = phi
                        final_chosen_E[t, m] = 0
                    else:
                        chosen_mode[t, m] = 1
                        
                        # get the chosen MEC server j
                        j = n - minit - 2
                        chosen_server[t, m] = j
                        server_exe_cost[t, m] = server_cost_mat[m, j]
                        final_chosen_cost[t, m] = server_cost_mat[m, j]
                        server_exe_E[t, m] = server_E_mat[m, j]
                        final_chosen_E[t, m] = server_E_mat[m, j]

        B[t+1] = B[t] - final_chosen_E[t] + e[t]
        t += 1

    # 1. the battery energy level vs. time slot
    plt.figure(1)
    plt.title('Evolution of battery energy level')
    plt.xlabel('time slot')
    plt.ylabel('battery energy level')
    for i in range(N):
        plt.plot(np.arange(T), B[:,i], linewidth=0.5)
    plt.plot(np.arange(T), np.full(T, theta + E_H_max), linewidth=0.5)

    # 2. the average execution cost vs. time slot
    plt.figure(2)
    plt.title('Evolution of average execution cost')
    plt.xlabel('time slot')
    plt.ylabel('average execution cost')

    accumulated = 0
    avg_cost = np.zeros((T,N))

    for i in range(N):
        request_num = 0
        for t in range(T):
            accumulated += final_chosen_cost[t,i]
            if(chosen_mode[t,i] != 3):
                request_num += 1
            
            avg_cost[t,i] = accumulated / request_num
        plt.plot(np.arange(T), avg_cost[:,i] , linewidth=0.75, label = 'Mobile ' + str(i+1))
    plt.legend()

    plt.show()