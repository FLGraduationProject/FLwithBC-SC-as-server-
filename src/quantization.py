import torch

def tensor2Chunk(x, n_chunks):
    chunks = []
    for i in range(n_chunks-1):
        chunks.append(x[int(i/n_chunks*len(x)) : int((i+1)/n_chunks*len(x))])
    chunks.append(x[int((n_chunks-1)/n_chunks)*len(x):])
    return chunks

def Qchunk2chunk(x, num_bits=8):
    return (torch.tensor(q_x)-zero_point)*scale


def chunk2Qchunk(x, num_bits=8):
    qmin = 0.
    qmax = 2.**num_bits - 1.
    min_val, max_val = x.min(), x.max()

    scale = (max_val - min_val) / (qmax - qmin)

    initial_zero_point = qmin - min_val / scale

    zero_point = 0
    if initial_zero_point < qmin:
        zero_point = qmin
    elif initial_zero_point > qmax:
        zero_point = qmax
    else:
        zero_point = initial_zero_point

    zero_point = int(zero_point)
    q_x = zero_point + x / scale
    q_x.clamp_(qmin, qmax).round_()
    q_x = q_x.round().byte()
    return q_x.tolist(), scale, zero_point
    # return QTensor(tensor=q_x, scale=scale, zero_point=zero_point)