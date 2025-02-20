extends Node

var character_scene = preload("res://scenes/characters/character_node_2d.tscn")  # Carica la scena del personaggio
var tile_width: int = Global.TW
var tile_height: int = Global.TH
var battle_data: Dictionary
@onready var data_grid = $DataGrid  # ✅ Primo livello: DataGrid
@onready var battle_system = $BattleSystem  # ✅ Primo livello: DataGrid
@onready var units_container = $DataGrid/UnitsContainer  # ✅ UnitsContainer è dentro DataGrid

func _ready():
	var characters = battle_data.units.enemies

	for el in characters:  # Creiamo 3 istanze
		var character_instance = character_scene.instantiate()
		character_instance.initialize(el)  # Passiamo la cartella dell'animazione
		#print("CREATO:" + str(char) + "COORD:" + str(coord))
		# Posizioniamo i personaggi in modo che non si sovrappongano
 
		
		units_container.add(character_instance)  # Aggiungiamo alla scena
	data_grid.build_grid_data()
	
