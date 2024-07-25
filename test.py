#!/usr/bin/env python3

import prompt_toolkit
import sys
import random
import argparse

# Evaluate command line arguments.
def evalArgs():
	parser = argparse.ArgumentParser(description='Take a test.')

	# Define command line arguments.
	parser.add_argument('-n', '--number', type=int, help='number of questions', required=False)
	parser.add_argument('-f', '--file', type=str, help='questions file', required=True)
	parser.add_argument('-e', '--explanation', action='store_true', help='provided explanations for right answers', required=False)
	
	# Parse the arguments
	args = parser.parse_args()

	return args.number, args.file, args.explanation

# Get questions from a file.
def getQuestions(fileName):
	formatted_data = {}

	# Load the data from the file
	try:
		with open(fileName, 'r') as file:
			for line in file:
				line = line.strip()
				parts = line.split('|')
				id = int(parts[0])
				question = parts[1][1:-1]
				choices = parts[2][1:-1].split('","')
				correct_choice_indices = list(map(int, parts[3].split(',')))
				explanation = parts[4][1:-1]

				formatted_data[id] = { 'question': question, 'choices': choices, 'correct_choice_indices': correct_choice_indices, 'explanation': explanation }
	except FileNotFoundError:
		print("Error: File",fileName,"was not found.")
		sys.exit()

	return formatted_data

# Print a question.
def askQuestion(question, choices, correct_choice_indices):
	# Map numbers to letters
	numToAlpha = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

	# Store the correct choices
	correctChoices = []
	i = 0
	while i < len(correct_choice_indices):
		correctChoices.append(choices[correct_choice_indices[i]].replace(' ','').lower())
		i = i + 1

	# Shuffle the choices list
	random.shuffle(choices)

	# Get index of correct choices post shuffle
	newIndices = []
	num = 0
	for i in choices:
		if i.replace(' ', '').lower() in correctChoices:
			newIndices.append(numToAlpha[num])
		num = num + 1

	# Print the question text.
	print(question)

	# Print the choices.
	num = 0
	for i in choices:
		print('\t', numToAlpha[num], end='')
		print(")", i)
		num = num + 1

	# Prompt the user.
	answer = list(prompt_toolkit.prompt('Answer: ').lower().replace(' ','').split(','))

	# Evaluate the user's input
	if answer == ['exit']:
		sys.exit()
	elif sorted(answer) == sorted(newIndices) or sorted(answer) == sorted(correctChoices):
		return True
	else:
		return False

# Calculate grade
def calcGrade(correctAnswers, incorrectAnswers):
	numQuestions = correctAnswers + incorrectAnswers
	return (correctAnswers / numQuestions) * 100

def main():
	correctAnswers = 0
	incorrectAnswers = 0

	# Evaluate command line arguments
	rounds, file, explanation = evalArgs()

	# Load questions from file.
	questions = getQuestions(file)

	# Shuffle the questions.
	questionsList = list(questions.items())
	random.shuffle(questionsList)

	# Ask the user questions.
	for item in questionsList[:rounds]:
		q = item[1]
		# Ask the user a question.
		outcome = askQuestion(q['question'], q['choices'], q['correct_choice_indices'])
		# Evaluate the outcome.
		if outcome:
			print("\033[32m" + "Correct!" + "\033[0m")
			correctAnswers = correctAnswers + 1
			
			if explanation:
				print("\033[34m" + "Explanation:" + "\033[0m", end=' ')
				print(q['explanation'])
			print()
		else:
			print("\033[31m" + "Incorrect!" + "\033[0m")
			incorrectAnswers = incorrectAnswers + 1
			print("\033[34m" + "Explanation:" + "\033[0m", end=' ')
			print(q['explanation'])
			print()

	# Print the results.
	print("Your grade is", calcGrade(correctAnswers,incorrectAnswers), "%")

main()
