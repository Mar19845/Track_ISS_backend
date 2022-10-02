from numpy.linalg import norm
from sgp4.api import Satrec
from sgp4.api import jday
from datetime import datetime
from scipy.integrate import ode
import numpy as np

#CONSTS
# gravitational constant
G_meters = 6.67430e-11       # m**3 / kg / s**2
G = G_meters * 10**-9 # km**3/ kg / s**2
EARTH_EQUATORIAL_RADIUS = 6378.135  # equatorial radius
EARTH_FLATTENING_CONSTANT = 1 / 298.26
GEO_SYNC_RADIUS = 42164.57
EARTH_MU=5.972e24 * G

class Debris(object):
    def __init__(self,s,t):
        self.t=t
        self.s=s
        self.satellite = Satrec.twoline2rv(s, t)
        self.propagate
        self.get_trayectory
        self.trayectory=[]
    
    def propagate(self):
        #get actual date
        self.now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        now = self.now.split()
        #separar la fecha y la hora
        year,month,day=now[0].split('-')
        hour,minute,seconds=now[1].split(':')
        #get jd and fr from jday funcation
        self.jd, self.fr = jday(int(year),int(month),int(day),int(hour),int(minute),int(seconds))
        
        #get position and velocity based on jd and fr
        e, self.position, self.velocity = self.satellite.sgp4(self.jd, self.fr)
        
        return self.position,self.velocity
    
    def two_body(self,t,y,mu=EARTH_MU):
        rx,ry,rz,vx,vy,vz=y
        r=np.array([rx,ry,rz])
        #calc norm of r
        norm_r=np.linalg.norm(r)

        #two body aceleration
        ax,ay,az= r*mu/norm_r**3
        return [vx,vy,vz,ax,ay,az]
    
    def get_trayectory(self,tspan=100.0*60.0,dt=100.0,mu=EARTH_MU):
        #r0,v0=d.propagar()
        r0=[*self.position]
        v0=[*self.velocity]
        
        #number of steps
        n_steps=int(np.ceil(tspan/dt))
        ys=np.zeros((n_steps,6))
        ts=np.zeros((n_steps,1))

        #initial conditions
        y0=r0+v0
        ys[0]=np.array(y0)
        step=1

        #solver
        solver=ode(self.two_body)
        solver.set_integrator('lsoda')
        solver.set_initial_value(y0,0)
        solver.set_f_params(mu)

        while step<n_steps:
            solver.integrate(solver.t+dt)
            #print(solver.t,solver.y)
            ts[step]=solver.t
            ys[step]=solver.y
            step+=1

        self.rs=ys[:,:3]

        return self.rs
    
    def animate(self):
        self.propagate()
        self.pos = self.get_trayectory()
        self.pos = self.pos[-1:]
        
        self.last_pos = self.pos[-1]
        self.trayectory.append(self.last_pos.tolist())
        self.trayectory_f = np.asarray(self.trayectory)
        
        return self.trayectory_f[::, 0], self.trayectory_f[::, 1], self.trayectory_f[::, 2]