from scipy.optimize import fsolve
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
L = 1000                # the input size of the computation task (in bit)
X = 737.5               # the number of CPU cycles needed on processing one bit of task
W = L * X               # the number of CPU cycles needed on processing one task
E_H_max = 48e-6         # the upper bound of the energy arrive at the mobile device (in J)
p_H = E_H_max/(2*tau)   # the average Energy Harvesting (EH) power (in W)
g0 = pow(10, -4)        # the path-loss constant

## parameter control
T = 1000                # the number of time slot
tau_d = 0.002           # execution deadline (in second)
d = 50                  # the distance between the mobile device and the MEC server (in meter)
E_min = 0.02e-3         # the minimum amout of battery output energy (in J)
V = 1e-5                # the weight of penalty (the control parameter introduced by Lyapunov Optimization)
rho = 0.6               # the probability that the computation task is requested

E_max_hat = min(max(k * W * np.power(f_max,2), p_tx_max * tau), E_max)
theta = E_max_hat + V*phi/E_min

## storage
B = np.zeros(T)             # the battery energy level
B_hat = np.zeros(T)         # the virtual battery energy level
e = np.zeros(T)             # the amout of the harvested and stored energy (in J)
chosen_mode = np.zeros(T)   # {0: local, 1: remote, 2: drop, 3: no task request}
f = np.zeros(T)             # the CPU-cycle frequency of local execution
p = np.zeros(T)             # the transmit power of computation offloading
cost = np.zeros((T, 3))
E = np.zeros((T, 3))

if __name__ == "__main__":
    
    t = 0
    while(t < T-1):
        # generative the task request
        zeta = np.random.binomial(1, rho)
        # generative the virtual battery level
        B_hat[t] = B[t] - theta

        # step 1: get optimal energy harvesting
        E_H_t = np.random.uniform(0, E_H_max)

        if(B_hat[t] <= 0):
            e[t] = E_H_t

        # step 2: get optimal computation offloading strategy
        if(zeta == 0):
            # chosen mode has to be 3
            chosen_mode[t] = 3
        else:
            # chosen_mode is chosen from [0,1,2]
            # channel power
            h = np.random.exponential(g0 / np.power(d, 4))

            # step 2.1: solve the optimization problem P_ME
            # calculate f_L and f_U
            f_L = max(np.sqrt(E_min/(k*W)), W/tau_d)
            f_U = min(np.sqrt(E_max/(k*W)), f_max)

            if(f_L <= f_U):
                # the sub-problem is feasible

                if(B_hat[t] < 0):
                    f_0 = np.power(V / (-2 * B_hat[t] * k), 1/3)
                else:
                    # complex number
                    f_0 = -np.power(V / (2 * B_hat[t] * k), 1/3)
                
                if((B_hat[t] >= 0) or ((B_hat[t] < 0) and (f_0 > f_U))):
                    f[t] = f_U
                elif((B_hat[t] < 0) and (f_L <= f_0) and (f_0 <= f_U)):
                    f[t] = f_0
                elif((B_hat[t] < 0) and (f_0 < f_L)):
                    f[t] = f_L

                # check if f[t] is zero
                if(f[t] == 0):
                    print('   something wrong! f is 0  [ME]')

                # calculate the delay of mobile exec
                cost[t,0] = W / f[t]
                # calculate the energy consumption of mobile exec
                E[t,0] = k * W * np.power(f[t], 2)
                # calculate the value of optimization goal
                J_m = -B_hat[t] * k * W * np.power(f[t], 2) + V * W / f[t]

            else:
                # the sub-problem is not fasible
                f[t] = 0
                cost[t, 0] = 0
                E[t, 0] = 0
                J_m = np.inf

            # step 2.2: solve the optimization problem P_SE  p[t] > 0
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

            #calculate p_U
            if(E_tmp >= E_max):
                p_U = 0
            else:
                # calculate p_E max
                y = lambda x: x * L - omega * np.log2(1 + (h * x) / sigma) * E_max
                p_E_max = fsolve(y,100)
                p_U = min(p_tx_max, p_E_max)

            if(p_L <= p_U):
                # the sub-problem is feasible
                # calculate p_0
                vir_bat = B_hat[t]
                
                y = lambda x: vir_bat * np.log2(1 + h*x/sigma) + h*(V - vir_bat*x) /(np.log(2) * (sigma + h*x))
                p_0 = fsolve(y, 0.5)

                if((B_hat[t] >= 0) or ((B_hat[t] < 0) and (p_U < p_0))):
                    p[t] = p_U
                elif((B_hat[t] < 0) and (p_L > p_0)):
                    p[t] = p_L
                elif((B_hat[t] <0) and (p_L <= p_0) and (p_0 <= p_U)):
                    p[t] = p_0

                # check wheter p[t] is zero
                if(p[t] == 0):
                    print('   something wrong! p is 0  [SE]')
                
                # calculate the delay of MEC server exec
                cost[t,1] = L / (omega * np.log2(1 + (h * p[t] / sigma)))
                # calculate the energy consumption of MEC server exec
                E[t,1] = p[t] * cost[t,1]
                # calculate the value of optimization goal
                J_s = (-B_hat[t] * p[t] + V) * cost[t,1]

            else:
                # the sub-problem is not feasible because
                p[t] = 0
                cost[t, 1] = 0
                E[t, 1] = 0
                J_s = np.inf

            # step 3: choose the best execution mode
            J_d = V * phi
            #print(' J_m: ', J_m)
            #print(' J_s: ', J_s)

            mode = np.argmin([J_m, J_s, J_d])
            chosen_mode[t] = mode

        # step 4: according to the chosen execution mode, calculate the real dealy and energy consumption
        if(chosen_mode[t] == 0):
            # mobile execution is chosen
            cost[t, 2] = cost[t, 0]
            E[t, 2] = E[t, 0]
        elif(chosen_mode[t] == 1):
            # MEC server execution is chosen
            cost[t, 2] = cost[t, 1]
            E[t, 2] = E[t, 1]
        elif(chosen_mode[t] == 2):
            # task is dropped, the delay is the task dropping penalty and the 
            # energy consumption is zero
            cost[t, 2] = phi
            E[t, 2] = 0
        else:
            # no task is requested, the delay and the energy consumption are
            # both zero
            cost[t, 2] = 0
            E[t, 2] = 0
        
        ## step 5: update the battery energy level and go to next time slot
        B[t + 1] = B[t] - E[t, 2] + e[t]
        t += 1
    


    # 1. the battery energy level vs. time slot
    plt.figure(1)
    plt.title('Evolution of battery energy level')
    plt.xlabel('time slot')
    plt.ylabel('battery energy level')
    plt.plot(np.arange(T), B, linewidth=0.5)
    plt.plot(np.arange(T), np.full(T, theta + E_H_max), linewidth=0.5)

    # 2. the average execution cost vs. time slot
    plt.figure(2)
    plt.title('Evolution of average execution cost')
    plt.xlabel('time slot')
    plt.ylabel('average execution cost')

    accumulated = 0
    avg_cost = np.zeros(T)
    request_num = 0

    for i in range(T):
        accumulated += cost[i,2]
        if(cost[i,2] != 0):
            request_num += 1
        
        avg_cost[i] = accumulated / request_num

    plt.plot(np.arange(T), avg_cost , linewidth=0.75)

    # 3. the average ratio of each chosen mode vs. time slot
    plt.figure(3)
    plt.title('Evolution of average ratio of chosen modes')
    plt.xlabel('time slot')
    plt.ylabel('average ratio of chosen modes')
    
    avg_ratio = np.zeros((T,3))
    mobile_exe = 0.0
    server_exe = 0.0
    drop = 0.0
    request_num = 0.0

    for i in range(1,T):
        if(cost[i,2] == 0):
            avg_ratio[i] = avg_ratio[i-1]
            continue
        else:
            request_num += 1
            if(chosen_mode[i] == 0):
                mobile_exe += 1
            elif(chosen_mode[i] == 1):
                server_exe += 1
            else:
                drop += 1
        
        avg_ratio[i] = np.array([mobile_exe, server_exe, drop]) / request_num

    plt.plot(np.arange(T), avg_ratio[0:T,0], linewidth=0.75, label = 'Mobile execution')
    plt.plot(np.arange(T), avg_ratio[0:T,1], linewidth=0.75, label = 'MEC Server execution')
    plt.plot(np.arange(T), avg_ratio[0:T,2], linewidth=0.75, label = 'Drop')
    plt.legend()

    plt.show()