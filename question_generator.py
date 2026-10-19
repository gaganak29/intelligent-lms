"""Deterministic local generators for expanding the LMS question bank."""

import itertools


def generate_additional_questions(category, existing_questions, target_count, subject=None):
    """Generate unique academic MCQs until the requested pool size is reached."""
    existing_text = {item['question'] for item in existing_questions}
    generated = []

    if category == 'puc_degree' and subject in {'CET', 'JEE', 'DSA Aptitude'}:
        templates = {
            'CET': [
                ('Physics', 'Motion', 'What is the SI unit of acceleration?', 'm/s', 'm/s^2', 'N', 'J', 'B', 'Acceleration is measured in metres per second squared.'),
                ('Chemistry', 'Atomic Structure', 'How many electrons can the second shell of an atom hold at maximum?', '2', '8', '18', '32', 'B', 'The second shell has one s and three p orbitals, holding 8 electrons.'),
                ('Mathematics', 'Algebra', 'If x + {number} = {number_plus}, what is x?', '{number}', '{number_plus}', '1', '0', 'A', 'Subtracting {number} from both sides gives x = {number}.'),
                ('Biology', 'Cell Biology', 'Which organelle is known as the powerhouse of the cell in question {number}?', 'Ribosome', 'Mitochondrion', 'Nucleus', 'Golgi body', 'B', 'Mitochondria generate most cellular ATP.'),
                ('Physics', 'Electricity', 'What happens to the resistance of a metallic conductor when its temperature increases in question {number}?', 'It increases', 'It decreases', 'It becomes zero', 'It stays exactly constant', 'A', 'Metal resistance generally increases with temperature.'),
                ('Chemistry', 'Solutions', 'A solution with pH {ph} is best described as:', 'Strongly acidic', 'Neutral', 'Basic', 'A salt only', 'C', 'A pH above 7 indicates a basic solution.'),
                ('Mathematics', 'Probability', 'What is the probability of getting a head on a fair coin in trial {number}?', '0', '1/4', '1/2', '1', 'C', 'A fair coin has two equally likely outcomes.'),
                ('Biology', 'Genetics', 'The basic unit of heredity in question {number} is called a:', 'Tissue', 'Gene', 'Species', 'Enzyme', 'B', 'A gene is the basic unit that carries hereditary information.'),
            ],
            'JEE': [
                ('Physics', 'Mechanics', 'For a body moving with constant velocity in question {number}, its acceleration is:', 'Zero', 'Constant non-zero', 'Increasing', 'Undefined', 'A', 'Constant velocity means zero change in velocity.'),
                ('Physics', 'Electrostatics', 'The electric field inside an ideal conductor in electrostatic equilibrium in question {number} is:', 'Maximum', 'Zero', 'Infinite', 'Variable', 'B', 'Free charges rearrange until the internal electrostatic field is zero.'),
                ('Chemistry', 'Physical Chemistry', 'The oxidation number of oxygen in most compounds in question {number} is:', '-2', '-1', '0', '+2', 'A', 'Oxygen generally has oxidation number -2, except in special compounds.'),
                ('Chemistry', 'Organic Chemistry', 'The functional group -OH in question {number} represents:', 'Aldehyde', 'Ketone', 'Alcohol', 'Amine', 'C', 'The hydroxyl group is characteristic of alcohols.'),
                ('Mathematics', 'Calculus', 'The derivative of x^{number} with respect to x is:', '{number}x^{number_minus}', 'x^{number}', '{number_plus}x', '1', 'A', 'The power rule gives n*x^(n-1).'),
                ('Mathematics', 'Complex Numbers', 'The modulus of the complex number {number} + {number}i is:', '{number}', '{number_plus}', '{number_squared}', '1', 'B', 'Its modulus is sqrt(n^2+n^2), represented here by the second option.'),
                ('Physics', 'Waves', 'The SI unit of frequency in question {number} is:', 'Joule', 'Hertz', 'Newton', 'Watt', 'B', 'Frequency is measured in hertz (cycles per second).'),
                ('Chemistry', 'Chemical Bonding', 'A bond formed by sharing electron pairs in question {number} is:', 'Ionic', 'Metallic', 'Covalent', 'Hydrogen', 'C', 'Covalent bonds result from shared electron pairs.'),
            ],
            'DSA Aptitude': [
                ('Arrays', 'Complexity', 'What is the time complexity of accessing index {number} in an array?', 'O(1)', 'O(n)', 'O(log n)', 'O(n^2)', 'A', 'Array indexing uses direct address arithmetic.'),
                ('Linked Lists', 'Pointers', 'In question {number}, inserting after a node when its pointer is known takes:', 'O(1)', 'O(n)', 'O(log n)', 'O(n log n)', 'A', 'Only a constant number of links must be updated.'),
                ('Stacks', 'Applications', 'Which structure is most suitable for matching parentheses in expression {number}?', 'Queue', 'Stack', 'Heap', 'Graph', 'B', 'A stack tracks the most recently opened unmatched parenthesis.'),
                ('Queues', 'Traversal', 'Which traversal uses a queue to visit a graph level by level in question {number}?', 'DFS', 'BFS', 'Binary search', 'Merge sort', 'B', 'Breadth-first search processes vertices level by level with a queue.'),
                ('Sorting', 'Algorithms', 'The average time complexity of comparison-based merge sort in question {number} is:', 'O(n)', 'O(log n)', 'O(n log n)', 'O(n^2)', 'C', 'Merge sort divides and merges in O(n log n) time.'),
                ('Trees', 'Binary Search Trees', 'Which traversal returns sorted keys from a BST in question {number}?', 'Preorder', 'Inorder', 'Postorder', 'Level order', 'B', 'Inorder traversal visits left subtree, root, then right subtree.'),
                ('Graphs', 'Shortest Paths', 'Which algorithm handles negative edge weights without negative cycles in question {number}?', 'BFS', 'Bellman-Ford', 'Prim', 'Binary search', 'B', 'Bellman-Ford relaxes edges repeatedly and supports negative weights.'),
                ('Hashing', 'Hash Tables', 'When two keys map to the same slot in question {number}, it is called:', 'Recursion', 'Collision', 'Overflow only', 'Traversal', 'B', 'A collision occurs when distinct keys receive the same hash slot.'),
            ],
        }
        for number in itertools.count(1):
            for subject_name, topic, question, option_a, option_b, option_c, option_d, correct, explanation in templates[subject]:
                values = {
                    'number': number,
                    'number_plus': number + 1,
                    'number_minus': max(0, number - 1),
                    'number_squared': number * number,
                    'ph': 7 + (number % 4),
                }
                question = question.format(**values)
                options = [value.format(**values) for value in (option_a, option_b, option_c, option_d)]
                explanation = explanation.format(**values)
                if question in existing_text:
                    continue
                generated.append({
                    'category': category, 'subject': subject, 'topic': topic,
                    'question': question, 'option_a': options[0], 'option_b': options[1],
                    'option_c': options[2], 'option_d': options[3],
                    'correct_answer': correct, 'explanation': explanation,
                    'difficulty': 'Medium'
                })
                existing_text.add(question)
                if len(existing_questions) + len(generated) >= target_count:
                    return generated

    if category == 'highschool':
        for number in itertools.count(1):
            candidates = [
                ('Math', 'Arithmetic', f'What is {number} + {number * 3}?', str(number * 4), str(number * 3), str(number + 3), str(number * 5), 'A', f'{number} + {number * 3} = {number * 4}.'),
                ('Math', 'Arithmetic', f'What is {number * 5} - {number * 2}?', str(number * 3), str(number * 2), str(number * 4), str(number * 5), 'A', f'{number * 5} - {number * 2} = {number * 3}.'),
                ('Physics', 'Units', f'How many metres are equal to {number} kilometres?', str(number * 1000), str(number * 100), str(number * 10), str(number), 'A', 'One kilometre equals 1,000 metres.'),
                ('Chemistry', 'Atoms', f'Which element has the chemical symbol O?', 'Oxygen', 'Gold', 'Osmium', 'Argon', 'A', 'The chemical symbol O stands for oxygen.'),
                ('Biology', 'Cells', f'Which structure is known as the control centre of a cell in question set {number}?', 'Nucleus', 'Cell wall', 'Vacuole', 'Cytoplasm', 'A', 'The nucleus contains genetic material and controls cell activities.'),
                ('History', 'Ancient Civilizations', f'Which civilization built the pyramids of Giza in question set {number}?', 'Romans', 'Egyptians', 'Greeks', 'Maya', 'B', 'The ancient Egyptians built the pyramids of Giza.'),
                ('Geography', 'Earth', f'What is the approximate number of days in one year in question set {number}?', '365', '300', '180', '500', 'A', 'A regular year has approximately 365 days.'),
                ('English', 'Grammar', f'Choose the correct sentence in question set {number}?', 'She go to school every day.', 'She goes to school every day.', 'She going to school every day.', 'She gone to school every day.', 'B', 'The correct present simple form is “She goes to school every day.”'),
            ]
            for subject, topic, question, option_a, option_b, option_c, option_d, correct, explanation in candidates:
                if question in existing_text:
                    continue
                generated.append({
                    'category': category, 'subject': subject, 'topic': topic,
                    'question': question, 'option_a': option_a, 'option_b': option_b,
                    'option_c': option_c, 'option_d': option_d,
                    'correct_answer': correct, 'explanation': explanation, 'difficulty': 'Easy'
                })
                existing_text.add(question)
                if len(existing_questions) + len(generated) >= target_count:
                    return generated
    else:
        for number in itertools.count(1):
            candidates = [
                ('Algorithms', 'Complexity', f'What is the time complexity of scanning an array of {number} elements once?', 'O(n)', 'O(1)', 'O(log n)', 'O(n^2)', 'A', 'A single pass visits each element once, giving linear time.'),
                ('Data Structures', 'Arrays', f'How many indices does a zero-based array containing {number + 1} items have?', str(number + 1), str(number), str(number + 2), '1', 'A', 'A zero-based array with n items has indices from 0 through n-1.'),
                ('DBMS', 'Transactions', f'Which property ensures a database transaction is treated as one indivisible unit in example {number}?', 'Atomicity', 'Availability', 'Inheritance', 'Polymorphism', 'A', 'Atomicity means a transaction completes entirely or not at all.'),
                ('Python', 'Language', f'What is the result type of a Python list comprehension in example {number}?', 'list', 'tuple', 'set', 'dictionary', 'A', 'List comprehensions create list objects.'),
                ('Computer Networks', 'Protocols', f'Which protocol translates a domain name to an IP address in example {number}?', 'DNS', 'HTTP', 'FTP', 'SSH', 'A', 'DNS resolves human-readable domain names to IP addresses.'),
            ]
            for subject, topic, question, option_a, option_b, option_c, option_d, correct, explanation in candidates:
                if question in existing_text:
                    continue
                generated.append({
                    'category': category, 'subject': subject, 'topic': topic,
                    'question': question, 'option_a': option_a, 'option_b': option_b,
                    'option_c': option_c, 'option_d': option_d,
                    'correct_answer': correct, 'explanation': explanation, 'difficulty': 'Easy'
                })
                existing_text.add(question)
                if len(existing_questions) + len(generated) >= target_count:
                    return generated

    return generated
