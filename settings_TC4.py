from firedrake import *
import numpy as np

"""
    *********************************************
    *                 Test case                 *
    *********************************************"""
def test_case():
    #________________ Kind of data ________________#
    input_data = "measurements"  # from experiments
    #input_data = "created"       # set the wavemaker
    #______________ Temporal scheme _______________#
    scheme = "MMP"
    #  "SE": Symplectic-Euler ; "SV": Stormer-Verlet
    # "MMP": use the Modified Mid-Point VP approach
    #__________________ Dimension _________________#
    dim = "2D"
    #"2D": R(t) and b(x); "3D": R(y,t) and/or b(x,y)
    # if input = measurements, the dim must be 2D.
    #______ Path and name of the saved files ______#
    save_path = 'data/'+scheme+'/TC4_test/'
    # ----yl added. whether the seabed is flat or not
    bottom = 'flat' 
    # 'flat':b(x,y)=0; 'nonuniform':b(x,y)!=0
    # ----yl added. Whether or not to apply mild-slope approximation (MSA)
    FWF = 0
    # 1: use full weak forms (FWF); 0: use mild-slope approximations.
    save_pvd = False
    # Whether or not to save the 3D results into pvd files 
    return input_data, scheme, dim, save_path, bottom, FWF, save_pvd

"""
    *********************************************************************
    *                         Numerical domain                          *
    *********************************************************************"""
def domain(bottom):
    #______________________ Beach ______________________#
    H0 = 1.0                                  # Depth at rest (flat bottom)
    xb = 1.0                                           # Start of the beach
    sb = 0.0                                           # Slope of the beach
    # yl update
    def H_expr(function,x):
        function.interpolate(H0-conditional(le(x[0],xb),0.0,sb*(x[0]-xb)))
    #______________________ Basin ______________________#
    Hend = 1.0                              # Depth at the end of the beach
    if bottom=='nonuniform':
        Lx = xb +(H0-Hend)/sb                                 # Length in x
    else:
        Lx = 100
    Ly = 1.0                                                  # Length in y
    Lw = 1.0                                        # End of the x-transform
    res_x = 0.01                                             # x-resolution
    res_y = 1.0                                             # y-resolution
    n_z = 8                                         # Order of the expansion
    return H0, xb, sb, H_expr, Hend, Lx, Ly, Lw, res_x, res_y, n_z


"""
    **************************************************************************
    *                                Wavemaker                               *
    **************************************************************************"""
def load_wavemaker(dt):
    with open('202002/PistonMotion.dat','r') as data_f1:
        t_wm_0, wm_data_0 = np.loadtxt(data_f1, usecols=(0,1), unpack=True) # time and wavemaker position
    with open('202002/PistonVelocity.dat','r') as data_f2:
        t_vel_0, vel_data_0 = np.loadtxt(data_f2, usecols= (0,1), unpack=True) # time and wavemaker velocity
    # add an value to avoid overflow in the time loop
    t_wm     = np.append(t_wm_0,[t_wm_0[-1]+2*dt]) 
    wm_data  = np.append(wm_data_0,[wm_data_0[-1]])
    t_vel    = np.append(t_vel_0,[t_vel_0[-1]+2*dt])
    vel_data = np.append(vel_data_0,[vel_data_0[-1]])
    return t_wm, wm_data, t_vel, vel_data

def wavemaker(dim, H0, Ly, Lw, input_data):
    #_____________________________ Characteristics _____________________________#
    g = 9.81                                             # Gravitational constant
    lamb = 2.0                                                       # Wavelength
    k = 2*pi/lamb                                                   # Wave number
    w = sqrt(g*k*tanh(k*H0))                                     # Wave frequency
    Tw = 2*pi/w                                                     # Wave period
    gamma = 0.0                                                 # Wave amplitude
    t_stop = Constant(120.0)                                     # When to stop the wavemaker
    
    # yl update
    if input_data=='created':
        if dim == "2D":
            def WM_expr(function,x,t,t_stop):
                if t.values()[0] <= t_stop.values()[0]:
                    function.interpolate(conditional(le(x[0],Lw),-gamma*cos(w*t),0.0))
                else:
                    function.interpolate(conditional(le(x[0],Lw),-gamma*cos(w*t_stop),0.0))

            def dWM_dt_expr(function,x,t,t_stop):
                if t.values()[0] <= t_stop.values()[0]:
                    function.interpolate(conditional(le(x[0],Lw),gamma*w*sin(w*t),0.0))
                else:
                    function = Constant(0.0)

            def dWM_dy_expr(function,x,t,t_stop):
                function = Constant(0.0)
                
        elif dim == "3D":
            def WM_expr(function,x,t,t_stop):
                if t.values()[0] <= t_stop.values()[0]:
                    function.interpolate(conditional(le(x[0],Lw), gamma*((x[1]-0.5*Ly)/(0.5*Ly))*cos(w*t),0.0))
                else:
                    function.interpolate(conditional(le(x[0],Lw), gamma*((x[1]-0.5*Ly)/(0.5*Ly))*cos(w*t_stop),0.0))
            
            def dWM_dt_expr(function,x,t,t_stop):
                if t.values()[0] <= t_stop.values()[0]:
                    function.interpolate(conditional(le(x[0],Lw),-gamma*w*((x[1]-0.5*Ly)/(0.5*Ly))*sin(w*t),0.0))
                else:
                    function=Constant(0.0)

            def dWM_dy_expr(function,x,t,t_stop):
                if t.values()[0] <= t_stop.values()[0]:
                    function.interpolate(conditional(le(x[0],Lw), gamma*cos(w*t)/(0.5*Ly),0.0))
                else:
                    function.interpolate(conditional(le(x[0],Lw), gamma*cos(w*t_stop)/(0.5*Ly),0.0))
    
    elif input_data == "measurements": # linear interpolation of experimental data
        def WM_expr(function, x, Rt):  # Rt is a Constant
            function.interpolate(conditional(le(x[0],Lw),Rt,0.0))
        def dWM_dt_expr(function, x, Rt_t): # Rt_t is a Constant
            function.interpolate(conditional(le(x[0],Lw),Rt_t,0.0))
        def dWM_dy_expr(function):
            function = Constant(0.0)

    return g, lamb, k, w, Tw, gamma, t_stop, WM_expr, dWM_dt_expr, dWM_dy_expr


"""
    ***********************************
    *               Time              *
    ***********************************"""
def set_time(Tw):
    dt = 0.001                      # Time step
    T0 = 0.0                     # Initial time
    Tend = 0.1#120.0              # Final time
    t = T0                  # Temporal variable
    dt_save = 0.02          # saving time step
    return T0, t, dt, Tend, dt_save