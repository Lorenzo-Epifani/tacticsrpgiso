extends Node2D

var dragoon_scene = preload("res://test/dragoon.tscn")  # Carica la scena

func _ready():
	var dragoon_instance = dragoon_scene.instantiate()  # Istanzia la scena
	add_child(dragoon_instance)  # Aggiunge alla scena corrente

	# Trova AnimatedSprite2D all'interno dell'istanza
	var animated_sprite = dragoon_instance.get_node("AnimatedSprite2D")  # Cambia col nome corretto

	if animated_sprite and animated_sprite is AnimatedSprite2D:
		animated_sprite.play("walk")  # Avvia l'animazione "walk"
