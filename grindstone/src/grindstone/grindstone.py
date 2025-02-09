from __init__ import glob
from __init__ import json
from __init__ import os

# Clears the ".\out" directory incase something needed to be removed or an extra file appeared.
try:
    for f in glob.glob('out'):
        os.remove(f)
except IOError: pass

# Goes through every loot table file in ".\input" and checks to see if anything matches the list given.
# Any items prepended by "_" will include anything that includes the whole phrase.

class Grindstone:
    __item_cache = {}
    def __get_item_json(path : str) -> object:
        try:
            return Grindstone.__item_cache[path]
        except KeyError:
            with open(path, "r") as f:
                text = f.read()
                json_data = json.loads(text)
                data = (text, json_data)
                Grindstone.__item_cache[path] = data
                return data

    def apply_modifier(path:str, appended_data:object, predicate: callable[[str], bool]) -> None:
        try:
            for filedir in glob.glob('input\\*.json'):
                pass
        except IOError:
            os.mkdir('input')
        
        for filedir in glob.glob('input\\*.json'):
            newfiledir = filedir.replace('input', 'out')
            file_data : str = open(filedir, "r").read()
            result = predicate(file_data)
            if not isinstance(result, bool):
                raise ValueError("Predicate must be return boolean.")
            if result:
                try:
                    json_data : object = Grindstone.__get_item_json(filedir)[1]

                    depth : int = 0
                    json_path : list[str] = path.split('.')
                    step : str = json_path[depth]
                    objects_to_append_to : list[object] = list()
                    while (depth < len(json_path)):
                        step : str = json_path[depth]
                        if (step.endswith(']')):
                            index_s : str = step[step.index('[')+1]
                            real_step : str = step.rsplit('[')[0]
                            try:
                                index : int = int(index_s)
                                if len(objects_to_append_to) <= 0:
                                    try:
                                        json_data[real_step] = json_data[real_step]
                                    except KeyError:
                                        json_data[real_step] = list()
                                    objects_to_append_to[0] = json_data[real_step][index]
                                else:
                                    for k,v in enumerate(objects_to_append_to):
                                        objects_to_append_to[k] = v[real_step][index]
                            except ValueError as _:
                                if (index_s != '*'):
                                    raise ValueError("Please use a valid index, an Integer or *")

                                if len(objects_to_append_to) <= 0:
                                    try:
                                        json_data[real_step] = json_data[real_step]
                                    except KeyError:
                                        json_data[real_step] = list()

                                    for _,v in enumerate(json_data[real_step]):
                                        objects_to_append_to.append(v)
                                else:
                                    for k,v in enumerate(objects_to_append_to):                                        
                                        print(v)
                                        for _,w in enumerate(v[real_step]):
                                            try:
                                                v[w] = v[w]
                                            except KeyError:
                                                v[w] = list()
                                            objects_to_append_to[k] = v[w]
                        else:
                            if len(objects_to_append_to) <= 0:
                                try:
                                    json_data[step] = json_data[step]
                                except KeyError:
                                    json_data[step] = list()
                                objects_to_append_to = [json_data[step]]
                            else:
                                for k,v in enumerate(objects_to_append_to):
                                    try:
                                        v[step] = v[step]
                                    except KeyError:
                                        v[step] = list()
                                    objects_to_append_to[k] = v[step]
                        depth += 1
                    for k,v in enumerate(objects_to_append_to):
                        v.append(appended_data)

                    try:
                        open(newfiledir, 'r')
                    except IOError:
                        try:
                            os.mkdir(newfiledir.rsplit('\\', 1)[0])
                        except FileExistsError: pass
                    with open(newfiledir, "w+") as out:
                        json.dump(json_data, out)
                    print(f'Saved updated json to {newfiledir}')
                except json.decoder.JSONDecodeError as err:
                    print(f'Something went wrong reading file: {filedir}, skipping...')
                    # print(err)