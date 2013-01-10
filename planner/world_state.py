# Operations on world state dictionary.
# Format of the dictionary expected by the planner is:
#   {key : value, ...}
#   key = string: atom name
#   value = list of tuples, each tuple represents atom's terms.

def add(world_state, atom, binding_tuple):
    if not isinstance(binding_tuple, tuple):
        binding_tuple = (binding_tuple,)
    if atom in world_state:
        world_state[atom].append(binding_tuple)
    else:
        world_state[atom] = [binding_tuple]

def set(world_state, atom, bindings):
    if isinstance(bindings, tuple):
        world_state[atom] = [bindings]
    elif isinstance(bindings, list):
        world_state[atom] = []
        for b in bindings:
            if isinstance(b, tuple):
                world_state[atom].append(b)
            else:
                world_state[atom].append((b,))
    else:
        world_state[atom] = [(bindings,)]

def remove(world_state, atom, binding_tuple):
    world_state[atom] = [t for t in world_state.get(atom, []) if t != binding_tuple]
