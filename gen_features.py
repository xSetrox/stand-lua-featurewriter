import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('filename', type=str, nargs=1,
                    help='The file name')
                    
    args = parser.parse_args()
    file_name = args.filename[0]
    # i would use a context manager here but i want the exception to be handled up here. 
    try:
        lua_file = open(file_name, 'r')
    except FileNotFoundError:
        print(file_name, 'was not found.')
        exit()
    
    lines = lua_file.readlines()
    feature_counts = {
        'actions':0,
        'toggles':0,
        'toggle loops': 0,
        'sliders':0,
        'dividers':0,
        'lists':0, 
        'text inputs':0, 
        'colors':0, 
        'read-onlys':0, 
        'hyperlinks':0
    }

    feature_matching = {
        'menu.action': 'actions',
        'menu.toggle' : 'toggles',
        'menu.toggle_loop' : 'toggle loops',
        'menu.slider' : 'sliders',
        'menu.slider_float': 'sliders',
        'menu.click_slider': 'sliders',
        'menu.click_slider_float': 'sliders',
        'menu.list': 'lists',
        'menu.list_select' : 'lists',
        'menu.list_action' : 'lists',
        'menu.text_input': 'text inputs',
        'menu.colour': 'colors',
        'menu.color': 'colors',
        'menu.divider' : 'dividers',
        'menu.readonly' : 'read-onlys',
        'menu.hyperlink' : 'hyperlinks',
        'menu.action_slider' : 'sliders',
    }
    
    feature_writeout = ""
    for l in lines:
        if not l.startswith('--'):
            for f in feature_matching.keys():
                # we simply append a ( to prevent the same thing from being counted twice
                # because if we ask python if "menu.toggle" is in a string, it will say yes to menu.toggle, but also menu.toggle_loop
                # which matters because they are counted as different categories
                if f + '(' in l:
                    feature_counts[feature_matching[f]] += 1
                    breakdown_pieces = l.split(f + '(')
                    # i love you! sorry!
                    breakdown_piece_of_breakdown_piece = breakdown_pieces[1].split(',')
                    line_summary = f'{breakdown_piece_of_breakdown_piece[0]} > {breakdown_piece_of_breakdown_piece[1]}'
                    feature_writeout += line_summary.strip() + '\n'

    new_file_name = file_name.replace('.lua', '') + '_features.txt'
    new_file = open((new_file_name), 'w+')
    new_file.write('Features list generated using Lance\'s feature-writer\n')
    new_file.write(str(feature_counts) + '\n')
    new_file.write(feature_writeout)

    print('Features saved to', new_file_name, f'!\nCounts:\n', feature_counts)
