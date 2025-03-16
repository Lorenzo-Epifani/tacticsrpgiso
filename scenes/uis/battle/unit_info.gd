extends Control
@onready var sprite_display = $TextureRect
@onready var panel = $PanelContainer

func update_unit_info(unit_data):
	var unit = unit_data['unit']
	var statics = unit_data['statics']
	if unit:
		#Global.dbg(unit)
		var portrait = unit["portrait"]
		sprite_display.texture = load(portrait)
		sprite_display.size = Vector2(300, 300)  # Imposta una dimensione esatta in pixel
		
		panel.size = Global.screen_frac(get_viewport_rect(),2,4) # Imposta una dimensione in funzione del viewport
		#sprite_display.position = Vector2(430, 200)  # Posiziona la texture a (X=100, Y=200)
		sprite_display.position = get_viewport_rect().size - sprite_display.get_size()
		panel.position = get_viewport_rect().size - panel.get_size()
		sprite_display.flip_h=false

		if unit["team"]==Global.team.ENEMY: 
			panel.position.x=0
			sprite_display.position.x=0
			sprite_display.flip_h=true
		
	
				
		

		propagate_call("set_visible", [true])
	else:
		propagate_call("set_visible", [false])
		
