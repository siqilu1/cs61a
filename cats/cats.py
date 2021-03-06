"""Typing test implementation"""

from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    >>> ps = ['short', 'really long', 'tiny']
    >>> s = lambda p: len(p) <= 5
    >>> choose(ps, s, 0)
    >>> 'short
    >>> choose(ps, s, 1)
    >>> 'tiny'
    """
    p_index, list = len(paragraphs), []
    for i in range(p_index):
        if select(paragraphs[i]):
            list.append(paragraphs[i])
    if k < len(list):
        return list[k]
    else:
        return ""



def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'

    def helper(sentence):
        sentence = split(lower(remove_punctuation(sentence)))
        for i in range(len(topic)): 
            if topic[i] in sentence:
                return True
        return False
    return helper



def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    correctness = 0

    if len(typed_words) == 0:
        return 0.0
    elif len(typed_words) <= len(reference_words):
        for i in range(len(typed_words)):
            if typed_words[i] == reference_words[i]:
                correctness += 1
    else:
        for i in range(len(reference_words)):
            if typed_words[i] == reference_words[i]:
                correctness += 1
    return correctness/len(typed_words)*100



def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'

    words = len(typed)/5
    time = elapsed/60
    return words/time




###########
# Phase 2 #
###########



def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.

    user_words --> str
    valid_words --> list 
    diff_fucntion --> func
    limit --> int
    """
    if user_word in valid_words:
        return user_word
    else:
        lowest_diff_word = min(valid_words, key=lambda x: diff_function(user_word, x, limit))
        lowest_diff = diff_function(user_word, lowest_diff_word, limit)
        if lowest_diff > limit:
            return user_word
        else:
            return lowest_diff_word


def shifty_shifts(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.

    >>> from cats import shifty_shifts, autocorrect
    >>> import tests.construct_check as test
    >>> big_limit = 10
    >>> shifty_shifts("car", "cad", big_limit)
    >>> 1

    >>> shifty_shifts("this", "that", big_limit)
    >>> 2

    >>> shifty_shifts("one", "two", big_limit)
    >>>  3
    """

    if start == goal:
        return 0
    elif limit == 0:
        return 1
    elif len(start) == 0:
        return len(goal)
    elif len(goal) == 0:
        return len(start)
    else:
        if start[0] != goal[0]:
            return shifty_shifts(start[1:], goal[1:], limit - 1) + 1
        else:
            return shifty_shifts(start[1:], goal[1:], limit)



def pawssible_patches(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL.

    >>> big_limit = 10
    >>> pawssible_patches("cats", "scat", big_limit)       # cats -> scats -> scat
    2
    >>> pawssible_patches("purng", "purring", big_limit)   # purng -> purrng -> purring
    2
    >>> pawssible_patches("ckiteus", "kittens", big_limit) # ckiteus -> kiteus -> kitteus -> kittens
    3

    """

    if start == goal: # Fill in the condition
        return 0

    elif len(start) == 0: # Feel free to remove or add additional cases
        return len(goal)
    
    elif len(goal) == 0:
        return len(start)

    elif limit == 0:
        return 1

    else:
        if start[0] != goal[0]:
            add_diff = pawssible_patches(start, goal[1:], limit-1) + 1
            remove_diff = pawssible_patches(start[1:], goal, limit-1) + 1
            substitute_diff = pawssible_patches(start[1:], goal[1:], limit-1) + 1
            return min(add_diff, remove_diff, substitute_diff)
        else:
            return pawssible_patches(start[1:], goal[1:], limit)


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'


###########
# Phase 3 #
###########


def report_progress(typed, prompt, user_id, send):
    """Send a report of your id and progress so far to the multiplayer server."""

    num_all_correct, i = 0, 0
    while i < len(typed) and typed[i] == prompt[i]:
        num_all_correct, i = num_all_correct+1, i+1
    progress_percent = num_all_correct / len(prompt)
    send({'id': user_id, 'progress': progress_percent})
    return progress_percent


def fastest_words_report(times_per_player, words):
    """Return a text description of the fastest words typed by each player."""
    game = time_per_word(times_per_player, words)
    fastest = fastest_words(game)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def time_per_word(times_per_player, words):
    """Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.
    """

    times = [ [ times_per_player[p][i+1] - times_per_player[p][i] for i in range(len(words)) ] for p in range(len(times_per_player))]
    return game(words, times)


def fastest_words(game):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        game: a game data abstraction as returned by time_per_word.
    Returns:
        a list of lists containing which words each player typed fastest
    """
    player_indices = range(len(all_times(game)))  # contains an *index* for each player
    word_indices = range(len(all_words(game)))    # contains an *index* for each word

    result = [[] for player in player_indices]    # list of lists for each player

    for word in word_indices:   # loop through every single word
        work_at = word_at(game, word)
        list_time = [time_item[word] for time_item in all_times(game)] # a list of lists; within each sublist, contains all time_per_word for each player
        smallest_timelapse = min(list_time)
        smallest_index = list_time.index(smallest_timelapse)
        result[smallest_index].append(work_at)
    return result


def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]


def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def all_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def all_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])

enable_multiplayer = True  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)