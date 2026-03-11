# SPDX-FileCopyrightText: 2026 Avogadro Project
# SPDX-License-Identifier: BSD 3-Clause
# ******************************************************************************
# This source file is part of the Avogadro project.
#
# This source code is released under the New BSD License, (the "License").
# ******************************************************************************
"""Input generation for Q-Chem (https://www.q-chem.com/)."""


def generateInputFile(input_json: dict) -> tuple[str, list[str]]:
    # Collect warning strings as we go
    warnings = []

    # Extract options:
    opts = input_json['options']
    title = opts['Title']
    calculate = opts['Calculation Type']
    theory = opts['Theory']
    basis = opts['Basis']
    charge = opts['Charge']
    multiplicity = opts['Multiplicity']

    # Convert to code-specific strings
    calcStr = ''
    if calculate == 'Single Point':
        calcStr = 'SP'
    elif calculate == 'Equilibrium Geometry':
        calcStr = 'Opt'
    elif calculate == 'Frequencies':
        calcStr = 'Freq'
    else:
        warnings.append('Unhandled calculation type: %s' % calculate)

    theoryStr = ''
    if theory in ['HF', 'B3LYP', 'B3LYP5', 'EDF1', 'M062X', 'MP2', 'CCSD']:
        theoryStr = theory
    else:
        warnings.append('Unhandled theory type: %s' % theory)

    basisStr = ''
    if basis in ['STO-3G', '3-21G', '6-31G(d)', '6-31G(d,p)', '6-31+G(d)',
                 '6-311G(d)', 'cc-pVDZ', 'cc-pVTZ']:
        basisStr = 'BASIS %s' % basis
    elif basis in ['LANL2DZ', 'LACVP']:
        basisStr = 'ECP %s' % basis
    else:
        warnings.append('Unhandled basis type: %s' % basis)

    generated_input = ''

    generated_input += '$rem\n'
    generated_input += '   JOBTYPE %s\n' % calcStr
    generated_input += '   METHOD %s\n' % theoryStr
    generated_input += '   %s\n' % basisStr
    generated_input += '   GUI 2\n'
    generated_input += '$end\n\n'

    generated_input += '$comment\n   %s\n$end\n\n' % title

    generated_input += '$molecule\n'
    generated_input += f'   {charge} {multiplicity}\n'
    generated_input += '$$coords:___Sxyz$$\n'
    generated_input += '$end\n'

    return generated_input, warnings


def generateInput(input_json: dict, debug: bool) -> dict:

    generated_input, warnings = generateInputFile(input_json)

    filename = input_json['options']['Filename Base'] + '.qcin'

    result = {
        'files': [
            {'filename': filename, 'contents': generated_input},
        ],
        'mainFile': filename,
    }

    if warnings:
        result['warnings'] = warnings

    return result
