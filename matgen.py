import numpy as np
from typing import Tuple
from munkres import Munkres

class MatrixGenerator:    
    def __init__(
        self,
        n: int = 15,
        v: int = 15,
        distribution_type: str = "uniform",
        a_min: float = 0.12,
        a_max: float = 0.2,
        beta_min: float = 0.93,
        beta_max: float = 0.98,
    ):
        if n <= 0 or v <= 0:
            raise ValueError("n и v должны быть больше 0")
        if a_min >= a_max:
            raise ValueError("a_min должен быть меньше a_max")
        if beta_min >= beta_max:
            raise ValueError("beta_min должен быть меньше beta_max")
        if beta_max >= 1.0:
            print("Внимание: beta_max установлен в 0.99 для гарантии убывания")
            beta_max = 0.99
        if distribution_type not in ["uniform", "concentrated"]:
            raise ValueError("distribution_type должен быть 'uniform' или 'concentrated'")
        
        self.n = n
        self.v = v
        self.distribution_type = distribution_type
        self.a_min = a_min
        self.a_max = a_max
        self.beta_min = beta_min
        self.beta_max = beta_max

        self._generate_data()
    
    def _generate_beta_matrix(self) -> np.ndarray:
        if self.distribution_type == "uniform":
            beta_matrix = np.random.uniform(
                self.beta_min, self.beta_max, (self.n, self.v)
            )
            
        elif self.distribution_type == "concentrated":
            beta_matrix = np.zeros((self.n, self.v))
            max_delta = (self.beta_max - self.beta_min) / 4
            
            for i in range(self.n):
                delta_i = np.random.uniform(0, max_delta)
                
                beta1_i = np.random.uniform(
                    self.beta_min, 
                    self.beta_max - delta_i
                )
                
                beta2_i = beta1_i + delta_i
                
                beta_matrix[i] = np.random.uniform(beta1_i, beta2_i, self.v)
        
        return beta_matrix
    
    def _generate_data(self):
        self.C_matrix = np.random.uniform(
            self.a_min, self.a_max, (self.n, self.v)
        )
        
        self.beta_matrix = self._generate_beta_matrix()
        
        for j in range(1, self.v):
            self.C_matrix[:, j] = self.C_matrix[:, j-1] * self.beta_matrix[:, j-1]
        
        self.D_matrix = self.C_matrix.copy()
    
    def get_D_matrix(self) -> np.ndarray:
        return self.D_matrix
    
class algo:
    def __init__(self, matrix):
        self._params = np.array(matrix)

    def _params(self):
        return self.__params
    
    def _find_max_in_column(self, column_id, excluded=None):
        if excluded is None:
            excluded = set()
        
        col = self._params[:, column_id]
        
        mask = [i for i in range(len(col)) if i not in excluded]
        
        if not mask:
            return -1, -1
        
        valid_values = col[mask]
        
        max_val = np.max(valid_values)
        max_idx_in_valid = np.argmax(valid_values)
        row_idx = mask[max_idx_in_valid]
        
        return max_val, row_idx
    
    def _find_k_min_in_column(self, column_id, excluded_rows=None, k=1):
        if excluded_rows is None:
            excluded_rows = set()
        
        col = self._params[:, column_id]
        
        mask = [i for i in range(len(col)) if i not in excluded_rows]
        
        if not mask:
            return -1, -1
        
        valid_values = col[mask]
        
        k = min(k, len(valid_values))
        
        k_smallest_indices = np.argpartition(valid_values, k - 1)
        kth_idx_in_valid = k_smallest_indices[k - 1]
        
        kth_val = valid_values[kth_idx_in_valid]
        row_idx = mask[kth_idx_in_valid]
        
        return kth_val, row_idx
    
    def Munkres_Alg(self):
        """Венгерский алгоритм для минимизации (min)"""
        res = 0
        sizes = self._params.shape
        assigned = set()
        values = []

        m = Munkres()
        indexes = m.compute(self._params.tolist())
        total = 0
        for row, column in indexes:
            value = self._params[row][column]
            total += value
            assigned.add(row)
            values.append(value)
        return total, np.array(values)
    
    def Munkres_Alg_Max(self):
        """Венгерский алгоритм для максимизации (max)"""
        max_value = np.max(self._params)
        cost_matrix = max_value - self._params
        
        m = Munkres()
        indexes = m.compute(cost_matrix.tolist())
        
        total = 0
        values = []
        assigned = set()
        for row, column in indexes:
            value = self._params[row][column]  
            total += value
            assigned.add(row)
            values.append(value)
        return total, np.array(values)


    def Greedy(self):
        res = 0
        _, cols = self._params.shape
        assigned = set()
        values = []

        for i in range(cols):
            val, row = self._find_max_in_column(i, assigned)
            
            if row != -1:
                res += val
                assigned.add(row)
                values.append(val)

        return res, np.array(values)
    
    def Thrifty(self):
        res = 0
        _, cols = self._params.shape
        assigned = set()
        values = []

        for i in range(cols):
            val, row = self._find_k_min_in_column(i, assigned)
            
            if row != -1:
                res += val
                assigned.add(row)
                values.append(val)

        return res, np.array(values)
    
    def Greedy_Thrifty(self, x):
        res = 0
        _, cols = self._params.shape
        assigned = set()
        values = []

        for i in range(cols):
            if i < x:
                val, row = self._find_max_in_column(i, assigned)
            else:
                val, row = self._find_k_min_in_column(i, assigned)
            
            if row != -1:
                res += val
                assigned.add(row)
                values.append(val)

        return res, np.array(values)
    
    def Thrifty_Greedy(self, x):
        res = 0
        _, cols = self._params.shape
        assigned = set()
        values = []

        for i in range(cols):
            if i < x:
                val, row = self._find_k_min_in_column(i, assigned)
            else:
                val, row = self._find_max_in_column(i, assigned)
            
            if row != -1:
                res += val
                assigned.add(row)
                values.append(val)

        return res, np.array(values)

if __name__ == "__main__":
    #Example
    gen1 = MatrixGenerator(15, 15, "concentrated") #or uniform
    print(gen1.D_matrix)
    a = algo(gen1.D_matrix)
    #print(a.Munkres_Alg())
    sum1, pupu = a.Greedy()
    sum2, pupupu = a.Thrifty()
    # print(a.Greedy())
    # print(a.Thrifty())
    print(sum1, sum2)
    # print(a.Greedy_Thrifty(1))
    # print(a.Thrifty_Greedy(1))
    
