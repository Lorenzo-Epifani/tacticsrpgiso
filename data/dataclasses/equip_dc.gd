class_name equip_dc

var name: String
var id: String
var id_cat: String
var stats: Dictionary

func _init(name: String, id: String, id_cat: String, known_skills:Dictionary, sprite="") -> void:
	self.name = name #NOME;CLASSE;RAZZA
	self.stats = stats #LEVEL,EXP,ATK,DEF,SPD,HP;SPATK,SPDEF
	self.id = id #LEVEL,EXP,ATK,DEF,SPD,HP;SPATK,SPDEF
	self.id_cat = id_cat #LEVEL,EXP,ATK,DEF,SPD,HP;SPATK,SPDEF
	
		self.sprite = Global.item_2_sprite(self.meta['race'],self.meta['class_'])
	else:
		self.sprite = sprite
		
func generate():
	pass #TODO
"""static func from_sql(unit_from_sql):
	var usql = unit_from_sql
	return unit_dc.new(usql['meta'],usql['stats'],usql['chosen_skills'],usql['known_skills'],usql['equip'],usql['id'])

static func dummy(dummyn:int):
	var dummy_meta={}
	var dummy_stats={}
	match dummyn:
		1:
			dummy_meta={"name":"placeholder1", "class_":"black_mage", "race":"nu_mou"}
			dummy_stats={"level":1,"exp":0,"atk":5,"def":6,"spd":5,"hp":20}
		2:
			dummy_meta={"name":"placeholder2", "class_":"defender", "race":"bangaa"}
			dummy_stats={"level":2,"exp":0,"atk":8,"def":4,"spd":4,"hp":25}
	return unit_dc.new(dummy_meta,dummy_stats,{},{},{})
	

func deepcopy():
	return unit_dc.new(self.meta,self.stats,self.chosen_skills,self.known_skills,self.equip,self.id,self.portrait)
"""
