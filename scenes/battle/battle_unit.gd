extends Node
class_name BattleUnit  # La tua classe è ora riconosciuta come "BattleUnit"
@onready var BASE_UNIT 
@onready var soft_stat 
@onready var orient 
@onready var position 
@onready var meta 
@onready var status = {}
@onready var equip 
@onready var chosen_skills 
@onready var char2d = $BattleUnit2D  
@onready var sprite = $BattleUnit2D/Sprite2D  # Riferimento diretto al nodo BattleData
@onready var portrait
@onready var team
@onready var id #AUTOGENERATE FOR ENEMIES
@onready var party_member

# Called when the node enters the scene tree for the first time.
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  #LA POSITION QUI è DA INTENDERE IN COORDINATE TILE, LA POSITION DEL BUNIT2d E DELLO SPRITE IN COORDINATE SU SCHERMO!
  #LA POSITION QUI è DA INTENDERE IN COORDINATE TILE, LA POSITION DEL BUNIT2d E DELLO SPRITE IN COORDINATE SU SCHERMO!
  #LA POSITION QUI è DA INTENDERE IN COORDINATE TILE, LA POSITION DEL BUNIT2d E DELLO SPRITE IN COORDINATE SU SCHERMO!
  #LA POSITION QUI è DA INTENDERE IN COORDINATE TILE, LA POSITION DEL BUNIT2d E DELLO SPRITE IN COORDINATE SU SCHERMO!
  #LA POSITION QUI è DA INTENDERE IN COORDINATE TILE, LA POSITION DEL BUNIT2d E DELLO SPRITE IN COORDINATE SU SCHERMO!
  #LA POSITION QUI è DA INTENDERE IN COORDINATE TILE, LA POSITION DEL BUNIT2d E DELLO SPRITE IN COORDINATE SU SCHERMO!
func __initialize(_soft_stat, _position, _meta, _chosen_skills={}, _equip=[], _orient=Global.orient.SOUTH, _team=Global.team.ENEMY):
	soft_stat = _soft_stat
	soft_stat['act_hp'] = soft_stat['hp']
	position = _position
	meta = _meta
	chosen_skills = _chosen_skills
	equip = _equip
	team = _team
	orient = _orient
	id=Global.uuids()
	portrait = Global.rc_2_portrait(meta['race'],meta['class_'])
	
func __from_party_member(character_node, _position, _orient=Global.orient.SOUTH):
	party_member = character_node
	var c_n = character_node
	position = _position
	orient = _orient
	
	meta = c_n.meta
	soft_stat = c_n.stats
	chosen_skills = c_n.chosen_skills
	equip = c_n.equip
	id=c_n.id
	
	if c_n.portrait=="":
		portrait = Global.rc_2_portrait(meta['race'],meta['class_'])
	else:
		portrait = c_n['portrait']
	team = Global.team.MY
	soft_stat['act_hp'] = soft_stat['hp']
	
func from_dataclass(unit_dataclass, _position, _team = Global.team.MY, _orient=Global.orient.SOUTH):
	BASE_UNIT = unit_dataclass.duplicate()
	var udc = unit_dataclass
	position = _position
	orient = _orient
	meta = udc.meta #name,class,race
	soft_stat = udc.stats
	chosen_skills = udc.chosen_skills
	equip = udc.equip
	id=udc.id
	
	if not udc.portrait:
		portrait = Global.rc_2_portrait(meta['race'],meta['class_'])
	else:
		portrait = udc['portrait']
	team = _team
	soft_stat['act_hp'] = soft_stat['hp']
	
func playy(anim_name, wait=0, tail=1000,reset="walk"):
	get_node("BattleUnit2D").playy(anim_name, wait, tail,reset)

func apply_damage(wait=800,dmg_amount=1):
	#func playy(anim_name, wait=0, tail=1000,reset="walk"):
	#		await get_tree().create_timer(wait/1000).timeout
	var waitms = float(wait) / 1000
	await get_tree().create_timer(waitms).timeout	
	var reset = "walk" if soft_stat['act_hp']/soft_stat['hp']>=0.15 else "tired"
	GlobalAnimations.show_damage(self.position,100)
	playy("damaged",0,0,reset)
	pass
	

func reload_soft_stats():
	#TODO IN BATTLE E NEL PARTY E' DIVERSO! (Ci sono i debuff)
	pass	

func die():
	#TODO
	pass
