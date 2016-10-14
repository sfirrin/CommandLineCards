import os
import ConfigParser
import random

def get_path_and_files( paths ):
    for i in range( len( paths ) ):
        print( str( i ) + ' - ' + paths[i] )

    while True:
        try:
            path_input = raw_input( 'Enter the number of the path, or another full path:\n' )

            try:
                # Check to see if the path input corresponds to a path in the config's input
                path = paths[ int( path_input ) ]
            except ValueError:
                # If what was entered was not an index, treat it as a path
                path = path_input

            return path, [ note for note in os.listdir( path ) ]

        except OSError:
            print( 'I could not find that path. Please try again' )


def get_response( prompt ):
    user_response = ''
    print( prompt )
    while True:
        current_response = raw_input( '>' )
        user_response += current_response + '\n'
        if current_response in [ 'add', 'flag', 'exit' ]:
            break
        # If the user has entered a response, give them more lines to type
        if not current_response:
            break
    return user_response.strip()



def review_cards(notecards, notes_text):
    # Returns the flagged cards
    randomize = raw_input('Randomize? [Y/n]')

    if not randomize or randomize.lower() == 'y':
        random.shuffle(notecards)

    flagged = []
    for note in notecards:
        clue_response = get_response( note[0] )
        if clue_response == 'exit':
            break
        answer_response = get_response( note[1].strip() )
        if answer_response == 'exit':
            break
        if 'flag' in [ clue_response, answer_response ]:
            flagged.append( note )
            print( 'Note flagged for more review ')
        elif 'add' in [ clue_response, answer_response ]:
            to_add_to_notes = get_response(
                'Enter what you would like to add to this card\'s definition' )
            # Adding the user's input to the definition in the notes file
            notes_text = notes_text.replace(note[1], note[1] + '\n' + to_add_to_notes)
            # Adding it to the card as well, in case the user wants to see it again
            note[1] += '\n' + to_add_to_notes
        print('')

    print ( '\nReview complete with ' + str( len( flagged ) ) + ' flagged cards' )
    if flagged:
        review_flagged = raw_input( 'Review these flagged cards? [Y/n] ' )
        if review_flagged.lower() in ['', 'y']:
            notes_text = review_cards( flagged, notes_text )
    return notes_text


def get_notecards( note_contents ):
    split_notes = note_contents.split('\n\n')

    notecards = []

    for note in split_notes:
        note_lines = note.split('\n')
        clue = note_lines[0].replace('# ', '')
        answer = '\n'.join(note_lines[1:])
        if answer == '':
            continue
        notecards.append([clue, answer])

    return notecards


def main():

    config = ConfigParser.ConfigParser()
    config.read('config.ini')
    paths = [ pair[1] for pair in config.items( 'paths' ) ]

    path, path_files = get_path_and_files( paths )

    print('')

    while True:
        for i in range( len( path_files ) ):
            print( str(i) + ' - ' + path_files[ i ] )

        print('')
        # TODO: Allow user to use cards from multiple files by entering '1 6 3 9' etc.
        file_index = raw_input(
            'Enter the number of the notes you would like to review, or "exit" to end execution:\n' )
        if file_index == 'exit':
            break
        file_index = int( file_index )

        with open( path + '/' + path_files[file_index], 'rb' ) as note_file:
            note_contents = note_file.read()

        notecards = get_notecards( note_contents )

        print( str( len( notecards ) ) + ' notes found' )

        print( "Enter 'exit' to end review, 'flag' to flag a card for further review,"
               " or 'add' to add lines to the notes file" )

        # TODO: Store user answers to questions?, possibly compare their development over time

        changed_notes = review_cards( notecards, note_contents )

        if changed_notes != note_contents:
            with open( path + '/' + path_files[file_index], 'w+' ) as note_file:
                note_file.write( changed_notes )


if __name__ == '__main__':
    main()