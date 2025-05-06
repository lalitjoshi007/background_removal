# rembg_model.py
from rembg import new_session

#  Load model once and reuse
session = new_session(model_name="isnet-general-use", providers=["CUDAExecutionProvider", "CPUExecutionProvider"])
