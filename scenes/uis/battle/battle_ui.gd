extends Node
#BattleUI


func update_unit_info(unit_data):
	var unit_info_ui = find_child("UnitInfo", true, false)
	unit_info_ui.update_unit_info(unit_data)

func hide_():
	propagate_call("set_visible", [false])

func show_():
	propagate_call("set_visible", [true])
