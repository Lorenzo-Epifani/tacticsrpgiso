extends Resource
# DEFINISCE UN UNITA' INDIPENDENTEMENTE DALLE INFO DI BATTAGLIA (POSIZIONE, TEAM ECC)
class_name unit_dc

var meta:Dictionary
var stats:Dictionary
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
		
func generate():
	pass #TODO

static func from_sql(unit_from_sql):
	var usql = unit_from_sql
	return unit_dc.new(usql['meta'],usql['stats'],usql['chosen_skills'],usql['known_skills'],usql['equip'],usql['id'])

static func dummy(dummyn:int):
	var dmeta={}
	var dstats={}
	match dummyn:
		1:
			dmeta={"name":"placeholder1", "class_":"black_mage", "race":"nu_mou"}
			dstats={"level":1,"exp":0,"atk":5,"def":6,"spd":5,"hp":20}
		2:
			dmeta={"name":"placeholder2", "class_":"defender", "race":"bangaa"}
			dstats={"level":2,"exp":0,"atk":8,"def":4,"spd":4,"hp":25}
	return unit_dc.new(dmeta,dstats,{},{},{})
	

func deepcopy():
	return unit_dc.new(self.meta,self.stats,self.chosen_skills,self.known_skills,self.equip,self.id,self.portrait)
