extends Node


func over_tile_sprite(type):
	var sprite = AnimatedSprite2D.new()
	# type MOVE, HEAL or ATTACK!!!!!
	# type MOVE, HEAL or ATTACK!!!!!
	# type MOVE, HEAL or ATTACK!!!!!
	var frames = SpriteFrames.new()  # Creiamo un nuovo set di animazioni
	var dirnamee = "res:///assets/ground/hlayer/{ty}".format({"ty":type})
	var dir = DirAccess.open(dirnamee)
	if dir:
		var files = dir.get_files()  # Otteniamo tutti i file nella cartella
		files.sort()  # Ordiniamo i file (importante per la sequenza dell'animazione)
		for file in files:
			if file.ends_with(".png"):  # Controlliamo che sia un'immagine PNG
				var texture = load(dirnamee + "/" + file)  # Carichiamo l'immagine
				frames.add_frame("default", texture)  # Aggiungiamo il frame
		sprite.sprite_frames = frames
		sprite.visible=true
		# Impostiamo la velocità dell'animazione
		frames.set_animation_speed("default", 5) 
	return sprite
	
func show_damage(grid_position: Vector2i, amount: int):
	var modcolor
	var position = Global.g2w_vec(grid_position)
	
	if amount < 0:
		modcolor = Color(0, 1, 0, 0.7)
	elif amount > 0:
		modcolor = Color(1, 0, 0, 0.7)
	else:
		modcolor = Color.WHITE
	var damage_label = Label.new()
	damage_label.z_as_relative = false
	damage_label.z_index = int(position.y) + 200
	var amount_txt=str(amount).replace("-", "")
	
	damage_label.text = amount_txt
	damage_label.position = position
	damage_label.add_theme_font_override("font", preload("res://assets/ui/font.ttf"))
	# Imposto il colore (opzionale, rosso per il danno)
	damage_label.add_theme_color_override("font_color", Color.WHITE)
	damage_label.add_theme_color_override("outline_color", Color.BLACK)
	damage_label.add_theme_constant_override("outline_size", 5)
	damage_label.modulate = modcolor
	damage_label.scale=Vector2(0.6,0.6)
	get_tree().current_scene.add_child(damage_label)

	# Creo il tween per animare il testo
	var tween = create_tween()
	var move_y = get_viewport().size.y/50

	tween.tween_property(damage_label, "position:y", position.y - move_y, 1.0).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_OUT)
	tween.tween_property(damage_label, "modulate:a", 0.0, 1.0)

	# Alla fine dell'animazione elimino il nodo
	tween.tween_callback(damage_label.queue_free)
	#for elem in target_list:
