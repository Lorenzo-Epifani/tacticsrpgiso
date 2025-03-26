extends Node
var BN = Global.battle_nodes()

func atk_map():
	var bp_root = get_parent().get_parent()
	bp_root.set_state("CHOOSE_ATK")
	compute_atk_map()

func compute_atk_map(atk_range=1,h_atk_range="TODO"):
	var _atk_range=atk_range+1
	#TODO ATK RANGE map AND HEIGHT HANDLING!
	var atk_map = {}
	var cursor = BN.get_battle_cursor()
	var location = cursor.cursor_content["location"]
	var hlayer = BN.get_HLayer()
	var data_grid = BN.get_data_grid()
	for x in range(location.x - _atk_range, location.x + _atk_range):
		for y in range(location.y - _atk_range, location.y + _atk_range):
			var distance = abs(location.x - x) + abs(location.y - y)
			if distance < _atk_range and distance !=0:
				atk_map[Vector2i(x,y)] = true
				#	data_grid.add_edit_entry(Vector2(x,y),null,null,null,"MOVE")
	for elem in atk_map:
		data_grid.add_edit_entry(elem,null,null,null,"ATK")
	hlayer.reload_tiles()
# Called when the node enters the scene tree for the first time.
func _input(event):
	var bp_root = BN.get_bp_root()
	var cursor_content = BN.get_battle_cursor().cursor_content
	var target = cursor_content['unit']
	var can_i_atk_here = cursor_content.get("predict", "") == "ATK"  and target and target.team==Global.team.ENEMY
	var bp_state = bp_root.get_state()
	
	if event is InputEventKey and event.pressed:
		var key_states = [event.keycode, bp_state, can_i_atk_here]
		match key_states:
			[KEY_Z,bp_root.STATE.CHOOSE_ATK,true]:
				 #TODO: IL TARGET E NEMICO?
				var turnqueue = BN.get_bp_root().get_turn_queue()
				var hlayer = BN.get_HLayer()
				attaaack(turnqueue[0]["unit"],target)
				hlayer.erase_all()
			[KEY_X,bp_root.STATE.CHOOSE_ATK,true]:
				pass#UNDO ACTION #TODOace with function body.

func attaaack(attacker,target):
	var orient
	var bp_root = BN.get_bp_root()
	bp_root.set_state("LOADING")
	var diff=target.position-attacker.position
	if diff.x >0: orient = Global.orient.EAST
	elif diff.x < 0: orient = Global.orient.WEST
	elif diff.y >0: orient = Global.orient.NORTH
	elif diff.y < 0: orient = Global.orient.SOUTH
	attacker.orient=orient
	#attacker.playy("attack")
	$AttackLogic.attack_multi_exec(attacker,target)
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass
