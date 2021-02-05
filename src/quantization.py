import torch


def sig_exp(num):
    n = num
    exp = 0
    while True:
        if n>=2:
            n /= 2
            exp += 1
        elif n<1:
            n *= 2
            exp -= 1
        else:
            break
    return int((n-1)*pow(2,8)), exp


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


def modelPruning(params, prune_rate):
    vectors = [torch.flatten(params[key]) for key in params.keys()]
    small_elements = [torch.topk(abs(vector), int(len(vector)*prune_rate), largest=False)[1] for vector in vectors]
    dic = {}
    for idx, vector in enumerate(vectors):
        for small_element in small_elements[idx]:
            vector[small_element] = 0
        dic[list(params.keys())[idx]] = vector.reshape(params[list(params.keys())[idx]].shape)
    return dic


def codebook(q_x, scale, zero_point):
    dic = {}
    for idx, e in enumerate(q_x):
        if e != zero_point:
            if e not in dic:
                dic[e] = []
            dic[e].append(idx)
    sig, exp = sig_exp(scale)
    print(dic)
    return (sig, exp, zero_point, dic)


def decodebook(cbook, length):
  decodeTensor = torch.zeros(length)
  for key in cbook[0].keys():
    for idx in cbook[0][key]:
      decodeTensor[idx] = (key-cbook[2]) * cbook[1]
  return decodeTensor