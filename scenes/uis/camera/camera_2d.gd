extends Camera2D
#Camera2D

@export var cursor: Node2D  # Il cursore da seguire
@export var follow_speed: float = 3.0  # Velocità di movimento della camera
var tile_width: int = Global.TW
var tile_height: int = Global.TH


func _ready():
	print("camera2d READY")

	if cursor == null:
		cursor = get_parent().find_child("CursorNode2D", true, false)  # Cerca il nodo "Cursor"
func _process(delta):
	if cursor:
		var grid_x = cursor.cursor_position.x
		var grid_y = cursor.cursor_position.y

		# Conversione da coordinate griglia a coordinate mondo (solo diagonali)

		# Movimento fluido usando lerp()
		var new_position = cursor.world_position
		position = position.lerp(new_position, follow_speed * delta)
