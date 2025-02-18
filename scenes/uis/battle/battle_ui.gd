extends Node


func update_unit_info(unit_data):
	var unit_info_ui = find_child("UnitInfo", true, false)
	unit_info_ui.update_unit_info(unit_data)
