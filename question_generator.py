"""Deterministic local generators for expanding the LMS question bank."""

import hashlib
import random
from functools import lru_cache

DSA_APTITUDE_TOPICS = (
    'Arrays',
    'Strings',
    'Linked Lists',
    'Stacks',
    'Queues',
    'Hash Maps',
    'Searching',
    'Sorting',
    'Trees',
    'Graphs',
)


def _shuffle_options(options, answer, seed_text):
    correct_index = ord(answer.upper()) - ord('A')
    indexed_options = list(enumerate(str(option) for option in options))
    seed = int.from_bytes(hashlib.sha256(seed_text.encode('utf-8')).digest(), 'big')
    random.Random(seed).shuffle(indexed_options)
    shuffled_options = [option for _, option in indexed_options]
    shuffled_answer = chr(ord('A') + next(
        index for index, (original_index, _) in enumerate(indexed_options)
        if original_index == correct_index
    ))
    return shuffled_options, shuffled_answer


def _question(category, subject, topic, text, options, answer, explanation, difficulty='Medium', exam=None):
    shuffled_options, shuffled_answer = _shuffle_options(options, answer, text)
    return {
        'category': category,
        'subject': subject,
        'exam': exam,
        'topic': topic,
        'question': text,
        'option_a': shuffled_options[0],
        'option_b': shuffled_options[1],
        'option_c': shuffled_options[2],
        'option_d': shuffled_options[3],
        'correct_answer': shuffled_answer,
        'explanation': explanation,
        'difficulty': difficulty,
    }


def _numeric_options(answer):
    distractors = []
    for value in (answer + 2, answer - 1, answer + 5, answer * 2, answer + 1):
        if value != answer and value not in distractors:
            distractors.append(value)
        if len(distractors) == 3:
            break
    return [answer, *distractors]


@lru_cache(maxsize=3)
def _exam_candidates(category, subject):
    questions = []

    if subject == 'CET':
        for value in range(2, 1002):
            attempt_group = (value - 2) // 50
            variant = ((value - 2) // 3 + attempt_group) % 3
            physics_topic = ('Kinematics', 'Laws of Motion', 'Work and Energy', 'Current Electricity', 'Waves', 'Optics')[
                (value // 9 + attempt_group) % 6
            ]
            if physics_topic == 'Kinematics':
                acceleration, time = value + 2, value % 8 + 2
                initial_speed = value + 2
                if variant == 0:
                    answer = initial_speed + acceleration * time
                    text = f'A car moving at {initial_speed} m/s accelerates at {acceleration} m/s² for {time} s. Find its final speed.'
                    explanation = f'v = u + at = {initial_speed} + {acceleration} × {time} = {answer} m/s.'
                elif variant == 1:
                    answer = initial_speed * time + 0.5 * acceleration * time ** 2
                    text = f'A particle has initial speed {initial_speed} m/s and acceleration {acceleration} m/s². How far does it travel in {time} s?'
                    explanation = f's = ut + ½at² = {initial_speed} × {time} + ½ × {acceleration} × {time}² = {answer} m.'
                else:
                    final_speed = initial_speed + acceleration * time
                    answer = time
                    text = f'A body speeds up from {initial_speed} m/s to {final_speed} m/s at {acceleration} m/s². How long does the change take?'
                    explanation = f't = (v - u) / a = ({final_speed} - {initial_speed}) / {acceleration} = {answer} s.'
                options = _numeric_options(round(answer, 2))
            elif physics_topic == 'Laws of Motion':
                mass, acceleration = value + 3, value % 9 + 2
                if variant == 0:
                    answer = mass * acceleration
                    text = f'A {mass} kg trolley accelerates at {acceleration} m/s². What net force acts on it?'
                    explanation = f'F = ma = {mass} × {acceleration} = {answer} N.'
                elif variant == 1:
                    force = mass * acceleration
                    answer = acceleration
                    text = f'A net force of {force} N acts on a {mass} kg object. Find its acceleration.'
                    explanation = f'a = F / m = {force} / {mass} = {answer} m/s².'
                else:
                    force, duration = value + 4, value % 7 + 2
                    answer = force * duration
                    text = f'A constant force of {force} N acts for {duration} s. What impulse is delivered?'
                    explanation = f'Impulse = FΔt = {force} × {duration} = {answer} N·s.'
                options = _numeric_options(answer)
            elif physics_topic == 'Work and Energy':
                mass, speed, height = value + 2, value % 10 + 3, value + 2
                if variant == 0:
                    force, distance = value + 3, value % 10 + 2
                    answer = force * distance
                    text = f'A {force} N force moves a crate {distance} m in the force direction. Calculate the work done.'
                    explanation = f'W = Fd = {force} × {distance} = {answer} J.'
                elif variant == 1:
                    answer = 0.5 * mass * speed ** 2
                    text = f'Calculate the kinetic energy of a {mass} kg ball moving at {speed} m/s.'
                    explanation = f'KE = ½mv² = ½ × {mass} × {speed}² = {answer} J.'
                else:
                    answer = mass * 10 * height
                    text = f'A {mass} kg object is held {height} m above the ground. Take g = 10 m/s²; find its gravitational potential energy.'
                    explanation = f'PE = mgh = {mass} × 10 × {height} = {answer} J.'
                options = _numeric_options(round(answer, 2))
            elif physics_topic == 'Current Electricity':
                resistance, current = value + 2, value % 9 + 2
                if variant == 0:
                    answer = resistance * current
                    text = f'Find the voltage across a {resistance} Ω resistor carrying {current} A.'
                    explanation = f'V = IR = {resistance} × {current} = {answer} V.'
                elif variant == 1:
                    answer = current ** 2 * resistance
                    text = f'How much electrical power is dissipated by a {resistance} Ω resistor carrying {current} A?'
                    explanation = f'P = I²R = {current}² × {resistance} = {answer} W.'
                else:
                    voltage = resistance * current
                    answer = current
                    text = f'A {voltage} V source is connected across a {resistance} Ω resistor. Find the current.'
                    explanation = f'I = V / R = {voltage} / {resistance} = {answer} A.'
                options = _numeric_options(answer)
            elif physics_topic == 'Waves':
                frequency, wavelength = value + 2, value % 12 + 2
                if variant == 0:
                    answer = frequency * wavelength
                    text = f'A wave has frequency {frequency} Hz and wavelength {wavelength} m. Find its speed.'
                    explanation = f'v = fλ = {frequency} × {wavelength} = {answer} m/s.'
                elif variant == 1:
                    speed = frequency * wavelength
                    answer = frequency
                    text = f'A sound wave travels at {speed} m/s with wavelength {wavelength} m. What is its frequency?'
                    explanation = f'f = v / λ = {speed} / {wavelength} = {answer} Hz.'
                else:
                    answer = 1 / frequency
                    text = f'A wave completes {frequency} cycles each second. What is its period?'
                    explanation = f'T = 1 / f = 1 / {frequency} = {answer} s.'
                options = _numeric_options(round(answer, 2))
            else:
                focal_length, object_distance = value + 4, value + 20
                if variant == 0:
                    image_distance = focal_length * object_distance / (object_distance - focal_length)
                    answer = round(image_distance, 2)
                    text = f'A convex lens has focal length {focal_length} cm and an object is {object_distance} cm away. Find the image distance.'
                    explanation = f'Using 1/f = 1/u + 1/v gives v = fu/(u-f) = {answer} cm.'
                elif variant == 1:
                    object_distance = value + 2
                    image_distance = value + 3
                    answer = round(image_distance / object_distance, 2)
                    text = f'An object {object_distance} cm tall forms an image {image_distance} cm tall. What is the magnitude of magnification?'
                    explanation = f'|m| = image height / object height = {image_distance} / {object_distance} = {answer}.'
                else:
                    answer = value + 2
                    medium_speed = 3e8 / answer
                    text = f'Light travels at {medium_speed:.0f} m/s in a medium. Find its refractive index (c = 3 × 10⁸ m/s).'
                    explanation = f'n = c / v = 3 × 10⁸ / {medium_speed:.0f} = {answer}.'
                options = _numeric_options(round(answer, 2))
            questions.append(_question(
                category, 'Physics', physics_topic, text, options, 'A', explanation,
                exam=subject,
            ))

            chemistry_topic = ('Mole Concept', 'Acids and Bases', 'Gas Laws', 'Redox Reactions')[
                (value // 9 + attempt_group) % 4
            ]
            if chemistry_topic == 'Mole Concept':
                if variant == 0:
                    moles, molar_mass = value + 2, value + 12
                    answer = moles * molar_mass
                    text = f'Find the mass of {moles} mol of a substance with molar mass {molar_mass} g/mol.'
                    explanation = f'm = nM = {moles} × {molar_mass} = {answer} g.'
                elif variant == 1:
                    moles = value + 2
                    answer = moles * 6.022
                    text = f'Approximately how many ×10²³ particles are present in {moles} mol of a substance?'
                    explanation = f'N = nNₐ = {moles} × 6.022 × 10²³ = {answer:.3f} × 10²³ particles.'
                else:
                    amount, molar_mass = value + 2, value + 10
                    mass = amount * molar_mass
                    answer = amount
                    text = f'A {mass} g sample has molar mass {molar_mass} g/mol. How many moles are present?'
                    explanation = f'n = m / M = {mass} / {molar_mass} = {answer} mol.'
                options = _numeric_options(round(answer, 2))
            elif chemistry_topic == 'Acids and Bases':
                if variant == 0:
                    answer = value % 10 + 2
                    text = f'Calculate the pH when [H⁺] = 1.0 × 10⁻{answer} mol/L.'
                    explanation = f'pH = -log₁₀[H⁺] = {answer}.'
                elif variant == 1:
                    poh = value % 10 + 2
                    answer = 14 - poh
                    text = f'A solution has pOH {poh} at 25°C. What is its pH?'
                    explanation = f'pH + pOH = 14, so pH = 14 - {poh} = {answer}.'
                else:
                    answer = value + 2
                    text = f'What is the hydrogen-ion concentration of a solution with pH {answer}?'
                    explanation = f'[H⁺] = 10⁻ᵖᴴ = 1 × 10⁻{answer} mol/L.'
                    options = [f'1×10⁻{answer}', f'1×10⁻{answer + 1}', f'1×10⁻{answer - 1}', f'{answer} mol/L']
                if variant != 2:
                    options = _numeric_options(answer)
            elif chemistry_topic == 'Gas Laws':
                if variant == 0:
                    moles = value + 2
                    answer = moles * 22.4
                    text = f'What volume does {moles} mol of an ideal gas occupy at STP?'
                    explanation = f'At STP, V = n × 22.4 = {moles} × 22.4 = {answer} L.'
                elif variant == 1:
                    pressure_1, volume_1, pressure_2 = value + 2, value + 5, value + 3
                    answer = round(pressure_1 * volume_1 / pressure_2, 2)
                    text = f'A gas occupies {volume_1} L at {pressure_1} atm. What volume will it occupy at {pressure_2} atm if temperature is constant?'
                    explanation = f'Boyle’s law gives V₂ = P₁V₁/P₂ = {pressure_1} × {volume_1}/{pressure_2} = {answer} L.'
                else:
                    volume_1, temp_1, temp_2 = value + 2, value + 250, value + 300
                    answer = round(volume_1 * temp_2 / temp_1, 2)
                    text = f'A gas occupies {volume_1} L at {temp_1} K. Find its volume at {temp_2} K at constant pressure.'
                    explanation = f'Charles’s law gives V₂ = V₁T₂/T₁ = {volume_1} × {temp_2}/{temp_1} = {answer} L.'
                options = _numeric_options(round(answer, 2))
            else:
                oxygen_count = value + 2
                charge = value % 3 + 1
                answer = 2 * oxygen_count - charge
                symbol = ('X', 'Y', 'Z')[value % 3]
                text = f'What is the oxidation state of {symbol} in {symbol}O{oxygen_count}⁻{charge}?'
                explanation = f'Oxygen contributes -{2 * oxygen_count}; the ion charge is -{charge}, so {symbol} must be +{answer}.'
                if variant == 1:
                    electron_count = value + 2
                    answer = electron_count
                    text = f'An atom loses {electron_count} electrons during a reaction. By how much does its oxidation number change?'
                    explanation = f'Loss of {electron_count} electrons increases the oxidation number by {electron_count}.'
                elif variant == 2:
                    reactant_moles = value + 2
                    answer = reactant_moles * 2
                    text = f'Each mole of a reducing agent transfers 2 mol of electrons. How many moles of electrons are transferred by {reactant_moles} mol?'
                    explanation = f'Electron transfer = {reactant_moles} × 2 = {answer} mol e⁻.'
                options = _numeric_options(answer)
            questions.append(_question(
                category, 'Chemistry', chemistry_topic, text, options, 'A', explanation,
                exam=subject,
            ))

            math_topic = ('Algebra', 'Quadratic Equations', 'Geometry', 'Sequences', 'Probability')[
                (value // 9 + attempt_group) % 5
            ]
            if math_topic == 'Algebra':
                if variant == 0:
                    answer = value + 2
                    constant = answer * 3
                    text = f'Solve 3x - {answer} = {2 * answer} for x.'
                    explanation = f'3x = {3 * answer}, hence x = {answer}.'
                elif variant == 1:
                    x = value + 2
                    coefficient = value % 7 + 2
                    constant = coefficient * x
                    answer = x
                    text = f'If f(x) = {coefficient}x + 1, what is f({x})?'
                    explanation = f'f({x}) = {coefficient} × {x} + 1 = {constant + 1}.'
                    answer = constant + 1
                else:
                    x = value + 2
                    y = value % 8 + 3
                    total = x + y
                    answer = x
                    text = f'If x + y = {total} and y = {y}, find x.'
                    explanation = f'x = {total} - {y} = {answer}.'
                options = _numeric_options(answer)
            elif math_topic == 'Quadratic Equations':
                first_root, second_root = value + 2, value + 15
                if variant == 0:
                    answer = first_root + second_root
                    text = f'A quadratic has roots {first_root} and {second_root}. What is their sum?'
                    explanation = f'Sum of roots = {first_root} + {second_root} = {answer}.'
                elif variant == 1:
                    answer = first_root * second_root
                    text = f'A quadratic has roots {first_root} and {second_root}. What is their product?'
                    explanation = f'Product of roots = {first_root} × {second_root} = {answer}.'
                else:
                    answer = 1 if first_root != second_root else 0
                    text = f'How many distinct real roots does x² - {first_root + second_root}x + {first_root * second_root} = 0 have?'
                    explanation = f'The equation factors as (x-{first_root})(x-{second_root}) = 0 and has {answer + 1} distinct real roots.'
                    answer += 1
                options = _numeric_options(answer)
            elif math_topic == 'Geometry':
                if variant == 0:
                    base, height = value + 4, value + 3
                    answer = base * height / 2
                    text = f'Find the area of a triangle with base {base} cm and height {height} cm.'
                    explanation = f'A = ½bh = ½ × {base} × {height} = {answer} cm².'
                elif variant == 1:
                    radius = (value + 2) * 7
                    answer = 22 * radius / 7
                    text = f'Find the circumference of a circle of radius {radius} cm. Use π = 22/7.'
                    explanation = f'C = 2πr = 2 × 22/7 × {radius} = {answer} cm.'
                else:
                    legs = value + 3
                    answer = legs * 2 ** 0.5
                    text = f'A right isosceles triangle has equal legs of {legs} cm. What is the hypotenuse?'
                    explanation = f'By Pythagoras, c = √({legs}²+{legs}²) = {answer} cm.'
                options = _numeric_options(round(answer, 2))
            elif math_topic == 'Sequences':
                first_term, difference = value + 2, value + 3
                if variant == 0:
                    position = value % 10 + 6
                    answer = first_term + (position - 1) * difference
                    text = f'Find the {position}th term of an AP with first term {first_term} and common difference {difference}.'
                    explanation = f'aₙ = a₁ + (n-1)d = {first_term} + ({position}-1)×{difference} = {answer}.'
                elif variant == 1:
                    term_count = value % 8 + 4
                    answer = term_count * (2 * first_term + (term_count - 1) * difference) / 2
                    text = f'Find the sum of the first {term_count} terms of an AP starting at {first_term} with common difference {difference}.'
                    explanation = f'Sₙ = n/2[2a+(n-1)d] = {answer}.'
                else:
                    answer = difference
                    text = f'An AP has consecutive terms {first_term}, {first_term + difference}, ... What is its common difference?'
                    explanation = f'Common difference = {first_term + difference} - {first_term} = {answer}.'
                options = _numeric_options(round(answer, 2))
            else:
                red, blue = value + 3, value + 4
                if variant == 0:
                    answer = round(red / (red + blue), 2)
                    text = f'A bag has {red} red and {blue} blue counters. What is the probability of selecting a red counter?'
                    explanation = f'P(red) = {red}/({red}+{blue}) = {answer}.'
                elif variant == 1:
                    answer = round(blue / (red + blue), 2)
                    text = f'A bag has {red} red and {blue} blue counters. What is the probability of not selecting a red counter?'
                    explanation = f'P(not red) = {blue}/({red}+{blue}) = {answer}.'
                else:
                    sides = value + 2
                    answer = sides * sides
                    text = f'Two fair dice are rolled. How many equally likely ordered outcomes have both dice showing a number from 1 to {sides}?'
                    explanation = f'There are {sides} choices for each die, giving {sides} × {sides} = {answer} outcomes.'
                options = _numeric_options(round(answer, 2))
            questions.append(_question(
                category, 'Mathematics', math_topic, text, options, 'A', explanation,
                exam=subject,
            ))

    elif subject == 'JEE':
        for value in range(2, 1002):
            attempt_group = (value - 2) // 50
            variant = ((value - 2) // 3 + attempt_group) % 3
            physics_topic = ('Electrostatics', 'Mechanics', 'Optics', 'Thermodynamics', 'Magnetism', 'Modern Physics')[
                (value // 9 + attempt_group) % 6
            ]
            if physics_topic == 'Electrostatics':
                charge, distance = value + 2, value + 3
                if variant == 0:
                    answer = round(9000 * charge / distance, 2)
                    text = f'Find the electric potential {distance} m from a +{charge} μC point charge (k = 9 × 10⁹).'
                    explanation = f'V = kq/r = 9×10⁹ × {charge}×10⁻⁶/{distance} = {answer} V.'
                elif variant == 1:
                    answer = round(9000 * charge / distance ** 2, 2)
                    text = f'What is the electric-field magnitude {distance} m from a +{charge} μC point charge?'
                    explanation = f'E = kq/r² = 9×10⁹ × {charge}×10⁻⁶/{distance}² = {answer} N/C.'
                else:
                    capacitance, voltage = value + 2, value + 10
                    answer = capacitance * voltage
                    text = f'A {capacitance} μF capacitor is connected across {voltage} V. Find its charge in μC.'
                    explanation = f'Q = CV = {capacitance} × {voltage} = {answer} μC.'
                options = _numeric_options(answer)
            elif physics_topic == 'Mechanics':
                mass, speed, radius = value + 2, value % 12 + 3, value + 2
                if variant == 0:
                    answer = round(mass * speed ** 2 / radius, 2)
                    text = f'A {mass} kg body moves at {speed} m/s in a circle of radius {radius} m. Find its centripetal force.'
                    explanation = f'F = mv²/r = {mass} × {speed}²/{radius} = {answer} N.'
                elif variant == 1:
                    impulse = value + 3
                    answer = round(impulse / mass, 2)
                    text = f'A {mass} kg ball at rest receives an impulse of {impulse} N·s. What speed does it gain?'
                    explanation = f'J = Δp = mv, so v = {impulse}/{mass} = {answer} m/s.'
                else:
                    angle = 30 if value % 2 else 60
                    answer = round(mass * 9.8 * (0.5 if angle == 60 else 0.866), 2)
                    text = f'Find the component of a {mass} kg block’s weight down a smooth {angle}° incline (g = 9.8 m/s²).'
                    explanation = f'F = mg sinθ = {mass} × 9.8 × sin({angle}°) ≈ {answer} N.'
                options = _numeric_options(answer)
            elif physics_topic == 'Optics':
                focal, obj = value + 5, value + 22
                if variant == 0:
                    answer = round(focal * obj / (obj - focal), 2)
                    text = f'A convex lens with focal length {focal} cm views an object {obj} cm away. Find the image distance.'
                    explanation = f'1/f = 1/u + 1/v gives v = fu/(u-f) = {answer} cm.'
                elif variant == 1:
                    answer = 2
                    text = 'An object is placed at 2f from a convex lens. At what distance from the lens does its real image form, in units of f?'
                    explanation = 'For an object at 2f, the image also forms at 2f.'
                else:
                    answer = round(focal / (obj - focal), 2)
                    text = f'An object is {obj} cm from a concave mirror of focal length {focal} cm. Find the magnitude of magnification.'
                    explanation = f'|m| = f/(u-f) = {focal}/({obj}-{focal}) = {answer}.'
                options = _numeric_options(answer)
            elif physics_topic == 'Thermodynamics':
                moles, temperature = value + 2, value + 280
                if variant == 0:
                    answer = round(moles * 8.314 * temperature, 2)
                    text = f'Find PV for {moles} mol of an ideal gas at {temperature} K (R = 8.314 J mol⁻¹ K⁻¹).'
                    explanation = f'PV = nRT = {moles} × 8.314 × {temperature} = {answer} J.'
                elif variant == 1:
                    answer = round(1.5 * moles * 8.314 * 20, 2)
                    text = f'A monatomic ideal gas of {moles} mol is heated by 20 K at constant volume. Find ΔU.'
                    explanation = f'ΔU = 3nRΔT/2 = 3 × {moles} × 8.314 × 20/2 = {answer} J.'
                else:
                    answer = 0
                    text = f'For an ideal gas at {temperature} K, what is ΔU during an isothermal process?'
                    explanation = 'Ideal-gas internal energy depends only on temperature, so an isothermal process has ΔU = 0.'
                options = _numeric_options(answer)
            elif physics_topic == 'Magnetism':
                if variant == 0:
                    current, length, field = value + 2, value + 2, value % 5 + 2
                    answer = current * length * field
                    text = f'A {length} m wire carrying {current} A is perpendicular to a {field} T field. Find the magnetic force.'
                    explanation = f'F = BIL = {field} × {current} × {length} = {answer} N.'
                elif variant == 1:
                    turns, flux, duration = value + 2, value + 1, value % 6 + 2
                    answer = round(turns * flux / duration, 2)
                    text = f'Flux through each of {turns} coil turns changes by {flux} Wb in {duration} s. Find the induced emf.'
                    explanation = f'|ε| = NΔΦ/Δt = {turns} × {flux}/{duration} = {answer} V.'
                else:
                    ratio, voltage = value + 2, value + 5
                    answer = voltage * ratio
                    text = f'A transformer has turns ratio Ns/Np = {ratio}. If Vp = {voltage} V, find Vs.'
                    explanation = f'Vs/Vp = Ns/Np, so Vs = {voltage} × {ratio} = {answer} V.'
                options = _numeric_options(answer)
            else:
                energy_ev = value + 2
                if variant == 0:
                    work_function = value % 6 + 2
                    answer = energy_ev
                    photon_energy = energy_ev + work_function
                    text = f'Light of photon energy {photon_energy} eV strikes a metal with work function {work_function} eV. Find the maximum photoelectron kinetic energy.'
                    explanation = f'Kmax = Ephoton - φ = {photon_energy} - {work_function} = {answer} eV.'
                elif variant == 1:
                    answer = 'A'
                    text = f'A radioactive isotope has a half-life of {value % 20 + 2} hours. What fraction remains after one half-life?'
                    options = ['1/2', '1/3', '1/4', '2/3']
                    explanation = 'After one half-life, half of the original nuclei remain.'
                else:
                    answer = energy_ev
                    text = f'An electron is accelerated through {energy_ev} V. How much energy does it gain in eV?'
                    explanation = f'An electron gains {energy_ev} eV when accelerated through {energy_ev} V.'
                if variant != 1:
                    options = _numeric_options(answer)
                else:
                    answer = 'A'
            questions.append(_question(
                category, 'Physics', physics_topic, text, options, 'A', explanation,
                'Hard', exam=subject,
            ))

            chemistry_topic = ('Mole Concept', 'Chemical Equilibrium', 'Redox Reactions', 'Chemical Bonding', 'Electrochemistry')[
                (value // 9 + attempt_group) % 5
            ]
            if chemistry_topic == 'Mole Concept':
                if variant == 0:
                    moles, molar_mass = value + 2, value + 15
                    answer = moles * molar_mass
                    text = f'Calculate the mass of {moles} mol of a compound with molar mass {molar_mass} g/mol.'
                    explanation = f'm = nM = {moles} × {molar_mass} = {answer} g.'
                    options = _numeric_options(answer)
                elif variant == 1:
                    answer = value + 2
                    sample_mass = answer * 12
                    text = f'A {sample_mass} g sample has molar mass 12 g/mol. Find its amount in moles.'
                    explanation = f'n = m/M = {sample_mass}/12 = {answer} mol.'
                    options = _numeric_options(answer)
                else:
                    moles = value + 2
                    answer = round(6.022 * moles, 3)
                    text = f'How many ×10²³ molecules are present in {moles} mol? (Nₐ = 6.022 × 10²³ mol⁻¹)'
                    explanation = f'N = nNₐ = {moles} × 6.022 = {answer} × 10²³ molecules.'
                    options = _numeric_options(answer)
            elif chemistry_topic == 'Chemical Equilibrium':
                if variant == 0:
                    concentration = value + 2
                    answer = concentration
                    text = f'For A ⇌ B, [A] = 1 M and [B] = {concentration} M at equilibrium. Find Kc.'
                    explanation = f'Kc = [B]/[A] = {concentration}/1 = {answer}.'
                    options = _numeric_options(answer)
                elif variant == 1:
                    answer = 'decreases'
                    text = f'For an exothermic reaction with ΔH = -{value + 2} kJ/mol, how does increasing temperature affect product yield?'
                    options = ['decreases', 'increases', 'unchanged', 'becomes zero']
                    explanation = 'Increasing temperature favors the endothermic reverse reaction, reducing product yield.'
                else:
                    rate = value + 2
                    answer = rate
                    text = f'At equilibrium the forward rate is {rate} mol L⁻¹ s⁻¹. What is the reverse rate?'
                    options = [str(rate), str(rate + 1), str(rate * 2), '0']
                    explanation = f'Forward and reverse rates are equal at equilibrium: {rate} mol L⁻¹ s⁻¹.'
                answer = 'A'
            elif chemistry_topic == 'Redox Reactions':
                if variant == 0:
                    oxygen_count, charge = value + 2, value % 3 + 1
                    oxidation = 2 * oxygen_count - charge
                    text = f'Find the oxidation state of X in the ion XO{oxygen_count}⁻{charge}.'
                    explanation = f'Oxygen contributes -{2 * oxygen_count}; X must be +{oxidation} for the ion charge -{charge}.'
                    options = [f'+{oxidation}', f'+{oxidation + 2}', f'+{oxidation - 1}', f'-{oxidation}']
                elif variant == 1:
                    amount = value + 2
                    text = f'An atom gains {amount} electrons. By how much does its oxidation number change?'
                    explanation = f'Gain of {amount} electrons decreases the oxidation number by {amount}.'
                    options = [str(-amount), str(amount), '0', str(-2 * amount)]
                else:
                    amount = value + 2
                    text = f'How many moles of electrons are accepted by {amount} mol of ions if each ion gains 2 electrons?'
                    explanation = f'Electron amount = {amount} × 2 = {2 * amount} mol.'
                    options = [str(2 * amount), str(amount), str(amount + 2), str(2 / amount)]
                answer = 'A'
            elif chemistry_topic == 'Chemical Bonding':
                if variant == 0:
                    carbon_count = value + 2
                    sigma_bonds = 3 * carbon_count + 1
                    text = f'How many sigma bonds are present in one molecule of the alkane C{carbon_count}H{2 * carbon_count + 2}?'
                    options = [str(sigma_bonds), str(sigma_bonds - 1), str(sigma_bonds + 1), str(2 * carbon_count)]
                    explanation = f'There are {carbon_count - 1} C–C and {2 * carbon_count + 2} C–H sigma bonds, totaling {sigma_bonds}.'
                elif variant == 1:
                    domains = 2 + value % 3
                    hybridization = ('sp', 'sp²', 'sp³')[domains - 2]
                    text = f'A central atom has {domains} electron domains and no lone pairs. What hybridization is expected?'
                    options = [hybridization, 'sp³', 'dsp²', 'sp']
                    explanation = f'{domains} electron domains correspond to {hybridization} hybridization.'
                else:
                    text = 'Which molecule has a non-zero dipole moment?'
                    options = ['H₂O', 'CO₂', 'BF₃', 'CCl₄']
                    explanation = 'Bent H₂O has an asymmetric charge distribution and a non-zero dipole moment.'
                answer = 'A'
            else:
                if variant == 0:
                    current, duration = value + 2, value + 3
                    answer = current * duration
                    text = f'A current of {current} A flows for {duration} s. What charge passes through the circuit?'
                    explanation = f'Q = It = {current} × {duration} = {answer} C.'
                    options = _numeric_options(answer)
                elif variant == 1:
                    voltage, current = value + 2, value + 2
                    answer = voltage * current
                    text = f'An electrochemical cell supplies {voltage} V at {current} A. Find its electrical power output.'
                    explanation = f'P = VI = {voltage} × {current} = {answer} W.'
                    options = _numeric_options(answer)
                else:
                    time = value + 2
                    text = f'In an electrolytic cell, how many moles of electrons pass when {time} A flows for 96485 s?'
                    answer = time
                    explanation = f'n(e⁻) = It/F = {time} × 96485/96485 = {time} mol.'
                    options = _numeric_options(answer)
                answer = 'A'
            answer = 'A'
            questions.append(_question(
                category, 'Chemistry', chemistry_topic, text, options, answer, explanation,
                'Hard', exam=subject,
            ))

            math_topic = ('Algebra', 'Quadratic Equations', 'Calculus', 'Complex Numbers', 'Probability')[
                (value // 9 + attempt_group) % 5
            ]
            if math_topic == 'Algebra':
                if variant == 0:
                    answer = value + 2
                    coefficient = value % 7 + 2
                    text = f'Solve {coefficient}x + {answer} = {coefficient * answer + answer} for x.'
                    explanation = f'{coefficient}x = {coefficient * answer}, so x = {answer}.'
                elif variant == 1:
                    x, coefficient = value + 2, value % 8 + 2
                    answer = coefficient * x + 1
                    text = f'If f(x) = {coefficient}x + 1, evaluate f({x}).'
                    explanation = f'f({x}) = {coefficient} × {x} + 1 = {answer}.'
                else:
                    answer = value + 2
                    text = f'If 2x + y = {3 * answer} and y = {answer}, find x.'
                    explanation = f'2x = {3 * answer} - {answer} = {2 * answer}, so x = {answer}.'
                options = _numeric_options(answer)
            elif math_topic == 'Quadratic Equations':
                first, second = value + 2, value + 16
                if variant == 0:
                    answer = first + second
                    text = f'A quadratic has roots {first} and {second}. Find their sum.'
                    explanation = f'Sum of roots = {first} + {second} = {answer}.'
                elif variant == 1:
                    answer = first * second
                    text = f'A quadratic has roots {first} and {second}. Find their product.'
                    explanation = f'Product of roots = {first} × {second} = {answer}.'
                else:
                    answer = 2
                    text = f'How many real roots does x² - {first + second}x + {first * second} = 0 have?'
                    explanation = f'The equation factors as (x-{first})(x-{second}) = 0 and has two real roots.'
                options = _numeric_options(answer)
            elif math_topic == 'Calculus':
                power = value + 3
                if variant == 0:
                    answer = power
                    text = f'What is d(x^{power})/dx at x = 1?'
                    explanation = f'd(x^{power})/dx = {power}x^{power - 1}, which equals {answer} at x=1.'
                elif variant == 1:
                    coefficient = value + 2
                    answer = 0
                    text = f'Find the slope of y = {coefficient}x² at x = 0.'
                    explanation = f'dy/dx = {2 * coefficient}x, so the slope at x=0 is 0.'
                else:
                    gradient, lower, upper = value + 2, value + 2, value + 8
                    answer = gradient * (upper - lower)
                    text = f'If dx/dt = {gradient}, how much does x change from t={lower} to t={upper}?'
                    explanation = f'Δx = {gradient} × ({upper}-{lower}) = {answer}.'
                options = _numeric_options(answer)
            elif math_topic == 'Complex Numbers':
                real, imag = value + 2, value + 3
                if variant == 0:
                    answer = round((real ** 2 + imag ** 2) ** 0.5, 2)
                    text = f'Find the modulus of {real} + {imag}i.'
                    explanation = f'|z| = √({real}² + {imag}²) = {answer}.'
                    options = _numeric_options(answer)
                elif variant == 1:
                    answer = real + imag
                    text = f'What is the real part of ({real} + {imag}i) + ({imag} - {real}i)?'
                    explanation = f'The real part is {real} + {imag} = {answer}.'
                    options = _numeric_options(answer)
                else:
                    text = 'What is i² in the complex number system?'
                    options = ['-1', '0', '1', 'i']
                    explanation = 'By definition, i is a square root of -1, so i² = -1.'
                    answer = 'A'
            else:
                if variant == 0:
                    red, blue = value + 3, value + 4
                    answer = round(red / (red + blue), 2)
                    text = f'A box has {red} red and {blue} blue balls. Find the probability of drawing a red ball.'
                    explanation = f'P(red) = {red}/({red}+{blue}) = {answer}.'
                    options = _numeric_options(answer)
                elif variant == 1:
                    numerator = value + 2
                    text = f'An event has probability {numerator}/{numerator + 1}. What is the probability of its complement?'
                    options = [f'1/{numerator + 1}', f'{numerator}/{numerator + 1}', '1/2', '0']
                    explanation = f'P(complement) = 1 - {numerator}/{numerator + 1} = 1/{numerator + 1}.'
                    answer = 'A'
                else:
                    outcomes = value + 2
                    answer = outcomes ** 2
                    text = f'Two independent trials each have {outcomes} possible outcomes. How many ordered pairs are possible?'
                    explanation = f'The multiplication rule gives {outcomes} × {outcomes} = {answer} pairs.'
                    options = _numeric_options(answer)
            answer = 'A'
            questions.append(_question(
                category, 'Mathematics', math_topic, text, options, answer, explanation,
                'Hard', exam=subject,
            ))

    elif subject == 'DSA Aptitude':
        templates = {
            'Arrays': [
                ('What is the time complexity of reading an array value at a known index in an array of {size} values?', ('O(1)', 'O(log n)', 'O(n)', 'O(n log n)'), 'Array indexing accesses a known position directly.'),
                ('A linear scan may inspect all {size} array values. What is its worst-case time complexity?', ('O(n)', 'O(1)', 'O(log n)', 'O(n²)'), 'A linear scan can visit every element once.'),
                ('Inserting at the start of an array with {size} elements requires shifting later values. What is the time complexity?', ('O(n)', 'O(1)', 'O(log n)', 'O(n log n)'), 'The existing values may all need to shift one position.'),
                ('Removing the first item from an array of {size} elements requires closing the gap. What is the time complexity?', ('O(n)', 'O(1)', 'O(log n)', 'O(n log n)'), 'After removal, the remaining elements may need to shift.'),
                ('A loop visits each of the {size} array elements once. What is its time complexity?', ('O(n)', 'O(1)', 'O(log n)', 'O(n²)'), 'One constant-time visit per element gives linear time.'),
            ],
            'Strings': [
                ('A routine scans all {size} characters of a string once to count vowels. What is its time complexity?', ('O(n)', 'O(1)', 'O(log n)', 'O(n²)'), 'Each character is checked once.'),
                ('A mutable character array of length {size} is reversed using two pointers. What is the time complexity?', ('O(n)', 'O(1)', 'O(log n)', 'O(n²)'), 'The two pointers swap each character at most once.'),
                ('A palindrome check compares characters from both ends of a string of length {size}. What is the worst-case time complexity?', ('O(n)', 'O(1)', 'O(log n)', 'O(n²)'), 'At most half the characters are compared, which is linear time.'),
                ('Two strings of length {size} are compared character by character. What is the worst-case time complexity?', ('O(n)', 'O(1)', 'O(log n)', 'O(n²)'), 'The comparison may examine every character.'),
                ('KMP searches a pattern of length {size} in a text of length {size} + 1. What is its time complexity?', ('O(n + m)', 'O(nm)', 'O(1)', 'O(n² log n)'), 'KMP preprocesses the pattern and scans the text in linear time.'),
            ],
            'Linked Lists': [
                ('What is the time complexity of accessing the item at position {size} in a singly linked list from its head?', ('O(n)', 'O(1)', 'O(log n)', 'O(n log n)'), 'Nodes must be followed sequentially from the head.'),
                ('A pointer to the head is available. What is the time complexity of inserting a new node at the head of a linked list with {size} nodes?', ('O(1)', 'O(log n)', 'O(n)', 'O(n log n)'), 'Only the new node link and head pointer need updating.'),
                ('What is the worst-case time complexity of searching for a value in a linked list with {size} nodes?', ('O(n)', 'O(1)', 'O(log n)', 'O(n log n)'), 'The value may be in the last node or absent.'),
                ('Floyd’s cycle-detection algorithm processes a linked list of {size} nodes. What is its extra-space complexity?', ('O(1)', 'O(log n)', 'O(n)', 'O(n²)'), 'It uses two pointers and no collection proportional to the list length.'),
                ('A linked list has {size} nodes. What is the time complexity of finding its tail when starting at the head?', ('O(n)', 'O(1)', 'O(log n)', 'O(n log n)'), 'Without a tail pointer, traversal continues node by node.'),
            ],
            'Stacks': [
                ('A fixed-capacity stack contains {size} items. What is the time complexity of pushing one item when space is available?', ('O(1)', 'O(log n)', 'O(n)', 'O(n log n)'), 'A push updates the top position and stores one item.'),
                ('A stack contains {size} items. What is the time complexity of popping its top item?', ('O(1)', 'O(log n)', 'O(n)', 'O(n log n)'), 'A pop removes the item at the top directly.'),
                ('Which access order does a stack with {size} stored items follow?', ('Last in, first out', 'First in, first out', 'Smallest in, first out', 'Random in, first out'), 'A stack removes the most recently added item first.'),
                ('Which structure is commonly used to check whether {size} opening and closing brackets are properly nested?', ('Stack', 'Queue', 'Hash map only', 'Binary search tree'), 'A stack tracks the most recent unmatched opening bracket.'),
                ('A depth-first traversal stores up to {size} pending vertices explicitly. Which structure is typically used?', ('Stack', 'Queue', 'Heap', 'Hash map'), 'Depth-first traversal uses a stack, either explicitly or through recursion.'),
            ],
            'Queues': [
                ('Which access order does a queue containing {size} items follow?', ('First in, first out', 'Last in, first out', 'Largest in, first out', 'Random in, first out'), 'A queue removes items in the order they were added.'),
                ('A linked queue with head and tail pointers contains {size} items. What is the time complexity of enqueue?', ('O(1)', 'O(log n)', 'O(n)', 'O(n log n)'), 'The tail pointer allows the new item to be appended directly.'),
                ('A linked queue with a head pointer contains {size} items. What is the time complexity of dequeue?', ('O(1)', 'O(log n)', 'O(n)', 'O(n log n)'), 'Dequeue advances the head pointer to the next node.'),
                ('Which structure does breadth-first search use to process vertices by distance from the source in a graph of {size} vertices?', ('Queue', 'Stack', 'Sorted array', 'Recursion only'), 'A queue processes discovered vertices in FIFO order.'),
                ('In a circular queue of capacity {size} that reserves one slot to distinguish full from empty, when is it full?', ('The next rear position equals front', 'Rear equals front in every case', 'Front is always zero', 'The queue has one item'), 'The queue is full when advancing rear would meet front.'),
            ],
            'Hash Maps': [
                ('Two different keys among {size} stored entries map to the same hash-table slot. What is this called?', ('A collision', 'A rotation', 'A traversal', 'An underflow'), 'A collision occurs when distinct keys map to the same slot.'),
                ('Under uniform hashing, what is the expected lookup time in a hash map with {size} entries?', ('O(1)', 'O(log n)', 'O(n)', 'O(n log n)'), 'With a suitable hash function, the expected number of probes is constant.'),
                ('Which method stores multiple colliding keys in a list at a hash-table slot for a map with {size} entries?', ('Separate chaining', 'Binary search', 'Tree rotation', 'Linear probing only'), 'Separate chaining keeps a collection of entries at each slot.'),
                ('A hash table has {size} stored entries and {size} slots. What is its load factor?', ('1', '0', '{size}', '0.5'), 'Load factor is entries divided by slots, so {size}/{size} equals 1.'),
                ('If all {size} keys collide in one hash-table bucket, what can worst-case lookup time become?', ('O(n)', 'O(1)', 'O(log n)', 'O(n log n)'), 'A lookup may need to inspect every key in the bucket.'),
            ],
            'Searching': [
                ('What must be true of the data before standard binary search can be used on {size} values?', ('The values are sorted', 'The values are all distinct', 'The values are positive', 'The values form a tree'), 'Binary search relies on sorted order to discard half the range.'),
                ('What is the time complexity of binary search on {size} sorted values?', ('O(log n)', 'O(1)', 'O(n)', 'O(n log n)'), 'Each comparison halves the remaining search interval.'),
                ('What is the best-case time complexity of linear search on {size} values when the target is first?', ('O(1)', 'O(log n)', 'O(n)', 'O(n²)'), 'The first comparison finds the target immediately.'),
                ('What is the worst-case time complexity of linear search when looking for a value among {size} items?', ('O(n)', 'O(1)', 'O(log n)', 'O(n log n)'), 'The search may inspect every item.'),
                ('After one binary-search comparison, at most what fraction of a sorted range of {size} values remains?', ('One half', 'All of it', 'One quarter', 'Two thirds'), 'Binary search discards one half of the current interval per comparison.'),
            ],
            'Sorting': [
                ('What is the worst-case time complexity of merge sort on {size} values?', ('O(n log n)', 'O(n)', 'O(n²)', 'O(log n)'), 'Merge sort splits into levels and merges all values at each level.'),
                ('What is the best-case time complexity of insertion sort on an already sorted list of {size} values?', ('O(n)', 'O(1)', 'O(log n)', 'O(n²)'), 'Each item needs only a constant check as the list is traversed once.'),
                ('What is the worst-case time complexity of bubble sort on {size} values?', ('O(n²)', 'O(n)', 'O(log n)', 'O(n log n)'), 'Repeated passes compare pairs across the list.'),
                ('Which property does stable sorting preserve when equal keys appear among {size} records?', ('Their original relative order', 'Their numeric values change', 'The list becomes reversed', 'Every key becomes unique'), 'A stable sort keeps equal-key records in their original relative order.'),
                ('What is quicksort’s worst-case time complexity when sorting {size} values with consistently unbalanced partitions?', ('O(n²)', 'O(n)', 'O(log n)', 'O(n log n)'), 'Unbalanced partitions can require a quadratic number of comparisons.'),
            ],
            'Trees': [
                ('Which traversal visits keys in sorted order in a binary search tree containing {size} keys?', ('Inorder', 'Preorder', 'Postorder', 'Level order'), 'Inorder visits left subtree, node, then right subtree.'),
                ('What is the search time complexity in a balanced binary search tree with {size} nodes?', ('O(log n)', 'O(1)', 'O(n)', 'O(n log n)'), 'A balanced tree reduces the remaining search subtree by height.'),
                ('Which data structure is typically used for level-order traversal of a tree with {size} nodes?', ('Queue', 'Stack', 'Hash map', 'Sorted array'), 'Level-order traversal processes nodes breadth first using a queue.'),
                ('A full binary tree has {size} internal nodes. How many leaves does it have?', ('{size} + 1', '{size}', '2 × {size}', '{size} − 1'), 'In a full binary tree, the number of leaves is one greater than the internal-node count.'),
                ('What is the worst-case search time in a completely skewed binary search tree with {size} nodes?', ('O(n)', 'O(1)', 'O(log n)', 'O(n log n)'), 'A skewed tree can have height proportional to its number of nodes.'),
            ],
            'Graphs': [
                ('Which traversal finds shortest paths by edge count from a source in an unweighted graph of {size} vertices?', ('Breadth-first search', 'Depth-first search', 'Inorder traversal', 'Heap sort'), 'BFS visits vertices in increasing distance from the source.'),
                ('Which traversal explores a graph of {size} vertices by following a path before backtracking?', ('Depth-first search', 'Breadth-first search', 'Binary search', 'Merge sort'), 'DFS follows a path deeply before exploring alternatives.'),
                ('In an undirected graph with {size} edges, what is the sum of all vertex degrees?', ('2 × {size}', '{size}', '{size} + 1', '{size} − 1'), 'Each undirected edge contributes one degree to each endpoint.'),
                ('What is the space complexity of an adjacency-list representation of a graph with {size} vertices and {size} edges?', ('O(V + E)', 'O(V²)', 'O(E²)', 'O(1)'), 'Adjacency lists store vertices and their incident edges.'),
                ('Which shortest-path algorithm supports negative edge weights when no reachable negative cycle exists in a graph of {size} vertices?', ('Bellman-Ford', 'Dijkstra', 'Prim', 'Kruskal'), 'Bellman-Ford supports negative edges and detects reachable negative cycles.'),
            ],
        }
        for size in range(2, 502):
            for topic in DSA_APTITUDE_TOPICS:
                for text, options, explanation in templates[topic]:
                    formatted_text = text.format(size=size)
                    formatted_options = tuple(option.format(size=size) for option in options)
                    questions.append(_question(
                        category, topic, topic, formatted_text, formatted_options, 'A',
                        explanation.format(size=size), 'Medium', exam=subject,
                    ))

    return questions


@lru_cache(maxsize=2)
def _general_candidates(category):
    questions = []
    for value in range(2, 502):
        if category == 'highschool':
            total = value * 4
            questions.append(_question(
                category, 'Math', 'Arithmetic',
                f'A library has {value} shelves with 4 books on each shelf. How many books are there?',
                _numeric_options(total), 'A',
                f'{value} × 4 = {total} books.',
                'Easy',
            ))
            difference = value * 3
            questions.append(_question(
                category, 'Math', 'Arithmetic',
                f'A runner completes {value * 5} laps and then runs {difference} fewer laps the next day. How many laps are run the next day?',
                _numeric_options(value * 2), 'A',
                f'{value * 5} − {difference} = {value * 2} laps.',
                'Easy',
            ))
            length = value + 3
            width = value + 1
            questions.append(_question(
                category, 'Math', 'Geometry',
                f'What is the area of a rectangle that is {length} cm long and {width} cm wide?',
                _numeric_options(length * width), 'A',
                f'Area = length × width = {length} × {width} = {length * width} cm².',
                'Easy',
            ))
            acceleration = value + 2
            time = value + 1
            questions.append(_question(
                category, 'Physics', 'Motion',
                f'A trolley starts from rest and accelerates at {acceleration} m/s² for {time} s. What is its final speed?',
                _numeric_options(acceleration * time), 'A',
                f'Using v = u + at, v = 0 + {acceleration} × {time} = {acceleration * time} m/s.',
                'Medium',
            ))
            resistance = value + 4
            current = value + 1
            questions.append(_question(
                category, 'Physics', 'Electricity',
                f'What voltage is measured across a {resistance} Ω resistor carrying {current} A?',
                _numeric_options(resistance * current), 'A',
                f'Ohm’s law gives V = IR = {resistance} × {current} = {resistance * current} V.',
                'Medium',
            ))
            acid_power = value + 1
            questions.append(_question(
                category, 'Chemistry', 'Acids and Bases',
                f'A solution has hydrogen-ion concentration 10⁻{acid_power} mol/L. What is its pH?',
                _numeric_options(acid_power), 'A',
                f'pH = -log₁₀[H⁺] = {acid_power}.',
                'Medium',
            ))
            moles = value + 1
            molar_mass = value + 5
            questions.append(_question(
                category, 'Chemistry', 'Mole Concept',
                f'What is the mass of {moles} mol of a substance with molar mass {molar_mass} g/mol?',
                _numeric_options(moles * molar_mass), 'A',
                f'Mass = nM = {moles} × {molar_mass} = {moles * molar_mass} g.',
                'Medium',
            ))
            cell_cycles = value % 8 + 1
            starting_cells = value + 1
            cells = starting_cells * (2 ** cell_cycles)
            questions.append(_question(
                category, 'Biology', 'Cell Biology',
                f'Starting with {starting_cells} cells, each cell divides into two every cycle. How many cells result after {cell_cycles} cycles?',
                _numeric_options(cells), 'A',
                f'The number doubles each cycle: {starting_cells} × 2^{cell_cycles} = {cells} cells.',
                'Medium',
            ))
            dna_at = value + 2
            dna_gc = value + 1
            bonds = 2 * dna_at + 3 * dna_gc
            questions.append(_question(
                category, 'Biology', 'Genetics',
                f'A DNA segment has {dna_at} A–T pairs and {dna_gc} G–C pairs. How many hydrogen bonds hold these pairs together?',
                _numeric_options(bonds), 'A',
                f'Each A–T pair has 2 bonds and each G–C pair has 3: 2 × {dna_at} + 3 × {dna_gc} = {bonds}.',
                'Medium',
            ))
            elapsed = value + 1
            later_year = value + elapsed
            questions.append(_question(
                category, 'History', 'Historical Timelines',
                f'A historical timeline records an event in {value} CE and another {elapsed} years later. In what year CE did the second event occur?',
                _numeric_options(later_year), 'A',
                f'The second event occurred {elapsed} years after {value} CE: {value} + {elapsed} = {later_year} CE.',
                'Medium',
            ))
            longitude = value + 1
            questions.append(_question(
                category, 'Geography', 'Longitude and Time',
                f'Two locations differ by {longitude}° of longitude. What is their local solar-time difference in minutes?',
                [f'{longitude * 4}', f'{longitude * 2}', f'{longitude * 5}', f'{longitude * 8}'],
                'A',
                f'Earth rotates 15° per hour, or 4 minutes per degree: {longitude} × 4 = {longitude * 4} minutes.',
                'Medium',
            ))
            questions.append(_question(
                category, 'English', 'Subject-Verb Agreement',
                f'Choose the verb that correctly completes the sentence: “The student in seat {value} ___ ready for the exam.”',
                ['is', 'are', 'were', 'be'],
                'A',
                'The singular subject “student” takes the singular verb “is.”',
                'Easy',
            ))
        else:
            subject = 'Algorithms'
            total = value * 4
            questions.append(_question(
                category, subject, 'Arithmetic',
                f'A program processes {value} batches containing 4 records each. How many records does it process?',
                _numeric_options(total), 'A',
                f'{value} × 4 = {total} records.',
                'Easy',
            ))
            difference = value * 3
            questions.append(_question(
                category, subject, 'Arithmetic',
                f'A process handles {value * 5} tasks and completes {difference} fewer tasks in its next run. How many tasks does it complete next?',
                _numeric_options(value * 2), 'A',
                f'{value * 5} − {difference} = {value * 2} tasks.',
                'Easy',
            ))
            questions.append(_question(
                category, 'Data Structures', 'Complexity Analysis',
                f'An algorithm checks each of {value} elements once. What is its time complexity?',
                ['O(n)', 'O(1)', 'O(log n)', 'O(n²)'],
                'A',
                'A single pass visits each input element once, so the running time grows linearly.',
                'Medium',
            ))
            number = value + 3
            questions.append(_question(
                category, 'Python', 'Expressions',
                f'What value does the Python expression {number} // 2 return?',
                _numeric_options(number // 2), 'A',
                f'Floor division discards the fractional part: {number} // 2 = {number // 2}.',
                'Easy',
            ))
    return questions


def warm_question_candidate_cache():
    """Build question candidates during app startup rather than on a test request."""
    for exam in ('CET', 'JEE', 'DSA Aptitude'):
        _exam_candidates('puc_degree', exam)
    _general_candidates('highschool')
    _general_candidates('puc_degree')


def generate_additional_questions(
    category,
    existing_questions,
    target_count,
    subject=None,
    required_subject_counts=None,
    required_topic_counts=None,
):
    """Generate distinct academic MCQs without adding question-index text."""
    existing_text = {
        item['question'].strip().casefold()
        for item in existing_questions
    }
    candidates = (
        _exam_candidates(category, subject)
        if category == 'puc_degree' and subject in {'CET', 'JEE', 'DSA Aptitude'}
        else _general_candidates(category)
    )
    generated = []
    target_additions = max(0, target_count - len(existing_questions))

    for question in candidates:
        if (
            subject and subject != 'All'
            and not (category == 'puc_degree' and subject in {'CET', 'JEE', 'DSA Aptitude'})
            and question['subject'] != subject
        ):
            continue
        key = question['question'].strip().casefold()
        if key in existing_text:
            continue
        if required_subject_counts is not None:
            subject_needed = required_subject_counts.get(question['subject'], 0)
            if subject_needed <= 0:
                continue
            required_subject_counts[question['subject']] = subject_needed - 1
        if required_topic_counts is not None:
            topic_needed = required_topic_counts.get(question['topic'], 0)
            if topic_needed <= 0:
                continue
            required_topic_counts[question['topic']] = topic_needed - 1
        existing_text.add(key)
        generated.append(question)
        if len(generated) >= target_additions:
            break

    if required_subject_counts is not None and any(required_subject_counts.values()):
        raise RuntimeError('Not enough unique generated questions to fill each requested subject section.')
    if required_topic_counts is not None and any(required_topic_counts.values()):
        raise RuntimeError('Not enough unique generated questions to fill each requested topic section.')

    return generated
