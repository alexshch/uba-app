import torch
import numpy as np

data = [[1, 2],[3, 4]]
x_data = torch.tensor(data)
print(f"x_data: {x_data}")

np_array = np.array(data)
x_np = torch.from_numpy(np_array)
print(f"x_np: {x_np}")

device = torch.accelerator.current_accelerator().type if torch.accelerator.is_available() else "cpu"

tensor = torch.rand(3,4).to(device)
print(f"Random tensor: {tensor}")

print(f"Shape of tensor: {tensor.shape}")
print(f"Datatype of tensor: {tensor.dtype}")
print(f"Device tensor is stored on: {tensor.device}")

tensor = torch.ones(4, 4)
print(f"Device tensor is stored on: {tensor.device}")

print(f"First row: {tensor[0]}")
print(f"First column: {tensor[:, 0]}")
print(f"Last column: {tensor[..., -1]}")
tensor[:,1] = 0
print(tensor)
t1 = torch.cat([tensor, tensor, tensor], dim=1)
print(t1)