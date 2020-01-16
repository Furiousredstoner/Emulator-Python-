class Component:
  #def __init__(self):
  #self = self
  def Dialog(self,Msgtype,CompName,Msg):
    CompName = "["+str(CompName)+"]: "
    if Msgtype == "Error":
      self.type = "Error: "
    elif Msgtype is None:
      self.type = ""
    print(CompName+self.type,Msg)
  pass