extends Control
@onready var sprite_display = $TextureRect
@onready var panel = $PanelContainer
@onready var name_label = $PanelContainer/Name
@onready var hp_bar = $PanelContainer/HealthBar

func update_unit_info(unit_data):
	var unit = unit_data['unit']
	var statics = unit_data['statics']
	if unit:
		#Global.dbg(unit)
		var portrait = unit["portrait"]
		sprite_display.texture = load(portrait)
		sprite_display.size = Vector2(300, 300)  # Imposta una dimensione esatta in pixel
		name_label.text=unit.meta['name']
		name_label.scale=Vector2(1.7,1.7)
		hp_bar.scale=Vector2(0.7,0.7)
		
		hp_bar.max_value=unit['soft_stat']['hp']
		hp_bar.min_value=0
		hp_bar.value = hp_bar.max_value
		
		#name_label.label_settings = LabelSettings.new().font_color = Color(0,1,0)
		panel.size = Global.screen_frac(get_viewport_rect(),2,4) # Imposta una dimensione in funzione del viewport
		#sprite_display.position = Vector2(430, 200)  # Posiziona la texture a (X=100, Y=200)
		sprite_display.position = get_viewport_rect().size - sprite_display.get_size()
		
		
		name_label.position.x=0+ Global.screen_frac(get_viewport_rect(),20,4).x
		name_label.position.y=panel.size.y/3
		
		hp_bar.position.y = 1.5*panel.size.y/3
		hp_bar.position.x = name_label.position.x
		#name_label.position = get_viewport_rect().size - name_label.size
		
		panel.position = get_viewport_rect().size - panel.get_size()
		sprite_display.flip_h=false

		if unit["team"]==Global.team.ENEMY: 
			panel.position.x=0
			
			name_label.position.x=panel.size.x/2.1
			name_label.position.y=panel.size.y/3
			
			hp_bar.position.x = name_label.position.x
			hp_bar.position.y = 1.5*panel.size.y/3
			
			sprite_display.position.x=0
			sprite_display.flip_h=true
		
	
				
		

		propagate_call("set_visible", [true])
	else:
		propagate_call("set_visible", [false])
		
