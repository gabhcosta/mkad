class KeyResearcher():       
  def search_in(self, data:dict= None, key:str= None) -> list:
    """This function looks up a key within a nested dictionary and returns all values that match the given key.
    """

    # Input Validators
    if not isinstance(data, dict):
      raise ValueError(f'Expected type dict. Got {type(data)}')
    if not isinstance(key, str):
      raise ValueError(f'Expected type str. Got {type(key)}')

    self.occurrences= list()
    self.recursive_search(data, key)
    result= self.occurrences.copy()
    self.occurrences= list()
    return result
    
  def recursive_search(self, data:dict=None, key:str=None) -> None:
    for k,v in data.items():
      if isinstance(v, list):
        for i in range(len(v)):
          if k == key:
            self.occurrences.append(v)
          self.recursive_search(v[i], key)      
      elif isinstance(v, dict):
        if k == key:
          self.occurrences.append(v)
        self.recursive_search(v,key)
      else:
        if k == key:
          self.occurrences.append(v)
        continue