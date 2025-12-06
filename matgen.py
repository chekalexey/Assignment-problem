import numpy as np
from typing import Tuple

class MatrixGenerator:    
    def __init__(
        self,
        n: int = 15,
        v: int = 15,
        distribution_type: str = "uniform",
        a_min: float = 0.12,
        a_max: float = 0.22,
        beta_min: float = 0.85,
        beta_max: float = 0.99,
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


if __name__ == "__main__":
    #Example
    gen1 = MatrixGenerator(3, 3, "concentrated") #or uniform
    print(gen1.D_matrix)
    
