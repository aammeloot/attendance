'''
MIT License

Copyright (c) 2021 Aurélien Ammeloot

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from os import close
import typing
from random import randint
from random import shuffle

# Distribution (35% attend, 70% attend, 90% attend)
# Sum should be 1
DIST = (.1,.8,.2)

def generate_line(num: int, rate: int) -> dict:
    # User profile in dictionary
    profile = {}

    # Generate student number format 21xxxxxx
    profile['studentno'] = '21' + str(num).zfill(6)

    # Generate student attendance data: X = present, U = absent
    # Generate number 1 - 100 and if it's less than rate then X
    # Otherwise U, this weighs the random generation
    sem_attendance = []
    for counter in range(18):
        draw = randint(1,100)
        if draw < rate:
            sem_attendance.append('X')
        else:
            sem_attendance.append('U')
    
    actual_rate = sem_attendance.count('X') / len(sem_attendance) * 100
    actual_rate = int(actual_rate)

    # Now generate grade, I'm rougly taking the attendance and 
    # Applying a +/- 20% random correction
    correction = randint(-15,15)
    marks = actual_rate + correction

    # Making an adjustment to grade, if attendance under 20 grade will be 0
    if marks > 100:
        marks = 100
    if marks < 0:
        marks = 0

    # Add to profile
    profile['attendance'] = sem_attendance
    profile['grade'] = marks

    return profile


def generate_file(lines: int, destination: str) -> None:
    # Randomised rates
    randomised_rates = []
    # First filled with 20s
    for counter in range(int(lines * DIST[0])):
        randomised_rates.append(35)
    # 60s
    for counter in range(int(lines * DIST[1])):
        randomised_rates.append(70)
    # 80s
    for counter in range(int(lines * DIST[2])):
        randomised_rates.append(90)

    # Randomise the results    
    shuffle(randomised_rates)

    # List of results
    results = []
    for counter in range(len(randomised_rates)):
        results.append(generate_line(counter, randomised_rates[counter]))
    
    f = open(destination,'w')

    csv_lines = []
    # Generate a line
    for d in results:
        l = d['studentno'] + ','
        for a in d['attendance']:
            l += (a + ',')
        l += str(d['grade'])
        l += '\n'

        csv_lines.append(l)

    f.writelines(csv_lines)
    f.close()
    
def main() -> None:

    # Ask how many lines to generate
    amount = 0
    valid = False
    destination = ""

    # Input the lines of code
    while not valid:
        try:
            amount = int(input("Enter the amount of lines you want to generate"))
            valid = True
        except:
            print("Your input is not a valid numeric value")

    destination = input("Enter a name for your output file (will be a CSV)")

    generate_file(amount, destination)

if __name__ == '__main__':
    main()