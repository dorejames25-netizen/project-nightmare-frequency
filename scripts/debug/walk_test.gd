extends Node2D
## Walk test for room boundaries. Not part of the game.
## Open scenes/debug/walk_test.tscn and press F6.
##   Arrow keys     walk
##   Left click     walk to that point
##   F1             show or hide the helper shapes (floor, blockers, slots, exits)
##   1 to 6         jump to a room
## The stand-in player obeys WalkArea, Blockers, the Depth rule and the y-sort
## under Actors, and follows Exits to the next room.

const ROOMS: Array[String] = [
	"metro_platform",
	"station_concourse",
	"street_night",
	"service_corridor",
	"control_room",
	"tunnel",
]

@export var start_room: String = "metro_platform"
## Walking speed in scene pixels per second at the front edge of the floor.
@export var speed: float = 260.0
## Multiplies the Depth rule. Lower it if the player looks too big.
@export var height_factor: float = 1.0
## Hard cap on player height in scene pixels.
@export var max_height: float = 400.0

var room: Node2D
var room_id: String = ""
var player: Node2D
var label: Label

var walk: PackedVector2Array
var blockers: Array[PackedVector2Array] = []
var exits: Array[Polygon2D] = []
var horizon_y: float = 0.0
var height_per_px: float = 1.0

var has_target: bool = false
var target: Vector2 = Vector2.ZERO
var arrived_in: Polygon2D = null
var helpers_on: bool = false
var note: String = ""


func _ready() -> void:
	var layer := CanvasLayer.new()
	add_child(layer)
	label = Label.new()
	label.position = Vector2(8, 6)
	label.add_theme_font_size_override("font_size", 14)
	layer.add_child(label)
	load_room(start_room, "")


func load_room(id: String, from: String) -> void:
	if room != null:
		room.queue_free()
		room = null
		player = null
	var packed: PackedScene = load("res://scenes/rooms/%s.tscn" % id)
	if packed == null:
		note = "could not load " + id
		return
	room = packed.instantiate()
	add_child(room)
	move_child(room, 0)
	room_id = id

	walk = PackedVector2Array()
	var walk_node := room.get_node_or_null("WalkArea") as Polygon2D
	if walk_node != null:
		walk = walk_node.polygon

	blockers.clear()
	var blocker_root := room.get_node_or_null("Blockers")
	if blocker_root != null:
		for child in blocker_root.get_children():
			if child is Polygon2D:
				blockers.append((child as Polygon2D).polygon)

	exits.clear()
	var exit_root := room.get_node_or_null("Exits")
	if exit_root != null:
		for child in exit_root.get_children():
			if child is Polygon2D:
				exits.append(child as Polygon2D)

	horizon_y = 0.0
	height_per_px = 0.3
	var depth := room.get_node_or_null("Depth")
	if depth != null:
		horizon_y = float(depth.get_meta("horizon_y", 0.0))
		height_per_px = float(depth.get_meta("person_height_per_px", 0.3))

	# The stand-in player: a plain figure, one unit tall, feet at the origin.
	player = Node2D.new()
	player.name = "TestPlayer"
	var body := Polygon2D.new()
	body.color = Color(1, 1, 1, 0.85)
	body.polygon = PackedVector2Array([
		Vector2(-0.16, 0.0), Vector2(-0.16, -0.82), Vector2(-0.07, -0.86),
		Vector2(-0.07, -1.0), Vector2(0.07, -1.0), Vector2(0.07, -0.86),
		Vector2(0.16, -0.82), Vector2(0.16, 0.0),
	])
	player.add_child(body)
	var actors := room.get_node_or_null("Actors")
	if actors != null:
		actors.add_child(player)
	else:
		room.add_child(player)

	# Arrive at the exit that leads back to where we came from, else at PlayerStart.
	arrived_in = null
	var spawn := Vector2(688, 700)
	var start := room.get_node_or_null("PlayerStart") as Node2D
	if start != null:
		spawn = start.position
	if from != "":
		for zone in exits:
			if str(zone.get_meta("target", "")) == from and zone.has_meta("arrive"):
				spawn = zone.get_meta("arrive")
				arrived_in = zone
				break
	player.position = spawn
	has_target = false
	note = ""
	apply_helpers()
	update_player()


func allowed(p: Vector2) -> bool:
	if walk.size() < 3 or not Geometry2D.is_point_in_polygon(p, walk):
		return false
	for poly in blockers:
		if Geometry2D.is_point_in_polygon(p, poly):
			return false
	return true


func player_height(feet_y: float) -> float:
	var h := height_per_px * (feet_y - horizon_y) * height_factor
	return clampf(h, 8.0, max_height)


func update_player() -> void:
	var h := player_height(player.position.y)
	player.scale = Vector2(h, h)


func _physics_process(delta: float) -> void:
	if player == null:
		return
	var dir := Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
	if dir != Vector2.ZERO:
		has_target = false
	elif has_target:
		var to_target := target - player.position
		if to_target.length() < 3.0:
			has_target = false
		else:
			dir = to_target.normalized()

	if dir != Vector2.ZERO:
		# Slower when far away, so the walk matches the perspective.
		var near := maxf(player_height(768.0), 1.0)
		var pace := speed * clampf(player_height(player.position.y) / near, 0.2, 1.0)
		var step := dir * pace * delta
		var pos := player.position
		if allowed(pos + step):
			pos += step
		elif allowed(pos + Vector2(step.x, 0)):
			pos.x += step.x
		elif allowed(pos + Vector2(0, step.y)):
			pos.y += step.y
		else:
			has_target = false
		player.position = pos
		update_player()

	check_exits()
	label.text = "%s   feet (%d, %d)   height %d px   %s\narrows walk | click walk to | F1 helpers | 1-6 rooms" % [
		room_id, player.position.x, player.position.y, player_height(player.position.y), note,
	]


func check_exits() -> void:
	var inside: Polygon2D = null
	for zone in exits:
		if Geometry2D.is_point_in_polygon(player.position, zone.polygon):
			inside = zone
			break
	if inside == null:
		arrived_in = null
		note = ""
		return
	if inside == arrived_in:
		return
	var to := str(inside.get_meta("target", ""))
	if ROOMS.has(to):
		load_room(to, room_id)
	else:
		note = "exit '%s' is %s" % [inside.name, to if to != "" else "not set"]


func apply_helpers() -> void:
	if room == null:
		return
	for path in ["WalkArea", "Blockers", "AnimationSlots"]:
		var node := room.get_node_or_null(path) as CanvasItem
		if node != null:
			node.visible = helpers_on
	for zone in exits:
		zone.visible = helpers_on


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		target = get_global_mouse_position()
		has_target = true
	elif event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_F1:
			helpers_on = not helpers_on
			apply_helpers()
		elif event.keycode >= KEY_1 and event.keycode <= KEY_6:
			load_room(ROOMS[event.keycode - KEY_1], "")
