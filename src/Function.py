"""
    This file is part of SEA.

    SEA is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    SEA is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with SEA.  If not, see <http://www.gnu.org/licenses/>.

    Copyright 2013 by neuromancer
"""
from core import *

class Function:
  """An abstract function class"""
  parameter_typs = []
  parameter_locs = []
  parameter_vals = []
  read_operands  = []
  write_operands = []
  return_type    = None
  
  def __init__(self, pbase = None, pars = None):
    self.parameter_typs = []
    self.parameter_locs = []
    self.parameter_vals = []
    self.read_operands  = []
    self.write_operands = []
  
  def getParameters(self):
    return self.parameter_vals

  def getParameterLocations(self):
    return self.parameter_locs
  
  def getReadVarOperands(self):
    return filter(lambda o: o.isVar(), self.read_operands)
  
  def getWriteVarOperands(self):
    return filter(lambda o: o.isVar(), self.write_operands)
  
  def getEq(self):
    return []
  
  def __loadParameters__(self, pars):
    self.parameter_locs = []
    self.parameter_vals = []
    #print pars
    for (loc, ptype, offset) in pars:
      
      self.parameter_locs.append(loc)
      self.parameter_vals.append((ptype,offset))
    
  
  def __locateParameter__(self, disp, size):
    ptype, offset = self.pbase
    
    op = MemOp(getMemInfo(ptype), size, offset=offset+disp)
    op.type = ptype
    
    return op
  
class Skip_Func(Function):
  pass

class Gets_Func(Function):
  parameter_typs = [(Type("Ptr32",None), "DWORD", 0, True)]
  return_type    = "void"
  
  def __init__(self, pbase = None, pars = None):
    
    self.internal_size = 84
    
    if (type(pbase) <> type(None)):
      self.pbase = pbase
      for (ptype, size, disp, needed) in self.parameter_typs:
        self.parameter_locs.append((ptype, self.__locateParameter__(disp, size), needed))
    else:
      self.__loadParameters__(pars)
      # populate read operands
      
      #self.read_operands.append(self.parameter_locs[0])
      
      ptype,offset = self.parameter_vals[0]
      op = MemOp(getMemInfo(ptype), 1, offset)
      op.size_in_bytes = self.internal_size
      op.setType(ptype)

      # populate write operands
      self.write_operands = [op]
     
      # populate read operands
     
      op = InputOp("stdin", 1)
      op.size_in_bytes = self.internal_size

      self.read_operands = [op]
 

class Strlen_Func(Function):
  parameter_typs = [(Type("Ptr32",None), "DWORD", 0, True)]
  return_type    = Type("Num32",None)
  
  def __init__(self, pbase = None, pars = None):
    
    self.internal_size = 10
    
    if (pbase <> None):
      self.pbase = pbase
      for (ptype, size, disp, needed) in self.parameter_typs:
        self.parameter_locs.append((ptype, self.__locateParameter__(disp, size), needed))
    else:
      self.__loadParameters__(pars)
      
      # populate read operands
      
      self.read_operands.append(self.parameter_locs[0])
        
      # return value
      self.write_operands.append(RegOp("eax", "DWORD")) 

class Strcpy_Func(Function):
  parameter_typs = [(Type("Ptr32",None), "DWORD", 0, True), (Type("Ptr32",None), "DWORD", 4, True)]
  return_type    = "void"
  
  def __init__(self, pbase = None, pars = None):
    
    self.internal_size = 256+4
    
    if (type(pbase) <> type(None)):
      self.pbase = pbase
      for (ptype, size, disp, needed) in self.parameter_typs:
        self.parameter_locs.append((ptype, self.__locateParameter__(disp, size), needed))
    else:
      self.__loadParameters__(pars)
      
      # populate read operands
      ptype,offset = self.parameter_vals[0]
      op = MemOp(getMemInfo(ptype), 1, offset)
      op.size_in_bytes = self.internal_size
      op.setType(ptype)

      # populate write operands
      self.write_operands = [op]

      ptype,offset = self.parameter_vals[1]
      op = MemOp(getMemInfo(ptype), 1, offset)
      op.size_in_bytes = self.internal_size
      op.setType(ptype)

      # populate write operands
      self.read_operands = [op]

class Alloc_Func(Function):
  parameter_typs = [(Type("Num32",None), "DWORD", 0, True)]
  return_type    = "void *"
  
  def __init__(self, pbase = None, pars = None):
    
    self.parameter_locs = []
    self.parameter_vals = []
    self.read_operands  = []
    self.write_operands = []
    
    if (type(pbase) <> type(None)):
      self.pbase = pbase
      for (ptype, size, disp, needed) in self.parameter_typs:
        self.parameter_locs.append((ptype, self.__locateParameter__(disp, size), needed))
    else:
      self.__loadParameters__(pars)

class Free_Func(Function):
  parameter_typs = [(Type("Ptr32",None), "DWORD", 0, True)]
  return_type    = "void"
  
  def __init__(self, pbase = None, pars = None):
    
    self.parameter_locs = []
    self.parameter_vals = []
    self.read_operands  = []
    self.write_operands = []
    
    if (type(pbase) <> type(None)):
      self.pbase = pbase
      for (ptype, size, disp, needed) in self.parameter_typs:
        self.parameter_locs.append((ptype, self.__locateParameter__(disp, size), needed))
    else:
      self.__loadParameters__(pars)
      

funcs = {
    "printf" : Skip_Func,
    "puts"   : Skip_Func,
    "gets"   : Gets_Func,
    "malloc" : Alloc_Func,
    "free"   : Free_Func,
    "strcpy" : Strcpy_Func,
    "strlen" : Strlen_Func,
}
