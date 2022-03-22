from py_wake.examples.data.iea37._iea37 import IEA37_WindTurbines, IEA37Site
from py_wake.deficit_models.gaussian import IEA37SimpleBastankhahGaussian
from py_wake.utils.gradients import use_autograd_in, autograd, plot_gradients, fd, cs

# Other imports 
import numpy as np 
import openmdao.api as om  
from datetime import datetime

class PyWakeGrad(om.ExplicitComponent):
    def __init__(self, n_wt, method='rs', **kwargs):
        self.n_wt = n_wt
        self.method = method 
        om.ExplicitComponent.__init__(self, **kwargs)
           
        self.site = IEA37Site(n_wt)
        self.wt = IEA37_WindTurbines()
        self.wfm = IEA37SimpleBastankhahGaussian(self.site, self.wt)
        # if method == 'autograd_an':
        #     self.wfm.wake_deficitModel.enable_autograd()
        #     print('init')

    def setup(self):
        self.add_input('x', np.zeros([self.n_wt]))
        self.add_input('y', np.zeros([self.n_wt]))
        self.add_output('Cost', 1.)
        self.add_output('cost', 1.)
        self.declare_partials('cost', 'x')
        self.declare_partials('cost', 'y')

    def compute(self, inputs, outputs):
        x = inputs['x']
        y = inputs['y']
        sim_res = self.wfm(x,y)
        outputs['cost'] = -self.wfm(x, y, wd=np.arange(0, 360, 22.5), ws=[9.8]).aep(normalize_probabilities=True).sum()
        outputs['Cost'] = outputs['cost']


    # def compute_partials(self, inputs, J):
    #     x = inputs['x']
    #     y = inputs['y']        
    #     if self.method == 'autograd':
    #         print('this is autograd')
    #         with use_autograd_in():
    #             dAEPdxy = self.wfm.dAEPdxy(gradient_method=autograd)(x, y, wd=np.arange(0, 360, 22.5), ws=[9.8])
    #             #J['cost', 'x'] = -dAEPdxy[0]
    #             #J['cost', 'y'] = -dAEPdxy[1]

    #     elif self.method == 'autograd_an':
    #         print('this is analytical autograd')
    #         with use_autograd_in():
    #             dAEPdxy = self.wfm.dAEPdxy(gradient_method=autograd)(x, y, wd=np.arange(0, 360, 22.5), ws=[9.8])
    #             #J['cost', 'x'] = -dAEPdxy[0]
    #             #J['cost', 'y'] = -dAEPdxy[1]

    #     elif self.method == 'cs':
    #         print('this is cs')
    #         dAEPdxy = self.wfm.dAEPdxy(gradient_method=cs)(x, y, wd=np.arange(0, 360, 22.5), ws=[9.8])
    #         #J['cost', 'x'] = -dAEPdxy[0]
    #         #J['cost', 'y'] = -dAEPdxy[1]

    #     elif self.method == 'fd':
    #         print('this is finite difference')
    #         dAEPdxy = self.wfm.dAEPdxy(gradient_method=fd)(x, y, wd=np.arange(0, 360, 22.5), ws=[9.8])
    #         #J['cost', 'x'] = -dAEPdxy[0]
    #         #J['cost', 'y'] = -dAEPdxy[1]
    #     J['cost', 'x'] = -dAEPdxy[0]
    #     J['cost', 'y'] = -dAEPdxy[1]





