extends Node

func execute_query(db, query: String, params: Array = []):
	"""Esegue una query SQL con parametri opzionali"""
	var result = db.query_with_bindings(query, params)
	return db.query_result if result else []

func get_tables(db):
	"""Ottiene la lista delle tabelle nel database"""
	var tab_list = execute_query(db, "SELECT name FROM sqlite_master WHERE type='table'")
	var tables_info_result = []
	for tab in tab_list:
		var tab_types = execute_query(db, "PRAGMA table_info(" + tab["name"] + ")")	
		var json_col=[]
		for el in  tab_types:
			if el["type"]=="JSON":
				json_col.append(el['name'])
		var result_entry ={
			"name":tab["name"],
			"json_col":json_col
		}
		tables_info_result.append(result_entry)  # Aggiunge il nome della tabella alla lista
	return tables_info_result
	
