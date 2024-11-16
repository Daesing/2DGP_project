from animation import SpriteCollection
from pico2d import delay
collections = SpriteCollection()

world = [[] for _ in range(4)]

def add_object(o, depth = 0):
    world[depth].append(o)

def add_objects(ol, depth=0):
    world[depth] += ol

def update():
    for layer in world:
        for o in layer:
            o.update()

def render():
    for layer in world:
        for o in layer:
            o.draw_animation(collections)


def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            del o  # Delete object(memory)
            return

    raise ValueError('Cannot delete non existing object')


def clear():
    for layer in world:
        layer.clear()

# collision list
collision_pairs = {}

def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        collision_pairs[group] = [[], []]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)

def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]: pairs[0].remove(o)
        if o in pairs[1]: pairs[1].remove(o)
    pass

def collide(a, b):
    al, ab, ar, at = a.get_bb()
    bl, bb, br, bt = b.get_bb()

    if ar < bl: return False
    if al > br: return False
    if at < bb: return False
    if ab > bt: return False

    return True


def handle_collisions():
    # 게임월드에 등록된 충돌 정보를 바탕으로, 실제 충돌 검사 실행
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:  # A list
            for b in pairs[1]:  # B list
                if collide(a, b):
                    #print(f'{group} collide')
                    a.handle_collision(group,b)
                    b.handle_collision(group,a)

    return None
