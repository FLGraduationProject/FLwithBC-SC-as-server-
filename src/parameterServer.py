import torch

import parameters as pm
import smartContract as sc
import quantization as q

def start_ps(server):
    ps = server
    for i in range(10):
        ps.update()

class parameterServer():
    def __init__(self, paramTensor, n_chunks, p_level):
      chunks = q.tensor2Chunk(paramTensor, n_chunks)
      for i, chunk in enumerate(chunks):
        qArr, scale, zero_point = q.chunkQuantization(chunk)
        print(qArr)
        sc.upload_chunk(i, qArr, scale, zero_point)
      self.n_chunks = n_chunks
      self.p_level = p_level
      self.update_infos = []


    def download_params(self):
      chunks = []
      for i in range(self.n_chunks):
        chunks.append(torch.tensor(q.Qchunk2chunk(sc.get_chunk(i))))
      return torch.cat(chunks)


    def upload(self, update_info):
      if len(self.update_infos) > self.p_level:
        return
      self.update_infos.append(update_info)

    
    def push(self, chunk_num, newChunk):
      sc.upload_chunk(chunk_num, newChunk)


    def update(self):
        print("------------------server updating------------------")
        print(self.update_infos)
        accepted_bids = {}
        for update_info in self.update_infos:
          for key in update_info.keys():
            if key in accepted_bids.keys():
              if accepted_bids[key][0] < update_info[key][0]:
                accepted_bids[key] = update_info[key]
            else:
              accepted_bids[key] = update_info[key]
        
        for key in accepted_bids.keys():
          accepted_bids[key][1].push(key)

        self.update_infos = []