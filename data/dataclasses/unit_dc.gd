extends Resource
# DEFINISCE UN UNITA' INDIPENDENTEMENTE DALLE INFO DI BATTAGLIA (POSIZIONE, TEAM ECC)
class_name unit_dc

var meta:Dictionary
var stats:Dictionary
var soft_stats:Dictionary
var chosen_skills:Dictionary
var known_skills:Dictionary
var equip:Dictionary
var id:String
var portrait:String

func _init(meta: Dictionary, stats: Dictionary, chosen_skills: Dictionary, known_skills:Dictionary, equip: Dictionary, id=Global.uuids(), portrait="") -> void:
	self.meta = meta #NOME;CLASSE;RAZZA
	self.stats = stats #LEVEL,EXP,ATK,DEF,SPD,HP;SPATK,SPDEF
	self.chosen_skills = chosen_skills
	self.known_skills = known_skills
	self.equip = equip
	self.id=id
	if portrait=="":
		self.portrait = Global.rc_2_portrait(self.meta['race'],self.meta['class_'])
	else:
		self.portrait = portrait
	reload_soft_things()	
	
	
static func generate():
	pass #TODO

static func from_sql(unit_from_sql):
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
	
	
func reload_soft_things():
	self.soft_stats = stats.duplicate(true)
	for stat_name in self.soft_stats:
		for eq in equip:
			if equip[eq]:
				var equip_document=Persistent.get_by_id("equip", equip[eq])
				if equip_document.stats.has(stat_name): self.soft_stats[stat_name] += equip_document.stats[stat_name]
			
		max(0,self.soft_stats[stat_name])
		#TODO EVENTUALI BUFF SPECIALI!
	
