extends Node
const TW: int = 32
const TH: int = 16
enum orient { SOUTH, EAST, NORTH, WEST }
enum team { MY, ENEMY, ALLIED, NEUTRAL }

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

func generate_pg(_race=null,_class=null):
	var rng = RandomNumberGenerator.new()
	var _DB=DB.data
	var idx=0
	rng.randomize()
	if !_race:	
		idx = rng.randi_range(0, _DB.razza.size() - 1)
		_race = _DB.razza[idx]['nome']
	if !_class:	
		var raceclasses = DB.classes_by_race(_race)
		idx = rng.randi_range(0, raceclasses.size() - 1)
		_class = raceclasses[idx]['nome']
	print([_race,_class])
	return [_race,_class]
	
	
func rc_2_portrait(race,class_):
	var portrait = "res://assets/pg/races/{race}/{class}/portrait.png".format({"race": race,"class":class_})
	return portrait

func battle_nodes():
	var target_node = get_node("/root/Game/EventContainer/BaseFight/FightGlobal")
	return target_node
	
	
func uuids() -> String:
	var hex_chars = "0123456789abcdef"
	var template = "yxxx-yxxx"
	var uuid = ""
	
	for i in template:
		if i == "x":
			uuid += hex_chars[randi() % 16]
		elif i == "y":
			uuid += hex_chars[(randi() % 4) + 8]  # 'y' può essere 8, 9, A o B
		else:
			uuid += i
	
	return uuid

func screen_frac(viewport,xratio: float, yratio: float) -> Vector2:
	return Vector2(viewport.size.x / xratio, viewport.size.y / yratio)
