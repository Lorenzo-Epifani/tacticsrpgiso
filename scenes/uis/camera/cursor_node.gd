#CursorNode2D

extends Node2D
@export var layer: TileMapLayer  # Riferimento al TileMap principale
@export var layer_index: int = 0  # Indice del layer su cui vogliamo muovere il cursore
var active_layer: int = 1  # Layer attivo su cui il cursore si trova
var cursor_position: Vector2i = Vector2i(0, 0)  # Posizione del cursore in coordinate della griglia
var cursor_content
var locked = false
var tile_width: int = Global.TW
var tile_height: int = Global.TH
var world_position : Vector2
var data_grid
var battle_ui
enum BattlePhases { DEPLOY, BATTLE, REWARDS }
@export var ui_manager: CanvasLayer  # Riferimento all'UI Manager

func _ready():
	
	print("cursornode READY")

	if battle_ui == null:
		battle_ui = get_parent().find_child("BattleUI", true, false)  # Cerca
	if data_grid == null:
		data_grid = get_parent().find_child("DataGrid", true, false)  # Cerca
	if ui_manager == null:
		ui_manager = get_parent().find_child("UIManager", true, false)  # Cerca UIManager
	layer = get_parent().find_child("Layer1", true, false)

	update_cursor_position()

func _input(event):
	var current_phase = get_parent().current_phase
	var BattlePhases = get_parent().BattlePhases
	
	if event is InputEventKey and event.pressed and !locked:
		if event.keycode == KEY_RIGHT:
			cursor_position += Vector2i(1, 0)  # Movimento isometrico a destra
		elif event.keycode == KEY_LEFT:
			cursor_position += Vector2i(-1, 0)  # Movimento isometrico a sinistra
		elif event.keycode == KEY_DOWN:
			cursor_position += Vector2i(0, -1)  # Movimento isometrico in basso
		elif event.keycode == KEY_UP:
			cursor_position += Vector2i(0, 1)  # Movimento isometrico in alto
		update_cursor_position()
	match current_phase:
		BattlePhases.DEPLOY:
			if event is InputEventKey and event.pressed:
				print(event.keycode)
				pass
		BattlePhases.BATTLE:
			if event is InputEventKey and event.pressed:
				pass
		BattlePhases.REWARDS:
			if event is InputEventKey and event.pressed:
				pass
	
func update_cursor_position():
	var phase = get_parent().current_phase
	# Converte la posizione della griglia in coordinate globali per il layer selezionato

	var world_x = Global.g2w(cursor_position.x,cursor_position.y)[0]
	var world_y = Global.g2w(cursor_position.x,cursor_position.y)[1]
	#var world_y = (cursor_position.x * tile_height / 2) - (cursor_position.y * tile_height / 2)
	world_position = Vector2(world_x, world_y)
	position = world_position  # Sposta il cursore nella posizione giusta

	var grid_coord = Global.w2g(world_position[0],world_position[1])
	print(grid_coord)
	#print("Cursore su:", cursor_position, "Grid", grid_coord, "→ Layer:", active_layer, "→ Posizione globale:", world_position)
	cursor_content = data_grid.get_at(Vector2i(grid_coord[0],grid_coord[1]))
	cursor_content['location']=Vector2i(grid_coord[0],grid_coord[1])
	battle_ui.update_unit_info(cursor_content)
	match phase:
		BattlePhases.DEPLOY:
			var deploy_scene = get_parent().find_child("DeployPhase", true, false)  # Cerca
			if deploy_scene:
				deploy_scene.update_deploy_info()
		BattlePhases.BATTLE:
			pass
		BattlePhases.REWARDS:
			pass
func lock():
	locked=true
	
func unlock():
	locked=false
	
func relocate(position:Vector2i):
	cursor_position=position
	update_cursor_position()
