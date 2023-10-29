
import numpy as np

class VaRCalculation:
    '''Python class to calculate VaR and ES.'''

    def __init__(self, time=1, alpha=95, freq=1,name="Portafolio"):
        self.time = time
        self.alpha = alpha
        self.freq = freq
        self.name = name


    def mc(self, x, alpha, n_sims=5000, seed=42):
        '''Monte Carlo VaR'''
        np.random.seed(seed)
        sim_returns = np.random.normal(x.mean(), x.std(), n_sims)
        return np.sqrt(self.time * self.freq) * np.percentile(sim_returns, alpha)

    def vc(self, x, alpha):
        '''Variance-covariance VaR'''
        from scipy import stats
        c = alpha / 100
        return np.sqrt(self.time * self.freq) * (x.std() * stats.norm.ppf(c))

    def hs(self, x, alpha):
        '''Historical Simulation VaR'''
        return np.sqrt(self.time * self.freq) * np.percentile(x, 100 - alpha)

    def es(self, x, alpha):
        '''Expected Shortfall'''
        from scipy import stats
        alpha = 1 - alpha / 100
        return - \
            (alpha ** -1 * stats.norm.pdf(stats.norm.ppf(alpha)) * x.std() * np.sqrt(
                self.time * self.freq) - x.mean()).flatten()[0]

    def predict(self, X, w):
        R = X.corr()
        vc_name = f"vc_{self.alpha}"
        hs_name = f"hs_{self.alpha}"
        mc_name = f"mc_{self.alpha}"
        es_name = f"es_{self.alpha}"


        var = {vc_name: 0, hs_name: 0, mc_name: 0, es_name: 0}        
        var_children = {}

        V = np.zeros(len(w))
        for i in range(len(w)):
            vc = self.vc(X.iloc[:, i], alpha=self.alpha)
            V[i] = np.abs(w[i]) * vc
            
            chld_namee = self.name + "/" +X.columns[i]
            var_children[chld_namee] = {vc_name:-abs(vc)}

            #item_label = 'vc_'+X.columns[i]
            #var[item_label] = -abs(vc)

        var[vc_name] = -np.sqrt(V @ R @ V.T)

        for i in range(len(w)):
            hc = None
            if w[i] < 0:
                hc = self.hs(X.iloc[:, i], alpha=self.alpha)
                V[i] = w[i] * hc
            else:
                hc = self.hs(X.iloc[:, i], alpha=100 - self.alpha)
                V[i] = w[i] * hc
            
            chld_namee = self.name + "/" +X.columns[i]
            var_children[chld_namee][hs_name]= -abs(hc)
            #item_label = 'hc_'+X.columns[i]
            #var[item_label] = -abs(hc)

        var[hs_name] = -np.sqrt(V @ R @ V.T)

        for i in range(len(w)):
            mc = None
            if w[i] < 0:
                mc = self.mc(X.iloc[:, i], alpha=self.alpha)
                V[i] = w[i] * mc
            else:
                mc = self.mc(X.iloc[:, i], alpha=100 - self.alpha)
                V[i] = w[i] * mc

            chld_namee = self.name + "/" +X.columns[i]
            var_children[chld_namee][mc_name]= -abs(mc)
            #item_label = 'mc_'+X.columns[i]
            #var[item_label] = -abs(mc)

        var[mc_name] = -np.sqrt(V @ R @ V.T)

        for i in range(len(w)):
            es = self.es(X.iloc[:, i], alpha=self.alpha)
            V[i] = np.abs(w[i]) * es

            chld_namee = self.name + "/" +X.columns[i]
            var_children[chld_namee][es_name]= -abs(es)
            #item_label = 'es_'+X.columns[i]
            #var[item_label] = -abs(es)

        var[es_name] = -np.sqrt(V @ R @ V.T)

        var_parent = {self.name :  var}

        var_parent.update(var_children)
 
        return var_parent