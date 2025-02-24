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
