class KeyResearcher():       
  def search_in(self, data, key):
    self.occ= list()
    self.recursive_search(data, key)
    result= self.occ.copy()
    self.occ= list()
    return result
    
  def recursive_search(self, data, key):
    for k,v in data.items():
      if isinstance(v, list):
        for i in range(len(v)):
          if k == key:
            self.occ.append(v)
          self.recursive_search(v[i], key)      
      elif isinstance(v, dict):
        if k == key:
          self.occ.append(v)
        self.recursive_search(v,key)
      else:
        if k == key:
          self.occ.append(v)
        continue