import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def load_data(filename):
    data = pd.read_csv(filename)
    return data['year'].values, data['days'].values

def normalize_data(years):
    min_year, max_year = np.min(years), np.max(years)
    return (years - min_year) / (max_year - min_year), min_year, max_year

def closed_form(X, Y):
    X_transpose_X = np.dot(X.T, X)
    X_transpose_Y = np.dot(X.T, Y)
    return np.linalg.inv(X_transpose_X).dot(X_transpose_Y).flatten()

def gradient_descent(X, Y, learning_rate, iterations):
    weights = np.zeros(2)
    n = len(Y)
    losses = []
    
    for t in range(1, iterations + 1):
        predictions = np.dot(X, weights)
        gradient = (1 / n) * np.dot(X.T, (predictions - Y))
        weights -= learning_rate * gradient

        loss = (1 / (2 * n)) * np.sum((predictions - Y) ** 2)
        losses.append(loss)

        if t % 10 == 0 and t <= 90:
            print(weights)

    return weights, losses

def main():
    filename = sys.argv[1]
    learning_rate = float(sys.argv[2])
    iterations = int(sys.argv[3])
    years, days = load_data(filename)
    
    # Question 1
    plt.plot(years, days, color="red")
    plt.title("Question 1")
    plt.xlabel('Year')
    plt.ylabel('Number of Frozen Days')
    plt.savefig("data_plot.jpg")
    plt.close()
    
    # Question 2
    normalized_years, min_year, max_year = normalize_data(years)
    X_normalized = np.column_stack((normalized_years, np.ones(len(years))))
    print("Q2:")
    print(X_normalized)
    
    # Question 3
    Y = days.reshape(-1, 1)
    weights = closed_form(X_normalized, Y)
    print("Q3:")
    print(weights)
    
    # Question 4
    print("Q4a:")
    print(np.array([0.0, 0.0]))
    final_weights, losses = gradient_descent(X_normalized, days, learning_rate, iterations)
    print("Q4b:", 0.5)
    print("Q4c:", 300)
    print("Q4d: I started with 0.01 and gradually increased up to 0.05 and then by 0.05 up to 0.1. From there I tried every 0.1 increase and found that a rate of 0.5 diverged quickly without converging on the loss plot. The 300 iterations seemed to be the closest for when I was comparing the weights from gradient descent with the closed-form solution weights.")
    
    plt.plot(range(1, iterations + 1), losses, color="red")
    plt.title("Question 4e")
    plt.xlabel('Number of Iterations')
    plt.ylabel('Mean Squared Error')
    plt.savefig("loss_plot.jpg")
    plt.close()
    
    # Question 5
    x_2023_normalized = (2023 - min_year) / (max_year - min_year)
    y_hat_2023 = weights[0] * x_2023_normalized + weights[1]
    print("Q5:", y_hat_2023)
    
    # Question 6
    sign = "=" if weights[0] == 0 else (">" if weights[0] > 0 else "<")
    print("Q6a:", sign)
    print("Q6b: A positive w (slope) means ice days are increasing over time, negative means decreasing, zero means the number of ice days has stayed stable.")
    
    # Question 7
    x_star = min_year - (weights[1] * (max_year - min_year)) / weights[0]
    print("Q7a:", x_star)
    print("Q7b: The prediction assumes a linear relationship between time and ice days, but climates are more complex than that. Major climate events, lake policy changes and other unexpected events will always be a factor that this linear relationship cannot account for over time. The prediction is completely oversimplifying weather and climate as a whole.")

if __name__ == "__main__":
    main()