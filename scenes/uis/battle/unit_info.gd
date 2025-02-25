extends Control
@onready var sprite_display = $TextureRect

func update_unit_info(unit_data):
	var unit = unit_data['unit']
	var statics = unit_data['statics']
	if unit:
		#Global.dbg(unit)
		var portrait = unit["portrait"]
		sprite_display.texture = load(portrait)
		sprite_display.size = Vector2(300, 300)  # Imposta una dimensione esatta in pixel
		sprite_display.position = Vector2(430, 200)  # Posiziona la texture a (X=100, Y=200)
		propagate_call("set_visible", [true])
	else:
		propagate_call("set_visible", [false])
