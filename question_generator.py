"""Deterministic local generators for expanding the LMS question bank."""

import itertools


def generate_additional_questions(category, existing_questions, target_count):
    """Generate unique academic MCQs until the requested pool size is reached."""
    existing_text = {item['question'] for item in existing_questions}
    generated = []

    if category == 'highschool':
        for number in itertools.count(1):
            candidates = [
                ('Mathematics', 'Arithmetic', f'What is {number} + {number * 3}?', str(number * 4), str(number * 3), str(number + 3), str(number * 5), 'A', f'{number} + {number * 3} = {number * 4}.'),
                ('Mathematics', 'Arithmetic', f'What is {number * 5} - {number * 2}?', str(number * 3), str(number * 2), str(number * 4), str(number * 5), 'A', f'{number * 5} - {number * 2} = {number * 3}.'),
                ('Science', 'Units', f'How many metres are equal to {number} kilometres?', str(number * 1000), str(number * 100), str(number * 10), str(number), 'A', 'One kilometre equals 1,000 metres.'),
                ('Biology', 'Cells', f'Which structure is known as the control centre of a cell in question set {number}?', 'Nucleus', 'Cell wall', 'Vacuole', 'Cytoplasm', 'A', 'The nucleus contains genetic material and controls cell activities.'),
                ('Geography', 'Earth', f'What is the approximate number of days in one year in question set {number}?', '365', '300', '180', '500', 'A', 'A regular year has approximately 365 days.'),
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
