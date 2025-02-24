extends Node

var db = SQLite.new()
var db_path = "res://data/persistent/persistent.db"  # Assicurati che il database sia qui

# Dizionario per memorizzare i dati del database
var data = {}

func _ready():
	db.path = db_path
	if db.open_db():
		load_all_data()  # 🔥 Carica tutte le tabelle
		print("✅ Database caricato con successo!")
	else:
		print("❌ Errore nell'apertura del database")

	
func execute_query(query: String, params: Array = []):
	"""Esegue una query SQL con parametri opzionali"""
	var result = db.query_with_bindings(query, params)
	return db.query_result if result else []

func classes_by_race(race: String):
	var nome_razza = race  # Sostituisci con il nome desiderato
	var sql = "SELECT classe.* FROM classe "\
			+ "INNER JOIN razza_classe ON classe.id = razza_classe.classe_id "\
			+ "INNER JOIN razza ON razza.id = razza_classe.razza_id " \
			+ "WHERE razza.nome = ?;"

# Assumendo che 'db' sia l'istanza di SQLite già aperta
	var result = db.query_with_bindings(sql, [nome_razza])
	#var result = db.query_with_bindings(query, params)
	return db.query_result if result else []

func get_tables():
	"""Ottiene la lista delle tabelle nel database"""
	var tab_list = execute_query("SELECT name FROM sqlite_master WHERE type='table'")
	var tables_info_result = []
	for tab in tab_list:
		var tab_types = execute_query("PRAGMA table_info(" + tab["name"] + ")")	
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
	

func load_all_data():
	"""Mappa ogni tabella in una variabile (Dizionario)"""
	var tables_infos = get_tables()  # Aggiungi altre tabelle se servono

	for tab_dict in tables_infos:
		data[tab_dict['name']] = execute_query("SELECT * FROM " + tab_dict['name'])
		for rowind in len(data[tab_dict['name']]):
			for cell in data[tab_dict['name']][rowind]:
				if cell in tab_dict["json_col"]:
					data[tab_dict['name']][rowind][cell]=JSON.parse_string(data[tab_dict['name']][rowind][cell])
				
	print("✅ Database di gioco esposto su DB.data !")
