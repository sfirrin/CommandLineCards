import os
import re
import random

def main():
    # TODO: Allow user to save their note directories and choose between them by entering the index
    # or entering a full path
    path = raw_input( 'Enter the path of your notes, or nothing to use current path:\n' )
    if path == '':
        path = '/run/media/stephen/01D1F11567B88C10/googledrive/school/comp455/notes'

    path_files = [ note for note in os.listdir( path ) ]

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

        split_notes = note_contents.split( '\n\n' )

        notecards = []

        for note in split_notes:
            note_lines = note.split( '\n' )
            clue = note_lines[0].replace( '# ', '' )
            answer = '\n'.join(note_lines[1:])
            if answer == '':
                continue
            notecards.append( [ clue, answer ] )
        # pprint( notecards )


        print( str( len( notecards ) ) + ' notes found' )

        print( "Enter 'exit' to end review, 'flag' to flag a card for further review," )
        print( "or 'add' to add lines to the notes file" )
        # TODO: Store user answers to questions?, possibly compare their development over time

        changed_notes = review_cards( notecards, note_contents )
        print(changed_notes)


        if changed_notes != note_contents:
            with open( path + '/' + path_files[file_index], 'w+' ) as note_file:
                note_file.write( changed_notes )
                print('should have written')


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


def get_response( prompt ):
    user_response = ''
    print( prompt )
    while True:
        current_response = raw_input( '>' )
        # If the user has entered a response, give them more lines to type
        if not current_response:
            break
        user_response += current_response + '\n'
    return user_response.strip()

if __name__ == '__main__':
    main()