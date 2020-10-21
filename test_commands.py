from performline.client import Client
c = Client("976794ca6e5897e27d1b439064691bb1c3eb0420")
tf = list(c.trafficsources())
brands2 = list(c.brands(limit=2))
# brands2 = list(c.brands(create_date=">20200810"))
