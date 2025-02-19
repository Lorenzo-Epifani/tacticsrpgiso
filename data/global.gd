extends Node
const TW: int = 32
const TH: int = 16



func dbg(obj):
	print("📌 Debug dell'oggetto:", obj)
	
	if obj == null:
		print("❌ L'oggetto è NULL!")
		return

	var data = {}
	for property in obj.get_property_list():
		var key = property.name
		var value = obj.get(key) if obj.has_method("get") else null
		data[key] = value
	
	print("📋 Contenuto dell'oggetto:\n", JSON.stringify(data, "\t"))
	
func w2g(world_x,world_y):
	var grid_y = (world_x / TW) - (world_y / TH)
	var grid_x = (world_x / TW) + (world_y / TH)
	return [grid_x,grid_y]
	
	
func g2w(grid_x,grid_y):
	var world_x = (grid_x * TW / 2) + (grid_y * TW / 2)
	var world_y = (grid_x * TH / 2) - (grid_y * TH / 2)
	return [world_x,world_y]
